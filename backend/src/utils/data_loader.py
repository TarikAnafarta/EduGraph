# -*- coding: utf-8 -*-
"""
Data loading utilities for curriculum data.
"""

import json
from pathlib import Path
from typing import List, Dict, Any


def load_curriculum_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Load curriculum data from JSON file.
    Accepts both dict with key "Matematik Kazanımları" or plain list.
    """
    raw_data = json.loads(Path(file_path).read_text(encoding="utf-8"))

    if isinstance(raw_data, dict) and "Matematik Kazanımları" in raw_data:
        return raw_data["Matematik Kazanımları"]

    return raw_data if isinstance(raw_data, list) else []


def validate_record(record: Dict[str, Any]) -> bool:
    """Validate if a record has the required fields."""
    return bool(record.get("id"))
