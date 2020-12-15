from token import Token
from token import Line
import re

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

        tabs =  line.count('   ')
        #print("Line:",line_count,"Tabs:",tabs)

        words = re.split(' |([a-zA-Z]+[0-9]+?)|(-?[0-9]+)|(!=)|(<=?)|(==?)|(>=?)|(\+=?)|(\-=?)|(\*=?)|(\/=?)|(%=?)|(\^=?)|(print\()|(\()|(\))|(".*?")|(\'.*?\')|(str\()|(int\()|( if\(? )|(\)?:)|( elif\(? )|( while )|( and )|( or )|(#.*?)|( in )|( for )|(range\()|(\,)|( break )', line)

        for i in range(len(words)):
            if words[i] != None:
                token_value = words[i].strip()
                if token_value == '#':
                    break

                if token_value != '':
                    line_tokens.append(Token(token_value, line_count, tabs))

        lines_of_tokens.append(Line(line_tokens, line_count, tabs))

    file.close()
    return lines_of_tokens
