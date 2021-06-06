from pickle import SHORT_BINBYTES
import Models.enums as enums
from Models.sentence import *
from Models.enums import FeatureName, ParserAction, RelationType
from Models.utils import token_node, tree

import collections #for Counter

class ParsingError(Exception):
    """ Exception """

    def __init__(self, message, partial_prediction):
        self.message = message
        self.tree = partial_prediction


class Parser(object):
    def __init__(self):
        # self.__oracle = Oracle()
        self.__stack = list()
        self.__buffer = list()
        self.__tree = None
        self.__history = list()

    def init(self, sentence):
        self.__stack = [Token(0)] # this init token is not belong to sentence, just a heuristic for easy coding
        self.__buffer = [token for token in sentence]
        self.__tree = tree(sentence, set_dependencies=False)
        self.__history = list()

        return self
        
    def get_tree(self):
        return self.__tree

    def get_stack(self):
        return list(self.__stack)

    def get_buffer(self):
        return list(self.__buffer)

    def history(self):
        return self.__history


    def parse(self, sentence):
        self.init(sentence)

        while not self.__is_final_state():
            current_state = ParserState(self)
            action = self.__predict_action(current_state)
            self.__exec(action)

        return self.__tree

    def __exec(self, action):
        # print(action)
        if action is ParserAction.SHIFT:
            self.shift()
        elif action is ParserAction.REDUCE:
            self.reduce()
        
        elif action is ParserAction.LEFT:
            self.left(RelationType.NONAME)
        elif action is ParserAction.LEFT_DOBJ:
            self.left(RelationType.DOBJ)
        elif action is ParserAction.LEFT_NSUBJ:
            self.left(RelationType.NSUBJ)
        elif action is ParserAction.LEFT_DET:
            self.left(RelationType.DET)
        elif action is ParserAction.LEFT_COMPOUND:
            self.left(RelationType.COMPOUND)
        elif action is ParserAction.LEFT_NMOD:
            self.left(RelationType.NMOD)
        elif action is ParserAction.LEFT_ROOT:
            self.left(RelationType.ROOT)
        # elif action is ParserAction
        elif action is ParserAction.RIGHT_ROOT:
            self.right(RelationType.ROOT)
        elif action is ParserAction.RIGHT_NMOD:
            self.right(RelationType.NMOD)
        elif action is ParserAction.RIGHT_COMPOUND:
            self.right(RelationType.COMPOUND)
        elif action is ParserAction.RIGHT_DET:
            self.right(RelationType.DET)
        elif action is ParserAction.RIGHT:
            self.right(RelationType.NONAME)
        elif action is ParserAction.RIGHT_DOBJ:
            self.right(RelationType.DOBJ)
        elif action is ParserAction.RIGHT_NSUBJ:
            self.right(RelationType.NSUBJ)
        elif action is ParserAction.RIGHT_PUNCT:
            self.right(RelationType.PUNCT)
        elif action is ParserAction.RIGHT_NUMMOD:
            self.right(RelationType.NUMMOD)
        elif action is ParserAction.RIGHT_CASE:
            self.right(RelationType.CASE)

    def shift(self):
        self.__stack.append(self.__buffer[0])
        self.__buffer = self.__buffer[1:]
        self.__history.append(ParserAction.SHIFT)
        # print("shift\n\n")
    
    def reduce(self):
        self.__stack.pop()
        self.__history.append(ParserAction.REDUCE)
        # print("reduce\n\n")

    def left(self, opt):
        dependent = self.__stack.pop()
        head = self.__buffer[0]
        self.__tree.add_dependency(head.tid, dependent.tid, opt)
        self.__history.append(ParserAction.get_parser_action("left", opt))

    def right(self, opt):
        dependent, self.__buffer = self.__buffer[0], self.__buffer[1:]
        head = self.__stack[-1]
        self.__stack.insert(len(self.__stack), dependent)
        self.__tree.add_dependency(head.tid, dependent.tid, opt)
        self.__history.append(ParserAction.get_parser_action("right", opt))

    def get_dependencies_by_head(self, head):
        return self.__tree.get_dependencies_by_head(head)

    def next_stack(self):
        return self.__stack[-1] if self.stack_size() > 0 else False

    def next_buffer(self):
        return self.__buffer[0] if self.buffer_size() > 0 else False

    def stack_size(self):
        return len(self.__stack)

    def buffer_size(self):
        return len(self.__buffer)

    def __is_final_state(self):
        return len(self.__buffer) == 0
            #  and len(self.__stack) == 1

    def __predict_action(self, currentState):
        rightmost_stack_pos = currentState[FeatureName.POS_S0]
        leftmost_buffer_pos = currentState[FeatureName.POS_B0]
        if rightmost_stack_pos == None:

            if leftmost_buffer_pos == 'V':
                """
                Find a root for sentence
                """
                return ParserAction.RIGHT_ROOT
            if leftmost_buffer_pos == 'E':
                """
                We here define E will have same meaning as V in case
                e.g.: "đến" with "đi đến"
                """
                return ParserAction.RIGHT_ROOT
            
            return ParserAction.SHIFT

        
        if rightmost_stack_pos == 'N':
            if leftmost_buffer_pos == 'P':
                """ 
                pronoun appears after noun often is DET
                e.g: Chiec xe [nay], chiec xe [nao]
                """
                return ParserAction.RIGHT_DET
            if leftmost_buffer_pos == 'Np':
                """
                Proper noun often appear after is Compound
                e.g.: [Thành phố] [Huế]
                """
                return ParserAction.RIGHT_COMPOUND
            if leftmost_buffer_pos == 'N':
                """
                N after N:
                e.g: [Thời gian] [xe buýt]
                """
                if self.history()[-1] == ParserAction.REDUCE:
                    """
                    In case that last action is REDUCE, the N now rarely depent on the head N
                    e.g: [thanh pho]---(reduced [Hue]---[luc]
                    """
                    return ParserAction.REDUCE
                return ParserAction.SHIFT
            if leftmost_buffer_pos == 'E':
                if ParserAction.LEFT_NSUBJ in self.history():
                    """
                    e.g.: [Thời gian | N] [xe buýt | N ] [từ | E]
                    In this example, we got 'Thời gian' as a NMOD of 'từ'
                    """
                    return ParserAction.LEFT_NMOD
                """
                In Vietnamese, we can often see that V E maybe abbre -> E
                e.g.: đi đến -> đến (same meaning as 'go to')
                We here define that will be as a V
                """
                return ParserAction.LEFT_NSUBJ
            if leftmost_buffer_pos == 'M':
                """
                In our story, numerical appear to indicate the time
                e.g: [luc] [20]
                """
                return ParserAction.RIGHT_NUMMOD
            if leftmost_buffer_pos == 'Ny':
                """
                In our story, abbreviation appear in case name of bus
                e.g: [xe buyt] [B3]
                """
                return ParserAction.RIGHT_NMOD
            elif leftmost_buffer_pos == 'F':
                """
                punctuation not depend on P only denpendent of ROOT
                """
                return ParserAction.REDUCE

            return ParserAction.SHIFT

        if rightmost_stack_pos == 'E':

            if leftmost_buffer_pos == 'N':
                """
                e.g.: 'đến thành phố'
                """
                if len([action for action in self.history() if action == ParserAction.RIGHT_DOBJ]):
                    return ParserAction.RIGHT_NMOD
                return ParserAction.RIGHT_DOBJ
            if leftmost_buffer_pos == 'Np':
                """
                e.g.: [từ] [Huế]
                """
                return ParserAction.RIGHT_DOBJ
            elif leftmost_buffer_pos == 'F':
                """
                punctuation not depend on P only denpendent of ROOT
                """
                if len(self.__stack) > 2:
                    return ParserAction.REDUCE
                return ParserAction.RIGHT_PUNCT
            elif leftmost_buffer_pos == 'E':
                """
                e.g: 'từ ... đến' -> heuristic
                """
                return ParserAction.RIGHT_CASE

            return ParserAction.SHIFT

        if rightmost_stack_pos == 'P':
            if leftmost_buffer_pos == 'E':
                """
                In our story, the pronoun only be used as a det so it should be reduce to create new arc
                e.g.: Xe bus <-- [nao] [den]
                """
                return ParserAction.REDUCE
            elif leftmost_buffer_pos == 'F':
                """
                punctuation not depend on P only denpendent of ROOT
                """
                return ParserAction.REDUCE

            return ParserAction.SHIFT
        
        if rightmost_stack_pos == 'Np':
            
            if leftmost_buffer_pos == 'N':
                """
                After Np is a N often do not create a arc
                e.g: thanh pho [Hue] [luc]
                """
                return ParserAction.REDUCE
            
            if leftmost_buffer_pos == 'E':
                """
                e.g.: [từ] DN (this should be reduced) [đến] Huế
                """
                return ParserAction.REDUCE

            if leftmost_buffer_pos == 'F':
                """
                punctuation not depend on P only denpendent of ROOT
                """
                return ParserAction.REDUCE

            return ParserAction.SHIFT
        
        if rightmost_stack_pos == 'M':
            if leftmost_buffer_pos == 'Nu':
                """
                Unit noun is appear after number in order to modify the mean of M
                But in our story, after normalize we can do not care about it, but for 
                readability, I we keep it on my tree
                """
                return ParserAction.RIGHT_NMOD
            if leftmost_buffer_pos == 'F':
                """
                punctuation not depend on P only denpendent of ROOT
                """
                return ParserAction.REDUCE

            return ParserAction.SHIFT
        
        if rightmost_stack_pos == 'Nu':
            if leftmost_buffer_pos == 'F':
                """
                punctuation not depend on P only denpendent of ROOT
                """
                return ParserAction.REDUCE
            
            return ParserAction.SHIFT
        
        if rightmost_stack_pos == 'Ny':
            if leftmost_buffer_pos == 'E':
                """
                abbreviation here is Name of bus
                the name often appear AFTER noun, so, it should be reduced
                e.g.: [xe buýt] [B3] [từ]
                """
                return ParserAction.REDUCE
            
            return ParserAction.SHIFT

        return ParserAction.SHIFT

class ParserState(object):

    def __init__(self, parser):

        stack, buffer = parser.get_stack(), parser.get_buffer()
        tree = parser.get_tree()

        def get(iterable, index, threshold=None):
            if threshold is None:
                threshold = index if index >= 0 else abs(index+1)

            return iterable[index] if len(iterable) > threshold else None

        self.s0 = get(stack, -1) # rightmost member in stack
        self.s1 = get(stack, -2) # 'vice' rightmost member in stack
        self.b0 = get(buffer, 0) # leftmost member in buffer
        self.b1 = get(buffer, 1) # 'vice' leftmost member in buffer

        # At this step, I only one to use 2 member which may influence to our decision
        # on choosing the dependence relation or the next action we need to do

    def __getitem__(self, key): #key: enums.FeatureName

        try:
            if key is enums.FeatureName.POS_S0:
                return self.s0.pos
            if key is enums.FeatureName.POS_S1:
                return self.s1.pos
            if key is enums.FeatureName.POS_B0:
                return self.b0.pos
            if key is enums.FeatureName.POS_B1:
                return self.b1.pos

        except (TypeError, AttributeError):
            return None

