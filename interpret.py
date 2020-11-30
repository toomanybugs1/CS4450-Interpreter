import sys
import parse

def main():
    # Verify correct usage of command
    if len(sys.argv) != 2:
        print("Usage: python interpret.py <script>")
        return

    tokens = parse.parse_for_tokens(sys.argv[1])
    for token in tokens:
        print(token)

main()
