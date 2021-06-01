import Models.enums as enums
from Models.sentence import *
from Models.enums import ParserAction, RelationType
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
        self.__stack = [Token(0)] #root
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
            action = self.predictAction(current_state)

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

    @staticmethod
    def get_transitions(sentence, tree):
        parser = Parser().init(sentence)
        transitions = list()

        while not parser.__is_final_state():
            do_shift = True

            transitions.append(ParserState(parser))

            if parser.stack_size() > 0 and parser.buffer_size() > 0:
                q, s = parser.next_buffer().tid, parser.next_stack().tid
                rel = tree.dependency_exists(q, s)
                if rel:
                    parser.left(rel)
                    do_shift = False
                else:
                    rel = tree.dependency_exists(s, q)
                    if rel and len(tree.get_dependencies_by_head(q)) == len(parser.get_dependencies_by_head(q)):
                        parser.right(rel)
                        do_shift = False

            if do_shift and parser.buffer_size() > 0:
                parser.shift()

        return (transitions, parser.history())


class ParserState(object):

    def __init__(self, parser):

        stack, buffer = parser.get_stack(), parser.get_buffer()
        tree = parser.get_tree()

        def get(iterable, index, threshold=None):
            if threshold is None:
                threshold = index if index >= 0 else abs(index+1)

            return iterable[index] if len(iterable) > threshold else None

        self.s0 = get(stack, -1)
        self.s1 = get(stack, -2)
        self.q0 = get(buffer, 0)
        self.q1 = get(buffer, 1)

    def __getitem__(self, key): #key: enums.FeatureTemplateName

        try:
            if key is enums.FeatureTemplateName.POS_S0:
                return self.s0.pos
            if key is enums.FeatureTemplateName.POS_S1:
                return self.s1.pos
            if key is enums.FeatureTemplateName.POS_Q0:
                return self.q0.pos
            if key is enums.FeatureTemplateName.POS_Q1:
                return self.q1.pos

        except (TypeError, AttributeError):
            return None


    def __str__(self):
        return "s0: {}\ns1: {}\nq0: {}\nq1: {}\nq2: {}\nq3: {}\ns0h: {}\ns0l: {}\ns0r: {}\nq0l: {}".format(self.s0, self.s1, self.q0, self.q1, self.q2, self.q3, self.s0h, self.s0l, self.s0r, self.q0l)
