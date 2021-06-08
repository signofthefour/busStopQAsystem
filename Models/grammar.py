from Models.utils import tree
import pdb
from Models.enums import RelationType

CITYSEM={'hồ_chí_minh': 'HCMC', 'đà_nẵng': 'DANANG', 'huế': 'HUE'}

class WHICH:
    def __init__(self, x, QUERY_TYPE) -> None:
        self.x = x
    
    def __str__(self) -> str:
        return "{}WHICH({})".format(
            "" if self.x else "\\x.",
            "x" if self.x is None else '{}'.format(self.x))

class WHATTIME:
    def __init__(self, x) -> None:
        self.x = x
    
    def __str__(self) -> str:
        return "{}WHATTIME({})".format(
            "" if self.x else "\\x.",
            "x" if self.x is None else '{}'.format(self.x))

class DET:
    def __init__(self, object):
        self.x = object.SEM
    
    def __str__(self) -> str:
        return "DET({})".format(self.x if self.x is not None else '?x')

class NAME:
    def __init__(self, objectN, objectName):
        self.name = objectName.SEM
        self.x = objectName.VAR
    
    def __str__(self) -> str:
        return "NAME({}, {})".format(self.name, self.x)

class DEST:
    def __init__(self, cityName) -> None:
        self.bus = None
        self.name = cityName.SEM
    
    def __str__(self) -> str:
        return "{}DEST({}, {})".format("\\f." if self.bus is None else "", \
                                        "f" if self.bus is None else self.bus,\
                                        self.name)

class ROUTE:
    def __init__(self, source, dest, bus, time) -> None:
        self.source = source
        self.dest = dest
        self.bus = bus
        self.time = time

    def __str__(self) -> str:
        return "{}{}{}{}RUOTE({}, {}, {}, {})".format(
            "\\s " if   self.source  is None else "",
            "d " if     self.dest    is None else "",
            "b " if     self.bus    is None else "",
            "t." if     self.time       is None else "",
            "s" if      self.source  is None else "SOURCE(" + str(self.source.SEM) + ")",
            "d" if      self.dest    is None else "DEST(" + str(self.dest.SEM) + ")",
            "b" if      self.bus    is None else self.bus,
            "t" if      self.time       is None else self.time
        )

class BUS:
    def __init__(self, bus) -> None:
        self.bus = bus.VAR if bus else bus
    
    def __str__(self) -> str:
        return "BUS{}".format(
            "" if self.bus is None else '({})'.format(self.bus)
        )

class TIME:
    def __init__(self, time=None) -> None:
        self.time = time

    def __str__(self) -> str:
        return "{}TIME({})".format(
            "\\t." if self.time is None else "",
            "t" if self.time is None else self.time
            )

class GrammarStucture():
    def __init__(self, SEM, VAR, CHILDREN, GNAME=""):
        self.GNAME = GNAME
        self.SEM = SEM
        self.VAR = VAR
        self.CHILDREN = CHILDREN
    
    def __str__(self) -> str:
        return self.GNAME + '[SEM<{}>{}]'.format(self.SEM, \
            ',VAR<{}>'.format(self.VAR) if self.VAR else "?") + \
            ('\n--> ' if len(self.CHILDREN) else '')  + \
            ' + '.join([str(child) for child in self.CHILDREN])
    
    def getString(self, i=1):
        tab = '\t'*i
        children = ""
        for child in self.CHILDREN:
            children += '\n' + tab  + '(' + (child if isinstance(child, str) else child.getString(i+1))
        children += ')'
        return self.GNAME + '[SEM<{}>{}]'.format(self.SEM, \
            ',VAR<{}>'.format(self.VAR) if self.VAR else "") + children

class TimeMod(GrammarStucture):
    def __init__(self, SEM, VAR='t1'):
        super().__init__(SEM, VAR, [],  "TIME-MOD")

class BusTime(GrammarStucture):
    def __init__(self, CHILDREN):
        SEM = TIME(CHILDREN[1].SEM)
        VAR = 't1'
        super().__init__(SEM, VAR, CHILDREN, GNAME="BUS-TIME")

class CityN(GrammarStucture):
    # CITY-N[SEM<thanhpho>, VAR<c1>]
    def __init__(self, SEM, VAR) -> None:
        super().__init__(SEM, VAR, [], "CITY-N")

class CityName(GrammarStucture):
    # CITY-NAME[SEM<'DaNang'>, VAR<d1>]
    def __init__(self, SEM, VAR) -> None:
        super().__init__(SEM, VAR, [], "CITY-NAME")

class CityCNP(GrammarStucture):
    def __init__(sefl, CHILDREN):
        if len(CHILDREN) == 2:
            SEM = NAME(*CHILDREN)
            VAR = CHILDREN[1].VAR
            super().__init__(SEM, VAR, CHILDREN, GNAME="CITY-CNP")
        elif len(CHILDREN) == 1:
            SEM = NAME(None, CHILDREN[0])
            VAR = CHILDREN[0].VAR
            super().__init__(SEM, VAR, CHILDREN, GNAME="CITY-CNP")

class BusName(GrammarStucture):
    def __init__(self, SEM, VAR) -> None:
        super().__init__(SEM, VAR, [], "BUS-NAME")

class BusN(GrammarStucture):
    def __init__(self, SEM, VAR) -> None:
        SEM = BUS(None)
        super().__init__(SEM, VAR, [], "BUS-N")

class BusCNP(GrammarStucture):
    def __init__(sefl, CHILDREN):
        SEM = BUS(CHILDREN[1])
        VAR = CHILDREN[1].VAR
        super().__init__(SEM, VAR, CHILDREN, GNAME="BUS-CNP")

class BusNP(GrammarStucture):
    def __init__(self, CHILDREN):
        SEM = [child.SEM for child in CHILDREN]
        for sem in SEM:
            for _sem in SEM:
                GrammarParsing.semUpdate(sem, _sem)
        VAR = CHILDREN[0].VAR
        super().__init__(SEM, VAR, CHILDREN, GNAME="BUS-NP")

    def getString(self, i=1):
        tab = '\t'*i
        children = ""
        for child in self.CHILDREN:
            children += '\n' + tab  + '(' + (child if isinstance(child, str) else child.getString(i+1))
        children += ')'
        return self.GNAME + '[SEM<{}>{}]'.format(' & '.join(str(sem) for sem in self.SEM), \
            ',VAR<{}>'.format(self.VAR) if self.VAR else "") + children

class PTime(GrammarStucture):
    def __init__(self, SEM, VAR) -> None:
        super().__init__(SEM, VAR, [], "P-TIME")

class QDet(GrammarStucture):
    def __init__(self, SEM, VAR):
        super().__init__(SEM, VAR, [], GNAME="QDET")

class WhichQ(GrammarStucture):
    def __init__(self, CHILDREN):
        SEM = WHICH(BUS(CHILDREN[0]), 'WHICH')
        VAR = CHILDREN[0].VAR
        super().__init__(SEM, VAR, CHILDREN, "WHICH-QUERY")

class WhatTime(GrammarStucture):
    def __init__(self):
        SEM = WHATTIME(None)
        VAR = 't1'
        super().__init__(SEM, VAR, [], "TIME-QUERY")
    
class BusRoute(GrammarStucture):
    def __init__(self, CHILDREN):
        source = CHILDREN[1].SEM.source if CHILDREN[1] else None
        dest = CHILDREN[3].SEM.dest if CHILDREN[3] else None
        CHILDREN = [child for child in CHILDREN if child is not None]
        SEM = ROUTE(source=source, dest=dest, bus=None, time=None)
        VAR = 'r'
        super().__init__(SEM, VAR, CHILDREN, GNAME="BUS-ROUTE")

class BusSource(GrammarStucture):
    def __init__(self, CHILDREN):
        SEM = ROUTE(source=CHILDREN[0], dest=None, bus=None, time=None)
        VAR = 'r1'
        super().__init__(SEM, VAR, CHILDREN, GNAME="BUS-SRC")

class BusDest(GrammarStucture):
    def __init__(self, CHILDREN):
        SEM = ROUTE(source=None, dest=CHILDREN[0], bus=None, time=None)
        VAR = 'r2'
        super().__init__(SEM, VAR, CHILDREN, GNAME="BUS-DEST")

class S(GrammarStucture):
    def __init__(self, CHILDREN, isWhich):
        if isWhich:
            busNp = BusNP(CHILDREN[1:])
            CHILDREN=[CHILDREN[0], busNp]
            SEM = [CHILDREN[0].SEM, *busNp.SEM]
            if isinstance(SEM[0].x, BUS):
                for sem in SEM:
                    if isinstance(sem, ROUTE): sem.bus=SEM[0].x
            if isinstance(SEM[-1], TIME):
                for sem in SEM:
                    if isinstance(sem, ROUTE): sem.time=SEM[-1]
            VAR = CHILDREN[0].VAR
            super().__init__(SEM, VAR, CHILDREN, GNAME="S")
            self.GAP = CHILDREN[0].VAR

        else:
            busNp = BusNP(CHILDREN[1:])
            CHILDREN=[CHILDREN[0], busNp]
            CHILDREN[0].SEM.x = CHILDREN[0].VAR
            SEM = [CHILDREN[0].SEM, *busNp.SEM]
            VAR = CHILDREN[0].VAR
            self.GAP = CHILDREN[0].VAR

            for sem in SEM:
                for _sem in SEM:
                    GrammarParsing.semUpdate(sem, _sem)

            super().__init__(SEM, VAR, CHILDREN, GNAME="S")
    
    def getString(self, i=1):
        tab = '\t'*i
        children = ""
        for child in self.CHILDREN:
            children += '\n' + tab  + '(' + (child if isinstance(child, str) else child.getString(i+1))
        children += ')'
        return self.GNAME + '[GAP<{}> SEM<{}>{}]'.format(self.GAP, ' & '.join(['({})'.format(str(sem)) for sem in self.SEM]), \
            ',VAR<{}>'.format(self.VAR) if self.VAR else "") + children


class GrammarParsing():
    def __init__(self, tree) -> None:
        self.tree = tree
        self.root_index = self.tree.nodes[0].siblings[0][0].tid
    
    def parsing(self, start_index=None):
        def order(node):
            return node[0].tid
        children = list()
        dep_node = sorted(self.tree.nodes[self.root_index].siblings[:-1], key=order)
        # dep_node = self.tree.nodes[self.root_index].siblings[:-1].sort(key=)
        for node, dependency in dep_node: 
            # print(node)
            # ignore question mark
            child = self.__parsing(node)
            if dependency == RelationType.DOBJ:
                if self.tree.nodes[self.root_index].wordform in ['đến']:
                    child = BusRoute((
                            None,
                            None,
                            self.tree.nodes[self.root_index].wordform,
                            BusDest([child])
                    ))
                if self.tree.nodes[self.root_index].wordform in ['từ']:
                    child = BusRoute((
                        self.tree.nodes[self.root_index].wordform,
                        BusSource([child]),
                        self.tree.nodes[self.root_index].siblings[-2][0].wordform,
                        self.__parsing(self.tree.nodes[self.root_index].siblings[-2][0])
                    ))
                    children.append(child)
                    break
            children.append(child)
        
        # for child in children: print(child.getString())
        isWhich = None
        for child in children:
            if type(child) == WhichQ:
                isWhich = True
            elif type(child) == WhatTime:
                isWhich = False
        grammarStructure = S(children, isWhich)
        # print(grammarStructure.getString())
        return grammarStructure

    def __parsing(self, node):
        node.wordform = node.wordform.lower()
        # this parsing utilize the dependency graph from previous stage
        if node.wordform == 'xe_buýt':
            child, dependency = node.siblings[0]
            if dependency == RelationType.DET:
                return WhichQ(
                            (BusN('XEBUYT', 'b1'),
                            QDet(child.wordform.upper(), "?b")))
            if dependency == RelationType.NMOD:
                return BusCNP(
                        (BusN('XEBUYT', 'b1'), 
                        BusName(child.wordform, 'b2')))
            # print(dependency)
        if node.wordform == 'thành_phố':
            child, dependency = node.siblings[0]
            if dependency == RelationType.COMPOUND:
                return CityCNP(
                        (CityN('THANHPHO', 'c1'), 
                        CityName(CITYSEM[child.wordform.lower()], 'c2')))
        if node.wordform in list(CITYSEM.keys()):
            return CityCNP(
                [CityName(CITYSEM[node.wordform], 'c1')]
            )
        if node.wordform == 'lúc':
            child, dependency = node.siblings[0]
            return BusTime(
                (PTime(node.wordform, None),
                TimeMod(child.wordform, None))
            )
        if node.wordform == 'thời_gian':
            return WhatTime()

        if node.wordform in ['đến', 'tới']:
            child, dependency = node.siblings[0]
            isDest = True
            dest = self.__parsing(child)
            return BusDest([dest])

    @staticmethod
    def semUpdate(sem, _sem):
        if type(sem) in [BUS, WHICH, ROUTE]:
            if type(_sem) in [BUS, WHICH, ROUTE]:
                if type(_sem) == WHICH:
                    if _sem.x is None: _sem.x = sem.x if type(sem) == WHICH else sem.bus
                else:
                    if _sem.bus is None: _sem.bus = sem.x if type(sem) == WHICH else sem.bus
        if type(sem) in [TIME, WHATTIME, ROUTE]:
            if type(_sem) in [TIME, WHATTIME, ROUTE]:
                if type(_sem) == WHATTIME:
                    if _sem.x is None: _sem.x = sem.x if type(sem) == WHATTIME else sem.time
                else:
                    if _sem.time is None: _sem.time = sem.x if type(sem) == WHATTIME else sem.time
