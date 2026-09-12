# uCode 2 Reset and Rescaffold Plan

**Status:** Canonical clean-restart plan  
**Date:** 2026-08-20

## Identity

uCode 2 is the second and only additional uCode generation. It experiments
with spatial and 3D interpretations of stable uCode 1 artifacts, beginning
with Minecraft-oriented lifting and extending to future 3D products.

uCode 2 is not ProseUI, a media server, HomeNest, or a renamed uCode3/uCode4.
Earlier documents and packages using those identities are research inputs.

## Current-tree policy

The existing `multimedia/` tree contains useful concepts and exploratory code:

- Three.js scene and camera experiments;
- world, scene, spatial, portal, and persistence vocabulary;
- controller/layback interaction concepts;
- wireframe themes;
- geographic and device mapping ideas;
- Minecraft lifting notes.

None of its Python, Rust, JavaScript, package metadata, runtime boundaries, or
tests are considered production foundations. uCode 2 will restart from a clean
scaffold after the uCode 1 handoff contracts are frozen. Existing code is
preserved as reference and may be selectively ported only after its behavior is
understood and covered by new tests.

Media-server/player, household automation, voice, TV, kiosk, and HomeKit work
belongs to the separate HomeNest project. Concepts may be referenced, but code
must not be copied into uCode 2 without a new ownership decision.

## Entry criteria

Implementation begins only after uCode 1 freezes:

- lattice-first `uvox/2`;
- semantic runtime-state/behavior contracts;
- asset and provenance manifests;
- Software Library/Runtime Capsule identity and versioning;
- at least one compatibility-tested uCode 1 vertical slice.

## Rescaffold sequence

1. Quarantine the existing `multimedia/` tree as a legacy reference and
   inventory every module as `retain-concept`, `candidate-code`,
   `HomeNest-owned`, `obsolete-name`, or `discard-after-review`.
2. Write the uCode 2 package boundaries and dependency direction.
3. Create a clean workspace beside, not inside, the legacy `ucode4` package.
4. Implement an `uvox/2` validator/importer with golden fixtures.
5. Implement a renderer-neutral spatial scene model.
6. Build one 2D-to-3D lift demonstrator.
7. Target Minecraft datapacks first; add schematics or mods only when needed.
8. Re-evaluate legacy Three.js, spatial, portal, controller, and theme code
   module by module. Port behavior with tests rather than renaming directories.

## Non-goals for the reset

- No HomeNest/media-server implementation.
- No uCode3 or uCode4 compatibility naming.
- No direct BBC BASIC/AMOS execution.
- No dependency on uCore UI implementation details.
- No promise that arbitrary BASIC logic converts automatically to Minecraft.
- No reuse of generated artifacts, caches, or installed package metadata as
  source.

## First deliverable

A command-line proof that validates a frozen uCode 1 `uvox/2` fixture, lifts
its terrain/layer/entity data into a neutral spatial scene, and emits a small
Minecraft datapack or structure-oriented artifact with a compatibility report.
