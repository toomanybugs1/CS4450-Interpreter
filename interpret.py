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
        # this must be some form of assignment
        if line.tokens[0].value == 'var':


main()
