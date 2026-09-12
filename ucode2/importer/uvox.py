"""Validator and importer for uCode uvox/1.0 and uvox/2.0 fixtures."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class UvoxCell:
    x: int
    y: int
    char: str
    layer: int = 0
    fg: int = 7
    bg: int = 0
    coord: str = ""


@dataclass
class UvoxManifest:
    format: str
    grid_id: str
    cols: int
    rows: int
    cells: List[UvoxCell]
    created_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def cell_at(self, x: int, y: int, layer: Optional[int] = None) -> Optional[UvoxCell]:
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                if layer is None or cell.layer == layer:
                    return cell
        return None


def validate_uvox(data: Dict[str, Any]) -> UvoxManifest:
    """Validate uvox dict structure and return typed manifest."""
    fmt = data.get("format", "")
    if not (fmt.startswith("uvox/1") or fmt.startswith("uvox/2")):
        raise ValueError(f"Unsupported uvox format: {fmt}. Expected uvox/1.0 or uvox/2.0")

    cols = int(data.get("cols", 0))
    rows = int(data.get("rows", 0))
    if cols <= 0 or rows <= 0:
        raise ValueError(f"Invalid grid dimensions: {cols}x{rows}")

    grid_id = str(data.get("gridId", data.get("grid_id", "default")))
    raw_cells = data.get("cells", [])
    if not isinstance(raw_cells, list):
        raise ValueError("Field 'cells' must be a list")

    parsed_cells: List[UvoxCell] = []
    for c in raw_cells:
        x = int(c.get("x", 0))
        y = int(c.get("y", 0))
        char = str(c.get("char", " "))
        layer = int(c.get("layer", 0))
        fg = int(c.get("fg", 7))
        bg = int(c.get("bg", 0))
        coord = str(c.get("coord", f"({x},{y})"))
        parsed_cells.append(UvoxCell(x=x, y=y, char=char, layer=layer, fg=fg, bg=bg, coord=coord))

    return UvoxManifest(
        format=fmt,
        grid_id=grid_id,
        cols=cols,
        rows=rows,
        cells=parsed_cells,
        created_at=str(data.get("createdAt", data.get("created_at", ""))),
        metadata=data.get("metadata", {}),
    )


def load_uvox_file(file_path: Path | str) -> UvoxManifest:
    """Load and validate an uvox JSON file from disk."""
    path = Path(file_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Uvox file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return validate_uvox(data)
