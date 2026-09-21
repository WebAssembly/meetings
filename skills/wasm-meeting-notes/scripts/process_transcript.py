import re
import sys

def get_initials(name, existing_initials):
    # Remove parenthetical / bracketed annotations like "(Guest)", "(to Everyone)", etc.
    clean_name = re.sub(r'\(.*?\)', '', name).strip()
    clean_name = re.sub(r'\[.*?\]', '', clean_name).strip()

    parts = clean_name.split()
    if not parts:
        return "UNK"

    base_initials = "".join(p[0].upper() for p in parts if p and (p[0].isalpha() or p[0].isdigit()))
    if not base_initials:
        base_initials = "XX"

    if base_initials not in existing_initials:
        return base_initials

    # Collision resolution
    # Try adding the second letter of the last name (e.g. Thomas Long -> TLo)
    if len(parts) >= 2 and len(parts[-1]) >= 2:
        candidate = base_initials[:-1] + parts[-1][0:2].capitalize()
        if candidate not in existing_initials:
            return candidate

    # Try adding the second letter of the first name (e.g. Thomas Long -> ThL)
    if len(parts[0]) >= 2:
        candidate = parts[0][0:2].capitalize() + base_initials[1:]
        if candidate not in existing_initials:
            return candidate

    # Fallback to appending a number
    counter = 1
    while True:
        candidate = f"{base_initials}{counter}"
        if candidate not in existing_initials:
            return candidate
        counter += 1

def is_timestamp_or_header(line):
    # Matches common WebVTT, SRT, and markdown timestamp or header patterns
    if not line:
        return True
    if line.startswith('#'):
        return True
    if line == 'WEBVTT' or line.startswith('NOTE') or line.startswith('Kind:') or line.startswith('Language:'):
        return True
    # WebVTT / SRT timestamp ranges: 00:03:47.000 --> 00:03:51.000
    if re.match(r'^\d\d?:\d\d(?::\d\d)?(?:\.\d+)?\s*-->\s*\d\d?:\d\d(?::\d\d)?(?:\.\d+)?', line):
        return True
    # Standalone timestamps: ### 00:03:28 or [00:03:28] or 00:03:28
    if re.match(r'^(?:###\s*)?\[?\d\d?:\d\d(?::\d\d)?(?:\.\d+)?\]?$', line):
        return True
    # Cue sequence numbers
    if re.match(r'^\d+$', line):
        return True
    return False

def extract_speaker_and_content(line):
    # Matches:
    # **Derek Schuff:** Content
    # **Derek Schuff**: Content
    # Derek Schuff: Content
    # 00:03:47 Derek Schuff: Content
    speaker_re = re.compile(r'^(?:(?:\d\d?:\d\d(?::\d\d)?(?:\.\d+)?)\s+)?(?:\*\*)?([^*:\n]{2,50}?)(?::\*\*|\*\*:|:\s*|\s*:\s*)(.*)$')
    m = speaker_re.match(line)
    if m:
        speaker_candidate = m.group(1).strip()
        # Ensure it's a realistic speaker name (1-6 words, doesn't look like a URL scheme)
        if not speaker_candidate.startswith('http') and len(speaker_candidate.split()) <= 6:
            return speaker_candidate, m.group(2).strip()
    return None, line

def main(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()

    # First pass: find all speakers and generate unique initials
    speakers = set()
    for line in raw_lines:
        stripped = line.strip().replace('\xa0', ' ').strip()
        if is_timestamp_or_header(stripped):
            continue
        speaker, _ = extract_speaker_and_content(stripped)
        if speaker:
            speakers.add(speaker)

    sorted_speakers = sorted(list(speakers))
    speaker_map = {}
    existing_initials = set()

    for speaker in sorted_speakers:
        initials = get_initials(speaker, existing_initials)
        speaker_map[speaker] = initials
        existing_initials.add(initials)

    print("Speaker Initials Mapping:")
    for speaker in sorted_speakers:
        print(f"  {speaker_map[speaker]}: {speaker}")

    # Second pass: clean up lines and attribute dialogue
    out_lines = []
    current_initials = None

    for line in raw_lines:
        stripped = line.strip().replace('\xa0', ' ').strip()
        if is_timestamp_or_header(stripped):
            continue

        speaker, content = extract_speaker_and_content(stripped)
        if speaker:
            current_initials = speaker_map[speaker]
            if content:
                out_lines.append(f"{current_initials}: {content}")
        else:
            if current_initials and stripped:
                out_lines.append(f"{current_initials}: {stripped}")

    with open(output_file, 'w', encoding='utf-8') as f:
        for out_line in out_lines:
            f.write(out_line + "\n\n")

    print(f"\nProcessed {len(out_lines)} dialogue turns written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_transcript.py <input_transcript> <output.txt>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
