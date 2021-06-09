from unicodedata import name
from Models.utils import tree
import pdb
from Models.enums import RelationType

CITYSEM={'hồ_chí_minh': 'HCMC', 'đà_nẵng': 'DANANG', 'huế': 'HUE'}

class WHICH:
    def __init__(self, x) -> None:
        self.x = x.SEM
        self.var=x.VAR
    
    def __str__(self) -> str:
        return "WHICHBUS({})".format(
            self.var)

    def getLogical(self) ->str:
        return str(self)

class WHATTIME:
    def __init__(self, x) -> None:
        self.x = x
    
    def __str__(self) -> str:
        return "{}WHATTIME({})".format(
            "" if self.x else "\\x.",
            "x" if self.x is None else '{}'.format(self.x))

    

class HOWLONG:
    def __init__(self, x) -> None:
        self.x = x
    
    def __str__(self) -> str:
        return "{}HOWLONG({})".format(
            "" if self.x else "\\x.",
            "x" if self.x is None else '{}'.format(self.x))

    def getLogical(self) -> str:
        return "HOWLONG({})".format(self.x)

class DET:
    def __init__(self, object):
        self.x = object.SEM
    
    def __str__(self) -> str:
        return "DET({})".format(self.x if self.x is not None else '?x')

class NAME:
    def __init__(self, objectN, objectName):
        self.name = objectName.SEM
        self.var = objectName.VAR

    def __init__(self, name:str, var:str):
        self.name = name
        self.var = var
    
    def __str__(self) -> str:
        return "NAME({}, {})".format(self.name, self.var)

class DEST:
    def __init__(self, cityName) -> None:
        self.bus = None
        self.name = cityName.SEM
    
    def __str__(self) -> str:
        return "{}DEST({}, {})".format("\\d." if self.bus is None else "", \
                                        "d" if self.bus is None else self.bus,\
                                        self.name)

class ROUTE:
    def __init__(self, source, dest=None, bus=None, time=None) -> None:
        self.source = source
        self.dest = dest
        self.bus = bus
        self.time = time # TIME object : semantic feature

    def __str__(self) -> str:
        return "{}{}{}{}ROUTE({}, {}, {}, {})".format(
            "\\s " if   self.source  is None else "",
            "d " if     self.dest    is None else "",
            "b " if     self.bus    is None else "",
            "t." if     self.time       is None else "",
            "s" if      self.source  is None else "SRC-CITY(" + str(self.source.SEM) + ")",
            "d" if      self.dest    is None else "DST-CITY(" + str(self.dest.SEM) + ")",
            "b" if      self.bus    is None else self.bus,
            "t" if      self.time       is None else self.time
        )

    def getLogical(self) -> str:
        return "ROUTE({}, {}, {}, {})".format(
            "s1" if      self.source  is None else "SRC-CITY({}, {})".format(self.source.SEM.name, self.source.SEM.var),
            "d1" if      self.dest    is None else "DST-CITY({}, {})".format(self.dest.SEM.name, self.dest.SEM.var),
            "b" if      self.bus    is None else self.bus if type(self.bus) == str else self.bus.getLogical(),
            "t1" if      self.time       is None else self.time if type(self.time) == str else self.time.getLogical()
        )

class BUS:
    def __init__(self, name, var) -> None:
        self.var = name.var
        self.name = name.name
    
    def __str__(self) -> str:
        return "BUS({}, {})".format(
            "" if self.name is None else self.name,
            "" if self.var is None else self.var
        )
    
    def getLogical(self) -> str:
        return "BUS({}, {})".format(
            "" if self.name is None else self.name,
            "" if self.var is None else self.var
        )

class TIME:
    def __init__(self, atime=None, dtime=None) -> None:
        self.atime = atime
        self.dtime = dtime

    def __str__(self) -> str:
        return "{}{}TIME({}, {})".format(
            "\\dt" if self.dtime is None else "",
            " at" if self.atime is None else '.' if self.dtime is None else "",
            "dt" if self.dtime is None else self.dtime,
            "at" if self.atime is None else self.atime
            )
    
    def getLogical(self) -> str:
        return "TIME({}, {})".format(
            "dt1" if self.dtime is None else self.dtime,
            "at1" if self.atime is None else self.atime
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
    def __init__(self, SEM, VAR) -> None:
        super().__init__(SEM, VAR, [], "CITY-NAME")

class CityCNP(GrammarStucture):
    def __init__(sefl, CHILDREN):
        if len(CHILDREN) == 2:
            SEM = NAME(CHILDREN[1].SEM, CHILDREN[1].VAR)
            VAR = CHILDREN[1].VAR
            super().__init__(SEM, VAR, CHILDREN, GNAME="CITY-CNP")
        elif len(CHILDREN) == 1:
            SEM = NAME(CHILDREN[0].SEM, CHILDREN[0].VAR)
            VAR = CHILDREN[0].VAR
            super().__init__(SEM, VAR, CHILDREN, GNAME="CITY-CNP")

class BusName(GrammarStucture):
    def __init__(self, SEM, VAR) -> None:
        SEM = BUS(SEM, 'b1')
        VAR = 'b1'
        super().__init__(SEM, VAR, [], "BUS-NAME")

class BusN(GrammarStucture):
    def __init__(self, SEM, VAR) -> None:
        super().__init__(SEM, VAR, [], "BUS-N")

class BusCNP(GrammarStucture):
    def __init__(sefl, CHILDREN):
        SEM = CHILDREN[1].SEM
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
        SEM = WHICH(CHILDREN[0])
        VAR = CHILDREN[0].VAR
        super().__init__(SEM, VAR, CHILDREN, "WHICH-QUERY")

class WhatTime(GrammarStucture):
    def __init__(self):
        SEM = WHATTIME(None)
        VAR = 't1'
        super().__init__(SEM, VAR, [], "TIME-QUERY")

class HowLong(GrammarStucture):
    def __init__(self):
        SEM = HOWLONG(None)
        VAR = 't1'
        super().__init__(SEM, VAR, [], "RTIME-QUERY")
    
class BusRoute(GrammarStucture):
    def __init__(self, CHILDREN):
        source = CHILDREN[1].SEM.source if CHILDREN[1] else None
        dest = CHILDREN[3].SEM.dest if CHILDREN[3] else None
        CHILDREN = [child for child in CHILDREN if child is not None]
        SEM = ROUTE(source=source, dest=dest)
        VAR = 'r'
        super().__init__(SEM, VAR, CHILDREN, GNAME="BUS-ROUTE")

class BusSource(GrammarStucture):
    def __init__(self, CHILDREN):
        SEM = ROUTE(source=CHILDREN[0], dest=None)
        VAR = 'r1'
        super().__init__(SEM, VAR, CHILDREN, GNAME="BUS-SRC")

class BusDest(GrammarStucture):
    def __init__(self, CHILDREN):
        SEM = ROUTE(source=None, dest=CHILDREN[0])
        VAR = 'r2'
        super().__init__(SEM, VAR, CHILDREN, GNAME="BUS-DEST")

class S(GrammarStucture):
    def __init__(self, CHILDREN, isWhich):
        if isWhich:
            busNp = BusNP(CHILDREN[1:])
            CHILDREN=[CHILDREN[0], busNp]
            SEM = [CHILDREN[0].SEM, *busNp.SEM]
            if isinstance(SEM[-1], TIME):
                for sem in SEM:
                    if isinstance(sem, ROUTE): sem.atime=SEM[-1]

            for sem in SEM:
                for _sem in SEM:
                    GrammarParsing.semUpdate(sem, _sem)
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
                            (BusN(NAME(None, None), 'b1'),
                            QDet(child.wordform.upper(), "?b")))
            if dependency == RelationType.NMOD:
                return BusCNP(
                        (BusN('XEBUYT', 'b1'), 
                        BusName(NAME(child.wordform, 'b2'), 'b2')))
            # print(dependency)
        if node.wordform == 'thành_phố':
            child, dependency = node.siblings[0]
            if dependency == RelationType.COMPOUND:
                return CityCNP(
                        (CityN('THANHPHO', 'c3'), 
                        CityName(CITYSEM[child.wordform.lower()], 'c' + str(list(CITYSEM.keys()).index(child.wordform.lower())))))
        if node.wordform in list(CITYSEM.keys()):
            return CityCNP(
                [CityName(CITYSEM[node.wordform],  'c' + str(list(CITYSEM.keys()).index(node.wordform.lower())))]
            )
        if node.wordform == 'lúc':
            child, dependency = node.siblings[0]
            return BusTime(
                (PTime(node.wordform, None),
                TimeMod(child.wordform, None))
            )
        if node.wordform == 'thời_gian':
            return HowLong()

        if node.wordform in ['đến', 'tới']:
            child, dependency = node.siblings[0]
            isDest = True
            dest = self.__parsing(child)
            return BusDest([dest])

    @staticmethod
    def semUpdate(sem, _sem):
        if type(sem) in [WHICH, ROUTE]:
            if type(_sem) in [WHICH, ROUTE]:
                if type(_sem) == WHICH:
                    if _sem.var is None: _sem.var = sem.var if type(sem) == WHICH else sem.bus
                else:
                    if _sem.bus is None: _sem.bus = sem.var if type(sem) == WHICH else sem.bus
            if type(_sem) in [BUS]:
                if _sem is None: _sem = sem.var if type(sem) == WHICH else sem.bus.var
        if type(sem) in [BUS]:
            if type(_sem) in [WHICH, ROUTE]:
                if type(_sem) == WHICH:
                    if _sem.var is None: _sem.var = sem.var
                else:
                    if _sem.bus is None: _sem.bus = sem
            if type(_sem) in [BUS]:
                if _sem is None: _sem = sem
        if type(_sem) in [ROUTE]:
            if type(sem) in [TIME]:
                if _sem.time is None: _sem.time = sem
        # if type(sem) in [TIME, WHATTIME, ROUTE]:
        #     if type(_sem) in [TIME, WHATTIME, ROUTE]:
        #         if type(_sem) == WHATTIME:
        #             if _sem.x is None: _sem.x = sem.x if type(sem) == WHATTIME else sem.atime
        #         else:
        #             if _sem.atime is None: _sem.atime = sem.x if type(sem) == WHATTIME else sem.atime
