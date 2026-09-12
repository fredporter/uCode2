"""2D GridCore/NetHack to 3D Spatial Scene Voxel Lifter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from ..importer.uvox import UvoxManifest
from ..spatial.scene import SpatialScene, Voxel


@dataclass
class LifterConfig:
    wall_height: int = 3
    generate_ceiling: bool = False
    wall_block: str = "minecraft:stone_bricks"
    floor_block: str = "minecraft:smooth_stone"
    accent_block: str = "minecraft:mossy_stone_bricks"
    door_block: str = "minecraft:oak_door"
    stair_block: str = "minecraft:stone_brick_stairs"
    chest_block: str = "minecraft:chest"
    torch_frequency: int = 4  # Torch every N wall blocks


class VoxelLifter:
    """Lifts a 2D uCode/NetHack grid into a 3D SpatialScene."""

    def __init__(self, config: Optional[LifterConfig] = None):
        self.config = config or LifterConfig()

    def lift(self, manifest: UvoxManifest) -> SpatialScene:
        scene = SpatialScene(
            name=f"lifted_{manifest.grid_id}",
            width=manifest.cols,
            height=self.config.wall_height + 2,
            depth=manifest.rows,
        )

        wall_count = 0
        for cell in manifest.cells:
            x = cell.x
            z = cell.y  # 2D Y becomes 3D Z depth
            char = cell.char

            if char in ("#", "W"):  # Wall
                wall_count += 1
                # Foundation & wall column
                scene.add_voxel(Voxel(x=x, y=0, z=z, block_type="minecraft:bedrock"))
                for y in range(1, self.config.wall_height + 1):
                    block = (
                        self.config.accent_block
                        if (x + z + y) % 5 == 0
                        else self.config.wall_block
                    )
                    scene.add_voxel(Voxel(x=x, y=y, z=z, block_type=block))

                # Wall parapet / cap
                scene.add_voxel(
                    Voxel(
                        x=x,
                        y=self.config.wall_height + 1,
                        z=z,
                        block_type="minecraft:stone_brick_slab",
                        properties={"type": "bottom"},
                    )
                )

                # Periodic lighting torch
                if wall_count % self.config.torch_frequency == 0:
                    scene.add_voxel(
                        Voxel(
                            x=x,
                            y=self.config.wall_height,
                            z=z,
                            block_type="minecraft:lantern",
                            properties={"hanging": "false"},
                        )
                    )

            elif char in (".", " "):  # Open floor
                scene.add_voxel(Voxel(x=x, y=0, z=z, block_type=self.config.floor_block))
                if self.config.generate_ceiling:
                    scene.add_voxel(
                        Voxel(
                            x=x,
                            y=self.config.wall_height + 1,
                            z=z,
                            block_type="minecraft:stone_bricks",
                        )
                    )

            elif char == "+":  # Door
                # Threshold floor
                scene.add_voxel(Voxel(x=x, y=0, z=z, block_type="minecraft:polished_andesite"))
                # Lower & upper door halves
                scene.add_voxel(
                    Voxel(
                        x=x,
                        y=1,
                        z=z,
                        block_type=self.config.door_block,
                        properties={"half": "lower", "facing": "north"},
                    )
                )
                scene.add_voxel(
                    Voxel(
                        x=x,
                        y=2,
                        z=z,
                        block_type=self.config.door_block,
                        properties={"half": "upper", "facing": "north"},
                    )
                )
                # Lintel above door
                for y in range(3, self.config.wall_height + 1):
                    scene.add_voxel(Voxel(x=x, y=y, z=z, block_type=self.config.wall_block))

            elif char in ("<", ">"):  # Stairs (up or down)
                scene.add_voxel(Voxel(x=x, y=0, z=z, block_type=self.config.floor_block))
                scene.add_voxel(
                    Voxel(
                        x=x,
                        y=1,
                        z=z,
                        block_type=self.config.stair_block,
                        properties={"facing": "north", "half": "bottom"},
                    )
                )

            elif char in ("!", "$"):  # Item / Gold Chest
                scene.add_voxel(Voxel(x=x, y=0, z=z, block_type=self.config.floor_block))
                scene.add_voxel(
                    Voxel(
                        x=x,
                        y=1,
                        z=z,
                        block_type=self.config.chest_block,
                        properties={"facing": "south"},
                    )
                )

            elif char in ("m", "D"):  # Monster / Dragon
                scene.add_voxel(Voxel(x=x, y=0, z=z, block_type=self.config.floor_block))
                scene.add_voxel(
                    Voxel(
                        x=x,
                        y=1,
                        z=z,
                        block_type="minecraft:spawner",
                        metadata={"entity": "minecraft:zombie"},
                    )
                )

            elif char == "^":  # Trap
                scene.add_voxel(Voxel(x=x, y=0, z=z, block_type=self.config.floor_block))
                scene.add_voxel(
                    Voxel(
                        x=x,
                        y=1,
                        z=z,
                        block_type="minecraft:stone_pressure_plate",
                    )
                )

            elif char == "@":  # Player start spawn
                scene.add_voxel(Voxel(x=x, y=0, z=z, block_type="minecraft:gold_block"))

            else:
                # Fallback floor
                scene.add_voxel(Voxel(x=x, y=0, z=z, block_type=self.config.floor_block))

        return scene
