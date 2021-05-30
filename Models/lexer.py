from pyvi import ViTokenizer, ViPosTagger


class Word(object):
    def __init__(self, word, tag, position):
        self.word = word
        self.tag = tag
        self.position = position
    
    def print(self):
        print("WORD: {} with POS TAG: {} in position: {}".format(self.word, self.tag, self.position))

""" Tokenized and POS the input in VietNamese Language
@param sentenece: Vietnamese sentence

@return: dictionary object in form: list(Word)
"""
def extractSentence(sentence):
    tokenize =  ViTokenizer.tokenize(sentence)
    posObject = ViPosTagger.postagging(tokenize)
    sentenceFeature = list(map(lambda w, t, p: Word(w, t, p), posObject[0], posObject[1], list(range(0, len(posObject[0])))))

    return sentenceFeature

from tqdm import tqdm
if __name__=="__main__":
    sentence = u"Xe bus nào đến thành phố Huế lúc 20 giờ?"
    words = extractSentence(sentence)
    for word in words:
        word.print()
