'''
Usage: python3 parse_token.py \<Device,attribute,action\>
Outputs the token converted to an entity name and its state in text file called parsed_token.txt
If the token contains multiple devices, then each entity name will be separated by a space
Each token with its corresponding state is found on its own line, separated by a space
e.g. one line could be switch.air_cooler on
                       input_select.null_time night

'''

import sys

def process_single_token(token, f):
    token_list = token.replace("<", "").replace(">", "").split(",")

    attribute_list = list(token_list[1])
    for i in range(len(attribute_list)):
        if attribute_list[i].isupper():
            attribute_list[i] = "_" + attribute_list[i].lower()
    attribute = "".join(attribute_list)

    device = ""
    if (token_list[0] == "Shades/Blinds"):
        device = "shades_blinds"
    else:
        device = token_list[0].lower()
    entity = ""
    if (attribute == "switch"):
        entity = "switch." + device
    else:
        entity = "input_select." + device + "_" + attribute
    f.write(entity + " " + token_list[2] + "\n")

if __name__ == "__main__":
    token = sys.argv[1]
    f = open("parsed_token.txt", "w")
    entity = ""
    if ((token != "<s>") and (token != "</s>")):
        if "-" in token:
            entity = ""
            token_list = token.replace("<", "").replace(">", "").split(",")
            token_lists = []
            for i in range(len(token_list)):
                token_lists.append(token_list[i].split("-"))
            for i in range(len(token_lists[0])):
                ind_token = "<"
                for j in range(len(token_lists) - 1):
                    ind_token += token_lists[j][i] + ","
                ind_token += token_lists[len(token_lists) - 1][i] + ">"
                process_single_token(ind_token, f)
        else:
            process_single_token(token, f)