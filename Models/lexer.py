import re
from collections import namedtuple


Token = namedtuple('Token', ('name', 'value'))
Node = namedtuple('Node', ('name', 'items'))


class Lexer(object):
    """
    A tokenizer that takes a string and produces a sequence of
    `Token` instances. If no match found a SyntaxError is raised.
    """
    def __init__(self, patterns):
        """
        :param patterns: A sequence of (regex_pattern, token_name) tuples.
         Patterns are order dependent: first match wins
        """
        self.patterns = [
            (re.compile(bytes(p, 'utf8')), name) for p, name in patterns]

    def lex(self, raw, ignore_spaces=True):
        """
        :param raw: an input string
        :param ignore_spaces: if True, all whitespace characters are skipped
        :return: generator of tokens
        """
        self.raw = bytearray(raw, 'utf8')
        self.pos = 0
        endpos = len(self.raw)

        while self.pos != endpos:
            if ignore_spaces and self.raw[self.pos: self.pos + 1].isspace():
                self.pos += 1
                continue
            for p, name in self.patterns:
                m = p.match(self.raw[self.pos:])
                if m is not None:
                    val, offset = m.group(), m.end()
                    yield Token(name, str(val, 'utf8'))
                    self.pos += offset
                    break
            else:
                self.error('Illegal character')
        yield Token('EOF', None)

    def error(self, message):
        raise SyntaxError(message, self.get_debug_info())

    def get_debug_info(self, f_name=None):
        pos = self.pos + 1
        raw = self.raw
        line_no = raw[:pos].count(b'\n')
        line_start = max(raw.rfind(b'\n'), 0)
        line_end = max(raw.find(b'\n'), len(raw))
        line = str(raw[line_start:line_end], 'utf-8')
        offset = pos - line_start
        return (f_name, line_no, offset, line)


