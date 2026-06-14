# Subnet Tablature

An open-source, scalable fretboard architecture built on repeating 4-fret Subnet blocks and localized Gateway Markers, refactoring the physical fingerboard into an addressable [Subnet, Index] coordinate matrix.

## Official Technical Standard

The complete hardware system specifications, musical proof of concept (*Swan Lake* theme mapping), and dual-licensing framework (MIT + Solderpad SHL-2.1) are formally disclosed in the core specification file:

👉 **[Read the Full SPECIFICATION.md](./SPECIFICATION.md)**

## The Automation Tool (`tab_compiler.py`)
This repository includes a production-grade Python utility that automatically compiles traditional guitar tablature files into a human-friendly Subnet notation format while preserving pixel-perfect rhythmic grid alignment.

### Reading Format Suffix Shorthand
Notes are displayed inside clear, bracketed high-visibility reading tracks:
* **`[Subnet:Index]`** (e.g., `[4:2]` indicates Subnet Zone 4, localized Index fret 2).
* Open strings are globally designated as **`[0:0]`**.

### Quick Start Usage Guide
Save any traditional plain-text guitar tab into your project folder as `song.txt` and run the script straight from your terminal:

```powershell
python tab_compiler.py song.txt compiled_output.txt
```

### Machine-to-Machine API Mode
If you are passing data tokens into a backend program, MIDI sequencer, or an LED fretboard hardware configuration tool, pass the optional `--machine` flag to suppress brackets and generate raw comma-separated output values (`4,2`):

```powershell
python tab_compiler.py song.txt compiled_output.txt --machine
```
