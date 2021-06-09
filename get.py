from Models.grammar import S


with open("/Users/mac/Documents/NLP202/busStopQAsystem/abc.txt", 'r') as f:
    nF = ''
    for line in f.readlines():
        a = line.lower().split(' ')
        b = list(map(lambda x: x[0] + x[-1] if '.' in x else x[0], a))
        a = ''.join(b)
        print(a)