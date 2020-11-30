class Token:
    def __init__(self, type, value=None, line=None):
        self.type = type
        self.line = line
        if value is not None:
            self.value = value
        else:
            self.value = None

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
