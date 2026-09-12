"""uCode 2 Command Line Interface — Voxel Lifter Demonstrator."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .exporter.minecraft import MinecraftExporter
from .importer.uvox import load_uvox_file
from .lifter.voxel_lifter import LifterConfig, VoxelLifter


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ucode2",
        description="uCode 2 Spatial Engine — 2D GridCore to 3D Minecraft Voxel Lifter",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    lift_parser = subparsers.add_parser(
        "lift",
        help="Lift a 2D GridCore/NetHack uvox fixture into a 3D Minecraft datapack",
    )
    lift_parser.add_argument(
        "--fixture",
        "-f",
        type=str,
        required=True,
        help="Path to the input uvox JSON file (e.g. fixtures/nethack_floor.uvox.json)",
    )
    lift_parser.add_argument(
        "--out",
        "-o",
        type=str,
        default="dist/minecraft_datapack",
        help="Output directory for the Minecraft datapack (default: dist/minecraft_datapack)",
    )
    lift_parser.add_argument(
        "--wall-height",
        type=int,
        default=3,
        help="Height of lifted wall columns in blocks (default: 3)",
    )
    lift_parser.add_argument(
        "--ceiling",
        action="store_true",
        help="Generate closed ceiling over open floor tiles",
    )
    lift_parser.add_argument(
        "--json",
        action="store_true",
        help="Emit compatibility report as raw JSON to stdout",
    )

    return parser


def run_lift(args: argparse.Namespace) -> int:
    fixture_path = Path(args.fixture).resolve()
    if not fixture_path.exists():
        print(f"Error: Fixture file not found at {fixture_path}", file=sys.stderr)
        return 1

    try:
        manifest = load_uvox_file(fixture_path)
    except Exception as exc:
        print(f"Error validating uvox manifest: {exc}", file=sys.stderr)
        return 1

    config = LifterConfig(
        wall_height=args.wall_height,
        generate_ceiling=args.ceiling,
    )
    lifter = VoxelLifter(config)
    scene = lifter.lift(manifest)

    exporter = MinecraftExporter(scene)
    report = exporter.export(args.out)

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print("================================================================")
    print("           uCode 2 — 3D Spatial Voxel Lifter Demonstrator       ")
    print("================================================================")
    print(f"  Source Fixture:     {fixture_path.name} ({manifest.cols}x{manifest.rows}, {len(manifest.cells)} cells)")
    print(f"  Lifted Scene:       {scene.name}")
    print(f"  3D Dimensions:      {scene.width}W x {scene.height}H x {scene.depth}D (blocks)")
    print(f"  Total Voxels:       {scene.voxel_count}")
    print(f"  Output Directory:   {Path(args.out).resolve()}")
    print("----------------------------------------------------------------")
    print("  Block Palette Distribution:")
    for block, count in report["palette"].items():
        print(f"    - {block:<35} : {count:>5}")
    print("----------------------------------------------------------------")
    print(f"  Status:             {report['status']}")
    print(f"  Minecraft Target:   {report['target']}")
    print(f"  MCFunction Lines:   {report['total_commands']}")
    print("================================================================")
    print("Datapack generated successfully. Run `/function ucode2:build_floor` in Minecraft.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)
    if args.command == "lift":
        return run_lift(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
