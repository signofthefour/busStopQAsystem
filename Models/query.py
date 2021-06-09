from Models.database import Atime, Dtime, Rtime


class Query:
    def __init__(self, QUERYNAME, qObject, route) -> None:
        self.queryName = QUERYNAME
        self.queryObject = qObject
        self.route = route

    def __str__(self) -> None:
        if self.queryName == 'WHICH-QUERY':
            bus =  "?{}(BUS ?{})".format(self.queryObject.var, self.queryObject.var)
            dtime = "DTIME(?{} {} {})".format(
                self.queryObject.var,
                self.route.source.SEM.name if self.route.source else '?s',
                self.route.time.dtime if self.route.time and self.route.time.dtime else '?dt' )
            atime = "ATIME(?{} {} {})".format(
                self.queryObject.var,
                self.route.dest.SEM.name if self.route.dest else '?d',
                self.route.time.atime if self.route.time and self.route.time.atime else '?at')
            return "PRINT-ALL {} {} {}".format(bus, atime, dtime)
        if self.queryName == 'RTIME-QUERY':
    
            rtime = "RUN-TIME({} {} {} ?{})".format(
                self.route.bus.name,
                self.route.source.SEM.name,
                self.route.dest.SEM.name,
                self.queryObject.x
                )
            return "PRINT-ALL {}".format(rtime)

    def execute(self, snapshot):
        import itertools
        if self.route.time:
            if self.route.time.dtime:
                self.route.time.dtime = self.route.time.dtime[0:-3] + ':' + self.route.time.dtime[-2:]
            if self.route.time.atime:
                self.route.time.atime = self.route.time.atime[0:-3] + ':' + self.route.time.atime[-2:]
        if self.queryName == 'WHICH-QUERY':
            dtime = Dtime(
                None,
                self.route.source.SEM.name if self.route.source else None,
                self.route.time.dtime if self.route.time else None)
            atime = Atime(
                None,
                self.route.dest.SEM.name if self.route.dest else None,
                self.route.time.atime if self.route.time else None)
            sameDtime = [_dtime for _dtime in snapshot["DTIME"] if _dtime == dtime]
            sameAtime = [_atime for _atime in snapshot["ATIME"] if _atime == atime]
            results = [(a, d) for a, d in itertools.product(sameAtime, sameDtime) if a.bus == d.bus]
            return results


        if self.queryName == 'RTIME-QUERY':
            rtime = Rtime(self.route.bus.name,
                self.route.source.SEM.name,
                self.route.dest.SEM.name,
                None)
            results = [_rtime for _rtime in snapshot["RUNTIME"] if _rtime == rtime]
            return results
