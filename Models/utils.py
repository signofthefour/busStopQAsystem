from Models.sentence import Sentence, Token
import re
from pyvi import ViTokenizer, ViPosTagger

class tree(object):

    def __init__(self, sentence, set_dependencies=True):
        self.nodes = [token_node(id=index) for index in range(len(sentence) + 1)]
        self.dependencies = set()

        for index, token in enumerate(sentence, 1):
            self.nodes[index].init(token.wordform, token.pos)

            if set_dependencies:
                self.add_dependency(token.head, index, token.dtype)
                self.nodes[index].head = token.head
                self.nodes[index].dtype = token.dtype

    def __eq__(self, other):
        return set(self.dependencies) == set(other.dependencies)

    def add_dependency(self, head, dependent, relation):
        self.nodes[int(dependent)].head = int(head)
        self.nodes[int(dependent)].dtype = relation
        self.nodes[int(head)].add_dependency(self.nodes[dependent], relation)
        self.dependencies.add((head, dependent, relation))


    def get_leftmost_child(self, tid):
        siblings = filter(lambda tupla: tupla[0] == tid, self.dependencies)
        try:
            child = min(siblings, key=lambda tupla: tupla[1])
            child = self.nodes[child[1]], child[2]
        except ValueError:
            child = None
        return child

    def get_rightmost_child(self, tid):
        siblings = filter(lambda tupla: tupla[0] == tid, self.dependencies) 
        try:
            child = max(siblings, key=lambda tupla: tupla[1])
            child = self.nodes[child[1]], child[2]
        except ValueError:
            child = None
        return child

    def get_head(self, tid):
        try:
            head, _, dt = next(filter(lambda triple: triple[1] == tid, self.dependencies))
        except StopIteration:
            head, dt = None, None

        return self[head]


    def dependency_exists(self, head, dep, rel=None):
        try:
            res = next(filter(lambda triple: triple[0] == head and triple[1] == dep, self.dependencies))[-1]
            res = res if not rel or rel == res else False
        except StopIteration:
            res = False

        return res

    def get_dependencies_by_head(self, head):
        return self.nodes[head].siblings

    def __getitem__(self, key):
        return self.nodes[key] if key else None

    def __str__(self):
        return "\n".join([str(node) for node in self.nodes[1:]]) + "\n"


class token_node(Token):
    def __init__(self, id=id, wordform=None, pos=None,):
        Token.__init__(self, id, wordform, pos)
        self.siblings = list()

    def add_dependency(self, node, relation):
        self.siblings.append((node, relation))

    def has_siblings(self):
        return len(self.siblings) > 0

    def get_token(self):
        return Token(self.tid, self.wordform, self.lemma, self.pos, self.xpos, self.feats, self.head, self.dtype)

    def __repr__(self):
        return "({}, {}, {}) -> {}".format(self.tid, self.wordform, self.pos, [s.tid for s, rel in self.siblings])


def getSentenceInformation(rawSentence):
    sentence = Sentence()
    normSentence = nomalize(rawSentence)   
    tokenize =  ViTokenizer.tokenize(normSentence)
    posObject = ViPosTagger.postagging(tokenize)
    tokens = list(\
        map(lambda w, t, p: Token(id=p, wordform=w, pos=t), \
            posObject[0], posObject[1], list(range(0, len(posObject[0])))))
    [sentence.add_token(token) for token in tokens]
    return sentence

def nomalize(sentence):
    sentence = sentence.replace('bus', u'buýt')
    # change [HH:MM]HR format to 'HH giờ MM phút'
    match = re.search(r'([0-9][0-9]:[0-9][0-9][HR])\w+', sentence)
    oldTime = match.group(0) if match else None
    if oldTime:
        newTime = oldTime[0:2] + " giờ " + oldTime[3:5] + " phút"
        sentence = sentence.replace(oldTime, newTime)
    return sentence



if __name__=="__main__":
    sentence = u"Xe bus nào đến thành phố Huế lúc 20:00HR?"
    sentence = getSentenceInformation(sentence)
