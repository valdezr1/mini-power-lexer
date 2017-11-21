# Rafael Valdez
# Concepts of Programming Languages

# Mini-power
# <stmts>ïƒ <stmt> {;<stmt>}
# <stmt>ïƒ (<print-stmt> | <assgmt-stmt>)
# <print-stmt>ïƒ PRINT(<id> | <const>)
# <assgmt-stmt>ïƒ <id> =(<expr> | <string>)
# <id>ïƒ <letter>{(<letter> | <digit>)}($|#|%)
# <expr>ïƒ <expr> (+| -) <term> | <term>
# <term>ïƒ <term> (*| /) <factor> | <factor>
# <factor>ïƒ <expr> ^<factor> | (<expr> )| <num-const> | <id>
# <const>ïƒ <num-const> | <string>
# <num-const>ïƒ <int-const> | <real-const>
# <int-const>ïƒ [(+|-)] <digit>{<digit>}
# <real-const>ïƒ [(+|-)] <digit>{<digit>}.{<digit>}
# <string>ïƒ Êº{(<letter> | <digit>)}Êº
# <digit>ïƒ (0| 1| 2| 3| 4| 5| 6| 7| 8| 9)
# <letter>ïƒ (a| b| c| d| e| f| g| h| i| j| k| l| m|n| o| p| q| r| s| t| u| v| w| x| y| z)

import sys

# Token Dictionary
tokens = {
    "=": "ASSIGN",
    ";": "SEMICOLON",
    "+": "PLUS",
    "-": "MINUS",
    "*": "TIMES",
    "/": "DIV",
    "^": "POWER",
    "(": "L-PAR",
    ")": "R-PAR",
    "ID": "IDENT",
    "DIG": "DIGIT",
    "%": "REAL",
    "#": "INTEGER",
    "$": "STRING",
    "PRINT": "PRINT",
    "FLOAT": "REAL_CONST",
    "INT":  "INT_CONST",
    "\"": "QUOTE"
}


# Des: Function to grab next character in input
# Par: index, read result from input file, main file to close
# Ret: return char of str, except if EOF then will return -1
def get_char(read_res, main_file):
    try:
        global cur_index
        cur_index = cur_index + 1
        if read_res[cur_index] == "\"":
            string_dec = read_res[cur_index]
            first = True
            cur_index = cur_index + 1
            while read_res[cur_index] != "\"" or first:
                if 'A' <= read_res[cur_index] <= 'Z' or read_res[cur_index] in ('!', '@', '#', '$', '%', '^', '&', '*',
                                                                                '(', ')', '_', '-', '=', '+', ',', '.',
                                                                                '?', '<', '>', '?', '/', '[', ']', '{',
                                                                                '}', '|', '\\', '`', '~', "\'"):
                    print("ERROR: Invalid String")
                    quit()
                string_dec = string_dec + read_res[cur_index]
                cur_index = cur_index + 1
                first = False
            string_dec = string_dec + read_res[cur_index]
            return string_dec
        if read_res[cur_index] == 'P':
            i = 0
            print_copy = "PRINT"
            while i < len(print_copy):
                if read_res[cur_index] != print_copy[i]:
                    return "Unexpected Token Result"
                i = i + 1
                cur_index = cur_index + 1
            return print_copy
        if read_res[cur_index] != ' ' and read_res[cur_index] != "\n":
            return read_res[cur_index]
    except IndexError:
        main_file.close()
        return "EOF. Closing File"


# Function that grabs the identifier
# Parameter: start character, read list
# Returns: name of identifier
def check_id(char, read_list):
    global cur_index
    identity = char
    cur_index = cur_index + 1
    while '0' <= read_list[cur_index] <= '9' or 'a' <= read_list[cur_index] <= 'z':
        identity = identity + read_list[cur_index]
        cur_index = cur_index + 1
    return identity


# Function that grabs the digit
# Parameter: start character, read list
# Returns: full number
def check_dig(char, read_list):
    global cur_index
    decimal_pres = False
    number = char
    cur_index = cur_index + 1
    while '0' <= read_list[cur_index] <= '9' or read_list[cur_index] == '.':
        if read_list[cur_index] == '.' and not decimal_pres:
            decimal_pres = True
            number = number + read_list[cur_index]
        elif read_list[cur_index] == '.' and decimal_pres:
            print("\nERROR: REAL_CONST unrecognized")
            quit()
        else:
            number = number + read_list[cur_index]
        cur_index = cur_index + 1
    return number


# Function to grab tokens appropriate to each char/sets of chars based on token dictionary
# Parameters: Checking character, read_list
# Returns: Appropriate Token (and potentially token name)
def get_token(char, read_list):
    try:
        global tokens, cur_index, token_count
        if 'a' <= char <= 'z':      # If beginning with a letter
            return tokens["ID"] + ' ' + check_id(char, read_list) + ' '
        elif '0' <= char <= '9':    # If beginning with a number
            ret_value = check_dig(char, read_list)
            if ret_value.find('.') >= 0:
                token_count = token_count + 1
                return tokens["FLOAT"] + ' ' + ret_value + '\n'
            else:
                token_count = token_count + 1
                return tokens["INT"] + ' ' + ret_value + '\n'

        elif char[0] == '\"':
            cur_index = cur_index + 1
            token_count = token_count + 1
            return "STRING " + char + '\n'  # If beginning with \"
        else:
            cur_index = cur_index + 1
            return tokens[char]
    except KeyError:
        print("\nERROR: Unrecognized Token")
        quit()


# MAIN
# Opens and Reads file
try:
    input_name = sys.argv[1]
    input_file = open(input_name, "r")

    read_file = input_file.read()

    # Initialize Current Index to Track Main File
    cur_index = -1  # Starts at -1 due to immediate incrementation in get_char

    value = ''
    char_list = []
    while value != "EOF. Closing File":
        value = get_char(read_file, input_file)
        if not (value is None or value == "EOF. Closing File"):
            char_list.append(value)

    # Re-initialize Current Index after list is attained w/o whitespace
    cur_index = cur_index - cur_index  # cur_index = 0 gave warnings so just subtracted it by self
    test_file = open("input.out", "w+")
    print("Processing input file " + input_name)
    token_count = 0
    while True:

        try:
            ret_val = get_token(char_list[cur_index], char_list)
            # Appends newline when necessary
            if ret_val in ("REAL", "INTEGER", "STRING", "ASSIGN", "PLUS", "TIMES", "MINUS",
                           "DIV", "POWER", "PRINT", "SEMICOLON", "R-PAR", "L-PAR"):
                test_file.write(ret_val + '\n')
                token_count = token_count + 1
            else:
                test_file.write(ret_val)

            # When index is too high, break the while loop and quit program
        except IndexError:
            break

    print(str(token_count) + " tokens produced")
    print("Result in file input.out")

except FileNotFoundError:
    print("File Does Not Exist")
    quit()
except IndexError:
    print("File Not Found")
    quit()











