from Models.query import Query
from Models.grammar import GrammarParsing, HOWLONG, ROUTE, WHICH
from Models import sentence
import os

from Models.utils import getSentenceInformation
from Models.parser import Parser
from Models.database import DATABASE, Dtime

# hyperparams
question_dir = "./Input/question/"
output_dir = "./Output"

CITY_ABR = {'HN': 'Hà Nội', 'HCMC': 'thành phố Hồ Chí Minh', 'DANANG': 'Đà Nẵng', 'HUE': 'Huế'}

def saveOuput(dir, data):
    with open(dir, 'w') as f:
        f.write(data)

def main(args):
    question_dir = args.input_dir
    output_dir = args.output_dir
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

            # Get grammar relation
            grammarStructure = GrammarParsing(tree).parsing()
            saveOuput(os.path.join(output_dir, filename[:-4], 'output_c.ans'), grammarStructure.getString())
            sem = grammarStructure.SEM
            if type(sem[0]) in [WHICH]:
                # Get logical form
                logicalForm = "WHICH-QUERY({})".format(' & '.join([s.getLogical() for s in sem]))
                saveOuput(os.path.join(output_dir, filename[:-4], 'output_d.ans'), logicalForm)
                
                # Get semantic procedure
                q = Query('WHICH-QUERY',sem[0],  [s for s in sem if type(s) == ROUTE][0])
                saveOuput(os.path.join(output_dir, filename[:-4], 'output_e.ans'), str(q))

                # Get answer
                answer = "Kết quả tra cứu tuyến xe yêu cầu:"
                results = q.execute(DATABASE)
                if len(results) == 0:
                    answer += '\nKhông có tuyến xe phù hợp nào.'
                for atime, dtime in results:
                    answer += '\n\t- Tuyến xe {} đi từ {} vào lúc {} giờ đến {} vào lúc {} giờ.'.format(dtime.bus,
                        CITY_ABR[dtime.city], dtime.time, CITY_ABR[atime.city], atime.time)
                saveOuput(os.path.join(output_dir, filename[:-4], 'output_f.ans'), answer)
            
            if type(sem[0]) in [HOWLONG]:
                # Get logical form
                logicalForm = "RTIME-QUERY({})".format(' & '.join([s.getLogical() for s in sem]))
                saveOuput(os.path.join(output_dir, filename[:-4], 'output_d.ans'), logicalForm)

                # Get semantic procedure
                q = Query('RTIME-QUERY', sem[0],  [s for s in sem if type(s) == ROUTE][0])
                saveOuput(os.path.join(output_dir, filename[:-4], 'output_e.ans'), str(q))

                # Get answer
                results = q.execute(DATABASE)
                answer = "Kết quả tra cứu tuyến xe yêu cầu:"
                if len(results) == 0:
                    answer += '\nKhông có tuyến xe phù hợp nào.'
                for rtime in results:
                    answer += '\n\t- Thời gian chuyến xe {} đi từ {} đến {} là {} giờ.'.format(
                        rtime.bus,
                        rtime.src,
                        rtime.dest,
                        rtime.time
                    )
                saveOuput(os.path.join(output_dir, filename[:-4], 'output_f.ans'), answer)

            # q = Query('WHICH-QUERY', [s for s in sem if type(s) == WHICH][0],  [s for s in sem if type(s) == ROUTE][0])
            

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="NLP Assignment")
    
    parser.add_argument(
      '--input_dir',
      default= "./Input/question",
      help= "directory of questions"
      )

    parser.add_argument(
      '--output_dir',
      default= "./Output",
      help= "directory of output"
      )
    
    args = parser.parse_args()
    main(args)