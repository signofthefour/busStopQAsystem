from Models.query import Query
from Models.grammar import GrammarParsing, HOWLONG, ROUTE, WHICH
from Models import sentence
import os

from Models.utils import getSentenceInformation
from Models.parser import Parser

# hyperparams
question_dir = "./Input/question/"
input_dir = "./Input"
output_dir = "./Output"

def saveOuput(dir, data):
    with open(dir, 'w') as f:
        f.write(data)

if __name__=="__main__":
    maltParser = Parser()
    for filename in os.listdir(question_dir):

        """
        Create output dir
        """
        if not os.path.exists(os.path.join(output_dir, filename[:-4])):
            os.makedirs(os.path.join(output_dir, filename[:-4]))
        
        with open(os.path.join(question_dir, filename), encoding='utf-8') as f:
            sentence = getSentenceInformation(f.readline())
            # Get dependency tree
            tree = maltParser.parse(sentence=sentence)
            saveOuput(os.path.join(output_dir, filename[:-4], 'output_b.ans'), str(tree))
            grammarStructure = GrammarParsing(tree).parsing()
            # print(grammarStructure.getString())
            saveOuput(os.path.join(output_dir, filename[:-4], 'output_c.ans'), grammarStructure.getString())
            # Get logical form
            sem = grammarStructure.SEM
            if type(sem[0]) in [WHICH]:
                logicalForm = "WHICH-QUERY({})".format(' & '.join([s.getLogical() for s in sem]))
                q = Query('WHICH-QUERY',sem[0],  [s for s in sem if type(s) == ROUTE][0])
            if type(sem[0]) in [HOWLONG]:
                logicalForm = "RTIME-QUERY({})".format(' & '.join([s.getLogical() for s in sem]))
                q = Query('RTIME-QUERY', sem[0],  [s for s in sem if type(s) == ROUTE][0])

            saveOuput(os.path.join(output_dir, filename[:-4], 'output_d.ans'), logicalForm)
            saveOuput(os.path.join(output_dir, filename[:-4], 'output_e.ans'), str(q))
            # q = Query('WHICH-QUERY', [s for s in sem if type(s) == WHICH][0],  [s for s in sem if type(s) == ROUTE][0])


