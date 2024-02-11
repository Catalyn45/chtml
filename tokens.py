from dataclasses import dataclass

@dataclass
class Token:
    pass

class OpenTag(Token):
    pass

class OpenTagSlash(Token):
    pass

class CloseTag(Token):
    pass

class Equals(Token):
    pass

class Different(Token):
    pass

@dataclass
class String(Token):
    content: str

class Plus(Token):
    pass

class Minus(Token):
    pass

class Multipy(Token):
    pass

class Division(Token):
    pass

@dataclass
class Identifier(Token):
    content: str

class EndOfFile(Token):
    pass