import math
from dataclasses import dataclass
from enum import Enum, auto

from parsing import (
    Parse,
    ParseError,
    Parser,
    delimited,
    exact,
    integer,
    one_of,
    separated,
    whitespace,
)
from typing_extensions import assert_never


def load_inputs() -> str:
    with open("inputs/day11", encoding="utf-8") as inputs_file:
        return inputs_file.read()


@dataclass(frozen=True)
class OperandOld:
    pass


@dataclass(frozen=True)
class OperandValue:
    value: int


Operand = OperandOld | OperandValue


class Operator(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()

    def operand_value(self, operand: Operand, *, old_value: int) -> int:
        match operand:
            case OperandOld():
                return old_value
            case OperandValue(value):
                return value
            case _:
                assert_never(operand)

    def apply(self, left: Operand, right: Operand, *, old_value: int) -> int:
        left_value = self.operand_value(left, old_value=old_value)
        right_value = self.operand_value(right, old_value=old_value)
        match self:
            case self.ADD:
                return left_value + right_value
            case self.SUB:
                return left_value - right_value
            case self.MUL:
                return left_value * right_value
            case self.DIV:
                return left_value // right_value
        raise ValueError(f"unsupported operator: {self}")


@dataclass(frozen=True)
class Operation:
    operator: Operator
    left: Operand
    right: Operand

    def apply(self, *, old_value: int) -> int:
        return self.operator.apply(self.left, self.right, old_value=old_value)


def operand() -> Parser[Operand]:
    def parser(stream: str) -> Parse[Operand]:
        try:
            _, stream = exact("old")(stream)
        except ParseError:
            value, stream = integer()(stream)
            return OperandValue(value), stream
        else:
            return OperandOld(), stream

    return parser


def operator() -> Parser[Operator]:
    char_to_operator = {
        "+": Operator.ADD,
        "-": Operator.SUB,
        "*": Operator.MUL,
        "/": Operator.DIV,
    }

    def parser(stream: str) -> Parse[Operator]:
        op, stream = one_of("+-*/")(stream)
        return char_to_operator[op], stream

    return parser


def operation() -> Parser[Operation]:
    def parser(stream: str) -> Parse[Operation]:
        left, stream = operand()(stream)
        _, stream = whitespace(1)(stream)
        op, stream = operator()(stream)
        _, stream = whitespace(1)(stream)
        right, stream = operand()(stream)
        return Operation(operator=op, left=left, right=right), stream

    return parser


@dataclass(frozen=True)
class Rule:
    monkey_num: int
    initial_items: list[int]
    operation: Operation
    modulo_test: int
    if_true: int
    if_false: int


def parse_rule(stream: str) -> Parse[Rule]:
    # Monkey 0:
    monkey_num, stream = delimited(exact("Monkey "), integer(), exact(":\n"))(stream)

    #   Starting items: 79, 98
    items, stream = delimited(
        exact("  Starting items: "), separated(integer(), ", "), exact("\n")
    )(stream)

    #   Operation: new = old * 19
    #   Operation: new = old + 6
    #   Operation: new = old * old
    oper, stream = delimited(exact("  Operation: new = "), operation(), exact("\n"))(
        stream
    )

    #   Test: divisible by 13
    modulo, stream = delimited(exact("  Test: divisible by "), integer(), exact("\n"))(
        stream
    )

    #     If true: throw to monkey 2
    if_true, stream = delimited(
        exact("    If true: throw to monkey "), integer(), exact("\n")
    )(stream)

    #     If false: throw to monkey 3
    if_false, stream = delimited(
        exact("    If false: throw to monkey "), integer(), exact("\n")
    )(stream)

    try:
        _, stream = exact("\n")(stream)
    except ParseError:
        pass  # we're at the end

    rule = Rule(
        monkey_num=monkey_num,
        initial_items=items,
        operation=oper,
        modulo_test=modulo,
        if_true=if_true,
        if_false=if_false,
    )
    return rule, stream


def parse_rules() -> list[Rule]:
    stream = load_inputs()
    rules = []
    while stream:
        rule, stream = parse_rule(stream)
        rules.append(rule)
    return rules


def create_monkeys(rules: list[Rule]) -> list[list[int]]:
    monkeys: list[list[int]] = [[] for _ in rules]
    for rule in rules:
        monkeys[rule.monkey_num].extend(rule.initial_items)
    return monkeys


def run_rounds(rounds: int, *, rules: list[Rule], relief: bool = True) -> int:
    monkeys = create_monkeys(rules)
    inspections = [0 for _ in rules]

    # divisor to use when we're not dividing the worry level by 3.
    # this has to be a multiple of all the modulo tests for congruency to be maintained.
    common_multiple = math.prod(rule.modulo_test for rule in rules)

    for _ in range(rounds):
        for rule in rules:
            monkey = monkeys[rule.monkey_num]

            for item in monkey:
                inspections[rule.monkey_num] += 1
                item = rule.operation.apply(old_value=item)

                if relief:
                    item //= 3
                else:
                    item %= common_multiple

                if item % rule.modulo_test == 0:
                    target = rule.if_true
                else:
                    target = rule.if_false

                monkeys[target].append(item)
            monkey.clear()

    monkey_business = math.prod(sorted(inspections, reverse=True)[:2])
    return monkey_business


rules = parse_rules()

part_1 = run_rounds(20, rules=rules)
print(f"part 1: {part_1}")

part_2 = run_rounds(10000, rules=rules, relief=False)
print(f"part 2: {part_2}")
