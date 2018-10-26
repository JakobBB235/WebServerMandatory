var_dict = {} #stores variables as key - value pair


# Executes var logic.
def command_print_var(line_split):
    count_quotation = 0  # Reuse block in command_var method? Does not work yet. 0 default is same as is statement
    for i in line_split:
        count_quotation += i.count('"')  # count = 2 is regular print. count = 0 means variables from var_dict
    if count_quotation == 2:
        return None


    try:#to eval. Works if string consists of numbers
        eval_this = ""
        for i in line_split:
            try:
                eval_this += var_dict[i]
            except KeyError:
                eval_this += i
                # print("Key is not found in dict")
        result = eval(eval_this) #Eval is a security risk. Runs string as code. Find alternative?
        return str(result)
    except TypeError: # Runs if a typeerror is thrown. Therefore the string contains text
        result = ""
        for i in line_split:
            try:
                result += var_dict[i].strip('"') + " "
            except KeyError:
                pass
                # print("Key is not found in dict")
        return result

    # Alternative to eval method. cannot parse decimal numbers
    # try:  # Works if string consists of numbers
    #     eval_this = ""
    #     for i in line_split:
    #         try:
    #             eval_this += var_dict[i] + " "
    #         except KeyError:
    #             eval_this += i + " "
    #     eval_split = eval_this.split(" ")
    #     result = 0
    #     if eval_split[1] == "+":  # With or without ""?
    #         result += int(eval_split[0])
    #         result += int(eval_split[2])
    #     elif eval_split[1] == "*":
    #         result += int(eval_split[0])
    #         result *= int(eval_split[2])
    #     elif eval_split[1] == "-":
    #         result += int(eval_split[0])
    #         result -= int(eval_split[2])
    #     # elif eval_split == "/":
    #     #     result += int(eval_split[0])
    #     #     result /= int(eval_split[2])
    #     return str(result)
    # except TypeError and ValueError:  # Runs if a typeerror is thrown. Therefore the string contains text
    #     result = ""
    #     for i in line_split:
    #         try:
    #             result += var_dict[i].strip('"') + " "
    #         except KeyError:
    #             pass
    #             # print("Key is not found in dict")
    #     return result


#returns the new, parsed line to be replaced with the old line.
def command_print(line):
    line_split = line.split(' ')
    line_split.remove("print")
    var_result = command_print_var(line_split) #command_print_var() Executes var logic. if not var: returns None
    if var_result != None:
        return var_result

    result = ' '.join(line_split)
    result = result.strip('"')
    return result


#Saves a variable in var_dict. var name is key, and the assigned value is value.
def command_var(line):
    line_split = line.split(' ')
    line_split.remove("var")
    var_dict[line_split[0]] = line_split[2]  #index 0 is key, index 2 is value.
    # var_dict.update()


start_tag = '(start-python-lang)'
end_tag = '(end-python-lang)'
commands_dict = {"print": command_print, "var": command_var} #dict containing valid commands. method ref as values


#Method called to start parsing html
def parse_html_custom(html):
    html_split = html.split('\n')
    logic_found = False
    # print("LENGTH", len(html_split))
    count = 0
    while True:
        line_strip = html_split[count].strip(' ') # removes spaces before lines
        #Alternatively use slicing.
        remember_spaces = len(html_split[count]) - len(line_strip) - 4 #-4 because start, and end tag is removed.

        if line_strip == start_tag: #start_tag = logic to process
            logic_found = True
            del html_split[count] # Deletes current line(the start tag)
            # count = count + 1 #NEW
            continue
        if line_strip == end_tag: #end_tag = no more logic to process
            del html_split[count] # Deletes current line(the end tag)
            html_final = '\r\n'.join(html_split)
            return html_final
        if logic_found:
            line_split = line_strip.split(' ') # to be able to get command
            command = line_split[0] #0 is command
            # print("command used:", command)
            # method is called through reference in dictionary current line is passed to the method
            result = commands_dict[command](line_strip)

            if result != None:
                result_indented = (' ' * remember_spaces) + result #Adds the correct indent
                html_split[count] = result_indented  # replaces current line with the new parsed line. = result
            else:
                # print("This is deleted:", html_split[count])
                del html_split[count] #Deletes lines not to be displayed in view like variable declaration: var a = 5
                count = count - 1 #Because line was deleted
                # print("LENGTH", len(html_split))
        count += 1 #count = count + 1

        if count == len(html_split)-1:
            return html
