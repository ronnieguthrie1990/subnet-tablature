import re
import sys
import os

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
    Processes all 6 strings simultaneously using a synchronized block-slice engine.
    Guarantees perfect vertical column alignment under any technique density.
    """
    if not block_lines:
        return block_lines
        
    max_orig_len = max(len(line) for line in block_lines)
    padded_lines = [line.ljust(max_orig_len, '-') for line in block_lines]
    output_buffers = [[] for _ in range(len(padded_lines))]
    
    col = 0
    while col < max_orig_len:
        # Phase 1: Determine the look-ahead token lengths for all strings at this column
        token_lengths = []
        for line in padded_lines:
            char = line[col]
            if char.isdigit():
                remaining = line[col:]
                match = re.match(r'(\d+[\dbrhp/\\~v]*)', remaining)
                if match:
                    token_lengths.append(len(match.group(1)))
                    continue
            token_lengths.append(1)
            
        # The entire block must advance by the maximum consumed length to stay synchronized
        slice_advance = max(token_lengths)
        
        # Guard rails to prevent overrunning the line boundary
        if col + slice_advance > max_orig_len:
            slice_advance = max_orig_len - col
            if slice_advance <= 0:
                break
                
        # Phase 2: Extract and compile the text segment slice for each string
        compiled_slices = []
        for line in padded_lines:
            segment = line[col:col+slice_advance]
            compiled_slices.append(parse_slice_text(segment, machine_mode))
            
        # Phase 3: Uniformly pad the output slice to match the longest expanded width
        max_compiled_width = max(len(s) for s in compiled_slices)
        for str_idx, comp_slice in enumerate(compiled_slices):
            if len(comp_slice) < max_compiled_width:
                # Maintain dash padding integrity unless we are framing the structural pipe
                orig_char = padded_lines[str_idx][col]
                padding_char = '-' if orig_char in ['-', '|'] or comp_slice.startswith('-') else ' '
                comp_slice = comp_slice.ljust(max_compiled_width, padding_char)
            output_buffers[str_idx].append(comp_slice)
            
        # Move the global pointer forward by the synchronized slice size
        col += slice_advance
        
    return ["".join(buf) for buf in output_buffers]

def process_content(text_content, machine_mode=False):
    """Slices text into operational blocks to maintain aligned grid configurations."""
    lines = text_content.splitlines()
    output_lines = []
    
    string_prefixes = ('E |', 'B |', 'G |', 'D |', 'A |', 'e |', 'b |', 'g |', 'd |', 'a |',
                       'E|', 'B|', 'G|', 'D|', 'A|', 'e|', 'b|', 'g|', 'd|', 'a|')
    
    current_block = []
    for line in lines:
        if any(line.strip().startswith(prefix) for prefix in string_prefixes):
            current_block.append(line)
        else:
            if current_block:
                output_lines.extend(process_block(current_block, machine_mode))
                current_block = []
            output_lines.append(line)
            
    if current_block:
        output_lines.extend(process_block(current_block, machine_mode))
        
    return "\n".join(output_lines)

def main():
    print("===================================================================")
    print("SUBNET TABLATURE COMPILER AUTOMATION UTILITY v5.4 (SLICE LOCKED)")
    print("===================================================================")
    
    arguments = [arg for arg in sys.argv if arg != "tab_compiler.py"]
    machine_mode = "--machine" in arguments
    if machine_mode:
        arguments.remove("--machine")
        print("[MODE] Raw Data Processing Machine Mode Active (, format)")
    else:
        print("[MODE] High-Visibility Player Notation Mode Active [:] format")
    
    if len(arguments) < 1:
        print("[ERROR] No input file provided.\nUsage: python tab_compiler.py <input_file> [output_file] [--machine]")
        return

    input_path = arguments[0]
    if not os.path.exists(input_path):
        print(f"[ERROR] File '{input_path}' does not exist.")
        return

    with open(input_path, 'r', encoding='utf-8', errors='ignore') as infile:
        raw_text = infile.read()

    print(f"Parsing '{input_path}' with synchronized block-slice alignment...")
    compiled_text = process_content(raw_text, machine_mode)
    output_path = arguments[1] if len(arguments) >= 2 else "compiled_output.txt"

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(compiled_text)

    print(f"[SUCCESS] Complete song processed safely. Saved to: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    main()
