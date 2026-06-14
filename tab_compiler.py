import re
import sys
import os
import argparse

def convert_fret_to_coordinate(fret_str, machine_mode=False):
    """Translates an absolute fret into a Subnet Tablature coordinate."""
    if not fret_str.isdigit():
        return fret_str
    fret = int(fret_str)
    if fret == 0:
        return "0" if machine_mode else "[0:0]"
    subnet = ((fret - 1) // 4) + 1
    index = ((fret - 1) % 4) + 1
    
    if machine_mode:
        return f"{subnet},{index}"
    return f"[{subnet}:{index}]"

def parse_slice_text(text_segment, machine_mode=False):
    """Finds and converts any absolute fret digits within a text segment block."""
    numbers = re.findall(r'\d+', text_segment)
    if not numbers:
        return text_segment
    compiled_segment = text_segment
    for num in numbers:
        coord = convert_fret_to_coordinate(num, machine_mode)
        compiled_segment = compiled_segment.replace(num, coord, 1)
    return compiled_segment

def process_block(block_lines, machine_mode=False):
    """
    Processes all strings simultaneously using a synchronized block-slice engine.
    Guarantees perfect vertical column alignment under any technique density.
    """
    if not block_lines:
        return block_lines
        
    max_orig_len = max(len(line) for line in block_lines)
    padded_lines = [line.ljust(max_orig_len, '-') for line in block_lines]
    output_buffers = [[] for _ in range(len(padded_lines))]
    
    col = 0
    while col < max_orig_len:
        token_lengths = []
        for line in padded_lines:
            if col >= len(line):
                token_lengths.append(1)
                continue
            char = line[col]
            if char.isdigit():
                remaining = line[col:]
                match = re.match(r'(\d+[\dbrhp/\\~v]*)', remaining)
                if match:
                    token_lengths.append(len(match.group(1)))
                    continue
            token_lengths.append(1)
            
        slice_advance = max(token_lengths) if token_lengths else 1
        
        if col + slice_advance > max_orig_len:
            slice_advance = max_orig_len - col
            if slice_advance <= 0:
                break
                
        compiled_slices = []
        for line in padded_lines:
            segment = line[col:col+slice_advance]
            compiled_slices.append(parse_slice_text(segment, machine_mode))
            
        max_compiled_width = max(len(s) for s in compiled_slices) if compiled_slices else 1
        for str_idx, comp_slice in enumerate(compiled_slices):
            if len(comp_slice) < max_compiled_width:
                orig_char = padded_lines[str_idx][col] if col < len(padded_lines[str_idx]) else '-'
                padding_char = '-' if orig_char in ['-', '|'] or comp_slice.startswith('-') else ' '
                comp_slice = comp_slice.ljust(max_compiled_width, padding_char)
            output_buffers[str_idx].append(comp_slice)
            
        col += slice_advance
        
    return ["".join(buf) for buf in output_buffers]

def process_content(text_content, machine_mode=False):
    """
    Slices text into operational blocks using an Instrument-Lock Safetynet.
    Allows standard dual-tracking arrangements (6 and 4 strings) and multiple 
    guitars (6 and 6 strings) but logs random alignment typos down the page.
    """
    lines = text_content.splitlines()
    output_lines = []
    
    TAB_LINE_PATTERN = re.compile(r'^\s*[A-Ga-g1-9][#b]?\s*\|')
    
    current_block = []
    block_line_start = 0
    primary_song_baseline = None
    registered_alternates = set()
    
    for idx, line in enumerate(lines, start=1):
        if TAB_LINE_PATTERN.match(line):
            if not current_block:
                block_line_start = idx
            current_block.append(line)
        else:
            if current_block:
                actual_count = len(current_block)
                
                # 1. Automatically lock onto the song's primary instrument size
                if primary_song_baseline is None:
                    primary_song_baseline = actual_count
                
                # 2. Track layout variations against strict validation filters
                if actual_count != primary_song_baseline:
                    # VALID INTERCHANGE 1: Allow 6-string track to switch to a 4-string bass line
                    if primary_song_baseline == 6 and actual_count == 4:
                        if actual_count not in registered_alternates:
                            registered_alternates.add(actual_count)
                            print(f"[DUAL TRACK LOG] Verified parallel 4-string bass track layout at line {block_line_start}. Initializing alignment engine safely.")
                    
                    # VALID INTERCHANGE 2: Allow multiple 6-string tracking blocks to coexist
                    elif primary_song_baseline == 6 and actual_count == 6:
                        pass
                        
                    # TYPO ERROR ATTEMPT: Catch accidental layout omissions (like dropping a line to 5 strings)
                    else:
                        print(f"[WARNING] Structural layout anomaly caught at line {block_line_start}. "
                              f"Expected a standard {primary_song_baseline}-string layout, but found an irregular "
                              f"{actual_count}-string block. Check for a copy/paste alignment typo!")
                
                output_lines.extend(process_block(current_block, machine_mode))
                current_block = []
            output_lines.append(line)
            
    if current_block:
        actual_count = len(current_block)
        # FIXED: Variable name updated to primary_song_baseline to match function initialization
        if primary_song_baseline is not None and actual_count != primary_song_baseline:
            if not (primary_song_baseline == 6 and actual_count == 4):
                print(f"[WARNING] Structural layout anomaly caught at line {block_line_start}. Expected valid tracking configuration, found {actual_count} strings.")
        output_lines.extend(process_block(current_block, machine_mode))
        
    return "\n".join(output_lines)
def main():
    print("===================================================================")
    print("SUBNET TABLATURE COMPILER AUTOMATION UTILITY v8.0 (STABLE RELEASE)")
    print("===================================================================")
    
    parser = argparse.ArgumentParser(description="Compile guitar tablature to Subnet coordinates safely.")
    parser.add_argument("input_file", help="Path to the input tablature text file.")
    parser.add_argument("output_file", nargs="?", default=None, 
                        help="Path to save the output. Defaults to 'compiled_<input_name>.txt'.")
    parser.add_argument("--machine", action="store_true", help="Activate Raw Data Machine processing format (, instead of [:])")
    
    args = parser.parse_args()

    if args.machine:
        print("[MODE] Raw Data Processing Machine Mode Active (, format)")
    else:
        print("[MODE] High-Visibility Player Notation Mode Active [:] format")
    
    if not os.path.exists(args.input_file):
        print(f"[ERROR] File '{args.input_file}' does not exist.")
        return

    input_abs = os.path.abspath(args.input_file)
    if args.output_file is None:
        base_dir = os.path.dirname(input_abs)
        base_name = os.path.basename(input_abs)
        output_path = os.path.join(base_dir, f"compiled_{base_name}")
    else:
        output_path = os.path.abspath(args.output_file)
        if output_path == input_abs:
            base_dir = os.path.dirname(output_path)
            base_name = os.path.basename(output_path)
            output_path = os.path.join(base_dir, f"compiled_{base_name}")
            print(f"[NOTE] Output file matched input file. Diverting output to save target safely: '{output_path}'")

    try:
        print(f"Reading raw data from target: '{args.input_file}'...")
        with open(args.input_file, 'r', encoding='utf-8', errors='ignore') as infile:
            raw_text = infile.read()
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to read input file: {e}")
        return

    if '\t' in raw_text:
        print("[NOTE] Tab characters caught and expanded to standard spacing to protect alignment integrity.")
        raw_text = raw_text.expandtabs(4)

    print("Parsing text layout structure via dynamic multi-string block alignment...")
    compiled_text = process_content(raw_text, args.machine)
    
    try:
        print(f"Writing parsed output to destination: '{output_path}'...")
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(compiled_text)
        print(f"[SUCCESS] Process complete! Saved to: {output_path}")
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to save output file: {e}")

if __name__ == "__main__":
    main()
