class exitFlag():
    def __init__(self):
        self.value = 0

    def exit(self):
        self.value = 1

    def check(self):
        return self.value
