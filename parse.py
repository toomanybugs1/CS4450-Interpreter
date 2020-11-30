from token import Token

def parse_for_tokens(filename):

    tokens = []

    file = open(filename, 'r')
    line_count = 0

    # We'll loop this way to preserve the line number
    while True:
        line_count += 1

        line = file.readline()

        if not line:
            break

        line.split()
        print(len(line))
        words = line.split(' ')

        for i in range(len(words)):
            token_value = words[i].strip()

            if token_value != '':
                tokens.append(Token('none', token_value, line_count))


    file.close()
    return tokens
