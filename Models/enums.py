import enum


class FeatureType(enum.Enum):
    """ Feature type of token """
    POS = 0             # part of speech
    LEMMA = 1
    DEPENDENCY = 2


class ParserAction(enum.Enum):
    " action of parser (shift, reduce, left-arc, right-arc)"

    SHIFT = 0
    LEFT = 1
    RIGHT = 2
    REDUCE = 3
    LEFT_NSUBJ = 4
    RIGHT_NSUBJ = 5
    LEFT_DOBJ = 6
    RIGHT_DOBJ = 7
    LEFT_DET = 8
    RIGHT_DET = 9
    LEFT_COMPOUND = 10
    RIGHT_COMPOUND = 11
    LEFT_NMOD = 12
    RIGHT_NMOD = 13
    LEFT_TMOD = 14
    RIGHT_TMOD = 15
    LEFT_NUMMOD = 16
    RIGHT_NUMMOD = 17
    LEFT_CASE = 18
    RIGHT_CASE = 19
    LEFT_ROOT = 20
    RIGHT_ROOT = 21


    @classmethod
    def get_parser_action(cls, action, relation):
        if action == "left":
            if relation is RelationType.NSUBJ:
                return ParserAction.LEFT_NSUBJ
            elif relation is RelationType.DOBJ:
                return ParserAction.LEFT_DOBJ
            elif relation is RelationType.NMOD:
                return ParserAction.LEFT_NMOD
            elif relation is RelationType.TMOD:
                return ParserAction.LEFT_TMOD
            elif relation is RelationType.NUMMOD:
                return ParserAction.LEFT_NUMMOD
            elif relation is RelationType.COMPOUND:
                return ParserAction.LEFT_COMPOUND
            elif relation is RelationType.CASE:
                return ParserAction.LEFT_CASE
            elif relation is RelationType.DET:
                return ParserAction.LEFT_DET
            elif relation is RelationType.ROOT:
                return ParserAction.LEFT_ROOT
            return ParserAction.LEFT
        elif action == "right":
            if relation is RelationType.NSUBJ:
                return ParserAction.RIGHT_NSUBJ
            elif relation is RelationType.DOBJ:
                return ParserAction.RIGHT_DOBJ
            elif relation is RelationType.NMOD:
                return ParserAction.RIGHT_NMOD
            elif relation is RelationType.TMOD:
                return ParserAction.RIGHT_TMOD
            elif relation is RelationType.NUMMOD:
                return ParserAction.RIGHT_NUMMOD
            elif relation is RelationType.COMPOUND:
                return ParserAction.RIGHT_COMPOUND
            elif relation is RelationType.CASE:
                return ParserAction.RIGHT_CASE
            elif relation is RelationType.DET:
                return ParserAction.RIGHT_DET
            elif relation is RelationType.ROOT:
                return ParserAction.RIGHT_ROOT
            return ParserAction.RIGHT
        return ParserAction.SHIFT


class RelationType(enum.Enum):
    """ Represent the dependency relation """
    NONAME = 0
    NSUBJ = 1
    DOBJ = 2
    NMOD = 3
    TMOD = 4
    NUMMOD = 5
    COMPOUND = 6
    CASE = 7
    DET = 8
    ROOT = 9

    @classmethod
    def get_relation_type(cls, relation):
        if isinstance(relation, RelationType):
            return relation
        if relation == "root":
            return RelationType.ROOT
        if relation == "nsubj":
            return RelationType.NSUBJ
        if relation == "dobj":
            return RelationType.DOBJ
        if relation == "nmod":
            return RelationType.NMOD
        if relation == "tmod":
            return RelationType.TMOD
        if relation == "nummod":
            return RelationType.NUMMOD
        if relation == "compound":
            return RelationType.COMPOUND
        if relation == 'case':
            return RelationType.CASE
        if relation == 'det':
            return RelationType.DET
        return RelationType.NONAME


class FeatureTemplateName(enum.Enum):
    POS_S0 = 0 
    POS_S1 = 1 
    POS_Q0 = 2 
    POS_Q1 = 3      