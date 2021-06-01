#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Models.enums import RelationType

import re

class Sentence(object):
    """ Represent Sentence as a list of Token """

    def __init__(self):
        self.__tokens = list()

    def add_token(self, token):
        self.__tokens.append(token)

    def clear(self):
        self.__tokens.clear()

    def __str__(self):
        return " ".join('(' + token.wordform + '{'+token.pos+'})' for token in self.__tokens)

    def __iter__(self):
        for token in self.__tokens:
            yield token

    def __len__(self):
        return len(self.__tokens)



class Token(object):
    """ Represent a word after using lexer as a Token to define a main
        object that is used in parser
    """
    def __init__(self, id, wordform=None, pos=None, head=None, dep=None):
        self.__id = int(id) if id is not None else None
        self.__wordform = wordform
        self.__pos = pos
        self.__head = int(head) if head else None
        self.__dtype = RelationType.get_relation_type(dep) if dep else None

    def init(self, wordform=None, lemma=None, pos=None, xpos=None, feats=None, head=None, dep=None):
        self.wordform = wordform
        self.pos = pos
        self.head = int(head) if head else None
        self.dtype = dep

    @property
    def tid(self):
        return self.__id

    @property
    def wordform(self):
        return self.__wordform

    @property
    def pos(self):
        return self.__pos

    @property
    def head(self):
        return self.__head

    @property
    def dtype(self):
        return self.__dtype
    
    @wordform.setter
    def wordform(self, wf):
        self.__wordform = wf

    @pos.setter
    def pos(self, pos):
        self.__pos = pos

    @head.setter
    def head(self, head):
        self.__head = head

    @dtype.setter
    def dtype(self, dtype):
        self.__dtype = RelationType.get_relation_type(dtype) if dtype else None

    def __str__(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t_\t_".format(self.tid, self.wordform, self.lemma, self.pos, self.xpos, self.feats, self.head if self.head else 0, self.dtype.name.lower() if self.dtype else "noname")
