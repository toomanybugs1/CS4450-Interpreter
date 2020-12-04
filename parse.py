from token import Token
from token import Line

def parse_for_tokens(filename):

    lines_of_tokens = []

    file = open(filename, 'r')
    line_count = 0

    # We'll loop this way to preserve the line number
    while True:
        line_count += 1
        line_tokens = []

        line = file.readline()

        if not line:
            break

        tabs =  line.count('\t')
        line.split()
        print(len(line))
        words = line.split(' ')

        for i in range(len(words)):
            token_value = words[i].strip()

            if token_value != '':
                line_tokens.append(Token(token_value, line_count, tabs))

        lines_of_tokens.append(Line(line_tokens, line_count, tabs))


    file.close()
    return lines_of_tokens
