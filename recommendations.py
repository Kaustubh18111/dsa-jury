"""
recommendations.py

RecommendationEngine implemented as a graph using an adjacency list
(dictionary of dictionaries): graph[product_id][neighbor_id] = weight.

- Nodes are product_ids.
- Undirected, weighted edges represent co-purchases.
- Edge weight = number of times products were purchased together.

Data structure choice:
- Adjacency list gives O(1) average neighbor access and efficient sparse graph
  representation.
"""
from __future__ import annotations
from typing import Dict, List
from itertools import combinations


class RecommendationEngine:
    def __init__(self) -> None:
        # Hash table of hash tables: adjacency list for the weighted graph
        self.graph: Dict[str, Dict[str, int]] = {}

    def _ensure_node(self, product_id: str) -> None:
        if product_id not in self.graph:
            self.graph[product_id] = {}

    def record_purchase(self, product_id_list: List[str]) -> None:
        """Record a single order by incrementing co-purchase edge weights.

        For each unique pair in the order, increment the undirected edge.
        """
        # Use set to avoid counting duplicates in the same order twice.
        unique_ids = list(dict.fromkeys(pid for pid in product_id_list if pid))
        for a, b in combinations(unique_ids, 2):
            if a == b:
                continue
            self._ensure_node(a)
            self._ensure_node(b)
            self.graph[a][b] = self.graph[a].get(b, 0) + 1
            self.graph[b][a] = self.graph[b].get(a, 0) + 1

    def get_recommendations(self, product_id: str, num_recommendations: int = 5) -> List[str]:
        """Return top-N product_ids most strongly connected to product_id.

        Sort neighbors by descending edge weight, then by product_id for stability.
        """
        neighbors = self.graph.get(product_id, {})
        sorted_neighbors = sorted(neighbors.items(), key=lambda kv: (-kv[1], kv[0]))
        return [pid for pid, _ in sorted_neighbors[: max(0, int(num_recommendations))]]

    def to_dict(self) -> Dict[str, Dict[str, int]]:
        """Serialize the adjacency list graph to a JSON-friendly mapping."""
        # Ensure ints are plain ints (not numpy etc.)
        return {a: {b: int(w) for b, w in nbrs.items()} for a, nbrs in self.graph.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, Dict[str, int]]) -> "RecommendationEngine":
        eng = cls()
        for a, nbrs in data.items():
            eng.graph[a] = {b: int(w) for b, w in nbrs.items()}
        return eng
