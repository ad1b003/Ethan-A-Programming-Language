import os, re

class Ethan:
    def __init__(self, fn):
        self.file_name = fn
        self.only_file_name = self.file_name.split("/")[-1].replace(".ethan", '')
        self.extra_paths = "/".join(self.file_name.split("/")[:-1])
        if self.extra_paths: self.extra_paths += '/'
        self.file_c = self.only_file_name + '.c'
        self.file_exe = self.only_file_name + '.exe'
        self.lang = self.dt_language()
        self.script = self.read()

    def dt_language(self):
        try:
            with open(self.file_name, 'r', encoding='utf8') as _file: #, encoding='uft-8'
                _1stline = _file.readline()
                _file.close()
                if re.match('#!English',_1stline) or re.match('#!english',_1stline): return 'en'
                elif re.match('#!বাংলা',_1stline): return 'bn'
                else: return 'en'
        except Exception as e:
            print("Error: Cann't read this file.\n\t" + str(e))
            return None

    def read(self):
        try:
            with open(self.file_name, 'r', encoding='utf8') as _file: #, encoding='uft-8'
                _script = _file.read()
                _file.close()
                return _script
        except Exception as e:
            print("Error: Cann't read this file.\n\t" + str(e))
            return None

    def execute(self):
        if self.lang == 'en':
            self.exe_en()
        elif self.lang == 'bn':
            self.exe_bn()
        else:
            return None

    def exe_en(self):
        import transpiler_en as en

        lexer = en.Lexer(self.script)
        tokens = lexer.tokenizer()
        transpiler = en.Transpiler(self.extra_paths + self.file_c)
        parser = en.Parser(tokens, transpiler)
        parser.parse()
        transpiler.transpile()

    def exe_bn(self):
        import transpiler_bn as bn

        lexer = bn.Lexer(self.script)
        tokens = lexer.tokenizer()
        transpiler = bn.Transpiler(self.extra_paths + self.file_c)
        parser = bn.Parser(tokens, transpiler)
        parser.parse()
        transpiler.transpile()

    """
    def build(self):
        print("Building...")
        _commmand = "gcc " + self.file_c + " -o " + self.file_exe
        os.system(_commmand)
        print("Building Completed!")

    def run(self):
        self.build()
        _command = self.only_file_name
        os.system(_command)
        print('\nExecuted!')
    """

while True:
    file_name = input("Enter the file name: ")
    if file_name:
        ethan = Ethan(file_name)
        ethan.execute()
    if file_name == '--exit':
        break