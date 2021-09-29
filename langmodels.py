import sys

"""
The main entry point of this program.
"""
def main():
    training_file_path = sys.argv[1]
    cli_flag = sys.argv[2] # Expects "-test"
    test_file_path = sys.argv[3]

    training_file_tokens = []
    with open(training_file_path) as training_file:
        for line in training_file:
            training_file_tokens.append(line.split())

    print(training_file_tokens)









if __name__ == "__main__":
    main()

