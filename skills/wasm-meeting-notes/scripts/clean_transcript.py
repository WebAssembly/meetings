import sys
import time
from llm_client import call_llm

def clean_line(text):
    """Calls the configured LLM to clean up a single line of text."""
    system_instruction = (
        "You are an expert editor for technical meeting transcripts. Your task is to take a single line of a transcript "
        "and clean up the language. "
        "Remove verbal filler words like 'um', 'uh', false starts, stutters, and unnecessary repetition. "
        "Specifically, ensure that partial thoughts or trailing sentence fragments at the end of the line are removed, as they are usually abandoned thoughts. "
        "Fix obvious grammatical errors, but maintain the technical meaning and the speaker's original intent and tone. "
        "DO NOT summarize the text. DO NOT combine it with other lines. "
        "Return ONLY the cleaned up text. "
        "If the line is just a short filler (e.g. 'Yeah.', 'Okay.', 'Um.'), you can leave it as is or slightly clean it up, but DO NOT remove it entirely."
    )
    try:
        cleaned = call_llm(system_instruction, text, response_json=False)
        if cleaned:
            # Strip accidental surrounding quotes if the model wrapped the entire response
            if (cleaned.startswith('"') and cleaned.endswith('"')) or (cleaned.startswith("'") and cleaned.endswith("'")):
                cleaned = cleaned[1:-1].strip()
            return cleaned
        return text
    except Exception as e:
        print(f"  Warning: Failed to clean line ({e}), preserving original.", file=sys.stderr)
        return text

def main(input_file, output_file):
    print(f"Reading from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    valid_lines = [line.strip() for line in lines if line.strip()]
    print(f"Processing {len(valid_lines)} lines through LLM...")

    cleaned_lines = []
    for i, line in enumerate(valid_lines):
        print(f"Processing line {i+1}/{len(valid_lines)}...")

        if i > 0:
            time.sleep(0.5)

        # Separate speaker initials
        if ': ' in line:
            speaker, content = line.split(': ', 1)
        else:
            speaker = ""
            content = line

        cleaned_content = clean_line(content)

        if speaker:
            cleaned_lines.append(f"{speaker}: {cleaned_content}")
        else:
            cleaned_lines.append(cleaned_content)

    print(f"\nWriting results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for cl in cleaned_lines:
            f.write(cl + "\n\n")

    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_transcript.py <input.txt> <output.txt>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
