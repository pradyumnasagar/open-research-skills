---
name: opentrons-ot2-protocols
description: "Opentrons Python Protocol API v2 for OT-2 and Flex robots. Liquid handling protocols for PCR, ELISA, plate stamping, magnetic bead cleanup. Hardware modules: thermocycler, heater-shaker, magnetic, temperature. Simulate with opentrons_simulate before robot runs. For vendor-agnostic protocols use pylabrobot-vendor-agnostic."
license: MIT
---



<!-- metadata:
category: ''
version: 1.0.0
author: Pradyumna Jayaram
tags: []
difficulty: beginner
sources: SciAgent-Skills-main/skills/lab-automation/opentrons-protocol-api/SKILL.md
-->

# Opentrons OT-2 / Flex Protocol API

## Overview

The Opentrons Python Protocol API v2 lets you write liquid-handling protocols as plain Python files that execute on OT-2 or Flex robots. Every protocol defines a `metadata` dict, an optional `requirements` dict (robot type), and a `run(protocol)` function receiving a `ProtocolContext`. The context exposes deck setup, pipette operations, hardware modules (thermocycler, heater-shaker, magnetic, temperature), and utility methods. Protocols can be simulated locally with `opentrons_simulate` before uploading to the robot via the Opentrons App or HTTP API. The OT-2 and Flex robots are the most widely deployed open liquid-handling platforms in academic biology labs, with a Python-first protocol model that integrates cleanly with other lab-automation tools.

Author: Pradyumna Jayaram.

## When to Use

- Setting up PCR reactions: distribute master mix, add templates, run a thermal profile on the thermocycler
- Running serial dilutions: step a multi-channel pipette across a 96-well plate to create dilution curves
- Performing ELISA plate layouts: blocking buffer, primary/secondary antibodies, substrate, with tip changes between reagents
- Automating magnetic bead cleanups: engage/disengage magnets, aspirate supernatant, wash, elute
- Plate reformatting and stamping: copy entire plates or transfer selected wells
- Integrating hardware modules: coordinate temperature, shaking, and liquid handling in one protocol
- For **vendor-agnostic protocols** (Hamilton, Tecan, Beckman), use `pylabrobot-vendor-agnostic` instead
- For **published protocol retrieval** to inform an automation script, use `protocolsio-protocol-repository` first

## Prerequisites

- **Python packages**: `opentrons` (includes the `opentrons_simulate` CLI)
- **Robot**: OT-2 (slots 1–11, Gen2 pipettes) or Flex (slots A1–D3, Flex pipettes)
- **Environment**: Python 3.10+; Opentrons App for upload to a physical robot
- **CLI**: `opentrons_simulate` for local testing before robot runs

```bash
pip install opentrons
# Verify installation and simulate
opentrons_simulate my_protocol.py
```

## Quick Start

A minimal protocol that distributes reagent to a plate:

```python
from opentrons import protocol_api

metadata = {"
    "protocolName": "Simple Reagent Distribution",
    "author": "Pradyumna Jayaram",
    "apiLevel": "2.19",
}

def run(protocol: protocol_api.ProtocolContext):
    tips    = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    source  = protocol.load_labware("nest_12_reservoir_15ml", "2")
    plate   = protocol.load_labware("corning_96_wellplate_360ul_flat", "3")
    p300    = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips])

    p300.distribute(50, source["A1"], plate.wells()[:12], new_tip="once")
    protocol.comment("Distribution complete")
```

```bash
opentrons_simulate simple_reagent_distribution.py
```

## Core API

### Module 1: Protocol Metadata and Deck Setup

```python
from opentrons import protocol_api

metadata = {
    "protocolName": "My Assay Protocol",
    "author": "Pradyumna Jayaram <pradyumna@example.org>",
    "description": "96-well assay setup with temperature control",
    "apiLevel": "2.19",
}

# Target a specific robot type
requirements = {"robotType": "OT-2", "apiLevel": "2.19"}  # or "Flex"

def run(protocol: protocol_api.ProtocolContext):
    # OT-2: slots numbered 1-11 in a 3-column x 4-row grid
    tips_300  = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    tips_20   = protocol.load_labware("opentrons_96_tiprack_20ul",  "4")
    source    = protocol.load_labware("nest_12_reservoir_15ml",     "2", label="Buffer Reservoir")
    plate     = protocol.load_labware("corning_96_wellplate_360ul_flat", "3")
    tube_rack = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", "5")

    p300 = protocol.load_instrument("p300_single_gen2", "left",  tip_racks=[tips_300])
    p20  = protocol.load_instrument("p20_single_gen2",  "right", tip_racks=[tips_20])
    print(f"Deck has {len(protocol.deck)} slots; pipettes: {[p300.name, p20.name]}")
```

OT-2 deck layout:
```
10 | 11 | Trash
 7 |  8 |  9
 4 |  5 |  6
 1 |  2 |  3
```

Flex deck uses grid coordinates (A1, A2, ... D3):
```
D1 | D2 | D3
C1 | C2 | C3
B1 | B2 | B3
A1 | A2 | A3
```

Common pipette names: OT-2: `p20_single_gen2`, `p300_single_gen2`, `p1000_single_gen2`, `p20_multi_gen2`, `p300_multi_gen2`. Flex: `p50_single_flex`, `p1000_single_flex`, `p50_multi_flex`, `p1000_multi_flex`, `flex_96channel_1000`.

### Module 2: Pipette Operations

```python
def run(protocol: protocol_api.ProtocolContext):
    tips   = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    source = protocol.load_labware("nest_12_reservoir_15ml", "2")
    dest   = protocol.load_labware("corning_96_wellplate_360ul_flat", "3")
    p300   = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips])

    p300.pick_up_tip()

    # Basic liquid movement
    p300.aspirate(100, source["A1"])
    p300.dispense(100, dest["A1"])

    # Air gap to prevent dripping during transport
    p300.aspirate(80, source["A2"])
    p300.air_gap(20)
    p300.dispense(100, dest["A2"])

    # Mix in place
    p300.mix(3, 60, dest["A1"])

    # Touch tip to remove exterior droplets; blow out residual
    p300.touch_tip(dest["A1"])
    p300.blow_out(dest["A1"].top())

    p300.drop_tip()
    protocol.comment("Low-level operations complete")
```

```python
# Adjust flow rates for viscous or sensitive samples
def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    p300 = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips])
    p300.flow_rate.aspirate = 50     # µL/s, default ~150 (slow for viscous)
    p300.flow_rate.dispense = 150
    p300.flow_rate.blow_out = 300
    print(f"Aspirate rate: {p300.flow_rate.aspirate} µL/s")
```

### Module 3: High-Level Operations (transfer / distribute / consolidate)

```python
def run(protocol: protocol_api.ProtocolContext):
    tips   = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    source = protocol.load_labware("corning_96_wellplate_360ul_flat", "2")
    dest   = protocol.load_labware("corning_96_wellplate_360ul_flat", "3")
    p300   = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips])

    # transfer(): 1-to-1, with optional per-well tip changes
    p300.transfer(100, source["A1"], dest["A1"],
                  new_tip="always", mix_after=(3, 50), blow_out=True, touch_tip=True)

    # transfer() with lists (pairwise)
    sources = source.wells()[:8]
    dests   = dest.wells()[:8]
    p300.transfer(75, sources, dests, new_tip="always")

    # distribute(): 1-to-many with a single tip
    p300.distribute(50, source["A1"], dest.wells()[:12],
                    new_tip="once", disposal_volume=10)

    # consolidate(): many-to-1 (collect, then dispense)
    p300.consolidate(50, source.wells()[:8], dest["A1"], mix_after=(3, 100))
    print("Compound transfer operations complete")
```

### Module 4: Labware, Liquids, and Wells

```python
def run(protocol: protocol_api.ProtocolContext):
    plate  = protocol.load_labware("corning_96_wellplate_360ul_flat", "1")
    p300   = protocol.load_instrument("p300_single_gen2", "left",
                                      tip_racks=[protocol.load_labware("opentrons_96_tiprack_300ul", "2")])

    # Wells by name, list, row, column
    plate["A1"]            # single well
    plate.wells()          # column-major: A1, B1, ..., H1, A2, ...
    plate.rows()[0]        # row A: [A1, A2, ..., A12]
    plate.columns()[0]     # column 1: [A1, B1, ..., H1]

    # Vertical position control
    p300.pick_up_tip()
    p300.aspirate(80, plate["A1"].bottom(z=1))   # 1 mm above well bottom
    p300.dispense(80, plate["A1"].top(z=-2))     # 2 mm below top
    p300.aspirate(80, plate["A1"].center())      # geometric center
    p300.drop_tip()
```

```python
# Define liquids for visual tracking in the Opentrons App
def run(protocol: protocol_api.ProtocolContext):
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", "1")
    plate     = protocol.load_labware("corning_96_wellplate_360ul_flat", "2")
    pbs    = protocol.define_liquid(name="1× PBS",    description="Phosphate buffered saline",    display_color="#0077BB")
    sample = protocol.define_liquid(name="Sample",    description="Cell lysate 1 mg/mL",         display_color="#EE7733")
    reservoir["A1"].load_liquid(liquid=pbs,    volume=10000)
    reservoir["A2"].load_liquid(liquid=sample, volume=5000)
    for well in plate.wells():
        well.load_empty()
```

### Module 5: Hardware Modules

```python
def run(protocol: protocol_api.ProtocolContext):
    # Temperature Module
    temp_mod   = protocol.load_module("temperature module gen2", "3")
    temp_plate = temp_mod.load_labware("corning_96_wellplate_360ul_flat")
    temp_mod.set_temperature(celsius=4)    # blocks until target reached
    # temp_mod.deactivate() at the end

    # Magnetic Module
    mag_mod   = protocol.load_module("magnetic module gen2", "6")
    mag_plate = mag_mod.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")
    mag_mod.engage(height_from_base=10)
    protocol.delay(seconds=300)
    mag_mod.disengage()

    # Heater-Shaker Module
    hs_mod   = protocol.load_module("heaterShakerModuleV1", "1")
    hs_plate = hs_mod.load_labware("corning_96_wellplate_360ul_flat")
    hs_mod.close_labware_latch()
    hs_mod.set_target_temperature(celsius=37)
    hs_mod.wait_for_temperature()
    hs_mod.set_and_wait_for_shake_speed(rpm=500)
    protocol.delay(minutes=30)
    hs_mod.deactivate_shaker()
    hs_mod.deactivate_heater()
    hs_mod.open_labware_latch()
```

```python
# Thermocycler Module (auto-occupies slots 7-11 on OT-2)
def run(protocol: protocol_api.ProtocolContext):
    tc_mod   = protocol.load_module("thermocyclerModuleV2")
    tc_plate = tc_mod.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")

    tc_mod.open_lid()
    tc_mod.set_lid_temperature(celsius=105)
    tc_mod.set_block_temperature(95, hold_time_seconds=180)

    profile = [
        {"temperature": 95, "hold_time_seconds": 15},
        {"temperature": 60, "hold_time_seconds": 30},
        {"temperature": 72, "hold_time_seconds": 30},
    ]
    tc_mod.execute_profile(steps=profile, repetitions=35, block_max_volume=25)

    tc_mod.set_block_temperature(72, hold_time_minutes=5)
    tc_mod.set_block_temperature(4)
    tc_mod.deactivate_lid()
    tc_mod.open_lid()
```

### Module 6: Advanced Protocol Features

```python
def run(protocol: protocol_api.ProtocolContext):
    # Pause for user input (robot stops, app shows message)
    protocol.pause(msg="Add 10 µL of enzyme to tube A1, then resume")

    # Timed delay (no user action)
    protocol.delay(seconds=30, msg="Waiting 30s for reaction incubation")
    protocol.delay(minutes=5)

    # Comment in run log
    protocol.comment("Starting serial dilution — columns 1 to 11")

    # Rail lights
    protocol.set_rail_lights(True)

    # Home all axes
    protocol.home()

    # Skip slow waits in simulation
    if protocol.is_simulating():
        protocol.comment("Sim mode — skipping 10-min incubation")
    else:
        protocol.delay(minutes=10)
```

## Key Concepts

### Slot numbering: OT-2 vs Flex

| Robot | Slot format | Example |
|-------|-------------|---------|
| OT-2  | Numeric string `"1"`–`"11"` | `"1"`, `"7"`, `"11"` |
| Flex | Grid string `"A1"`–`"D3"` | `"A1"`, `"C2"`, `"D3"` |

Use `requirements = {"robotType": "OT-2"}` or `"Flex"` to enforce; mismatches are caught at simulation time.

### Tip management

`new_tip="always"` (fresh tip every transfer), `"once"` (one tip for all), `"never"` (no tip change). Default is `"always"` to prevent cross-contamination, but for high-throughput applications with single-reagent dispensing, `"once"` saves tips.

### Flow rate for viscous samples

Viscous samples (≥20% glycerol, PEG, protein >5 mg/mL) require slower aspirate rates (25–50 µL/s). Foaming samples need slower dispense rates. Pre-wetting tips with `mix()` before critical transfers improves accuracy.

### Simulation vs physical run

`protocol.is_simulating()` is `True` during `opentrons_simulate` runs. Use this to skip long delays or wait steps that would make simulation slow.

## Common Workflows

### Workflow 1: PCR Setup and Run

```python
from opentrons import protocol_api

metadata = {"protocolName": "PCR Setup and Run", "author": "Pradyumna Jayaram", "apiLevel": "2.19"}

def run(protocol: protocol_api.ProtocolContext):
    tc_mod    = protocol.load_module("thermocyclerModuleV2")
    tc_plate  = tc_mod.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")
    tips_300  = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    tips_20   = protocol.load_labware("opentrons_96_tiprack_20ul",  "4")
    reagents  = protocol.load_labware("opentrons_24_tuberack_nest_1.5ml_snapcap", "2")
    p300      = protocol.load_instrument("p300_single_gen2", "left",  tip_racks=[tips_300])
    p20       = protocol.load_instrument("p20_single_gen2",  "right", tip_racks=[tips_20])

    # Distribute master mix
    tc_mod.open_lid()
    p300.distribute(20, reagents["A1"], tc_plate.wells()[:8],
                    new_tip="once", blow_out=True, blowout_location="source well")

    # Add templates
    for i in range(8):
        p20.transfer(5, reagents.wells()[i + 1], tc_plate.wells()[i],
                     new_tip="always", mix_after=(2, 10))

    # PCR cycling
    tc_mod.close_lid()
    tc_mod.set_lid_temperature(105)
    tc_mod.set_block_temperature(95, hold_time_seconds=180)
    profile = [
        {"temperature": 95, "hold_time_seconds": 15},
        {"temperature": 60, "hold_time_seconds": 30},
        {"temperature": 72, "hold_time_seconds": 30},
    ]
    tc_mod.execute_profile(steps=profile, repetitions=35, block_max_volume=25)
    tc_mod.set_block_temperature(72, hold_time_minutes=5)
    tc_mod.set_block_temperature(4)
    tc_mod.deactivate_lid()
    tc_mod.open_lid()
    protocol.comment("PCR complete — 8 reactions in wells A1:H1")
```

### Workflow 2: ELISA Serial Dilution

```python
from opentrons import protocol_api

metadata = {"protocolName": "ELISA Serial Dilution", "author": "Pradyumna Jayaram", "apiLevel": "2.19"}

def run(protocol: protocol_api.ProtocolContext):
    tips_300  = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    tips_300b = protocol.load_labware("opentrons_96_tiprack_300ul", "4")
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", "2")
    plate     = protocol.load_labware("corning_96_wellplate_360ul_flat", "3")
    multi     = protocol.load_instrument("p300_multi_gen2", "left",
                                          tip_racks=[tips_300, tips_300b])

    # Column 1: undiluted sample
    multi.transfer(100, reservoir["A2"], plate.columns()[0], new_tip="once")

    # Columns 2-12: diluent
    multi.distribute(100, reservoir["A1"],
                     [col[0] for col in plate.columns()[1:]],
                     new_tip="once", disposal_volume=10)

    # Serial dilution columns 1 -> 11
    multi.transfer(100,
                   [col[0] for col in plate.columns()[:11]],
                   [col[0] for col in plate.columns()[1:]],
                   mix_after=(5, 80), new_tip="always")

    # Equalize column 12
    multi.pick_up_tip()
    multi.aspirate(100, plate.columns()[11][0])
    multi.drop_tip()
    protocol.comment("ELISA serial dilution complete — 11 dilution steps")
```

### Workflow 3: Magnetic Bead Cleanup

```python
from opentrons import protocol_api

metadata = {"protocolName": "Bead Cleanup", "author": "Pradyumna Jayaram", "apiLevel": "2.19"}

def run(protocol: protocol_api.ProtocolContext):
    mag_mod   = protocol.load_module("magnetic module gen2", "4")
    bead_plate = mag_mod.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")
    tips      = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", "2")
    waste     = protocol.load_labware("nest_12_reservoir_15ml", "5")
    p300      = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips])

    mag_mod.engage(height_from_base=6)
    protocol.delay(seconds=120, msg="Beads pelleting")
    p300.transfer(90, bead_plate["A1"].bottom(z=0.5), waste["A1"], new_tip="once")

    for wash_num in range(2):
        mag_mod.disengage()
        p300.transfer(100, reservoir["A1"], bead_plate["A1"],
                      mix_after=(5, 80), new_tip="always")
        mag_mod.engage(height_from_base=6)
        protocol.delay(seconds=90)
        p300.transfer(100, bead_plate["A1"].bottom(z=0.5), waste["A2"], new_tip="always")

    mag_mod.disengage()
    elution = protocol.load_labware("corning_96_wellplate_360ul_flat", "3")
    p300.transfer(50, reservoir["A2"], bead_plate["A1"], mix_after=(10, 40), new_tip="always")
    mag_mod.engage(height_from_base=6)
    protocol.delay(seconds=120)
    p300.transfer(45, bead_plate["A1"].bottom(z=0.5), elution["A1"], new_tip="always")
    mag_mod.disengage()
    protocol.comment("Bead cleanup complete")
```

## Key Parameters

| Parameter | Function | Default | Range / Options | Effect |
|-----------|----------|---------|-----------------|--------|
| `new_tip` | transfer, distribute, consolidate | `"always"` | `"always"`, `"once"`, `"never"` | Tip-change strategy |
| `mix_after` | transfer | `None` | `(reps, volume)` | Mix in destination well after dispense |
| `mix_before` | transfer | `None` | `(reps, volume)` | Mix in source well before aspirate |
| `blow_out` | transfer | `False` | bool | Expel residual after dispense |
| `air_gap` | transfer | `0` | 0–max pipette µL | Air gap after aspirate |
| `disposal_volume` | distribute | `0` | 0–max pipette µL | Extra volume drawn to improve accuracy |
| `flow_rate.aspirate` | pipette property | model-specific | 1–1000 µL/s | Aspirate speed |
| `flow_rate.dispense` | pipette property | model-specific | 1–1000 µL/s | Dispense speed |
| `height_from_base` | `mag_mod.engage()` | — | 0–20 mm | Magnet height above plate base |
| `repetitions` | `tc_mod.execute_profile()` | — | 1–99 | PCR cycles |

## Best Practices

1. **Always simulate first**: `opentrons_simulate my_protocol.py` catches labware name errors, slot conflicts, and tip shortages before you touch a robot.

2. **Use compound operations over manual sequences**: `transfer()`, `distribute()`, and `consolidate()` handle tip management, air gaps, and blow-out correctly. Reserve low-level calls for operations not supported by these.

3. **Count tips before running**:
   ```python
   n_transfers = len(source_wells)
   tips_per_rack = 96
   racks_needed = -(-n_transfers // tips_per_rack)   # ceiling division
   ```

4. **Use `define_liquid()` and `load_liquid()`** for setup validation — the App shows color-coded wells with volumes, making it easy to verify correct reagent placement.

5. **Distinguish OT-2 and Flex slot names** with `requirements = {"robotType": "OT-2"}` or `"Flex"` to catch mismatches in simulation.

6. **Adjust flow rates for difficult liquids**: Viscous samples (≥20% glycerol, PEG, protein >5 mg/mL) need lower aspirate rates (25–50 µL/s). Foaming samples need lower dispense rates.

7. **Use `pause()` for manual steps, not `delay()`**: `pause()` stops the robot and notifies the operator; the run resumes on demand. `delay()` is for timed waits where no human action is needed.

## Common Recipes

### Recipe: Plate Replication (96-well to 96-well)

```python
from opentrons import protocol_api

metadata = {"protocolName": "Plate Replication", "apiLevel": "2.19"}

def run(protocol: protocol_api.ProtocolContext):
    tips   = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    source = protocol.load_labware("corning_96_wellplate_360ul_flat", "2")
    dest   = protocol.load_labware("corning_96_wellplate_360ul_flat", "3")
    p300   = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[tips])
    p300.transfer(100, source.wells(), dest.wells(), new_tip="always")
    protocol.comment("Plate replicated: 96 wells transferred")
```

### Recipe: Multi-Channel Column-by-Column Fill

```python
def run(protocol: protocol_api.ProtocolContext):
    tips      = protocol.load_labware("opentrons_96_tiprack_300ul", "1")
    reservoir = protocol.load_labware("nest_12_reservoir_15ml", "2")
    plate     = protocol.load_labware("corning_96_wellplate_360ul_flat", "3")
    multi     = protocol.load_instrument("p300_multi_gen2", "left", tip_racks=[tips])
    multi.distribute(100, reservoir["A1"],
                     [plate.columns()[i][0] for i in range(12)],
                     new_tip="once", disposal_volume=10)
```

### Recipe: Pause for Manual Reagent Addition

```python
def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware("corning_96_wellplate_360ul_flat", "1")
    # Robot stops, app shows the message; user clicks Resume after adding reagent
    protocol.pause(msg="Add 5 µL of compound to wells A1, B1, C1, then resume")
    print("Resumed after manual addition")
```

## Expected Outputs

- `opentrons_simulate` output: ASCII tree of the simulated run with success/failure status, run log, and any errors with line numbers
- On the robot: a run log in the Opentrons App showing each step, the labware layout, and timings
- Files: `.py` protocol files; uploads via the App or the HTTP API to `/protocols`

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `LabwareNotFoundError` | Wrong API name | Look up at [labware.opentrons.com](https://labware.opentrons.com/); case-sensitive |
| `OutOfTipsError` | More transfers than tips | Add tip racks to `tip_racks=[]`; or call `pipette.reset_tipracks()` |
| Volume > pipette max | Exceeds pipette capacity | Use `distribute()`; switch to `p1000_single_gen2` for >300 µL |
| `DeckConflictError` | Overlapping slots | Thermocycler auto-occupies slots 7–11; print `protocol.deck` to check |
| Module not attached | Wrong module string | Use exact: `"temperature module gen2"`, `"magnetic module gen2"`, `"thermocyclerModuleV2"`, `"heaterShakerModuleV1"` |
| Inaccurate volumes near min | Edge of calibrated range | Use a pipette whose range covers the volume; pre-wet with `mix()`; reduce flow rates |
| OT-2 protocol fails on Flex | Slot name mismatch | Set `requirements = {"robotType": "Flex"}` or `"OT-2"` |
| Inconsistent volumes for viscous samples | Default flow too fast | Lower `flow_rate.aspirate` to 25–50 µL/s |

## References

- [Opentrons Protocol API v2 documentation](https://docs.opentrons.com/v2/) — full API reference
- [Opentrons Labware Library](https://labware.opentrons.com/) — searchable catalog of API names
- [Opentrons GitHub](https://github.com/Opentrons/opentrons) — source and protocol examples
- [Opentrons Community Forum](https://discuss.opentrons.com/) — Q&A for protocol debugging
- [Protocol API tutorial](https://docs.opentrons.com/v2/tutorial.html) — step-by-step walkthrough

## Related Skills

- `pylabrobot-vendor-agnostic` — same workflow, vendor-agnostic across Hamilton, Tecan, Beckman
- `protocolsio-protocol-repository` — find published protocols to inform your automation
- `robot-deck-layout-calibration` — design and verify deck layouts across robot types
- `eln-elabftw`, `eln-chemotion`, `eln-openbis` — record the run in an ELN
- `western-blot-quantification` — sample-prep protocols that can be partially automated here