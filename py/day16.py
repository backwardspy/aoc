"""
credit to https://github.com/juanplopes/advent-of-code-2022/blob/main/day16.py
for the methodology. all i really did was make it less elegant. :)
"""
import re
from dataclasses import dataclass

line_pat = re.compile(
    r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
)


@dataclass(frozen=True)
class Node:
    flow_rate: int
    links: set[str]


Graph = dict[str, Node]
Connections = dict[str, dict[str, int]]


def load_graph() -> Graph:
    graph = {}
    with open("inputs/day16", encoding="utf-8") as inputs_file:
        for line in inputs_file:
            match = line_pat.match(line)
            if not match:
                raise ValueError(f"{line=} does not match pattern {line_pat=}")

            id, flow_rate, links = match.groups()
            graph[id] = Node(flow_rate=int(flow_rate), links=links.split(", "))
    return graph


def get_connections(graph: Graph) -> Connections:
    connections = {
        a: {b: 1 if b in node.links else 9999999999999 for b in graph.keys()}
        for a, node in graph.items()
    }

    # find all the shortest distances between nodes using floyd-warshall
    for k in graph:
        for i in graph:
            for j in graph:
                connections[i][j] = min(
                    connections[i][j], connections[i][k] + connections[k][j]
                )

    # we don't care about visiting anything with zero flow rate.
    connections = {
        a: {b: dist for b, dist in connection.items() if graph[b].flow_rate > 0}
        for a, connection in connections.items()
        if a == "AA" or graph[a].flow_rate > 0
    }

    return connections


def search(
    graph: Graph,
    *,
    start: str,
    connections: Connections,
    visited: int,
    masks: dict[str, int],
    seconds_remaining: int,
    total_flow: int,
    results: dict[int, int],
) -> None:
    results[visited] = max(results.get(visited, 0), total_flow)

    for neighbour, distance in connections[start].items():
        if visited & masks[neighbour]:
            continue

        # deduct travel time + valve turning time
        new_time = seconds_remaining - distance - 1

        if new_time <= 0:
            continue

        search(
            graph,
            start=neighbour,
            connections=connections,
            visited=visited | masks[neighbour],
            masks=masks,
            seconds_remaining=new_time,
            total_flow=total_flow + graph[neighbour].flow_rate * new_time,
            results=results,
        )


def main() -> None:
    graph = load_graph()
    connections = get_connections(graph)
    masks = {name: 1 << i for i, name in enumerate(connections)}

    results = {}
    search(
        graph,
        start="AA",
        connections=connections,
        visited=0,
        masks=masks,
        seconds_remaining=30,
        total_flow=0,
        results=results,
    )
    print(f"part 1: {max(results.values())}")

    results = {}
    search(
        graph,
        start="AA",
        connections=connections,
        visited=0,
        masks=masks,
        seconds_remaining=26,
        total_flow=0,
        results=results,
    )
    part_2 = max(
        score_a + score_b
        for a, score_a in results.items()
        for b, score_b in results.items()
        if not a & b
    )
    print(f"part 2: {part_2}")


if __name__ == "__main__":
    main()
