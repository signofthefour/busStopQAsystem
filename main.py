import os

from Models.lexer import extractSentence, Word

# hyperparams
question_dir = "./Input/question/"
input_dir = "./Input"
output_dir = "./Output"

if __name__=="__main__":
    for filename in os.listdir(question_dir):
        with open(os.path.join(question_dir, filename), encoding='utf-8') as f:
            word_feature = extractSentence(f.readline())
            print("==================================")
            [word.print() for word in word_feature]
            print("==================================\n\n")
