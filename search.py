"""
search.py

ProductSearch implemented as a Trie (prefix tree) for fast prefix-based
search/autocomplete on product names.

- Each TrieNode stores edges to child characters and a set of product_ids
  that complete at that node.
- We store product_ids as a set to avoid duplicates.

Complexity:
- Building/inserting a name of length L: O(L)
- Searching a prefix of length P: O(P) to reach the subtrie, then we collect
  all product_ids in that subtrie. For large trees, this can be bounded by
  the number of matches.
"""
from __future__ import annotations
from typing import Dict, Set, List


class TrieNode:
    def __init__(self) -> None:
        # Hash table: char -> TrieNode for O(1) child lookup by character
        self.children: Dict[str, TrieNode] = {}
        # Set of product IDs that end at this node (full name match)
        self.product_ids: Set[str] = set()


class ProductSearch:
    def __init__(self) -> None:
        self.root = TrieNode()

    @staticmethod
    def _normalize(text: str) -> str:
        """Normalize names/prefixes to ensure consistent trie traversal."""
        return text.strip().lower()

    def add_product_to_trie(self, name: str, product_id: str) -> None:
        """Insert a product name into the trie.

        We treat the name as a sequence of characters (including spaces). This
        mirrors common autocomplete behavior for multi-word names.
        """
        node = self.root
        for ch in self._normalize(name):
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.product_ids.add(product_id)

    def _collect_all_products(self, node: TrieNode, out: Set[str]) -> None:
        """DFS to accumulate all product_ids in the subtrie rooted at node."""
        out.update(node.product_ids)
        for child in node.children.values():
            self._collect_all_products(child, out)

    def search_by_prefix(self, prefix: str) -> List[str]:
        """Return all product_ids whose names start with the given prefix."""
        node = self.root
        for ch in self._normalize(prefix):
            if ch not in node.children:
                return []
            node = node.children[ch]
        results: Set[str] = set()
        self._collect_all_products(node, results)
        # Return a stable order: lexicographically sort the IDs
        return sorted(results)

    def remove_product_from_trie(self, name: str, product_id: str) -> None:
        """Optional helper to remove a product_id from a name's terminal node.
        This is not strictly required for the project, but helps keep the
        trie tidy if products are deleted.
        """
        path = []
        node = self.root
        for ch in self._normalize(name):
            if ch not in node.children:
                return  # name not present
            path.append((node, ch))
            node = node.children[ch]
        node.product_ids.discard(product_id)
        # Optional pruning of empty branches
        for parent, ch in reversed(path):
            child = parent.children[ch]
            if child.product_ids or child.children:
                break
            del parent.children[ch]
