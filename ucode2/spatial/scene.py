"""Renderer-neutral 3D spatial scene model."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Voxel:
    x: int
    y: int  # Vertical elevation
    z: int
    block_type: str
    properties: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_command(self, rel_x: int = 0, rel_y: int = 0, rel_z: int = 0) -> str:
        """Render standard Minecraft /setblock command."""
        props = ""
        if self.properties:
            prop_str = ",".join(f"{k}={v}" for k, v in sorted(self.properties.items()))
            props = f"[{prop_str}]"
        
        target_x = f"~{self.x + rel_x}" if (self.x + rel_x) != 0 else "~"
        target_y = f"~{self.y + rel_y}" if (self.y + rel_y) != 0 else "~"
        target_z = f"~{self.z + rel_z}" if (self.z + rel_z) != 0 else "~"
        return f"setblock {target_x} {target_y} {target_z} {self.block_type}{props}"


class SpatialScene:
    """Discrete 3D voxel scene representing a lifted structure."""

    def __init__(self, name: str, width: int = 0, height: int = 0, depth: int = 0):
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self._voxels: Dict[Tuple[int, int, int], Voxel] = {}

    def add_voxel(self, voxel: Voxel) -> None:
        self._voxels[(voxel.x, voxel.y, voxel.z)] = voxel
        if voxel.x >= self.width:
            self.width = voxel.x + 1
        if voxel.y >= self.height:
            self.height = voxel.y + 1
        if voxel.z >= self.depth:
            self.depth = voxel.z + 1

    def get_voxel(self, x: int, y: int, z: int) -> Optional[Voxel]:
        return self._voxels.get((x, y, z))

    def remove_voxel(self, x: int, y: int, z: int) -> Optional[Voxel]:
        return self._voxels.pop((x, y, z), None)

    @property
    def voxel_count(self) -> int:
        return len(self._voxels)

    def list_voxels(self) -> List[Voxel]:
        return sorted(self._voxels.values(), key=lambda v: (v.y, v.z, v.x))

    def palette_summary(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for v in self._voxels.values():
            counts[v.block_type] = counts.get(v.block_type, 0) + 1
        return dict(sorted(counts.items(), key=lambda item: -item[1]))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "dimensions": {
                "width": self.width,
                "height": self.height,
                "depth": self.depth,
            },
            "total_voxels": self.voxel_count,
            "palette": self.palette_summary(),
            "voxels": [
                {
                    "x": v.x,
                    "y": v.y,
                    "z": v.z,
                    "block": v.block_type,
                    "properties": v.properties,
                }
                for v in self.list_voxels()
            ],
        }
