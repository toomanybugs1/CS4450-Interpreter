keywords = {
    "=": "assignment"
}

class Token:
    def __init__(self, value=None, line=None, line_tab_count=None):
        self.line = line
        self.line_tab_count
        self.value = value

        if value in keywords.keys():
            self.type = keywords[value]
        else if value.isnumeric():
            self.type = 'number'
        else if isinstance(type, str):
            self.type = 'string'

        else:
            self.type = 'var'

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

class Lines:
    def __init__(self, tokens, num, tabs):
        self.tokens = tokens
        self.num = num
        self.tabs = tabs

    def __str__(self):
        return "Line: " + str(num)

    __repr__ = __str__

    def __len__(self):
        if (self.tokens is not None):
            return len(tokens)
