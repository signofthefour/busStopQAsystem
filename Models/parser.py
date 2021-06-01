import Models.enums as enums
from Models.sentence import *
from Models.enums import FeatureName, ParserAction, RelationType
from Models.utils import tree

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
        self.__stack = [Token(0)]
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
            avail_actions = self.__get_avail_actions()

            if len(avail_actions) == 0:
                raise ParsingError("Unable to parse the sentence", self.__tree)

            current_state = ParserState(self)
            # action = self.oracle.predict(configuration)
            action = self.__predict_action(current_state)

            if action in avail_actions: self.__exec(action)
            else:                       self.shift()

        return self.__tree

    def __exec(self, action):
        if action is ParserAction.SHIFT:
            self.shift()
        elif action is ParserAction.LEFT:
            self.left(RelationType.NONAME)
        elif action is ParserAction.LEFT_DOBJ:
            self.left(RelationType.DOBJ)
        elif action is ParserAction.LEFT_NSUBJ:
            self.left(RelationType.NSUBJ)
        elif action is ParserAction.RIGHT:
            self.right(RelationType.NONAME)
        elif action is ParserAction.RIGHT_DOBJ:
            self.right(RelationType.DOBJ)
        elif action is ParserAction.RIGHT_NSUBJ:
            self.right(RelationType.NSUBJ)

    def __get_avail_actions(self):
        moves = set()
        if self.buffer_size() > 0:
            moves.add(ParserAction.SHIFT)
            if self.stack_size() > 0:
                moves.update({action for action in ParserAction})

        return moves

    def shift(self):
        self.__stack.append(self.__buffer[0])
        self.__buffer = self.__buffer[1:]
        self.__history.append(ParserAction.SHIFT)
        print("shift")

    def left(self, opt):
        dependent = self.__stack.pop()
        head = self.__buffer[0]
        self.__tree.add_dependency(head.tid, dependent.tid, opt)
        self.__history.append(ParserAction.get_parser_action("left", opt))

    def right(self, opt):
        dependent, self.__buffer = self.__buffer[0], self.__buffer[1:]
        head = self.__stack.pop()
        self.__buffer.insert(0, head)
        self.__tree.add_dependency(head.tid , dependent.tid, opt)
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
        return len(self.__buffer) == 0 and len(self.__stack) == 1

    def __predict_action(self, currentState):
        rightmost_stack_pos = currentState[FeatureName.POS_S0]
        leftmost_buffer_pos = currentState[FeatureName.POS_B0]
        # print('left most buffer: {} and right most stack: {}'.format(leftmost_buffer_pos, rightmost_stack_pos))
        if rightmost_stack_pos == 'N': # noun
            if leftmost_buffer_pos == 'P': # pronoun
                """ 
                pronoun appears after noun often is DET
                e.g: Chiec xe [nay], chiec xe [nao]
                """
                return ParserAction.LEFT_DET
            if leftmost_buffer_pos == 'Np': # Proper noun
                """
                Proper noun often appear after is Compound
                e.g.: [Thành phố] [Huế]
                """
                return ParserAction.LEFT_COMPOUND
            if leftmost_buffer_pos == 'N':
                """
                N after N:
                e.g: [Thời gian] [xe buýt]
                """
                return ParserAction.LEFT_NMOD # it may be tmod, TODO: need more process here
            if leftmost_buffer_pos == '':
        

        return None

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

    def __getitem__(self, key): #key: enums.FeatureTemplateName

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


    # def __str__(self):
    #     return "s0: {}\ns1: {}\nq0: {}\nq1: {}\nq2: {}\nq3: {}\ns0h: {}\ns0l: {}\ns0r: {}\nq0l: {}".format(self.s0, self.s1, self.q0, self.q1, self.q2, self.q3, self.s0h, self.s0l, self.s0r, self.q0l)
