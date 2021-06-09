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
                self.route.time.dtime if self.route.time else '?dt')
            atime = "ATIME(?{} {} {})".format(
                self.queryObject.var,
                self.route.dest.SEM.name if self.route.dest else '?d',
                self.route.time.atime if self.route.time else '?at')
            return "PRINT-ALL {} {} {}".format(bus, atime, dtime)
        if self.queryName == 'RTIME-QUERY':
    
            rtime = "RUN-TIME({} {} {} ?{})".format(
                self.route.bus.name,
                self.route.source.SEM.name,
                self.route.dest.SEM.name,
                self.queryObject.x
                )
            return "PRINT-ALL {}".format(rtime)