import sys
import parse
import token
import copy

def main():
    # This variable lets us know if the previous if condition was true
    # If its false, then we know to execute the else/elif statement
    PREVIOUS_IF_SUCCESSFUL = False

    # When looping is above zero, execute the line and decrement
    # When its 0, set x back to the line where the while starts
    # When its -1, don't do anything
    LOOPING = -1
    WHILE_COND_LINE = -1

    # We'll store the for iterator and pop off the first item every time we loop
    # These are all stored in a stack so there can be loops inside loops
    # FOR_ITERATOR = []
    # FOR_START = -1
    # FOR_LOOP_END = -1
    FOR_STACK = []

    # These are stored lines because functions like str() need to be recalculated
    # when we loop
    STORED_LINES = {}

    # Verify correct usage of command
    if len(sys.argv) != 2:
        print("Usage: python interpret.py <script>")
        return

    lines = parse.parse_for_tokens(sys.argv[1])

    # look at all lines
    x = 0
    while x < len(lines):
        if (len(lines[x].tokens) > 0):
            for i in range(len(lines[x].tokens)):
                if x in STORED_LINES.keys():
                    lines[x].tokens = copy.deepcopy(STORED_LINES[x])

                if lines[x].tokens[i].type == 'str_func':
                    STORED_LINES[x] = copy.deepcopy(lines[x].tokens)

                    start_tok = i
                    for j in range(i, len(lines[x].tokens)):
                        if lines[x].tokens[j].type == 'closed_par':
                            end_tok = j
                            lines[x].str_statement(start_tok, end_tok)
                            break
                    break

                elif lines[x].tokens[i].type == 'int_func':
                    STORED_LINES[x] = copy.deepcopy(lines[x].tokens)

                    start_tok = i
                    for j in range(i, len(lines[x].tokens)):
                        if lines[x].tokens[j].type == 'closed_par':
                            end_tok = j
                            lines[x].int_statement(start_tok, end_tok)
                            break
                    break

            # this must be some form of assignment
            if lines[x].tokens[0].type == 'var':
                lines[x].eval()

            # print statement
            elif lines[x].tokens[0].type == 'print':
                lines[x].print_statement()

            # if keyword
            elif lines[x].tokens[0].type == 'if':
                # Determine how many lines to skip if the condition is false
                lines_to_skip_if_false = 1
                cur_line = x + 1
                conditional_tabs = lines[x].tabs

                while lines[cur_line].tabs > conditional_tabs:
                    lines_to_skip_if_false += 1
                    cur_line += 1

                if token.compare_full(copy.deepcopy(lines[x].tokens)).value == False:
                    x += lines_to_skip_if_false
                    PREVIOUS_IF_SUCCESSFUL = False
                    if LOOPING > 0:
                        LOOPING -= lines_to_skip_if_false

                    continue

                else:
                    PREVIOUS_IF_SUCCESSFUL = True

            elif lines[x].tokens[0].type == 'elif':
                # Determine how many lines to skip if the condition is false
                lines_to_skip_if_false = 1
                cur_line = x + 1
                conditional_tabs = lines[x].tabs

                while lines[cur_line].tabs > conditional_tabs:
                    lines_to_skip_if_false += 1
                    cur_line += 1

                # if one of the previous ifs was true, then skip
                if PREVIOUS_IF_SUCCESSFUL:
                    x += lines_to_skip_if_false
                    if LOOPING > 0:
                        LOOPING -= lines_to_skip_if_false

                    continue

                # if the previous ifs werent true, and neither was this one,
                # skip and keep going
                elif token.compare_full(copy.deepcopy(lines[x].tokens)).value == False:
                                x += lines_to_skip_if_false
                                if LOOPING > 0:
                                    LOOPING -= lines_to_skip_if_false
                                continue

                # if this one was successful, mark true and continue
                else:
                    PREVIOUS_IF_SUCCESSFUL = True

            elif lines[x].tokens[0].type == 'else':
                # Determine how many lines to skip if the previous if statement was true
                lines_to_skip_if_false = 1
                cur_line = x + 1
                conditional_tabs = lines[x].tabs

                while lines[cur_line].tabs > conditional_tabs:
                    lines_to_skip_if_false += 1
                    cur_line += 1

                # dont execute if the previous if statement was true
                if PREVIOUS_IF_SUCCESSFUL:
                    x += lines_to_skip_if_false
                    PREVIOUS_IF_SUCCESSFUL = False
                    if LOOPING > 0:
                        LOOPING -= lines_to_skip_if_false
                    continue

            elif lines[x].tokens[0].type == 'while':
                # Determine how many lines to skip if the condition is false
                lines_inside_while = 0
                cur_line = x + 1
                conditional_tabs = lines[x].tabs

                while lines[cur_line].tabs > conditional_tabs:
                    lines_inside_while += 1
                    cur_line += 1

                # if its true
                if token.compare_full(copy.deepcopy(lines[x].tokens)).value == True:
                    WHILE_COND_LINE = x
                    LOOPING = lines_inside_while
                    x += 1
                    continue
                else:
                    LOOPING = -1
                    x += lines_inside_while + 1
                    continue

            elif lines[x].tokens[0].type == "for":
                # Determine how many lines are in the loop
                lines_inside_for = 0
                cur_line = x + 1
                conditional_tabs = lines[x].tabs

                while lines[cur_line].tabs > conditional_tabs:
                    lines_inside_for += 1
                    cur_line += 1

                # for loop hasn't started
                if token.VARIABLE_MAP[lines[x].tokens[1].var_name].value == 'null':
                    range_left = []
                    range_right = []
                    comma_index = 0

                    for i in range(4, len(lines[x].tokens)):
                        if lines[x].tokens[i].type == 'comma':
                            comma_index = i
                            break
                        range_left.append(lines[x].tokens[i])

                    for i in range(comma_index + 1, len(lines[x].tokens) - 1):
                        range_right.append(lines[x].tokens[i])

                    range_1 = int(token.operate(range_left).value)
                    range_2 = int(token.operate(range_right).value)

                    FOR_STACK.insert(0, {
                        "FOR_ITERATOR": list(range(range_1, range_2)),
                        "FOR_START": x,
                        "FOR_END": x + lines_inside_for,
                        "FOR_VAR": lines[x].tokens[1].var_name
                    })
                    lines[x].tokens[1].value = FOR_STACK[0]['FOR_ITERATOR'].pop(0)
                    token.VARIABLE_MAP[lines[x].tokens[1].var_name].value = lines[x].tokens[1].value

                # still more to go in the loop
                elif len(FOR_STACK[0]['FOR_ITERATOR']) > 0:
                    lines[x].tokens[1].value = FOR_STACK[0]['FOR_ITERATOR'].pop(0)
                    token.VARIABLE_MAP[lines[x].tokens[1].var_name].value = lines[x].tokens[1].value

                # the loop is done
                else:
                    token.VARIABLE_MAP[FOR_STACK[0]["FOR_VAR"]].value = 'null'
                    x = FOR_STACK[0]["FOR_END"]
                    FOR_STACK.pop(0)

            elif lines[x].tokens[0].type == "break":
                token.VARIABLE_MAP[FOR_STACK[0]["FOR_VAR"]].value = 'null'
                x = FOR_STACK[0]['FOR_END'] + 1
                FOR_STACK.pop(0)


        # handle while loop stuff
        if LOOPING == 0:
            x = WHILE_COND_LINE
        elif LOOPING > 0:
            LOOPING -= 1
            x += 1
        # we're in a for loop
        elif len(FOR_STACK) > 0:
            # we're on the last line of the loop
            if x >= FOR_STACK[0]["FOR_END"]:
                x = FOR_STACK[0]["FOR_START"]
            # we're in the middle of the loop
            else:
                x += 1

        else:
            x += 1

main()
