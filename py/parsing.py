import itertools
import string
from typing import Callable, TypeVar

T = TypeVar("T")
Parse = tuple[T, str]  # (parsed value, remaining stream)
Parser = Callable[[str], Parse[T]]


class ParseError(Exception):
    def __init__(self, expected: str, stream: str):
        if len(stream) > 50:
            stream = stream[:47] + "..."
        super().__init__(f"expected {expected!r} in {stream!r}")


def exact(expected: str) -> Parser[str]:
    def parser(stream: str) -> Parse[str]:
        if not stream.startswith(expected):
            raise ParseError(expected, stream)
        return expected, stream[len(expected) :]

    return parser


def take_while(predicate: Callable[[str], bool]) -> Parser[str]:
    def parser(stream: str) -> Parse[str]:
        match = "".join(itertools.takewhile(predicate, stream))
        return match, stream[len(match) :]

    return parser


def integer() -> Parser[int]:
    def parser(stream: str) -> Parse[int]:
        digits, stream = take_while(lambda x: x in string.digits)(stream)
        return int(digits), stream

    return parser


def whitespace(size: int) -> Parser[str]:
    def parser(stream: str) -> Parse[str]:
        space = stream[:size]
        if len(space) != size or any(c not in string.whitespace for c in space):
            raise ParseError(" " * size, stream)
        return space, stream[size:]

    return parser


def separated(item_parser: Parser[T], separator: str) -> Parser[list[T]]:
    sep = exact(separator)

    def parser(stream: str) -> Parse[list[T]]:
        items = []
        while True:
            item, stream = item_parser(stream)
            items.append(item)
            if not stream.startswith(separator):
                break
            _, stream = sep(stream)
        return items, stream

    return parser


def delimited(before: Parser[str], inner: Parser[T], after: Parser[str]) -> Parser[T]:
    def parser(stream: str) -> Parse[T]:
        _, stream = before(stream)
        value, stream = inner(stream)
        _, stream = after(stream)
        return value, stream

    return parser


def one_of(chars: str) -> Parser[str]:
    def parser(stream: str) -> Parse[str]:
        char = stream[0]
        if char not in chars:
            raise ParseError(chars, stream)
        return char, stream[1:]

    return parser
