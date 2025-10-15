# -*- coding: utf-8 -*-
"""
Graph processing utilities for creating nodes and links from curriculum data.
"""

from typing import List, Dict, Any, Tuple
from .colors import score_to_color, TYPE_COLORS, TYPE_BASE_RADIUS, clamp01
from .text import esc, trim_label


class GraphProcessor:
    """Processes curriculum data into graph nodes and links."""

    def __init__(self):
        self.nodes: List[Dict[str, Any]] = []
        self.links: List[Dict[str, Any]] = []
        self._id_to_node: Dict[Any, Dict[str, Any]] = {}

    def process_records(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict], List[Dict]]:
        self.nodes = []
        self.links = []
        self._id_to_node = {}
        self._create_nodes(records)
        self._create_links(records)
        return self.nodes, self.links

    def _create_nodes(self, records: List[Dict[str, Any]]) -> None:
        for rec in records:
            node = self._create_node(rec)
            if node is not None:
                self._id_to_node[node["id"]] = node
                self.nodes.append(node)

    def _create_node(self, record: Dict[str, Any]) -> Dict[str, Any] | None:
        node_id = record.get("id")
        if not node_id:
            return None
        node_type = record.get("node_type") or record.get("type") or "kazanım"
        node_size = record.get("node_size")
        base_r = TYPE_BASE_RADIUS.get(node_type, 10)

        # radius boosts for hierarchy and performance
        if node_type == "kazanım":
            perf = clamp01(record.get("basari_puani") or 0.0)
            r = max(8, int(base_r + perf * 10))
            color = score_to_color(perf)
        else:
            r = base_r + (int(node_size) if isinstance(node_size, int) else 0)
            color = TYPE_COLORS.get(node_type) or "#90a4ae"

        kod = record.get("kazanim_kodu") or ""
        baslik = record.get("baslik") or ""
        konu = record.get("konu") or ""
        sinif = record.get("sinif")
        test = record.get("test") or ""
        basari = record.get("basari_puani") or 0.0

        label = self._create_label(node_type, baslik, kod, node_id)
        title = self._create_tooltip(baslik, kod, konu, sinif, test, basari, node_type)

        return {
            "id": node_id,
            "type": node_type,
            "r": int(r),
            "color": color,
            "label": label,
            "title": title,
        }

    def _create_label(self, node_type: str, baslik: str, kod: str, node_id: Any) -> str:
        if node_type in ("konu", "grup", "alt_grup"):
            return trim_label(esc(baslik or kod or str(node_id)), 40)
        # kazanım nodes usually shorter label
        return trim_label(esc(baslik or kod or str(node_id)), 24)

    def _create_tooltip(self, baslik: str, kod: str, konu: str, sinif: Any,
                        test: str, basari: float, node_type: str) -> str:
        items = []
        if baslik:
            items.append(f"<b>{esc(baslik)}</b>")
        if kod:
            items.append(f"<div>Kod: {esc(kod)}</div>")
        if konu:
            items.append(f"<div>Konu: {esc(konu)}</div>")
        if sinif not in (None, ""):
            items.append(f"<div>Sınıf: {esc(sinif)}</div>")
        if test:
            items.append(f"<div>Test: {esc(test)}</div>")
        if node_type == "kazanım":
            items.append(f"<div>Başarı: {int(clamp01(basari)*100)}%</div>")
        return "".join(items) or esc(baslik or kod)

    def _create_links(self, records: List[Dict[str, Any]]) -> None:
        for rec in records:
            child_id = rec.get("id")
            parent_id = rec.get("parent_id")
            if child_id and parent_id and child_id in self._id_to_node and parent_id in self._id_to_node:
                self.links.append({"source": parent_id, "target": child_id})



def create_graph_data(records: List[Dict[str, Any]]) -> Tuple[List[Dict], List[Dict]]:
    return GraphProcessor().process_records(records)
