import sys
import parse

def main():
    # Verify correct usage of command
    if len(sys.argv) != 2:
        print("Usage: python interpret.py <script>")
        return

    lines = parse.parse_for_tokens(sys.argv[1])
    # look at all lines
    for line in lines:
        if (len(line.tokens) > 0):

            for i in range(len(line.tokens)):
                if line.tokens[i].type == 'str_func':
                    start_tok = i
                    for j in range(i, len(line.tokens)):
                        if line.tokens[j].type == 'closed_par':
                            end_tok = j
                            line.str_statement(start_tok, end_tok)
                            break
                    break

            # this must be some form of assignment
            if line.tokens[0].type == 'var':
                line.eval()

            if line.tokens[0].type == 'print':
                line.print_statement()

main()
