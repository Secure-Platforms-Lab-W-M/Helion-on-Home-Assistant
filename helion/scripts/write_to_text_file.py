import sys

if __name__ == "__main__":
    if (len(sys.argv) == 1):
        f = open("../data/generated_data/validation/scenarios_from_evaluators/ha-scenarios.txt", "w")
        f.close()
    else:
        f = open("../data/generated_data/validation/scenarios_from_evaluators/ha-scenarios.txt", "a+")
        f.write("".join([sys.argv[1], " "])) #need to do this instead so that each token added is separated by space
        f.close()
