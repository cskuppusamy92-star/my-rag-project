from __future__ import annotations

from pathlib import Path
import pickle
from typing import Any


class GraphStore:
    def __init__(self):
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: list[dict[str, Any]] = []

    def add_node(
        self,
        node_id: str,
        node_type: str = "entity",
        **properties: Any,
    ) -> None:
        self.nodes[node_id] = {
            "id": node_id,
            "type": node_type,
            **properties,
        }

    def add_edge(
        self,
        source: str,
        relation: str,
        target: str,
        **properties: Any,
    ) -> None:
        self.edges.append(
            {
                "source": source,
                "relation": relation,
                "target": target,
                **properties,
            }
        )

    def get_node(self, node_id: str) -> dict[str, Any] | None:
        return self.nodes.get(node_id)

    def get_neighbors(self, node_id: str) -> list[dict[str, Any]]:
        results = []

        for edge in self.edges:
            if edge["source"] == node_id:
                results.append(edge)

        return results

    def find_relationships(
        self,
        source: str | None = None,
        relation: str | None = None,
        target: str | None = None,
    ) -> list[dict[str, Any]]:
        results = []

        for edge in self.edges:
            if source is not None and edge["source"] != source:
                continue

            if relation is not None and edge["relation"] != relation:
                continue

            if target is not None and edge["target"] != target:
                continue

            results.append(edge)

        return results

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "wb") as file:
            pickle.dump(
                {
                    "nodes": self.nodes,
                    "edges": self.edges,
                },
                file,
            )

    def load(self, path: str | Path) -> None:
        path = Path(path)

        if not path.exists():
            return

        with open(path, "rb") as file:
            data = pickle.load(file)

        self.nodes = data.get("nodes", {})
        self.edges = data.get("edges", [])

    def clear(self) -> None:
        self.nodes.clear()
        self.edges.clear()

    def __len__(self) -> int:
        return len(self.nodes)