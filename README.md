[![License: MIT](https://shields.io)](https://opensource.org)
[![License: Solderpad SHL-2.1](https://shields.io)](https://solderpad.org)
[![Language: Python 3.13](https://shields.io)](https://python.org)
[![Status: Production-Ready](https://shields.io)](#)

# Subnet Tablature

An open-source, scalable fretboard architecture built on repeating 4-fret Subnet blocks and localized Gateway Markers, refactoring the physical fingerboard into an addressable [Subnet, Index] coordinate matrix.

## Official Technical Standard

The complete hardware system specifications, musical proof of concept (*Swan Lake* theme mapping), and dual-licensing framework (MIT + Solderpad SHL-2.1) are formally disclosed in the core specification file:

👉 **[Read the Full SPECIFICATION.md](./SPECIFICATION.md)**

---

## The Automation Tool (`tab_compiler.py`)

This repository includes a production-grade Python utility that automatically compiles traditional ASCII guitar and bass tablature files into addressable Subnet notation formats while preserving pixel-perfect vertical grid alignment.

### Production Guardrails & Architecture
* **Slice-Locked Alignment Matrix:** Automatically ensures that when single-digit frets expand into longer coordinate sets (e.g., `12` becoming `[3:4]`), all trailing rhythms and measure pipes (`|`) remain vertically synchronized.
* **Hidden Tab Expansion Sanitizer:** Automatically catches and expands browser tab characters (`\t`) to standard spacing to protect vertical grid calculations from collapsing.
* **Strict Instrument Validation Safetynet:** Intelligently maps multi-instrument tracking configurations. It permits clean alternating layouts (such as 6-string guitar parts and 4-string bass sections) while instantly generating terminal alert warnings for stray copy-paste formatting typos.
* **Anti-Data Overwrite Protection:** Built-in safeguards check file paths to prevent the tool from accidentally overwriting your source asset file.

### Reading Format Suffix Shorthand

| Absolute Fret Position | Player Notation (Standard) | Machine Format Output (`--machine`) |
| :--- | :--- | :--- |
| **0 (Open String)** | `[0:0]` | `0` |
| **9 - 12 (e.g., Fret 12)** | `[3:4]` | `3,4` |
| **13 - 16 (e.g., Fret 14)** | `[4:2]` | `4,2` |

---

## Quick Start Usage Guide

### 1. Standard Conversion (Automated Destination)
Save any plain-text guitar tab into your project folder as `song.txt`. Run the script providing only the source file; the compiler will automatically output a new asset file named `compiled_song.txt` right next to it:

```powershell
python tab_compiler.py song.txt
```

### 2. Custom Destination Overrides
To explicitly declare an output file name and path structure, append a secondary string argument:

```powershell
python tab_compiler.py song.txt custom_output.txt
```

### 3. Machine-to-Machine API Mode
If you are passing data tokens directly into an external program, MIDI sequencer, or an LED fretboard hardware configuration utility, include the `--machine` flag to suppress brackets and generate raw comma-separated values (`4,2`):

```powershell
python tab_compiler.py song.txt --machine
```

---

## Input Alignment Formatting Guidelines

To achieve clean compilation execution runs and avoid triggering the tracking validation anomaly warnings, verify three things when copying clips from sites like Ultimate-Guitar:
1. **Vertical Boundary Alignment:** Ensure your starting measure pipes (`|`) align in a perfectly straight vertical line down the left margin.
2. **Right-Side Trailing Cleanup:** Remove text markers or instructions (like `x4` or `let ring`) placed directly on top of or behind individual string lines.
3. **Word Wrap Management:** Disable word-wrap parameters inside your local text editor so long tab measures do not hard-wrap onto secondary lines.
