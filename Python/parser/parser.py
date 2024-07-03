import glob
import os

from functools import reduce
import matplotlib.pyplot as plt
plt.rcParams['font.size']=13

ERROR_TYPE = ['Single', 'Random', 'Line', 'Square']
ERRORS_COUNT = [0, 0, 0, 0]     # vetor com a classificacao dos erros - [single, random, line, square]
ARQUIVOS = [
    
    
    # {'instabilidade':'old', 'tempo':'tempo', 'tamanho':'teste', 'chave':'#IT', 'chave2':' '},
    
    {'instabilidade':'alta', 'tempo':'3segundos', 'tamanho':'4gb', 'chave':'#IT', 'chave2':' '},
            {'instabilidade':'alta', 'tempo':'6segundos', 'tamanho':'4gb', 'chave':'#IT', 'chave2':' '},
            {'instabilidade':'alta', 'tempo':'3segundos', 'tamanho':'8gb', 'chave':'#IT', 'chave2':' '},
            {'instabilidade':'alta', 'tempo':'6segundos', 'tamanho':'8gb', 'chave':'#IT', 'chave2':' '},
    {'instabilidade':'media', 'tempo':'3segundos', 'tamanho':'4gb', 'chave':'#IT', 'chave2':' '},
            {'instabilidade':'media', 'tempo':'6segundos', 'tamanho':'4gb', 'chave':'#IT', 'chave2':' '},
            {'instabilidade':'media', 'tempo':'3segundos', 'tamanho':'8gb', 'chave':'#IT', 'chave2':' '},
            {'instabilidade':'media', 'tempo':'6segundos', 'tamanho':'8gb', 'chave':'#IT', 'chave2':' '},
    {'instabilidade':'baixa', 'tempo':'3segundos', 'tamanho':'4gb', 'chave':'#IT', 'chave2':' '},
            {'instabilidade':'baixa', 'tempo':'6segundos', 'tamanho':'4gb', 'chave':'#IT', 'chave2':' '},
            {'instabilidade':'baixa', 'tempo':'3segundos', 'tamanho':'8gb', 'chave':'#IT', 'chave2':' '},
            {'instabilidade':'baixa', 'tempo':'6segundos', 'tamanho':'8gb', 'chave':'#IT', 'chave2':' '},
    {'instabilidade':'DGEMM_XeonPhi', 'tempo': 'resultados_daniel', 'tamanho':'hpc', 'chave':'#SDC', 'chave2':'size:2048'},
    {'instabilidade':'DGEMM_K40', 'tempo': 'resultados_daniel', 'tamanho':'hpc', 'chave':'#SDC', 'chave2':'size:2048'}
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
        # para trocar a precisao do arrendondamento 
        # new_v.append(round((el/total)*100, 2))
        new_v.append(round((el/total)*100))
    # print(str(sum(new_v)))
    return new_v

for arq in ARQUIVOS:
    tempo = arq['tempo']
    tamanho = arq['tamanho']
    chave = arq['chave']
    chave2 = arq['chave2']
    instabilidade = arq['instabilidade']
    ERRORS_COUNT = [0, 0, 0, 0]
    file_location = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data', instabilidade,
                                tamanho,tempo,
                                    '*.log')
    filenames = glob.glob(file_location)

    errors = [] # lista contendo listas com os erros relativos
    errors_filename = [] # nome do arquivo contendo ligacao entre o nome do arquivo e qual index da lista de erros
    errors_avg = [] # lista contendo a media dos errors
    max_rel_errors = 0
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
        for line in data: # para cada linha
            if chave in line: # se tem #ERR
                considerar_erro = chave2 in line # verificacao se o erro e do tamanho correto (compatibilidade daniel)
                # print(line + ' - considerar_erro = '+ str(considerar_erro))
                if err_count > 0:
                    if err_count > 1:
                        err_type += 1
                        err_type += line_error
                        err_type += column_error
                    # print('(LINE) Iteracao teve ' + str(err_count) + ' erros, classificados como ' + ERROR_TYPE[err_type] + '\n')
                    ERRORS_COUNT[err_type] += 1
                    errors_filename.append(f)
                    max_rel_errors = max_rel_errors if max_rel_errors > len(rel_error) else len(rel_error)
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
                    # print('Erro relativo de [' + (('|' + str(x) + '|') if debug_line_error else str(x)) + ', ' + (('|' + str(y) + '|') if debug_column_error else str(y)) + '] = ' + str(relative_error(r, e)))
                    rel_error.append(relative_error_100(r, e))
                except:
                    print('Error reading file ' + f)
        if err_count > 0:
            if err_count > 1:
                err_type += 1
                err_type += line_error
                err_type += column_error
            # print('(FILE) Iteracao teve ' + str(err_count) + ' erros, classificados como ' + ERROR_TYPE[err_type] + '\n')
            ERRORS_COUNT[err_type] += 1
            errors_filename.append(f)
            max_rel_errors = max_rel_errors if max_rel_errors > len(rel_error) else len(rel_error)
            errors.append(rel_error)
            errors_avg.append(avg(rel_error))
                    
    x_scatter = []
    y_scatter = []
    count_elementos_incorretos = [0] * (max_rel_errors+1)
    total_elementos_incorretos = 0
    # print("Size of list = " + str(len(count_elementos_incorretos)))
    for index, error in enumerate(errors):
        # print(str(len(error)) + ' erros no arquivo ' + errors_filename[index] + ' com avg erro relativo = ' + str(errors_avg[index]))
        
        x_scatter.append(len(error))
        count_elementos_incorretos[len(error)] += 1
        total_elementos_incorretos += 1
        y_scatter.append(errors_avg[index])

        x = []
        y = []
        for i, e in enumerate(error):
            x.append(i)
            y.append(e)

    print("modelo = " + tempo + tamanho + " com instabilidade " + instabilidade)
    for i in range(max_rel_errors+1):
        if count_elementos_incorretos[i] > 0:
            print("Tamanho " + str(i) + " apareceu " + str(count_elementos_incorretos[i]) + " vezes - " + str((count_elementos_incorretos[i]/total_elementos_incorretos)*100) + "%")
    
    if(total_elementos_incorretos > 0):
        # criando scatter plot de todos
        plt.figure(newFigure())
        plt.scatter(x_scatter, y_scatter, marker='*', s=15)
        plt.ylim(0, 110)
        plt.xlim(0, 550)
        plt.xlabel('Número de elementos')
        plt.ylabel('Média erro relativo (%)')
        # plt.title('Erro relativo dos elementos')

        createFolder(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', tempo, 'Geral'))
        plt.savefig(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', tempo, 'Geral',tamanho + "_" + instabilidade) + ".pdf",bbox_inches='tight')

        # createFolder(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', instabilidade, tamanho, 'Geral'))
        # plt.savefig(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', instabilidade, tamanho, 'Geral', tempo)+ ".pdf",bbox_inches='tight')
        plt.close()
        
        #Criando plot da classificacao
        print(ERRORS_COUNT)
        new_errors = fixArray(ERRORS_COUNT)
        plt.figure(newFigure())
        plt.bar(ERROR_TYPE, new_errors)
        plt.ylim(0, 110)
        plt.ylabel("Número de ocorrências (%)")
        plt.xlabel("Classificação")
        # plt.title('Classificação dos erros')
        addlabels(ERROR_TYPE, new_errors)
        # createFolder(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', instabilidade, tamanho, 'Classificacao'))
        # plt.savefig(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', instabilidade, tamanho, 'Classificacao', tempo) + ".pdf",bbox_inches='tight')
        
        createFolder(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', tempo, 'Classificacao'))
        plt.savefig(os.path.join(os.path.realpath(os.path.dirname(__file__)), 'figuras', tempo, 'Classificacao', tamanho + "_" + instabilidade) + ".pdf",bbox_inches='tight')
        
        plt.close()
