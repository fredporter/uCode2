---
title: "uCode2+ Minecraft Bridge & 2D-to-3D Lift — Planning Notes"
status: planning
last_updated: 2026-08-14T00:00:00+10:00
category: planning
tags: [ucode2, minecraft, 3d, uvox, lift]
description: "Notated roadmap for the uCode -> uCode2 3D/Minecraft bridge. No implementation has started; these items live outside the base uCode runtime/display sprints."
---
# uCode2+ Minecraft Bridge — Planning Notes

> **Architecture authority (2026-08-20):** uCode 1 is the compatible 2D
> BBCSDL-based runtime and includes sprites/BOBs, capsules, LENS, and SKIN.
> uCode 2 begins with experimental 3D/spatial lifting. See
> `uCode/docs/UCODE_ARCHITECTURE.md` and
> `uCode/docs/UCODE_DELIVERY_SPRINTS_2026.md`. Earlier uCode3/uCode4 naming is
> historical and is not an additional product generation.

> **Status:** Planning only. Not scheduled in the uCode runtime/display sprint
> series. These items belong to the uCode2+ (3D/spatial) extension layer and are
> notated here so they are not lost.

## Source of record

The base **uCode** repo (`~/Code/uCode`) is advancing through a sprint series to
deliver a fully working runtime + GridCore/display system (Terminal & Teletext
display modes; Pixel, Grid, Layer editing tabs). uCode's clean exit point for
this bridge is a frozen lattice-first **`uvox/2` export**. The existing
GridSmith `uvox/1.0` exporter is an implemented compatibility seed, not the
complete or frozen handoff.

This document notates the uCode2+ work that consumes `.uvox` and lifts it into
3D / Minecraft.

## The clean handoff

```
uCode 1 (compatible 2D runtime) -- uvox/2 + semantic state --> uCode 2 (experimental 3D/spatial)
```

- uCode 1 writes `uvox/2` (lattice/register metadata, layers, cells,
  sprites/BOBs, interaction regions, geographic data, assets, provenance, and
  references to declarative behavior/state).
- uCode2 reads `.uvox`, lifts 2D -> 3D, and emits Minecraft assets.
- uCode 1 executes BBC BASIC/AMOS-compatible programs. uCode 2 consumes
  exported semantic behavior; it does not translate arbitrary BASIC source.

## uCode2+ scope (to be planned into future sprints)

### 2D -> 3D lift mechanics
- Grid cell -> block (tile mapping): `@` -> stone, `#` -> cobblestone, `~` ->
  water, solid char -> wall, space -> air, teletext block -> stained glass.
- Layer -> depth (z-axis): terrain Y=0-5, details Y=6-10, foreground Y=11-50,
  lighting -> light level, collision -> solid state, entities -> spawners.
- Teletext page -> lore (book and quill / signs); hold mode -> quest tracking;
  flash mode -> warning messages.
- Supported declarative behavior -> datapack functions, commands, entities, or
  mod code; unsupported behavior produces a compatibility report.
- Geographic coords -> biome / dimension mapping.

### Export targets
- Minecraft Forge mod, Fabric mod, datapack, Craftics arena, WorldEdit
  schematic, Spigot/Bukkit plugin.

### Mod architecture (uCodeWorlds)
- world_loader (reads .uvox), block_mapper (cell -> block + palettes),
  lore_importer (teletext -> books), game_logic (BASIC -> command blocks),
  geographic_bridge (uCode coords -> Minecraft coords).

## Open questions to resolve before scheduling
- Heightmap algorithm selection (terrain/foreground/collision layers as source).
- Block mapping rules + palette definitions.
- Whether to target datapacks first (lowest barrier) or Forge/Fabric mods.
- Craftics API-hook integration specifics.

## Dependencies
- uCode `uvox/2` and semantic-state formats must be frozen before uCode2 import
  work starts; version 1 remains readable through an explicit migration.
- GridCore shared foundation (the canonical Cell model) must be stable first.
