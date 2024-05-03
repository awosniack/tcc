import glob
import os

from functools import reduce
import matplotlib.pyplot as plt

ERROR_TYPE = ['Single', 'Random', 'Line', 'Square']
ERRORS_COUNT = [0, 0, 0, 0]
ARQUIVOS = [
    {'tempo':'3segundos', 'tamanho':'backup4gb', 'chave':'#IT', 'chave2':' '},
            {'tempo':'6segundos', 'tamanho':'backup4gb', 'chave':'#IT', 'chave2':' '},
            {'tempo':'3segundos', 'tamanho':'backup8gb', 'chave':'#IT', 'chave2':' '},
            {'tempo':'6segundos', 'tamanho':'backup8gb', 'chave':'#IT', 'chave2':' '},
            {'tempo': 'hpc', 'tamanho':'DGEMM_XeonPhi', 'chave':'#SDC', 'chave2':'size:2048'},
            {'tempo': 'hpc', 'tamanho':'DGEMM_K40', 'chave':'#SDC', 'chave2':'size:2048'}
            ]
FIGURE = 0
def newFigure():
    global FIGURE
    FIGURE +=1
    return FIGURE
# adicionar label em cima das barras
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

#       |read - expected|
#er = -------------------- x 100
#          |expected|
def relative_error(r, e):
    return (((abs(r-e)) / abs(e)) * 100)
# se erro relativo > 100, entao erro relativo = 100
def relative_error_100(r, e):
    rel = ((abs(r-e)) / abs(e)) * 100
    return rel if rel < 100 else 100

# calcula a media do vetor V
def avg(v):
    return reduce(lambda a, b: a + b, v) / len(v)

#cria pasta/subpastas se nao existe
def createFolder(path):
    if not os.path.exists(path):
        os.makedirs(path)

#troca valores do vetor por percentagens do valor total
def fixArray(v):
    total = sum(v)
    if total == 0:
        print('FATAL ERROR 0')
        total = 1
    new_v = []
    for el in v:
        new_v.append(round((el/total)*100))
    return new_v

for arq in ARQUIVOS:
    tempo = arq['tempo']
    tamanho = arq['tamanho']
    chave = arq['chave']
    chave2 = arq['chave2']
    ERRORS_COUNT = [0, 0, 0, 0]
    file_location = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data',tempo,
                                tamanho,
                                    '*.log')
    filenames = glob.glob(file_location)

    errors = [] # lista contendo listas com os erros relativos
    errors_filename = [] # nome do arquivo contendo ligacao entre o nome do arquivo e qual index da lista de erros
    errors_avg = [] # lista contendo a media dos errors
    # print(len(filenames))
    for f in filenames:
        #abrindo e lendo arquivo
        outfile = open(f,'r')
        data = outfile.readlines()
        outfile.close()
        #inicializando variaveis
        err_type = 0
        err_count = 0
        lines = set()
        columns = set()
        line_error = False
        column_error = False

        rel_error = []
        considerar_erro = False
        for line in data:
            if chave in line:
                considerar_erro = chave2 in line
                # print(line + ' - considerar_erro = '+ str(considerar_erro))
                if err_count > 0:
                    if err_count > 1:
                        err_type += 1
                        err_type += line_error
                        err_type += column_error
                    # print('Iteracao teve ' + str(err_count) + ' erros, classificados como ' + ERROR_TYPE[err_type] + '\n')
                    ERRORS_COUNT[err_type] += 1
                    errors_filename.append(f)
                    errors.append(rel_error)
                    errors_avg.append(avg(rel_error))

                err_type = 0 # resetando classificacao do erro na iteracao
                err_count = 0 # resetando contador de erros da iteracao
                rel_error = [] # resetando lista contendo os erros relativos da iteracao
                #--------------------------------------
                lines = set() # resetando set contendo linhas
                columns = set() # resetando set contendo colunas
                line_error = False # resetando booleano que indica se e um erro em linha
                column_error = False # resetando booleano que indica se e um erro em coluna
                #---------------------------------------

            if '#ERR' in line and considerar_erro:
                try:
                    err = line
                    words = err.split()
                    x = int(words[2][1:-1]) # removendo '[' e ','
                    y = int(words[3][:-2]) # removendo ']' e ','
                    r = float(words[5][:-1]) # removendo ','
                    e = float(words[7])
                    err_count+=1

                    #---------------------------------------------
                    #para verificar se e um elemento novo
                    #salvo quantos elementos tem no set de linha e coluna
                    len_lines = len(lines)
                    len_columns = len(columns)
                    #adiciono a linha e coluna aos sets
                    lines.add(x)
                    columns.add(y)

                    debug_line_error = False
                    debug_column_error = False

                    #comparo se a linha e/ou coluna ja existiam no set
                    if len_lines == len(lines):
                        # print('linha ' + str(x) + ' ja existe')
                        line_error = True
                        debug_line_error = True
                    if len_columns == len(columns):
                        # print('coluna ' + str(y) + ' ja existe')
                        column_error = True
                        debug_column_error = True
                    #-----------------------------------------------
                    #print('Erro relativo de [' + (('|' + str(x) + '|') if debug_line_error else str(x)) + ', ' + (('|' + str(y) + '|') if debug_column_error else str(y)) + '] = ' + str(relative_error(r, e)))
                    rel_error.append(relative_error_100(r, e))
                except:
                    print('Error reading file ' + f)
        if err_count > 0:
                    if err_count > 1:
                        err_type += 1
                        err_type += line_error
                        err_type += column_error
                    # print('Iteracao teve ' + str(err_count) + ' erros, classificados como ' + ERROR_TYPE[err_type] + '\n')
                    errors_filename.append(f)
                    errors.append(rel_error)
                    errors_avg.append(avg(rel_error))
                    
    x_scatter = []
    y_scatter = []
    for index, error in enumerate(errors):
        #print(str(len(error)) + ' erros no arquivo ' + errors_filename[index] + ' com avg erro relativo = ' + str(errors_avg[index]))
        
        x_scatter.append(len(error))
        y_scatter.append(errors_avg[index])

        x = []
        y = []
        for i, e in enumerate(error):
            x.append(i)
            y.append(e)

    # criando scatter plot de todos
    plt.figure(newFigure())
    plt.scatter(x_scatter, y_scatter, marker='*', s=5)
    plt.xlabel('Número de elementos')
    plt.ylabel('Média erro relativo (%)')
    # plt.title('Erro relativo dos elementos')
    createFolder(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', tempo, 'Geral'))
    plt.savefig(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', tempo, 'Geral', tamanho))

    #Criando plot da classificacao
    print(ERRORS_COUNT)
    new_errors = fixArray(ERRORS_COUNT)
    plt.figure(newFigure())
    plt.bar(ERROR_TYPE, new_errors)
    plt.ylabel("Número de ocorrências (%)")
    plt.xlabel("Classificação")
    # plt.title('Classificação dos erros')
    addlabels(ERROR_TYPE, new_errors)
    createFolder(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', tempo, 'Classificacao'))
    plt.savefig(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', tempo, 'Classificacao', tamanho))
