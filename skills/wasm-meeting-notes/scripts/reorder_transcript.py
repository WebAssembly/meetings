import sys
import json
import time
import re
from llm_client import call_llm

def parse_reorder_response(text):
    """
    Parses the LLM output into a list of nested index arrays.
    Handles bare JSON arrays, wrapped JSON objects (e.g. {"lines": [...]}),
    and markdown code fences.
    """
    text = text.strip()
    if text.startswith('```'):
        lines = text.splitlines()
        if lines[0].startswith('```'):
            lines = lines[1:]
        if lines and lines[-1].startswith('```'):
            lines = lines[:-1]
        text = '\n'.join(lines).strip()

    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for k in ['lines', 'reordered', 'result', 'indices', 'output']:
                if k in data and isinstance(data[k], list):
                    return data[k]
            for val in data.values():
                if isinstance(val, list):
                    return val
    except json.JSONDecodeError:
        pass

    m = re.search(r'\[\s*\[.*?\]\s*\]', text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass

    m_obj = re.search(r'\{.*?\}', text, re.DOTALL)
    if m_obj:
        try:
            data = json.loads(m_obj.group(0))
            if isinstance(data, dict):
                for val in data.values():
                    if isinstance(val, list):
                        return val
        except json.JSONDecodeError:
            pass

    return None

def reorder_chunk(lines_chunk):
    """
    Asks the configured LLM to reorder and merge a chunk of lines logically.
    """
    indexed_lines = [f"[{i}] {line}" for i, line in enumerate(lines_chunk)]
    prompt_text = "\n".join(indexed_lines)

    system_instruction = (
        "You are an expert editor for technical meeting transcripts. "
        "You are given a chronological snippet of a transcript where speakers are often interleaving or interrupting each other. "
        "Your goal is to reorganize these lines so that each speaker's complete thought is grouped together sequentially. "
        "Additionally, if a speaker has multiple lines that belong together as a single thought (e.g. they were broken up by an interrupter or they just spoke in short fragments), you should merge them. "
        "If a line is completely meaningless filler (like someone just saying 'Yeah' or 'Right') that does not add to the context, you may omit its index entirely. "
        "DO NOT summarize, alter, or remove any text other than complete omissions of meaningless filler. "
        "Respond with a JSON object containing a 'lines' field with an array of arrays of integers, where each sub-array represents a single line in the output. "
        "If a sub-array has multiple integers, those original lines will be concatenated into one. "
        "Example input:\n[0] A: Start\n[1] B: Interrupt\n[2] A: End\n"
        "Example output:\n{\"lines\": [[0, 2], [1]]}"
    )

    try:
        raw_resp = call_llm(system_instruction, prompt_text, response_json=True)
        return parse_reorder_response(raw_resp)
    except Exception as e:
        print(f"  Warning: LLM invocation failed ({e}). Falling back to original order.", file=sys.stderr)
        return None

def get_speaker(line):
    """Extracts speaker initials from a line (e.g. 'TL: text' -> 'TL')."""
    if ': ' in line:
        return line.split(': ', 1)[0]
    return None

def verify_indices(original_count, nested_indices, chunk):
    """
    Verifies that nested indices are valid, contain no duplicates,
    and only merge lines belonging to the same speaker.
    """
    if not isinstance(nested_indices, list):
        return False, set()

    flat_list = []
    for item in nested_indices:
        if isinstance(item, int):
            flat_list.append(item)
        elif isinstance(item, list):
            if not item:
                return False, set()
            speakers = [get_speaker(chunk[idx]) for idx in item if isinstance(idx, int) and 0 <= idx < len(chunk)]
            if len(set(speakers)) > 1:
                print(f"  Warning: LLM attempted to merge different speakers: {set(speakers)}")
                return False, set()
            for sub_item in item:
                if not isinstance(sub_item, int):
                    return False, set()
                flat_list.append(sub_item)
        else:
            return False, set()

    expected_set = set(range(original_count))
    actual_set = set(flat_list)

    if not actual_set.issubset(expected_set):
        return False, set()
    if len(flat_list) != len(actual_set):
        return False, set()

    dropped_indices = expected_set - actual_set
    return True, dropped_indices

def process_transcript(input_file, output_file, chunk_size=10):
    print(f"Reading from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    print(f"Processing {len(lines)} lines in chunks of {chunk_size}...")
    final_reordered_lines = []

    for i in range(0, len(lines), chunk_size):
        chunk = lines[i:i + chunk_size]

        if len(chunk) <= 1:
            final_reordered_lines.extend(chunk)
            continue

        print(f"Processing chunk {i // chunk_size + 1}/{(len(lines) + chunk_size - 1) // chunk_size}...")

        if i > 0:
            time.sleep(0.5)

        nested_indices = reorder_chunk(chunk)

        is_valid = False
        dropped = set()
        if nested_indices is not None:
            is_valid, dropped = verify_indices(len(chunk), nested_indices, chunk)

        if is_valid:
            if dropped:
                for d in dropped:
                    print(f"  Line removed (filler): {chunk[d]}")

            for item in nested_indices:
                if isinstance(item, int):
                    final_reordered_lines.append(chunk[item])
                elif isinstance(item, list):
                    merged_content = []
                    first_line = True
                    for idx in item:
                        line_text = chunk[idx]
                        if first_line:
                            merged_content.append(line_text)
                            first_line = False
                        else:
                            if ': ' in line_text:
                                merged_content.append(line_text.split(': ', 1)[1])
                            else:
                                merged_content.append(line_text)
                    final_reordered_lines.append(" ".join(merged_content))
        else:
            print("  Warning: Invalid or missing response from LLM. Falling back to original order for this chunk.")
            final_reordered_lines.extend(chunk)

    print(f"\nWriting results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in final_reordered_lines:
            f.write(line + "\n\n")

    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reorder_transcript.py <input.txt> <output.txt>")
        sys.exit(1)
    process_transcript(sys.argv[1], sys.argv[2])
