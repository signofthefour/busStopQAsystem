from Models.grammar import GrammarParsing
from Models import sentence
import os

from Models.utils import getSentenceInformation
from Models.parser import Parser

# hyperparams
question_dir = "./Input/question/"
input_dir = "./Input"
output_dir = "./Output"

if __name__=="__main__":
    maltParser = Parser()
    for filename in os.listdir(question_dir):
        with open(os.path.join(question_dir, filename), encoding='utf-8') as f:
            sentence = getSentenceInformation(f.readline())
            tree = maltParser.parse(sentence=sentence)
            # print("The final tree for question {} is: \n{}\n".format(filename[:-4], tree))
            # import pdb; pdb.set_trace();
            # import pdb; pdb.set_trace()
            print("sentence: {}".format(sentence))
            GrammarParsing(tree).parsing()
            print('=======================================')
