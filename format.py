import time

selected_keys = {
    "@article": ["author", "title", "journal", "volume", "number", "pages", "year"],
    "@book": ["author", "title", "publisher", "year"],
    "@inproceedings": ["author", "title", "booktitle", "pages", "year"],
}
brief_to_full = {
    "AAAI Conference on Artificial Intelligence": "AAAI Conference on Artificial Intelligence (AAAI)",
    "AIAA Infotech@Aerospace Conference": "AIAA Infotech@Aerospace Conference",
    "AIAA Journal on Guidance, Control, and Dynamics": "AIAA Journal on Guidance, Control, and Dynamics",
    "Allerton Conference on Communication": "Allerton Conference on Communication, Control, and Compution",
    "American Control Conference": "American Control Conference (ACC)",
    "Artificial Intelligence": "Artificial Intelligence",
    "Autonomous Agents and Multiagent Systems": "International Conference on Autonomous Agents and Multiagent Systems (AAMAS)",
    "Aviation Technology, Integration, and Operations": "AIAA Aviation Technology, Integration, and Operations Conference (ATIO)",
    "Communications of the ACM": "Communications of the ACM",
    "Computer Vision and Pattern Recognition": "IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)",
    "Conference on Decision and Control": "IEEE Conference on Decision and Control (CDC)",
    "Digital Avionics Systems Conference": "Digital Avionics Systems Conference (DASC)",
    "European Conference on Machine Learning": "European Conference on Machine Learning (ECML)",
    "Guidance, Navigation, and Control": "AIAA Guidance, Navigation, and Control Conference (GNC)",
    "IEEE Aerospace Conference": "IEEE Aerospace Conference",
    "IEEE Control Systems Magazine": "IEEE Control Systems Magazine",
    "IEEE Transactions on Aerospace and Electronic Systems": "IEEE Transactions on Aerospace and Electronic Systems",
    "IEEE Transactions on Automatic Control": "IEEE Transactions on Automatic Control",
    "IEEE Transactions on Computational Intelligence and AI in Games": "IEEE Transactions on Computational Intelligence and AI in Games",
    "IEEE Transactions on Control Systems Technology": "IEEE Transactions on Control Systems Technology",
    "IEEE Transactions on Signal Processing": "IEEE Transactions on Signal Processing",
    "Intelligent Robots and Systems": "IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)",
    "Intelligent Transportation Systems": "IEEE Intelligent Transportation Systems Conference (ITSC)",
    "International Conference on Acoustics, Speech, and Signal Processing": "International Conference on Acoustics, Speech, and Signal Processing (ICASSP)",
    "International Conference on Agents and Artificial Intelligence": "International Conference on Agents and Artificial Intelligence (ICAART)",
    "International Conference on Automated Planning and Scheduling": "International Conference on Automated Planning and Scheduling (ICAPS)",
    "International Conference on Machine Learning and Applications": "International Conference on Machine Learning and Applications (ICMLA)",
    "International Conference on Machine Learning": "International Conference on Machine Learning (ICML)",
    "International Conference on Robotics and Automation": "IEEE International Conference on Robotics and Automation (ICRA)",
    "International Conference on Spoken Language Processing": "International Conference on Spoken Language Processing (ICSLP)",
    "International Joint Conference on Artificial Intelligence": "International Joint Conference on Artificial Intelligence (IJCAI)",
    "International Speech Communication Association": "Annual Conference of the International Speech Communication Association (INTERSPEECH)",
    "Journal of Aerospace Computing": "Journal of Aerospace Computing, Information, and Communication",
    "Journal of Artificial Intelligence Research": "Journal of Artificial Intelligence Research",
    "Journal of Machine Learning Research": "Journal of Machine Learning Research",
    "Journal of Optimization Theory and Applications": "Journal of Optimization Theory and Applications",
    "Learning and Intelligent Optimization": "Learning and Intelligent Optimization (LION)",
    "Massachusetts Institute of Technology, Department of Aeronautics and Astronautics": "Massachusetts Institute of Technology, Department of Aeronautics and Astronautics",
    "Massachusetts Institute of Technology, Department of Electrical Engineering and Computer Science": "Massachusetts Institute of Technology, Department of Electrical Engineering and Computer Science",
    "Massachusetts Institute of Technology, Department of Mechanical Engineering": "Massachusetts Institute of Technology, Department of Mechanical Engineering",
    "Massachusetts Institute of Technology": "Massachusetts Institute of Technology",
    "Mathematics of Operations Research": "Mathematics of Operations Research",
    "Neural Information Processing Systems": "Advances in Neural Information Processing Systems (NeurIPS)",
    "Operations Research": "Operations Research",
    "Robotics: Science and Systems": "Robotics: Science and Systems (RSS)",
    "Special Interest Group on Data Communication": "ACM Special Interest Group on Data Communication (SIGCOMM)",
    "Stanford University, Department of Aeronautics and Astronautics": "Stanford University, Department of Aeronautics and Astronautics",
    "Stanford University, Department of Electrical Engineering": "Stanford University, Department of Electrical Engineering",
    "Stanford University, Department of Mechanical Engineering": "Stanford University, Department of Mechanical Engineering",
    "Tools and Algorithms for the Construction and Analysis of Systems": "International Conference on Tools and Algorithms for the Construction and Analysis of Systems (TACAS)",
    "Uncertainty in Artificial Intelligence": "Conference on Uncertainty in Artificial Intelligence (UAI)",
    "International Conference on Learning Representations": "International Conference on Learning Representations (ICLR)",
    "Empirical Methods in Natural Language Processing": "Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    "International Conference on Soft Robotics": "IEEE International Conference on Soft Robotics (RoboSoft)"
}


def read_bibtex(in_file: str):
    def remove_up_to(in_string, chars, times):
        count_before = {c: 0 for c in set(chars)}
        count_after = {c: 0 for c in set(chars)}

        for cb in in_string:
            if cb not in chars or count_before[cb] >= times:
                break
            else:
                count_before[cb] += 1
        for ca in in_string[::-1]:
            if ca not in chars or count_after[ca] >= times:
                break
            else:
                count_after[ca] += 1

        num_to_cut_before = sum(count_before.values())
        num_to_cut_after = sum(count_after.values())

        return in_string[num_to_cut_before:- num_to_cut_after]

    with open(in_file, 'r') as f:
        lines = f.readlines()

    # add all bibtex entries to a dict with key=ref_name
    bibs = dict()
    previous_line = ""
    for line in lines:
        # skip comments and empty lines
        line = line.strip()
        if not line or line.startswith("%") or line.startswith("}"):
            continue

        line = f"{previous_line} {line}" if previous_line else line  # concatenate lines within a {}

        # find a new entry
        if line.startswith("@"):
            assert previous_line == ""
            ref_type, ref_name = line.split("{")
            entry = {"ref_type": ref_type.replace(',', '').strip()}
            bibs[ref_name.replace(',', '').strip()] = entry
            continue
        else:
            # inside an entry
            assert "=" in line
            if line.count("{") > line.count("}"):
                previous_line = line
                continue
            else:
                previous_line = ""
                key, value = line.split("=", 1)
                entry[key.strip()] = remove_up_to(value.strip(), "{},", 1)

    return bibs


def write_bibtex(bibs, out_file: str):
    with open(out_file, 'w') as f:
        for ref_name, bib in bibs.items():
            f.write(f"{bib.get('ref_type')}{{{ref_name},\n")
            for key in bib:
                if key in ["ref_type", "ref_name"]:
                    continue
                f.write(f"\t{key} = {{{bib[key]}}}")
                if key == list(bib.keys())[-1]:
                    f.write("\n")
                else:
                    f.write(",\n")
            f.write("}\n")


def select_keys(bibs: list):
    for bib in bibs.values():
        for key in list(bib.keys()):
            if key not in ["ref_type"] + selected_keys[bib["ref_type"]]:
                del bib[key]

    return bibs


# TODO: use database to do online check
def online_check(bibs, log_file):
    return bibs


def remove_duplicates(bibs, log_file):
    duplicates = dict()
    for i in range(len(bibs)-1):
        ref_name = list(bibs.keys())[i]
        bib = bibs[ref_name]

        # skip entries already in duplicates
        if any(ref_name in duplicates[dup] for dup in duplicates):
            continue

        dup = {ref_name: []}
        for j in range(i+1, len(bibs)):
            another_ref_name = list(bibs.keys())[j]
            another_bib = bibs[another_ref_name]
            if bib['title'] == another_bib['title']:
                dup[ref_name].append(another_ref_name)
        if dup[ref_name]:
            duplicates.update(dup)

    # actually delete entries
    remove_names = []
    for dup in duplicates.values():
        remove_names.extend(dup)
    for ref_name in remove_names:
        del bibs[ref_name]

    # log the event
    with open(log_file, 'w+') as f:
        for dup in duplicates:
            f.write(f"{dup} <- {duplicates[dup]}\n")

    return bibs


def standard_conference_name(bibs):
    def replace_all(string, chars_in, char_out):
        for char in chars_in:
            string = string.replace(char, char_out)
        return string

    for ref_name, bib in bibs.items():
        if bib['ref_type'] == '@inproceedings':
            key_to_modify = 'booktitle'
        elif bib['ref_type'] == '@article':
            key_to_modify = 'journal'
        else:
            continue

        # ! 从长到短匹配，防止短串匹配到长串的错误
        for brief in sorted(brief_to_full.keys(), key=lambda x: -len(x)):
            if key_to_modify in bib and brief.lower() in replace_all(bib[key_to_modify], "{}", '').lower():
                bib[key_to_modify] = brief_to_full[brief]
                break

    return bibs


def reformat(in_file, out_file, log_file='logs.txt'):
    bibs = read_bibtex(in_file)
    bibs = online_check(bibs, log_file)
    bibs = select_keys(bibs)
    bibs = remove_duplicates(bibs, log_file)
    bibs = standard_conference_name(bibs)

    write_bibtex(bibs, out_file)


if __name__ == "__main__":
    reformat('in.bib', 'out.bib', f'{time.ctime()}.log')
