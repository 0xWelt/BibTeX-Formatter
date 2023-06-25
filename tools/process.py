import os
data = f"{os.path.dirname(os.path.abspath(__file__))}/../bfm/data"


def process_line(line: str):
    line = line.strip()

    # remove comments
    if "(" in line and ")" in line:
        line = line[:line.find("(")] + line[line.find(")")+1:]
    # swap final ", XXX" to first place
    if "," in line:
        parts = [part.strip() for part in line.split(",")]
        line = f"{parts[-1]} " + ", ".join(parts[:-1])

    return line


# Process IEEE journal from: https://en.wikipedia.org/wiki/List_of_IEEE_publications
with open('journal_raw.txt', 'r') as f:
    lines = f.readlines()
with open(f'{data}/IEEE_journal.txt', 'w') as f:
    f.write("# From: https://en.wikipedia.org/wiki/List_of_IEEE_publications\n")
    for line in lines:
        # skip "Part A,B,C.."
        if "Part" in line:
            continue
        # write line to output file
        f.write(process_line(line) + "\n")

# Process IEEE magazine from: https://en.wikipedia.org/wiki/List_of_IEEE_publications
with open('magazine_raw.txt', 'r') as f:
    lines = f.readlines()
with open(f'{data}/IEEE_magazine.txt', 'w') as f:
    f.write("# From: https://en.wikipedia.org/wiki/List_of_IEEE_publications\n")
    for line in lines:
        # skip "Part A,B,C.."
        if "Part" in line:
            continue
        # write line to output file
        f.write(process_line(line) + "\n")

# Process IEEE conference from: https://en.wikipedia.org/wiki/List_of_IEEE_conferences
with open('conference_raw.txt', 'r') as f:
    lines = f.readlines()
with open(f'{data}/IEEE_conference.txt', 'w') as f:
    f.write("# From: https://en.wikipedia.org/wiki/List_of_IEEE_conferences\n")
    for line in lines:
        # skip "Part A,B,C.."
        if "Part" in line:
            continue
        line = line.strip()
        # remove comments
        if "(" in line and ")" in line:
            line = line[:line.find("(")] + line[line.find(")")+1:]
        # write line to output file
        f.write(line + "\n")
