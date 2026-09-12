"""Golden tests for uCode 2 Voxel Lifter and Minecraft Datapack Exporter."""

import json
import tempfile
from pathlib import Path

import pytest

from ucode2.cli import main
from ucode2.exporter.minecraft import MinecraftExporter
from ucode2.importer.uvox import UvoxManifest, load_uvox_file, validate_uvox
from ucode2.lifter.voxel_lifter import LifterConfig, VoxelLifter
from ucode2.spatial.scene import SpatialScene, Voxel

FIXTURE_PATH = Path(__file__).resolve().parent.parent / "fixtures" / "nethack_floor.uvox.json"


def test_load_golden_uvox_fixture():
    manifest = load_uvox_file(FIXTURE_PATH)
    assert manifest.format == "uvox/2.0"
    assert manifest.grid_id == "nethack_floor_01"
    assert manifest.cols == 20
    assert manifest.rows == 15
    assert len(manifest.cells) == 300


def test_validate_uvox_invalid():
    with pytest.raises(ValueError, match="Unsupported uvox format"):
        validate_uvox({"format": "unknown/9.0", "cols": 10, "rows": 10, "cells": []})

    with pytest.raises(ValueError, match="Invalid grid dimensions"):
        validate_uvox({"format": "uvox/1.0", "cols": 0, "rows": 10, "cells": []})


def test_spatial_scene_model():
    scene = SpatialScene("test_scene")
    scene.add_voxel(Voxel(0, 0, 0, "minecraft:stone"))
    scene.add_voxel(Voxel(1, 2, 3, "minecraft:oak_door", properties={"half": "lower"}))

    assert scene.voxel_count == 2
    assert scene.width == 2
    assert scene.height == 3
    assert scene.depth == 4

    cmd = scene.get_voxel(1, 2, 3).to_command()
    assert cmd == "setblock ~1 ~2 ~3 minecraft:oak_door[half=lower]"

    palette = scene.palette_summary()
    assert palette["minecraft:stone"] == 1
    assert palette["minecraft:oak_door"] == 1


def test_voxel_lifter_rules():
    manifest = load_uvox_file(FIXTURE_PATH)
    config = LifterConfig(wall_height=3)
    lifter = VoxelLifter(config)
    scene = lifter.lift(manifest)

    assert scene.width == 20
    assert scene.depth == 15
    assert scene.height == 5  # y=0 to y=4
    assert scene.voxel_count > 1000

    palette = scene.palette_summary()
    # Must contain essential dungeon blocks
    assert "minecraft:stone_bricks" in palette
    assert "minecraft:smooth_stone" in palette
    assert "minecraft:oak_door" in palette
    assert "minecraft:chest" in palette
    assert "minecraft:stone_brick_stairs" in palette
    assert "minecraft:spawner" in palette
    assert "minecraft:gold_block" in palette


def test_minecraft_exporter():
    manifest = load_uvox_file(FIXTURE_PATH)
    lifter = VoxelLifter()
    scene = lifter.lift(manifest)
    exporter = MinecraftExporter(scene)

    with tempfile.TemporaryDirectory() as tmp_dir:
        report = exporter.export(tmp_dir)
        out_path = Path(tmp_dir)

        assert report["status"] == "COMPATIBLE"
        assert report["total_voxels"] == scene.voxel_count
        assert (out_path / "pack.mcmeta").is_file()
        assert (out_path / "structure.json").is_file()
        assert (out_path / "compatibility_report.json").is_file()
        
        mcfunction = out_path / "data" / "ucode2" / "function" / "build_floor.mcfunction"
        assert mcfunction.is_file()
        lines = mcfunction.read_text(encoding="utf-8").splitlines()
        assert len(lines) > 1000
        assert lines[0].startswith("# uCode 2 Voxel Lifter")
        assert any("setblock" in line for line in lines)


def test_cli_lift_end_to_end():
    with tempfile.TemporaryDirectory() as tmp_dir:
        code = main([
            "lift",
            "--fixture", str(FIXTURE_PATH),
            "--out", tmp_dir,
        ])
        assert code == 0
        assert (Path(tmp_dir) / "compatibility_report.json").is_file()
        assert (Path(tmp_dir) / "pack.mcmeta").is_file()
