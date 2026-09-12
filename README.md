# uCode 2: Spatial Interpretation & Minecraft Voxel Lifter

**uCode 2** is the spatial and 3D interpretation engine of the uDos ecosystem. It ingests stable, 2D uCode 1 artifacts (`uvox`, GridCore matrices, NetHack dungeon floors) and lifts them into neutral 3D spatial scenes, emitting Minecraft structures and datapacks.

---

## Architectural Boundary

- **uCode 1**: Strictly 2D. Owns BBC BASIC, GridCore surfaces, Mode 7 teletext, and native Capsule Pods.
- **uCode 2**: The spatial and 3D lifter boundary. Converts 2D grid worlds into 3D voxel representations and Minecraft datapacks.
- **HomeNest**: Media player, TV, voice, HomeKit, and household automation belong strictly in HomeNest.

---

## Quick Start: Voxel Lifter CLI

```bash
# Lift a 2D NetHack / GridCore floor into a Minecraft datapack
python3 -m ucode2.cli lift \
  --fixture fixtures/nethack_floor.uvox.json \
  --out dist/minecraft_datapack \
  --format datapack
```

This generates:
- `pack.mcmeta`: Datapack metadata for modern Minecraft (1.20+ / pack_format 48).
- `data/ucode2/function/build_floor.mcfunction`: Sequenced `/setblock` commands placing walls, floors, doors, stairs, chests, and lighting.
- `structure.json`: Spatial 3D scene representation.
- `compatibility_report.json`: Verification report detailing source cells, voxel count, and block palette breakdown.
