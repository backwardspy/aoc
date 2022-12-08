from dataclasses import dataclass
from typing import Generator

InputLines = Generator[str, None, None]


def input_lines() -> InputLines:
    with open("inputs/day7") as f:
        lines = (line.strip() for line in f)
        yield from lines


@dataclass
class FSNode:
    is_dir: bool
    size: int
    children: dict[str, "FSNode"]

    @staticmethod
    def dir_node() -> "FSNode":
        return FSNode(is_dir=True, size=0, children={})

    @staticmethod
    def file_node(size: int) -> "FSNode":
        return FSNode(is_dir=False, size=size, children={})

    def calculate_size(self) -> int:
        if self.is_dir:
            return sum(node.calculate_size() for node in self.children.values())
        else:
            return self.size


class FS:
    def __init__(self) -> None:
        self.tree = FSNode.dir_node()
        self.pwd = []

    def format_pwd(self) -> str:
        return f"/{'/'.join(self.pwd)}"

    @property
    def pwd_node(self) -> FSNode:
        node = self.tree
        for path in self.pwd:
            node = node.children[path]
        return node

    def cd(self, dir: str) -> None:
        match dir:
            case "..":
                if not self.pwd:
                    raise ValueError("already at top level")
                self.pwd.pop()
            case "/":
                self.pwd = []
            case dir:
                if dir not in self.pwd_node.children:
                    raise ValueError(f"nonexistent dir '{dir}' in {self.format_pwd()}")
                elif not self.pwd_node.children[dir].is_dir:
                    raise ValueError(f"{self.format_pwd()}/{dir} is not a directory")

                self.pwd.append(dir)

    def mkdir(self, name: str) -> None:
        if name in self.pwd_node.children:
            return
        self.pwd_node.children[name] = FSNode.dir_node()

    def mkfile(self, name: str, size: int) -> None:
        if name in self.pwd_node.children:
            raise ValueError(f"file \"{name}\" already exists at /{'/'.join(self.pwd)}")
        self.pwd_node.children[name] = FSNode.file_node(size)


def parse_fs(lines: InputLines) -> FS:
    # empty string is the top-level dir
    fs = FS()

    for line in lines:
        if line.startswith("$ cd "):
            fs.cd(line[5:])
        elif line == "$ ls":
            # we can safely ignore this line
            pass
        elif line.startswith("dir "):
            dirname = line[4:]
            fs.mkdir(dirname)
        else:
            size, name = line.split()
            fs.mkfile(name, int(size))

    return fs


def print_tree(node: FSNode, level: int = 0):
    indent = "│ " * level
    for name, child in node.children.items():
        print(f"{indent}{name}", end="")
        if child.is_dir:
            print()
            print_tree(child, level + 1)
        else:
            print(f" ({child.size})")


def size_directories(node: FSNode, maximum: int) -> int:
    if not node.is_dir:
        return 0

    total = 0
    if (size := node.calculate_size()) <= maximum:
        total += size

    for child in node.children.values():
        total += size_directories(child, maximum)

    return total


def find_deletion_candidate(node: FSNode, minimum: int) -> int:
    # hehehehehe
    best = 10000000000000000000

    if not node.is_dir:
        return best

    if (size := node.calculate_size()) >= minimum:
        best = size

    for child in node.children.values():
        if (size := find_deletion_candidate(child, minimum)) < best:
            best = size

    return best


fs = parse_fs(input_lines())
# print_tree(fs.tree)

part_1 = size_directories(fs.tree, 100000)
print(f"part 1: {part_1}")

total_space = 70000000
needed = 30000000
available = total_space - fs.tree.calculate_size()
minimum = needed - available
part_2 = find_deletion_candidate(fs.tree, minimum)
print(f"part 2: {part_2}")
