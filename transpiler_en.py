'''
    Lexer for programming language Ethan
'''

# Imports
import re

# Tokens Type

__INT__ = {
    'name': 'int32',
    'type' : 'int',
    'range' : range(-2147483648, 2147483648),
    'specifier' : '%d'
}

__LONG__ = {
    'name': 'int64',
    'type' : 'long',
    'range' : range(-9223372036854775808, 9223372036854775808),
    'specifier' : '%lld'
}

__FLOAT__ = {
    #range: -3.4e-38 to 3.4e38
    'name': 'float',
    'type' : 'float',
    'min': -3.4e-38,
    'max': 3.4e38,
    'specifier' : '%f'
}

__DOUBLE__ = {
    #range: -1.7e-308 to 1.7e308
    'name': 'double',
    'type' : 'double',
    'min': -1.7e-308,
    'max': 1.7e308,
    'specifier' : '%lf'
}

TT_INT = {
    'int': __INT__,
    'long': __LONG__,

}

TT_FLOAT = {
    'float': __FLOAT__,
    'double': __DOUBLE__
}

TT_EXP = 'EXP'
TT_STRING = 'STRING'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MULTIPLY'
TT_DIV = 'DIVIDE'
TT_MOD = 'MOD'
TT_IDX = 'IDX'
TT_EXC = 'EXC'
TT_EQ = 'EQ'
TT_EE = 'EE'
TT_NE = 'NE'
TT_GT = 'GT'
TT_GTE = 'GTE'
TT_LT = 'LT'
TT_LTE = 'LTE'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LSQB = 'LSQB'
TT_RSQB = 'RSQB'
TT_COMMA = 'COMMA'
TT_NEWLINE = 'NEWLINE'
TT_EOF = 'EOF'
TT_KEYWORD = 'KEYWORD'
TT_IDENTIFIRE = 'IDENTIFIRE'

KEYWORDS = [
    'int', 'long', 'float', 'double', 'exp', 'declare', 'as', 'let', 'imagine', 'now', 'if', 'else', 'then', 'end', 'while', 'repeat', 'and', 'or', 'not', 'print', 'get', 'separator'
    ]

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def match(self,type_, value=None):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        else:
            return f'{self.type}'

class Lexer:
    def __init__(self,text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def seek(self, step=1):
        if self.pos+step < len(self.text): return self.text[self.pos+step]
        else: return None

    def abort(self, message):
        print("Error: " + message)
        return None

    def tokenizer(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in '\n':
                tokens.append(Token(TT_NEWLINE))
                self.advance()
            elif self.current_char == '#':
                self.skip_comment()
            elif self.current_char == '.':
                if re.match('[\d]', self.seek()):
                    tokens.append(self.make_number())
                else:
                    char = self.current_char
                    self.advance()
                    return [], self.abort("Unexpected character: " + '"' + char + '"')
            elif re.search('[\.\d]', self.current_char):
                tokens.append(self.make_number())
            elif re.match('[\w]', self.current_char, re.UNICODE):
                tokens.append(self.make_identifire())
            elif self.current_char in ("'", '"'):
                tokens.append(self.make_string(self.current_char))
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, '+'))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, '-'))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, '*'))
                self.advance()
            elif self.current_char == '/':
                if self.seek() == '/': tokens.append(Token(TT_IDX))
                else: tokens.append(Token(TT_DIV, '/'))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TT_MOD, '%'))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA))
                self.advance()
            elif self.current_char == '=':
                if self.seek() == '=':
                    tokens.append(Token(TT_EE, '=='))
                    self.advance()
                else: tokens.append(Token(TT_EQ, '='))
                self.advance()
            elif self.current_char == '!':
                if self.seek() == '=':
                    tokens.append(Token(TT_NE, '!='))
                    self.advance()
                else: tokens.append(Token(TT_EXC))
                self.advance()
            elif self.current_char == '>':
                if self.seek() == '=':
                    tokens.append(Token(TT_GTE, '>='))
                    self.advance()
                else: tokens.append(Token(TT_GT, '>'))
                self.advance()
            elif self.current_char == '<':
                if self.seek() == '=':
                    tokens.append(Token(TT_LTE, '<='))
                    self.advance()
                else: tokens.append(Token(TT_LT, '<'))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, '('))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, ')'))
                self.advance()
            else:
                char = self.current_char
                self.advance()
                return [], self.abort("Unexpected character: " + '"' + char + '"')
        tokens.append(Token(TT_EOF))
        return tokens

    def skip_comment(self):
        self.advance()
        while self.current_char != '\n':
            self.advance()
        self.advance()

    def make_number(self):
        num_str = ''
        ln = len(self.text)
        dot_count = e_count = minus_count = 0

        while self.current_char != None and (re.match('[\.\d]', self.current_char) or self.current_char in 'Ee-'):
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'

            elif self.current_char == 'e' or self.current_char == 'E':
                if e_count == 1:
                    break
                elif self.pos+1 < ln and re.match('[\d]', self.seek(-1)):
                    if re.match('[\d]', self.seek()):
                        num_str += 'e'
                    elif self.seek() == '-':
                        if self.pos+2 < ln and re.match('[\d]', self.seek(2)):
                            num_str += 'e'
                        else:
                            break
                    else:
                        break
                else:
                    break
                e_count += 1

            elif self.current_char == '-':
                if minus_count == 1:
                    break
                elif self.pos+1 < ln and self.seek(-1) == 'e' or self.seek(-1) == 'E':
                    if re.match('[\d]', self.seek()):
                        num_str += '-'
                    else:
                        break
                else:
                    break
                minus_count += 1

            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0 and e_count == 0:
            # int
            num = int(num_str)
            if num in TT_INT['int']['range']:
                return Token(TT_INT['int']['type'], num)
            else:
                return Token(TT_INT['long']['type'], num)
        else:
            # float
            num = float(num_str)
            if e_count != 0:
                return Token('exp', num)
            else:
                if num >= TT_FLOAT['float']['min'] and num <= TT_FLOAT['float']['max']:
                    return Token(TT_FLOAT['float']['type'], num)
                elif num >= TT_FLOAT['double']['min'] and num <= TT_FLOAT['double']['max']:
                    return Token(TT_FLOAT['double']['type'], num)
                else:
                    return [], self.abort("Value overflowr: " + num)

    def make_identifire(self):
        id_str = ''

        while self.current_char != None and re.match('[\w]', self.current_char, re.UNICODE):
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIRE
        return Token(tok_type, id_str)

    def make_string(self, qt):
        string = ''
        self.advance()

        while self.current_char !=None and self.current_char != qt:
            string += self.current_char
            self.advance()

        self.advance()
        return Token(TT_STRING, string)

class Parser:
    def __init__(self, tokens, transpiler):
        self.tokens = tokens
        self.transpiler = transpiler
        self.idx = -1
        self.current_tok = None
        self.error = False
        self.declare_headers = {'stdlib': False, 'stdio': False, 'conio': False, 'math': False, 'complex': False, 'time': False}
        self.declared_vars = []
        self.declared_vars_int = []
        self.declared_vars_long = []
        self.declared_vars_float = []
        self.declared_vars_double = []
        self.declared_vars_exp = []
        self.datastack = []
        #self.expr_ln = 0
        self.advance()

    def advance(self):
        self.idx += 1
        self.current_tok = self.tokens[self.idx] if self.idx < len(self.tokens) else None

    def seek(self, step=1):
        if self.idx+step < len(self.tokens): return self.tokens[self.idx+step]
        else: return None

    def parse(self):
        print("Compiling started...")
        self.transpiler.wMain("int main() {\n")
        while self.current_tok.type == TT_NEWLINE:
            self.advance()

        while self.current_tok.type != TT_EOF:
            self.statement()
            if self.error: return None
        print("Compiling finished!")
        self.transpiler.wMain("return 0;\n}")

    def abort(self, message):
        print("Error: " + message)
        self.error = True

    def dt_header(self, file):
        if file == 'stdio':
            if self.declare_headers['stdio'] == False:
                self.declare_headers['stdio'] = True
                self.transpiler.wHead('#include <stdio.h>')

    def write_declare(self, _type, _varlist):
        if _type == 'exp': _type = 'double'
        self.transpiler.wMain(_type + ' ')
        self.transpiler.wMain(','.join(_varlist))
        self.transpiler.wMain(';\n')

        if _type == 'int':
            for var in _varlist: self.declared_vars_int.append(var)
        elif _type == 'long long int':
            for var in _varlist: self.declared_vars_long.append(var)
        elif _type == 'float':
            for var in _varlist: self.declared_vars_float.append(var)
        elif _type == 'double':
            for var in _varlist: self.declared_vars_double.append(var)
        elif _type == 'exp':
            for var in _varlist: self.declared_vars_exp.append(var)

    def dt_type(self, _types): #, length):
        if 'exp' in _types:
            self.datastack = []
            #self.expr_ln = 0
            return ('exp') #, length)
        elif 'double' in _types:
            self.datastack = []
            #self.expr_ln = 0
            return ('double') #, length)
        elif 'float' in _types:
            self.datastack = []
            #self.expr_ln = 0
            return ('float') #, length)
        elif 'long' in _types:
            self.datastack = []
            #self.expr_ln = 0
            return ('long') #, length)
        else:
            self.datastack = []
            #self.expr_ln = 0
            return ('int') #, length)

    def write_specifier_for_printf(self, _type):
        if _type == 'long':
            self.transpiler.set_data_type('%lld', '$_SPECIFIER')
        elif _type == 'exp':
            self.transpiler.set_data_type('%E', '$_SPECIFIER')
        elif _type == 'int':
            self.transpiler.set_data_type('%d', '$_SPECIFIER')
        elif _type == 'float':
            self.transpiler.set_data_type('%f', '$_SPECIFIER')
        elif _type == 'double':
            self.transpiler.set_data_type('%lf', '$_SPECIFIER')

    def write_scanf(self, _specifier, _varList):
        ln = len(_varList)
        # write specifier
        i = 0
        while i < ln:
            self.transpiler.wMain(_specifier)
            i += 1
        self.transpiler.wMain('", ')
        # write &varname
        i = 0
        while i<ln:
            if i+1 == ln: self.transpiler.wMain('&'+ _varList[i])
            else: self.transpiler.wMain('&'+ _varList[i] + ', ')
            i += 1
        self.transpiler.wMain(');\n')

    def type_check_for_reassign(self, _var, _type):
        if _type == 'long':
            if not _var in self.declared_vars_long:
                self.abort("Worng Type-Casting: " + "'" + _var + "'" + ' is not declared with ' + _type + ' type!')
        elif _type == 'exp':
            if not _var in self.declared_vars_exp:
                self.abort("Worng Type-Casting: " + "'" + _var + "'" + ' is not declared with ' + _type + ' type!')
        elif _type == 'int':
            if not _var in self.declared_vars_int:
                self.abort("Worng Type-Casting: " + "'" + _var + "'" + ' is not declared with ' + _type + ' type!')
        elif _type == 'float':
            if not _var in self.declared_vars_float:
                self.abort("Worng Type-Casting: " + "'" + _var + "'" + ' is not declared with ' + _type + ' type!')
        elif _type == 'double':
            if not _var in self.declared_vars_double:
                self.abort("Worng Type-Casting: " + "'" + _var + "'" + ' is not declared with ' + _type + ' type!')
        else:
            self.abort("Unexpected Data-Type: " + _type)

    def write_type_for_var_assign(self, _var, _type):
        if _type == 'long':
            self.declared_vars_long.append(_var)
            self.transpiler.set_data_type('long long int')
        elif _type == 'exp':
            self.declared_vars_exp.append(_var)
            self.transpiler.set_data_type('double')
        elif _type == 'int':
            self.declared_vars_int.append(_var)
            self.transpiler.set_data_type('int')
        elif _type == 'float':
            self.declared_vars_float.append(_var)
            self.transpiler.set_data_type('float')
        elif _type == 'double':
            self.declared_vars_double.append(_var)
            self.transpiler.set_data_type('double')
        else: self.abort("Unexpected Data-Type: " + _type + 'for ' + _var)

    def _nl(self):
        # NewLine
        while self.current_tok.type == TT_NEWLINE:
            self.advance()

    def isComparisionOperator(self):
        return self.current_tok.type == TT_GT or self.current_tok.type == TT_GTE or self.current_tok.type == TT_LT or self.current_tok.type == TT_LTE or self.current_tok.type == TT_EE or self.current_tok.type == TT_NE

    def isLogicalOperator(self):
        return self.current_tok.match(TT_KEYWORD, 'and') or self.current_tok.match(TT_KEYWORD, 'or')

    def var_declare(self):
        # declare
        _vars = []
        self.advance()
        
        if self.current_tok.type != TT_IDENTIFIRE:
            self.abort("Expected: An identifire\nGiven: " + self.current_tok.type)
        if self.current_tok.value in self.declared_vars:
            self.abort("Identifire: '" + self.current_tok.value + "' has been declared already!\n       Probably want to use 'now' to assign its value.")
        _vars.append(self.current_tok.value)
        self.declared_vars.append(self.current_tok.value)
        self.advance()
        if self.current_tok.type == TT_COMMA:
            while self.current_tok.type == TT_COMMA:
                self.advance()
                if self.current_tok.type != TT_IDENTIFIRE:
                    self.abort("Expected: An identifire\nGiven: " + self.current_tok.type)
                if self.current_tok.value in self.declared_vars:
                    self.abort("Identifire: '" + self.current_tok.value + "' has been declared already!\n       Probably want to use 'now' to assign its value.")
                _vars.append(self.current_tok.value)
                self.declared_vars.append(self.current_tok.value)
                self.advance()

        if not self.current_tok.match(TT_KEYWORD, 'as'):
            self.abort("Expected: keyword, 'as'\nGiven: " + self.current_tok.value)
        self.advance()
        if self.current_tok.match(TT_KEYWORD, 'int') or self.current_tok.match(TT_KEYWORD, 'long') or self.current_tok.match(TT_KEYWORD, 'float') or self.current_tok.match(TT_KEYWORD, 'double'):
            if self.current_tok.value == 'long':
                self.write_declare('long long int', _vars)
                for var in _vars: self.declared_vars_long.append(var)
                self.advance()
            elif self.current_tok.value == 'int':
                self.write_declare('int', _vars)
                for var in _vars: self.declared_vars_int.append(var)
                self.advance()
            elif self.current_tok.value == 'float':
                self.write_declare('float', _vars)
                for var in _vars: self.declared_vars_float.append(var)
                self.advance()
            elif self.current_tok.value == 'double':
                self.write_declare('double', _vars)
                for var in _vars: self.declared_vars_double.append(var)
                self.advance()
            elif self.current_tok.value == 'exp':
                self.write_declare('double', _vars)
                for var in _vars: self.declared_vars_exp.append(var)
                self.advance()
            else:
                self.abort("Unexpected: " + self.current_tok.value + "\n\tExpected: 'int', 'long', 'float' or 'double'")
        else:
            self.abort("Unexpected: " + self.current_tok.value + "\n\tExpected: 'int', 'long', 'float' or 'double'")

    def var_assign(self):
        # reassigning
        _varAssignText = '$let '
        _vars = []
        self.advance()
        if self.current_tok.type != TT_IDENTIFIRE:
            self.abort("Expected: An identifire\nGiven: " + self.current_tok.type)
        if self.current_tok.value in self.declared_vars:
            self.abort("Identifire: '" + self.current_tok.value + "' has been declared already!\n\tProbably want to use 'now' instead of 'let' to change its value.")
        _vars.append(self.current_tok.value)
        self.declared_vars.append(self.current_tok.value)
        _varAssignText += self.current_tok.value
        self.advance()
        if self.current_tok.type != TT_EQ:
            self.abort("Expected: '='\nGiven: " + self.current_tok.type)
        _varAssignText += ' = '
        self.advance()
        self.transpiler.wMain(_varAssignText)
        _type = self.expression()
        self.write_type_for_var_assign(_vars[0], _type)
        # ending with ' ; '
        self.transpiler.wMain(';\n')


        if self.current_tok.type == TT_COMMA:
            while self.current_tok.type == TT_COMMA:
                _varAssignText = '$let '
                self.advance()
                if self.current_tok.type != TT_IDENTIFIRE:
                    self.abort("Expected: An identifire\nGiven: " + self.current_tok.type)
                if self.current_tok.value in self.declared_vars:
                    self.abort("Identifire: '" + self.current_tok.value + "' has been declared already!\n\tProbably want to use 'now' instead of 'let' to change its value.")
                _vars.append(self.current_tok.value)
                self.declared_vars.append(self.current_tok.value)
                _varAssignText += self.current_tok.value
                self.advance()
                if self.current_tok.type != TT_EQ:
                    self.abort("Expected: '='\nGiven: " + self.current_tok.type)
                _varAssignText += ' = '
                self.advance()
                self.transpiler.wMain(_varAssignText)
                _type = self.expression()
                self.write_type_for_var_assign(_vars[-1], _type)
                # ending with ' ; '
                self.transpiler.wMain(';\n')
                _vars = []
        else:
            self.declared_vars.append(_vars[0])
            _vars = []

    def var_reassign(self):
        # reassign
        _vars = []
        _varAssignText = ''
        if self.current_tok.type != TT_IDENTIFIRE:
            self.abort("Expected: An identifire\nGiven: " + self.current_tok.type)
        if not self.current_tok.value in self.declared_vars:
            self.abort(self.current_tok.value + " hasn't been declared yet!")
        _varAssignText += self.current_tok.value
        _vars.append(self.current_tok.value)
        self.advance()
        if self.current_tok.type != TT_EQ:
            self.abort("Expected: '='\nGiven: " + self.current_tok.type)
        _varAssignText += ' = '
        self.advance()
        self.transpiler.wMain(_varAssignText)
        _type = self.expression()
        self.type_check_for_reassign(_vars[0], _type)
        self.transpiler.wMain(';\n')
        _vars = []
        if self.current_tok.type == TT_COMMA:
            while self.current_tok.type == TT_COMMA:
                _varAssignText = ''
                self.advance()
                if self.current_tok.type != TT_IDENTIFIRE:
                    self.abort("Expected: An identifire\nGiven: " + self.current_tok.type)
                if not self.current_tok.value in self.declared_vars:
                    self.abort(self.current_tok.value, "hasn't been declared yet!")
                _varAssignText += self.current_tok.value
                _vars.append(self.current_tok.value)
                self.advance()
                if self.current_tok.type != TT_EQ:
                    self.abort("Expected: '='\nGiven: " + self.current_tok.type)
                _varAssignText += ' = '
                self.advance()
                self.transpiler.wMain(_varAssignText)
                _type = self.expression()
                self.type_check_for_reassign(_vars[0], _type)
                self.transpiler.wMain(';\n')
                _vars = []

    def if_stmt(self):
        # if
        self.transpiler.wMain('if (')
        self.advance()
        self.comparision()
        if not self.current_tok.match(TT_KEYWORD, 'then'):
            self.abort("Expected: keyword, 'then'\nGiven: " + self.current_tok.value)
        self.transpiler.wMain(') {\n')
        self.advance()
        if self.current_tok.type != TT_NEWLINE:
            self.statement()
            self.transpiler.wMain('}\n')
            self.else_expr()
        else:
            self._nl()
            while not self.current_tok.match(TT_KEYWORD, 'end'):
                self.statement()   
            
            if not self.current_tok.match(TT_KEYWORD, 'end'):
                self.abort("Expected: 'end' keyword\n\tGiven: " + self.current_tok.value)
            self.transpiler.wMain('}\n')
            self.advance()
            if self.current_tok.type == TT_NEWLINE:
                self._nl()
            self.else_expr()

    def else_expr(self):
        if self.current_tok.match(TT_KEYWORD, 'else'):
            self.advance()
            if self.current_tok.match(TT_KEYWORD, 'if'):
                self.transpiler.wMain('else ')
                # else if
                self.if_stmt()
            else:
                # else
                self.transpiler.wMain('else {\n')
                if self.current_tok.type != TT_NEWLINE:
                    self.statement()
                else:
                    self._nl()
                    while not self.current_tok.match(TT_KEYWORD, 'end'):
                        self.statement()
                
                    if not self.current_tok.match(TT_KEYWORD, 'end'):
                        self.abort("Expected: 'end' keyword\n\tGiven: " + self.current_tok.value)
                    self.advance()
                self.transpiler.wMain('}\n')

    def while_stmt(self):
        # while
        self.transpiler.wMain('while (')
        self.advance()
        self.comparision()
        if not self.current_tok.match(TT_KEYWORD, 'repeat'):
            self.abort("Expected: 'repeat' keyword\nGiven: " + self.current_tok.value)
        self.transpiler.wMain(') {\n')
        self.advance()
        if self.current_tok.type != TT_NEWLINE:
            self.statement()
        else:
            self._nl()
            while not self.current_tok.match(TT_KEYWORD, 'end'):
                self.statement()   
            
            if not self.current_tok.match(TT_KEYWORD, 'end'):
                self.abort("Expected: 'end' keyword\n\tGiven: " + self.current_tok.value)
            self.advance()
        self.transpiler.wMain('}\n')

    def print_stmt(self):
        # print
        _isComma = False
        _end = '\\n'
        _separator = ' '
        self.dt_header('stdio')
        self.advance()
        self.transpiler.wMain('printf("')
        if self.current_tok.type == TT_STRING:
            # String
            if self.seek().type == TT_COMMA: self.transpiler.wMain(self.current_tok.value + '$_SEPARATOR"')
            else: self.transpiler.wMain(self.current_tok.value + '$_END"')
            self.advance()
        else:
            if self.seek().type == TT_COMMA: self.transpiler.wMain('$_SPECIFIER$_SEPARATOR", ')
            else: self.transpiler.wMain('$_SPECIFIER$_END", ')
            _type = self.expression()
            self.write_specifier_for_printf(_type)
        # ending with ' ; '
        self.transpiler.wMain(');\n')

        if self.current_tok.type == TT_COMMA:
            _isComma = True
            while self.current_tok.type == TT_COMMA:
                self.transpiler.wMain('printf("')
                self.advance()
                if self.current_tok.type == TT_STRING:
                    # string
                    if self.seek().type == TT_COMMA: self.transpiler.wMain(self.current_tok.value + '$_SEPARATOR"')
                    else: self.transpiler.wMain(self.current_tok.value + '$_END"')
                    self.advance()
                else:
                    if self.seek().type == TT_COMMA: self.transpiler.wMain('$_SPECIFIER$_SEPARATOR", ')
                    else: self.transpiler.wMain('$_SPECIFIER$_END", ')
                    _type = self.expression()
                    self.write_specifier_for_printf(_type)
                # ending with ' ; '
                self.transpiler.wMain(');\n')

        if self.current_tok.type == TT_EXC:
            while self.current_tok.type == TT_EXC:
                self.advance()
                if self.current_tok.match(TT_KEYWORD, 'separator'):
                    self.advance()
                    if self.current_tok.type != TT_STRING:
                        self.abort("Expected a string or a '.'")
                    else:
                        _separator = self.current_tok.value
                        self.advance()
                elif self.current_tok.match(TT_KEYWORD, 'end'):
                    self.advance()
                    if self.current_tok.type != TT_STRING:
                        self.abort("NEED STRING")
                    else:
                        _end = self.current_tok.value
                        self.advance()

        # Warping up
        if _isComma:
            self.transpiler.set_data_type(_separator, '$_SEPARATOR', -1)
            self.transpiler.set_data_type(_end, '$_END', -1)
        else:
            self.transpiler.set_data_type('', '$_SEPARATOR', -1)
            self.transpiler.set_data_type(_end, '$_END', -1)

    def get_stmt(self):
        # get
        _vars = []
        _undeclared_vars = []
        _is_undeclared = False
        self.advance()
        if self.current_tok.type != TT_IDENTIFIRE:
            self.abort("Expected: An identifire\nGiven: " + self.current_tok.type)
        if not self.current_tok.value in self.declared_vars:
            _is_undeclared = True
            _undeclared_vars.append(self.current_tok.value)
        _vars.append(self.current_tok.value)
        self.advance()
        if self.current_tok.type == TT_COMMA:
            while self.current_tok.type == TT_COMMA:
                self.advance()
                if self.current_tok.type != TT_IDENTIFIRE:
                    self.abort("Expected: An identifire\nGiven: " + self.current_tok.type)
                if not self.current_tok.value in self.declared_vars:
                    _is_undeclared = True
                    _undeclared_vars.append(self.current_tok.value)
                _vars.append(self.current_tok.value)
                self.advance()
        if not self.current_tok.match(TT_KEYWORD, 'as'):
            self.abort("Expected: keyword, 'as'\nGiven: " + self.current_tok.value)
        self.advance()
        if self.current_tok.match(TT_KEYWORD, 'int'):
            if _is_undeclared: self.write_declare('int', _undeclared_vars)
            self.transpiler.wMain('scanf("')
            self.write_scanf('%d', _vars)
            for var in _vars:
                self.declared_vars_int.append(var)
            self.advance()
        elif self.current_tok.match(TT_KEYWORD, 'long'):
            if _is_undeclared: self.write_declare('long long int', _undeclared_vars)
            self.transpiler.wMain('scanf("')
            
            self.write_scanf('%lld', _vars)
            for var in _vars: self.declared_vars_long.append(var)
            self.advance()
        elif self.current_tok.match(TT_KEYWORD, 'float'):
            if _is_undeclared: self.write_declare('float', _undeclared_vars)
            self.transpiler.wMain('scanf("')
            self.write_scanf('%f', _vars)
            for var in _vars: self.declared_vars_float.append(var)
            self.advance()
        elif self.current_tok.match(TT_KEYWORD, 'double'):
            if _is_undeclared: self.write_declare('double', _undeclared_vars)
            self.transpiler.wMain('scanf("')
            self.write_scanf('%lf', _vars)
            for var in _vars: self.declared_vars_double.append(var)
            self.advance()
        elif self.current_tok.match(TT_KEYWORD, 'exp'):
            if _is_undeclared: self.write_declare('double', _undeclared_vars)
            self.transpiler.wMain('scanf("')
            self.write_scanf('%E', _vars)
            for var in _vars: self.declared_vars_exp.append(var)
            self.advance()
        else:
            self.abort("Expected 'int', 'long', 'float' or 'double'")
        
        for var in _vars: self.declared_vars.append(var)

    def comp_expr(self):
        # comparision
        self.expression()
        if self.isComparisionOperator():
            self.transpiler.wMain(' ' + self.current_tok.value + ' ')
            self.advance()
            self.expression()
            if self.isLogicalOperator():
                _logicalOperator = self.current_tok.value
                if _logicalOperator == 'and': self.transpiler.wMain(' && ')
                else: self.transpiler.wMain(' || ')
                self.advance()
                self.comparision()
        else:
            self.abort("Expected < or > or =< or <=")

    def not_expr(self):
        self.transpiler.wMain('(')
        self.expression()
        if self.isComparisionOperator():
            self.transpiler.wMain(' ' + self.current_tok.value + ' ')
            self.advance()
            self.expression()
            self.transpiler.wMain(')')
            if self.isLogicalOperator():
                _logicalOperator = self.current_tok.value
                if _logicalOperator == 'and': self.transpiler.wMain(' && ')
                else: self.transpiler.wMain(' || ')
                self.advance()
                self.comparision()
        self.transpiler.wMain(')')        

        if self.isLogicalOperator():
            _logicalOperator = self.current_tok.value
            if _logicalOperator == 'and': self.transpiler.wMain(' && ')
            else: self.transpiler.wMain(' || ')
            self.advance()
            self.comparision()

    def comparision(self):
        # logical
        if self.current_tok.match(TT_KEYWORD, 'not'):
            self.transpiler.wMain('!')
            self.advance()
            self.not_expr()
        else:
            self.comp_expr()
    
    def expression(self):
        # expression
        self.term()
        while self.current_tok.type in (TT_PLUS, TT_MINUS):
            self.transpiler.wMain(self.current_tok.value)
            #self.expr_ln += 1
            self.advance()
            self.term()
        return self.dt_type(self.datastack) #self.expr_ln)

    def term(self):
        # term
        self.unary()
        while self.current_tok.type in (TT_MUL, TT_DIV, TT_MOD):
            self.transpiler.wMain(self.current_tok.value)
            #self.expr_ln += 1
            self.advance()
            self.unary()

    def unary(self):
        # unary
        if self.current_tok.type in (TT_PLUS, TT_MINUS):
            self.transpiler.wMain(self.current_tok.value)
            #self.expr_ln += 1
            self.advance()
        self.primary()

    def primary(self):
        _type = self.current_tok.type
        _value = self.current_tok.value
        #print("PRIMARY (" + str(_value) + ")("+_type+")")
        if _type in ('int', 'long', 'float', 'double', 'exp'):
            self.transpiler.wMain(str(self.current_tok.value))
            #self.expr_ln += len(str(self.current_tok.value))
            self.datastack.append(_type)
            self.advance()
        elif _type == TT_IDENTIFIRE:
            if not _value in self.declared_vars:
                self.abort(_value + " hasn't been declared yet!")
            else:
                _id = self.current_tok.value
                self.transpiler.wMain(_id)
                if _id in self.declared_vars_int:
                    self.datastack.append('int')
                elif _id in self.declared_vars_long:
                    self.datastack.append('long')
                elif _id in self.declared_vars_float:
                    self.datastack.append('float')
                elif _id in self.declared_vars_double:
                    self.datastack.append('double')
                elif _id in self.declared_vars_exp:
                    self.datastack.append('exp')
                self.advance()
        elif _type == TT_LPAREN:
            self.transpiler.wMain(self.current_tok.value)
            self.advance()
            self.expression()
            if self.current_tok.type != TT_RPAREN:
                self.abort("Expected: A ')'\nGiven: " + self.current_tok)
            self.transpiler.wMain(self.current_tok.value)
            #self.expr_ln += 2
            self.advance()
        else:
            self.abort("Unknown data-type :" + str(_value))

    def statement(self):
        if self.current_tok.type == TT_NEWLINE:
            self._nl()

        elif self.current_tok.match(TT_KEYWORD, 'declare'):
            self.var_declare()

        elif self.current_tok.match(TT_KEYWORD, 'let') or self.current_tok.match(TT_KEYWORD, 'imagine'):
            self.var_assign()

        elif self.current_tok.type == TT_IDENTIFIRE:
            self.var_reassign()

        elif self.current_tok.match(TT_KEYWORD, 'if'):
            self.if_stmt()

        elif self.current_tok.match(TT_KEYWORD, 'while'):
            self.while_stmt()

        elif self.current_tok.match(TT_KEYWORD, 'print'):
            self.print_stmt()

        elif self.current_tok.match(TT_KEYWORD, 'get'):
            self.get_stmt()

        else:
            if self.current_tok.value: self.abort("Unexpected " + self.current_tok.value)
            else: self.abort("Unexpected " + self.current_tok.type)

class Transpiler:
    def __init__(self, fn='out.c'):
        self.fn = fn
        self.header = ''
        self.main = ''
        self.other = ''

    def wHead(self, head):
        self.header += head + '\n\n'

    def wMain(self, code):
        self.main += code

    def set_data_type(self, _type, _pre='$let', _count=1):
        self.main = self.main.replace(_pre, _type, _count)
        #self.main.format(let = _type)

    def wOther(self, code):
        self.header += code

    def transpile(self):
        try:
            with open(self.fn, 'w') as f:
                f.write(self.header+self.other+self.main)
                f.close()
        except Exception as e:
            return "Error: " + str(e)


data = """
print "Enter 3 numbers:"
get x,y,z as int

if x>y and x>z then print x , 'is greater!' else if x<y and z<y then print y , 'is greater!' else print z , 'is greater!'

let i = 10
while i>0 repeat
    print i
    i = i - 1
end
print 'The End' !end ''
"""

test = """
# Methematical preceding check
declare a,b,c as int
now a = 1, b = 2, c = 3
print a+b*c, (a+b)*c
"""

"""

#This is for debuging process only.

lexer = Lexer(test)
tokens = lexer.tokenizer()
#print(tokens)

transpiler = Transpiler()
parser = Parser(tokens, transpiler)
parser.parse()
transpiler.transpile()

"""

"""
    * Fix bug in print statement
    * Add function
    * Warp up, clean up and refactore the code
"""