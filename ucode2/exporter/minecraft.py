"""Minecraft Datapack and Structure Exporter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from ..spatial.scene import SpatialScene


class MinecraftExporter:
    """Exports a SpatialScene to a modern Minecraft Datapack and structure artifacts."""

    def __init__(self, scene: SpatialScene):
        self.scene = scene

    def export(self, output_dir: Path | str) -> Dict[str, Any]:
        out = Path(output_dir).resolve()
        out.mkdir(parents=True, exist_ok=True)

        # 1. pack.mcmeta
        pack_mcmeta = {
            "pack": {
                "pack_format": 48,
                "description": f"uCode 2 Voxel Lifter — {self.scene.name}",
            }
        }
        (out / "pack.mcmeta").write_text(json.dumps(pack_mcmeta, indent=2), encoding="utf-8")

        # 2. Datapack function directory
        func_dir = out / "data" / "ucode2" / "function"
        func_dir.mkdir(parents=True, exist_ok=True)

        commands = [
            f"# uCode 2 Voxel Lifter — {self.scene.name}",
            f"# Dimensions: {self.scene.width}x{self.scene.height}x{self.scene.depth}, Voxels: {self.scene.voxel_count}",
            'tellraw @a [{"text":"[uCode 2] ","color":"gold","bold":true},{"text":"Generating lifted dungeon...","color":"yellow"}]',
        ]

        # Order voxels: bottom to top (Y), then Z, then X
        voxels = self.scene.list_voxels()
        for v in voxels:
            commands.append(v.to_command())

        commands.append(
            'tellraw @a [{"text":"[uCode 2] ","color":"gold","bold":true},{"text":"Dungeon floor construction complete!","color":"green"}]'
        )

        mcfunction_path = func_dir / "build_floor.mcfunction"
        mcfunction_path.write_text("\n".join(commands) + "\n", encoding="utf-8")

        # 3. Structure definition JSON
        scene_dict = self.scene.to_dict()
        structure_path = out / "structure.json"
        structure_path.write_text(json.dumps(scene_dict, indent=2), encoding="utf-8")

        # 4. Compatibility Report
        report = {
            "status": "COMPATIBLE",
            "scene_name": self.scene.name,
            "target": "Minecraft 1.20+ / Datapack pack_format 48",
            "dimensions": {
                "x_width": self.scene.width,
                "y_height": self.scene.height,
                "z_depth": self.scene.depth,
            },
            "total_voxels": self.scene.voxel_count,
            "total_commands": len(commands),
            "palette": self.scene.palette_summary(),
            "artifacts": [
                "pack.mcmeta",
                "data/ucode2/function/build_floor.mcfunction",
                "structure.json",
                "compatibility_report.json",
            ],
        }
        report_path = out / "compatibility_report.json"
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

        return report
