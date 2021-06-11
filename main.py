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

    a_answer = [
        """I used malt-parser, which is suggested by Mrs. Tuoi, as described in README.md.\nAnd everything is from scratch so I use my own syntax analyzer in parser.py"""]
    b_answer = []
    c_answer = []
    d_answer = []
    e_answer = []
    f_answer = []

    for filename in os.listdir(question_dir):

        """
        Create output dir
        """
        # if not os.path.exists(os.path.join(output_dir, filename[:-4])):
        #     os.makedirs(os.path.join(output_dir, filename[:-4]))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(os.path.join(question_dir, filename), encoding='utf-8') as f:
            sentence = getSentenceInformation(f.readline())
            # Get dependency tree
            tree = maltParser.parse(sentence=sentence)
            # saveOuput(os.path.join(output_dir, filename[:-4], 'output_b.ans'), str(tree))
            b_answer.append(str(tree) + '\n')
            
            # Get grammar relation
            grammarStructure = GrammarParsing(tree).parsing()
            # saveOuput(os.path.join(output_dir, filename[:-4], 'output_c.ans'), grammarStructure.getString())
            c_answer.append(grammarStructure.getString() + '\n')
            sem = grammarStructure.SEM
            if type(sem[0]) in [WHICH]:
                # Get logical form
                logicalForm = "WHICH-QUERY({})".format(' & '.join([s.getLogical() for s in sem]))
                # saveOuput(os.path.join(output_dir, filename[:-4], 'output_d.ans'), logicalForm)
                d_answer.append(logicalForm + '\n')
                
                # Get semantic procedure
                q = Query('WHICH-QUERY',sem[0],  [s for s in sem if type(s) == ROUTE][0])
                # saveOuput(os.path.join(output_dir, filename[:-4], 'output_e.ans'), str(q))
                e_answer.append(str(q) + '\n')

                # Get answer
                answer = "Kết quả tra cứu tuyến xe yêu cầu:"
                results = q.execute(DATABASE)
                if len(results) == 0:
                    answer += '\nKhông có tuyến xe phù hợp nào.'
                for atime, dtime in results:
                    answer += '\n\t- Tuyến xe {} đi từ {} vào lúc {} giờ đến {} vào lúc {} giờ.'.format(dtime.bus,
                        CITY_ABR[dtime.city], dtime.time, CITY_ABR[atime.city], atime.time)
                # saveOuput(os.path.join(output_dir, filename[:-4], 'output_f.ans'), answer)
                f_answer.append(answer + '\n')
            
            if type(sem[0]) in [HOWLONG]:
                # Get logical form
                logicalForm = "RTIME-QUERY({})".format(' & '.join([s.getLogical() for s in sem]))
                # saveOuput(os.path.join(output_dir, filename[:-4], 'output_d.ans'), logicalForm)
                d_answer.append(logicalForm + '\n')

                # Get semantic procedure
                q = Query('RTIME-QUERY', sem[0],  [s for s in sem if type(s) == ROUTE][0])
                # saveOuput(os.path.join(output_dir, filename[:-4], 'output_e.ans'), str(q))
                e_answer.append(str(q) + '\n')

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
                # saveOuput(os.path.join(output_dir, filename[:-4], 'output_f.ans'), answer)
                f_answer.append(answer + '\n')

            # q = Query('WHICH-QUERY', [s for s in sem if type(s) == WHICH][0],  [s for s in sem if type(s) == ROUTE][0])

    saveOuput(os.path.join(output_dir,  'output_a.txt'), '\n'.join(a_answer))
    saveOuput(os.path.join(output_dir,  'output_b.txt'), '\n'.join(b_answer))
    saveOuput(os.path.join(output_dir,  'output_c.txt'), '\n'.join(c_answer))
    saveOuput(os.path.join(output_dir,  'output_d.txt'), '\n'.join(d_answer))
    saveOuput(os.path.join(output_dir,  'output_e.txt'), '\n'.join(e_answer))
    saveOuput(os.path.join(output_dir,  'output_f.txt'), '\n'.join(f_answer))

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