---
name: pylabrobot-vendor-agnostic
description: "PyLabRobot hardware-agnostic Python liquid-handler library for Hamilton STAR, Tecan Freedom EVO, Opentrons OT-2, and simulator. Write protocols once, run on any robot. Async-first API. Plate reformatting, cherry-picking, serial dilutions. Use for vendor-agnostic workflows; use opentrons-ot2-protocols for Opentrons-only features."
license: MIT
---



<!-- metadata:
category: ''
version: 1.0.0
author: Pradyumna Jayaram
tags: []
difficulty: beginner
sources: SciAgent-Skills-main/skills/lab-automation/pylabrobot/SKILL.md
-->

# PyLabRobot Vendor-Agnostic Liquid Handling

## Overview

PyLabRobot is an open-source Python library that provides a unified API for liquid handling robots from multiple vendors. Write a protocol once and run it on Hamilton STAR, Tecan Freedom EVO, Opentrons OT-2, or a simulated backend without changing the protocol code. The library handles deck layout, resource management, pipette operations, and aspirate/dispense workflows through a clean, async-first interface. This enables portable wet-lab automation across shared facilities, core labs with multiple robot brands, and workflows that need to switch robots due to availability.

Author: Pradyumna Jayaram.

## When to Use

- Writing portable liquid-handling protocols that run on Hamilton, Tecan, or Opentrons without code changes
- Developing and testing protocols in simulation before booking hardware
- Plate reformatting and cherry-picking from lists or hit files
- Building serial dilution curves over 96- or 384-well plates
- Integrating liquid handling into Python data pipelines (analysis → robot → ELN)
- Rapid method development in Python rather than vendor scripting GUIs
- For Opentrons-specific features (temperature module, heater-shaker, thermocycler), use `opentrons-ot2-protocols` instead
- For simpler single-vendor deployment (just OT-2), PyLabRobot provides fewer built-in modules than the native Opentrons API

## Prerequisites

- **Python packages**: `pylabrobot`
- **Optional robot backends**: `pylabrobot[hamilton]`, `pylabrobot[opentrons]`, `pylabrobot[tecan]`
- **Python**: 3.9+
- **Hardware drivers**: Installed separately per vendor's instructions
- **Simulator**: Built-in via `SimulatorBackend` for development without hardware

```bash
pip install pylabrobot"
pip install "pylabrobot[hamilton]"   # Hamilton STAR driver
pip install "pylabrobot[opentrons]"  # Opentrons OT-2 driver  
pip install "pylabrobot[tecan]"      # Tecan Freedom EVO driver
```

## Quick Start

```python
import asyncio
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import SimulatorBackend
from pylabrobot.resources import Deck, Cos_96_Rd, HTF_L

async def main():
    # Initialize simulator backend
    backend = SimulatorBackend(open_browser=False)
    lh = LiquidHandler(backend=backend, deck=Deck())
    await lh.setup()

    # Assign deck resources
    plate = Cos_96_Rd(name="plate")
    tips  = HTF_L(name="tips")
    lh.deck.assign_child_resource(plate, rails=2)
    lh.deck.assign_child_resource(tips,  rails=5)

    # Simple liquid transfer
    await lh.pick_up_tips(tips["A1"])
    await lh.aspirate(plate["A1"], vols=50)
    await lh.dispense(plate["B1"], vols=50)
    await lh.drop_tips(tips["A1"])

    await lh.stop()
    print("Transfer complete: 50 µL from A1 -> B1")

asyncio.run(main())
```

## Core API

### Module 1: LiquidHandler — Setup and Backend Selection

```python
import asyncio
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import SimulatorBackend
from pylabrobot.resources import Deck

async def sim_workflow():
    # Simulator for protocol development
    backend = SimulatorBackend(open_browser=False)
    lh = LiquidHandler(backend=backend, deck=Deck())
    await lh.setup()
    # Run protocol
    await lh.stop()

asyncio.run(sim_workflow())
```

```python
import asyncio
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.hamilton import STAR
from pylabrobot.resources import Deck

async def hamilton_workflow():
    backend = STAR()
    lh = LiquidHandler(backend=backend, deck=Deck())
    await lh.setup()
    # Run protocol on Hamilton STAR
    await lh.stop()

# asyncio.run(hamilton_workflow())
```

```python
import asyncio
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends.opentrons import OT2
from pylabrobot.resources import Deck

async def opentrons_workflow():
    backend = OT2(host="192.168.1.101")
    lh = LiquidHandler(backend=backend, deck=Deck())
    await lh.setup()
    # Run protocol on Opentrons OT-2
    await lh.stop()

# asyncio.run(opentrons_workflow())
```

### Module 2: Deck and Resource Assignment

Resources (plates, tip racks, reservoirs) are assigned to deck positions (rails). Different robot types have different slot layouts; the `rails` parameter maps to each robot's physical slots.

```python
from pylabrobot.resources import (
    Deck,
    Cos_96_Rd,     # Corning 96-well round-bottom
    Cos_384_Sq,    # Corning 384-well square-bottom
    HTF_L,         # Hamilton tip rack (filtered, large)
    Trough_1_Row_1_Col_4,
)

deck = Deck()

# Assign resources to rails (robot-specific mapping handled by backend)
plate_96  = Cos_96_Rd(name="sample_plate")
plate_384 = Cos_384_Sq(name="assay_plate")
tips      = HTF_L(name="tip_rack")
reservoir = Trough_1_Row_1_Col_4(name="buffer")

# Rail positions (1-indexed, robot-specific)
deck.assign_child_resource(plate_96,  rails=1)
deck.assign_child_resource(plate_384, rails=4)
deck.assign_child_resource(tips,      rails=8)
deck.assign_child_resource(reservoir, rails=11)

print("Deck resources:", [r.name for r in deck.children])
```

### Module 3: Tip Operations

```python
# Pick up tips from the tip rack
await lh.pick_up_tips(tips["A1:H1"])   # all 8 tips in column 1 (96-channel mode)
await lh.pick_up_tips(tips["A1"])        # single tip
await lh.drop_tips()                    # drop all tips

# Multi-channel: pick from column
await lh.pick_up_tips(tips["A1:H1"])   # 8 tips at once
# For single-channel: pick one at a time
for well in ["A1", "B1", "C1"]:
    await lh.pick_up_tips(tips[well])
    await lh.drop_tips(tips[well])
```

### Module 4: Aspirate and Dispense

```python
import asyncio
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import SimulatorBackend
from pylabrobot.resources import Deck, Cos_96_Rd, HTF_L

async def aspirate_dispense():
    backend = SimulatorBackend(open_browser=False)
    lh = LiquidHandler(backend=backend, deck=Deck())
    await lh.setup()
    plate = Cos_96_Rd(name="plate")
    tips  = HTF_L(name="tips")
    lh.deck.assign_child_resource(plate, rails=1)
    lh.deck.assign_child_resource(tips,  rails=5)

    await lh.pick_up_tips(tips["A1"])

    # Single-well aspirate
    await lh.aspirate(plate["A1"], vols=100)

    # Multi-well with different volumes
    await lh.aspirate(plate["A1:A4"], vols=[50, 75, 100, 125])

    # Dispense with similar patterns
    await lh.dispense(plate["B1"], vols=100)
    await lh.dispense(plate["B1:B4"], vols=[50, 75, 100, 125])

    await lh.drop_tips()
    await lh.stop()

asyncio.run(aspirate_dispense())
```

### Module 5: Transfer — High-Level Convenience

`transfer()` combines aspirate and dispense in one call.

```python
# Simple transfer
await lh.transfer(plate["A1"], plate["B1"], transfer_volume=50)

# Multi-well pairwise
Await lh.transfer(
    plate["A1:A8"],
    plate["B1:B8"],
    transfer_volume=75
)
```

### Module 6: Coordinate and Well Notation

```python
from pylabrobot.resources import Coordinate

# Aspirate from a specific height above the well bottom
await lh.aspirate(
    plate["A1"],
    vols=50,
    flow_rates=100,
    offsets=Coordinate(0, 0, 1),   # 1 mm above bottom
)

# Access wells by name
well_a1 = plate["A1"]
col1 = plate["A1:H1"]       # 8 wells in column 1
row_a = plate["A1:A12"]      # 12 wells in row A
```

## Key Concepts

### Async-first Design

All robot operations are async coroutines (`async def`, `await`). Run them via `asyncio.run(main())` or use Jupyter's top-level `await` support. This enables non-blocking operations on real hardware.

### Backend Abstraction

The same protocol code runs unchanged on any supported backend:
- `SimulatorBackend` — browser-based visualizer for testing
- `STAR` — Hamilton STAR driver
- `OT2` — Opentrons OT-2 driver
- `Tecan` — Tecan Freedom EVO driver

The backend abstraction means only the initialization changes; the protocol stays the same.

### Well Notation

Wells are addressed by alphanumeric position (`"A1"`) or slice notation (`"A1:H1"` for column 1, `"A1:A12"` for row A).

## Common Workflows

### Workflow 1: 96-Well Serial Dilution

```python
import asyncio
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import SimulatorBackend
from pylabrobot.resources import Deck, Cos_96_Rd, HTF_L, Trough_1_Row_1_Col_4

async def serial_dilution():
    backend = SimulatorBackend(open_browser=False)
    lh = LiquidHandler(backend=backend, deck=Deck())
    await lh.setup()

    plate   = Cos_96_Rd(name="plate")
    tips    = HTF_L(name="tips")
    diluent = Trough_1_Row_1_Col_4(name="diluent")
    lh.deck.assign_child_resource(plate,   rails=1)
    lh.deck.assign_child_resource(tips,    rails=5)
    lh.deck.assign_child_resource(diluent, rails=9)

    # Add diluent to columns 2-12
    for col in range(2, 13):
        col_label = f"A{col}:H{col}"
        await lh.pick_up_tips(tips[f"A{col}:H{col}"])
        await lh.aspirate(diluent["A1:H1"], vols=100)
        await lh.dispense(plate[col_label], vols=100)
        await lh.drop_tips(tips[f"A{col}:H{col}"])

    # Serial transfer: col 1 -> 2 -> ... -> 11
    for col in range(1, 12):
        src = f"A{col}:H{col}"
        dst = f"A{col+1}:H{col+1}"
        await lh.pick_up_tips(tips[f"A{col}:H{col}"])
        await lh.aspirate(plate[src], vols=100)
        await lh.dispense(plate[dst], vols=100)
        await lh.drop_tips(tips[f"A{col}:H{col}"])

    print("Serial dilution complete: 12 columns, 2-fold steps")
    await lh.stop()

asyncio.run(serial_dilution())
```

### Workflow 2: Cherry-Picking from a Hit List

```python
import asyncio
import pandas as pd
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import SimulatorBackend
from pylabrobot.resources import Deck, Cos_96_Rd, HTF_L

async def cherry_pick(hit_list_csv: str, volume: float = 50.0):
    # CSV must have columns: source_well, dest_well
    hits = pd.read_csv(hit_list_csv)
    print(f"Cherry-picking {len(hits)} hits at {volume} µL each")

    backend = SimulatorBackend(open_browser=False)
    lh = LiquidHandler(backend=backend, deck=Deck())
    await lh.setup()

    src  = Cos_96_Rd(name="source")
    dst  = Cos_96_Rd(name="destination")
    tips = HTF_L(name="tips")
    lh.deck.assign_child_resource(src,  rails=1)
    lh.deck.assign_child_resource(dst,  rails=4)
    lh.deck.assign_child_resource(tips, rails=8)

    tip_wells = [w.name for w in tips.wells()]
    for i, row in hits.iterrows():
        await lh.pick_up_tips(tips[tip_wells[i]])
        await lh.transfer(src[row["source_well"]], dst[row["dest_well"]],
                          transfer_volume=volume)
        await lh.drop_tips(tips[tip_wells[i]])

    print(f"Cherry-pick complete: {len(hits)} transfers done")
    await lh.stop()

# asyncio.run(cherry_pick("hits.csv", volume=50))
```

### Workflow 3: Plate Stamping (Copy Entire Plate)

```python
import asyncio
from pylabrobot.liquid_handling import LiquidHandler
from pylabrobot.liquid_handling.backends import SimulatorBackend
from pylabrobot.resources import Deck, Cos_96_Rd, HTF_L

async def stamp_plate(src_plate_name: str, dst_plate_name: str, volume: float = 100.0):
    backend = SimulatorBackend(open_browser=False)
    lh = LiquidHandler(backend=backend, deck=Deck())
    await lh.setup()

    src = Cos_96_Rd(name=src_plate_name)
    dst = Cos_96_Rd(name=dst_plate_name)
    tips = HTF_L(name="tips")
    lh.deck.assign_child_resource(src,  rails=1)
    lh.deck.assign_child_resource(dst,  rails=4)
    lh.deck.assign_child_resource(tips, rails=8)

    # Column-by-column transfer
    for col in range(1, 13):
        col_label = f"A{col}:H{col}"
        await lh.pick_up_tips(tips[col_label])
        await lh.aspirate(src[col_label], vols=volume)
        await lh.dispense(dst[col_label], vols=volume)
        await lh.drop_tips(tips[col_label])

    print(f"Plate stamped: {src.name} -> {dst.name}")
    await lh.stop()

asyncio.run(stamp_plate("source_plate", "dest_plate", volume=80))
```

## Key Parameters

| Parameter | Function | Default | Range / Options | Effect |
|-----------|----------|---------|-----------------|--------|
| `vols` | aspirate, dispense | required | 0–tip max (µL) | Volume per well |
| `flow_rates` | aspirate, dispense | backend default | 10–1000 µL/s | Liquid flow speed |
| `blow_out_air_volume` | dispense | 0 | 0–30 µL | Air expelled after dispense |
| `offsets` | aspirate, dispense | `Coordinate(0,0,0)` | (x, y, z) | Position offset from well center |
| `open_browser` | SimulatorBackend | `True` | `True`, `False` | Open browser visualizer |
| `rails` | assign_child_resource | required | 1–max slots | Physical deck position |
| `transfer_volume` | transfer | required | 0–tip max (µL) | Volume for high-level transfer |

## Best Practices

1. **Always simulate first**: Use `SimulatorBackend(open_browser=True)` to visually verify your deck layout and liquid movements before touching hardware.

2. **Track tip consumption programmatically**: In cherry-picking or high-throughput runs, count tips against rack capacity (96 tips/rack) to avoid running out mid-protocol.

3. **Wrap protocols in try/finally** for cleanup:
   ```python
   try:
       await run_my_protocol(lh)
   finally:
       await lh.stop()  # releases hardware connections
   ```

4. **Reassign resources once at protocol start**. Modifying resource positions mid-run can desynchronize the robot's state tracking.

5. **Pre-calculate volume and tip requirements** before starting, asserting that resources are sufficient for the run.

6. **Use fresh tips per transfer when contamination matters**. Cross-contamination in cherry-picking can bias screening results.

## Common Recipes

### Recipe: Dispense with Post-Dispense Mixing

```python
async def dispense_and_mix(lh, src, dst, tips, volume=50, mix_vol=40, mix_reps=3):
    await lh.pick_up_tips(tips["A1"])
    await lh.aspirate(src["A1"], vols=volume)
    await lh.dispense(dst["A1"], vols=volume)
    for _ in range(mix_reps):
        await lh.aspirate(dst["A1"], vols=mix_vol)
        await lh.dispense(dst["A1"], vols=mix_vol)
    await lh.drop_tips(tips["A1"])
    print(f"Dispensed {volume} µL and mixed {mix_reps}×")
```

### Recipe: Full-Plate Format Change (96 → 384)

```python
async def reformat_96_to_384(lh, src_96, dst_384, tips96, tips384, volume=50):
    # 96-well to 384-well expansion
    for row_idx, row in enumerate("ABCDEFGH"):
        for col in range(1, 13):
            src_well = f"{row}{col}"
            # Map to 4 corresponding wells in 384 (2×2 cluster)
            row_pairs = [row, chr(ord(row) + 1)] if row != "H" else [row]
            for col_offset in [0, 1]:
                dst_col = (col - 1) * 2 + col_offset
                for dst_row in row_pairs:
                    dst_well = f"{dst_row}{dst_col + 1}"
                    await lh.pick_up_tips(tips96[f"{row}{col}"])
                    await lh.aspirate(src_96[src_well], vols=volume/4)
                    await lh.dispense(dst_384[dst_well], vols=volume/4)
                    await lh.drop_tips(tips384[f"{dst_row}{dst_col + 1}"])
```

### Recipe: Custom Volume Profile Across a Plate

```python
# Different volumes per column (e.g., dose-response)
volumes = [100, 75, 50, 25, 12.5, 6.25, 3.125, 1.56, 0.78, 0.39, 0.195, 0]
for col in range(1, 13):
    col_label = f"A{col}:H{col}"
    await lh.pick_up_tips(tips[col_label])
    await lh.aspirate(reservoir["A1"], vols=volumes[col-1])
    await lh.dispense(plate[col_label], vols=volumes[col-1])
    await lh.drop_tips(tips[col_label])
```

## Expected Outputs

- **Simulation**: Browser visualizer at `http://localhost:2121` showing animated deck and liquid movements
- **Physical run**: Actual liquid transfers on the robot
- **On-hardware log**: Command log available via the robot's software (Hamilton HAMILTON SW, Tecan Evowoer, Opentrons App)

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `RuntimeError: No backend connected` | `lh.setup()` not awaited | Ensure `await lh.setup()` before any liquid operation |
| `ResourceNotFoundError` | Resource not on deck | Call `deck.assign_child_resource(resource, rails=N)` before referencing wells |
| `asyncio.InvalidStateError` | Called outside async context | Wrap in `async def` and run via `asyncio.run(main())` |
| `KeyError` on well address | Wrong well notation | Use `"A1"`, `"H12"`, not `"a1"` or `"A01"` |
| `VolumeError`: exceeds tip capacity | Volume > tip max | Use appropriate tip type (HTF_L = up to 1000 µL) |
| "Simulator shows no movement" | `open_browser=False` | Set `open_browser=True` or open `http://localhost:2121` manually |
| `ImportError` on backend | Backend extras not installed | `pip install "pylabrobot[hamilton]"` or `opentrons` |
| Hamilton/Tecan-specific error | Driver not configured | See specific backend docs for connection setup |

## References

- [PyLabRobot documentation](https://docs.pylabrobot.org/) — official API and backend docs
- [PyLabRobot GitHub](https://github.com/PyLabRobot/pylabrobot) — source and issue tracker
- [Azeloglu & Bhatt, Device](https://www.cell.com/device/fulltext/S2666-9986(23)00100-0) — original publication
- [PyPI: pylabrobot](https://pypi.org/project/pylabrobot/) — package info

## Related Skills

- `opentrons-ot2-protocols` — Opentrons-only protocol API with more modules
- `protocolsio-protocol-repository` — find protocols to convert to PyLabRobot
- `robot-deck-layout-calibration` — design and verify deck layouts across robot types
- `eln-elabftw`, `eln-chemotion`, `eln-openbis` — record runs in an ELN
- `western-blot-quantification` — sample-prep protocols for downstream analysis