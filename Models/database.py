class Bus:
    def __init__(self, name) -> None:
        self.name = name

    def __eq__(self, name: str) -> bool:
        return self.name == name
    
    def __str__(self) -> str:
        return "(BUS {})".format(self.name)
class Atime:
    def __init__(self, bus, city, time) -> None:
        self.bus = bus
        self.city = city
        self.time = time

    def __eq__(self, a) -> bool:
        res = True if a.bus is None else self.bus == a.bus
        res = res and (True if a.city is None else self.city == a.city)
        res = res and (True if a.time is None else self.time == a.time)
        return res

    def __str__(self) -> str:
        return "ATIME({} {} {}HR)".format(self.bus, self.city, self.time)

class Dtime:
    def __init__(self, bus, city, time) -> None:
        self.bus = bus
        self.city = city
        self.time = time

    def __eq__(self, a) -> bool:
        res = True if a.bus is None else self.bus == a.bus
        res = res and True if a.city is None else self.city == a.city
        res = res and True if a.time is None else self.time == a.time
        return res

    def __str__(self) -> str:
        return "DTIME({} {} {}HR)".format(self.bus, self.city, self.time)

class Rtime:
    def __init__(self, bus, src, dest, time) -> None:
        self.bus = bus
        self.src = src
        self.dest = dest
        self.time = time

    def __eq__(self, r) -> bool:
        res = self.bus == r.bus
        res = res and (self.src == r.src)
        res = res and (self.dest == r.dest)
        return res

    def __str__(self) -> str:
        return "RUN-TIME({} {} {} {})".format(self.bus, self.src, self.dest, self.time)

DATABASE = {
'BUS' : [
    Bus('B1'),
    Bus('B2'),
    Bus('B3'),
    Bus('B4'),
    Bus('B5'),
    Bus('B6')
],

'ATIME' : [
    Atime('B1', 'HUE', '19:00'),
    Atime('B2', 'HUE', '22:30'),
    Atime('B3', 'HUE', '20:00'),
    Atime('B4', 'HCMC', '18:30'),
    Atime('B5', 'HN', '23:30'),
    Atime('B6', 'HN', '22:30'),
],

'DTIME' : [
    Dtime('B1', 'HCMC', '10:00'),
    Dtime('B2', 'HCMC', '14:30'),
    Dtime('B3', 'DANANG', '16:00'),
    Dtime('B4', 'DANANG', '8:30'),
    Dtime('B5', 'DANANG', '5:30'),
    Dtime('B6', 'HUE', '6:30'),
],

'RUNTIME' : [
    Rtime('B1', 'HCMC', 'HUE', '9:00'),
    Rtime('B2', 'HCMC', 'HUE', '8:00'),
    Rtime('B3', 'DANANG', 'HUE', '4:00'),
    Rtime('B4', 'DANANG', 'HCMC', '10:00'),
    Rtime('B5', 'DANANG', 'HN', '18:00'),
    Rtime('B6', 'HUE', 'HN', '16:00'),
]
}