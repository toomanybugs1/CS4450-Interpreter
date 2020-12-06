keywords = {
    "=": "eq",
    "+=": "pleq",
    "-=": "mieq",
    "*=": "mueq",
    "/=": "dieq",
    "%=": "moeq",
    "^=": "exeq",

    "+": "pl",
    "-": "mi",
    "*": "mu",
    "/": "di",
    "%": "mo",
    "^": "ex",

    "True": "bool",
    "False": "bool",

    "print(": "print",
    "str(": "str_func",
    ")": "closed_par"
}

VARIABLE_MAP = {}

class Token:
    def __init__(self, value=None, line=None, line_tab_count=None):
        self.line = line
        self.line_tab_count = line_tab_count
        self.value = value

        # If its an existing variable, return the variable
        if value in VARIABLE_MAP.keys():
            self.var_name = value
            self.value = VARIABLE_MAP[value].value
            self.type = VARIABLE_MAP[value].type

        # Type determination
        # Part 1: is it a keyword?
        elif value in keywords.keys():
            self.type = keywords[value]

            if value == 'True':
                self.value = True
            elif value == 'False':
                self.value = False

        # Part 2: is it a string?
        elif value[0] == '"' and value[-1] == '"':
            self.type = 'string'
            self.value = value.strip('"')
        elif value[0] == "'" and value[-1] == "'":
            self.type = 'string'
            self.value = value.strip("'")
        else:
            # Part 3: is it a number?
            try:
                self.value = float(value)

                # Part 3.5: what KIND of number is it?
                if self.value.is_integer():
                    self.value = int(self.value)
                    self.type = 'integer'
                else:
                    self.type = 'float'

            # Part 4: if it's none of the above, its a variable name (pointer)
            except ValueError:
                self.type = 'var'
                VARIABLE_MAP[self.value] = self
                self.var_name = value
                self.value = 'null'

    def __str__(self):
        if self.line is None:
            return "Token<{}, '{}'>".format(self.type, self.value)
        else:
            return "Token<{}, '{}', line: {}>".format(self.type, self.value, self.line)

    __repr__ = __str__

    def __len__(self):
        if self.value is not None:
            return len(self.value)
        else:
            return 0

class Line:
    def __init__(self, tokens, num, tabs):
        self.tokens = tokens
        self.num = num
        self.tabs = tabs

    def __str__(self):
        return "Line: " + str(self.num)

    __repr__ = __str__

    def __len__(self):
        if (self.tokens is not None):
            return len(tokens)

    def eval(self):
        # This is used to evaluate an assignment statement
        # token 0 is the variable, token 1 is the assignment operator
        assign(self.tokens[0], self.tokens[1], self.tokens[2:])

    def print_statement(self):
        value = operate(self.tokens[1:-1])

        if (value.type == 'var'):
            print(VARIABLE_MAP[value.var_name].value)
        else:
            print(value.value)


    def str_statement(self, start, end):
        value = operate(self.tokens[start+1:end])
        value.value = str(value.value)
        value.type = 'string'

        if (value.type == 'var'):
            new_token = VARIABLE_MAP[value.var_name]
            self.tokens[end] = new_token
        else:
            self.tokens[end] = value

        del self.tokens[start:end]

# Helper methods:
# Handle assignment operators
def assign(var_tok, operator_tok, operand_toks):
    operand = None
    if len(operand_toks) == 1:
        operand = operand_toks[0]
    else:
        operand = operate(operand_toks)

    if operand.type == 'var':
        operand = VARIABLE_MAP[operand.var_name]

    if operator_tok.type == 'eq':
        VARIABLE_MAP[var_tok.var_name].value = operand.value
    elif operator_tok.type == 'pueq':
        VARIABLE_MAP[var_tok.var_name].value += operand.value
    elif operator_tok.type == 'mieq':
        VARIABLE_MAP[var_tok.var_name].value -= operand.value
    elif operator_tok.type == 'mueq':
        VARIABLE_MAP[var_tok.var_name].value *= operand.value
    elif operator_tok.type == 'dieq':
        VARIABLE_MAP[var_tok.var_name].value /= operand.value
    elif operator_tok.type == 'moeq':
        VARIABLE_MAP[var_tok.var_name].value %= operand.value
    elif operator_tok.type == 'exeq':
        VARIABLE_MAP[var_tok.var_name].value ^= operand.value

# Evaluate an equation into one token
def operate(tokens):
    i = 0
    line_num = tokens[0].line
    line_tab = tokens[0].line_tab_count

    # get variable values before operation
    for tok in tokens:
        if tok.type == 'var':
            tok.value = VARIABLE_MAP[tok.var_name].value
            if tok.value == 'null':
                raise NameError('name ' + tok.var_name + ' is not defined on line ' + str(tok.line))


    while i < len(tokens) - 1:
        result = None

        if tokens[i].type == 'mu':
            if tokens[i-1].type == 'string':
                result = Token("'" + str(tokens[i-1].value * tokens[i+1].value + "'"), line_num, line_tab)
            else:
                result = Token(str(tokens[i-1].value * tokens[i+1].value), line_num, line_tab)

        elif tokens[i].type == 'di':
            result = Token(str(tokens[i-1].value / tokens[i+1].value), line_num, line_tab)
        elif tokens[i].type == 'mo':
            result = Token(str(tokens[i-1].value % tokens[i+1].value), line_num, line_tab)

        if result is not None:
            tokens[i+1] = result
            del tokens[i-1:i+1]
            i -= 1

        else:
            i += 1

    i = 0
    while i < len(tokens) - 1:
        result = None

        if tokens[i].type == 'pl':
            if tokens[i-1].type == 'string':
                result = Token("'" + str(tokens[i-1].value + tokens[i+1].value + "'"), line_num, line_tab)
            else:
                result = Token(str(tokens[i-1].value + tokens[i+1].value), line_num, line_tab)
        elif tokens[i].type == 'mi':
            result = Token(str(tokens[i-1].value - tokens[i+1].value), line_num, line_tab)
        elif tokens[i].type == 'ex':
            result = Token(str(tokens[i-1].value ^ tokens[i+1].value), line_num, line_tab)

        if result is not None:
            tokens[i+1] = result
            del tokens[i-1:i+1]
            i -= 1

        else:
            i += 1

    return tokens[0]
