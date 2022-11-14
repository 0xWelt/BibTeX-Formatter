import itertools
from argparse import ArgumentParser
from seatable_api import Base

SELECTED_KEYS = {
    "@article":
    ["author", "title", "journal", "volume", "number", "pages", "year"],
    "@book": ["author", "title", "publisher", "year"],
    "@inproceedings": ["author", "title", "booktitle", "pages", "year"],
}
STANDARD_NAMES = [
    "AAAI Conference on Artificial Intelligence (AAAI)",
    "ACM Special Interest Group on Data Communication (SIGCOMM)",
    "Advances in Neural Information Processing Systems (NeurIPS)",
    "AIAA Aviation Technology, Integration, and Operations Conference (ATIO)",
    "AIAA Guidance, Navigation, and Control Conference (GNC)",
    "AIAA Infotech@Aerospace Conference",
    "AIAA Journal on Guidance, Control, and Dynamics",
    "Allerton Conference on Communication, Control, and Compution",
    "American Control Conference (ACC)",
    "Annual Conference of the International Speech Communication Association (INTERSPEECH)",
    "Artificial Intelligence",
    "Communications of the ACM",
    "Conference on Empirical Methods in Natural Language Processing (EMNLP)",
    "Conference on Uncertainty in Artificial Intelligence (UAI)",
    "Digital Avionics Systems Conference (DASC)",
    "European Conference on Machine Learning (ECML)",
    "IEEE Aerospace Conference",
    "IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)",
    "IEEE Conference on Decision and Control (CDC)",
    "IEEE Control Systems Magazine",
    "IEEE Intelligent Transportation Systems Conference (ITSC)",
    "IEEE International Conference on Robotics and Automation (ICRA)",
    "IEEE International Conference on Soft Robotics (RoboSoft)"
    "IEEE Transactions on Aerospace and Electronic Systems",
    "IEEE Transactions on Automatic Control",
    "IEEE Transactions on Computational Intelligence and AI in Games",
    "IEEE Transactions on Control Systems Technology",
    "IEEE Transactions on Signal Processing",
    "IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)",
    "International Conference on Acoustics, Speech, and Signal Processing (ICASSP)",
    "International Conference on Agents and Artificial Intelligence (ICAART)",
    "International Conference on Automated Planning and Scheduling (ICAPS)",
    "International Conference on Autonomous Agents and Multiagent Systems (AAMAS)",
    "International Conference on Learning Representations (ICLR)",
    "International Conference on Machine Learning (ICML)",
    "International Conference on Machine Learning and Applications (ICMLA)",
    "International Conference on Spoken Language Processing (ICSLP)",
    "International Conference on Tools and Algorithms for the Construction and Analysis of Systems (TACAS)",
    "International Joint Conference on Artificial Intelligence (IJCAI)",
    "Journal of Aerospace Computing, Information, and Communication",
    "Journal of Artificial Intelligence Research",
    "Journal of Machine Learning Research",
    "Journal of Optimization Theory and Applications",
    "Learning and Intelligent Optimization (LION)",
    "Massachusetts Institute of Technology, Department of Aeronautics and Astronautics",
    "Massachusetts Institute of Technology, Department of Electrical Engineering and Computer Science",
    "Massachusetts Institute of Technology, Department of Mechanical Engineering",
    "Massachusetts Institute of Technology",
    "Mathematics of Operations Research",
    "Operations Research",
    "Robotics: Science and Systems (RSS)",
    "Stanford University, Department of Aeronautics and Astronautics",
    "Stanford University, Department of Electrical Engineering",
    "Stanford University, Department of Mechanical Engineering",
]
REPLACE_THRESHOLD = 0.5  # only replace names with similarity >= threshold


class BibTexFormatter:
    def __init__(self, args) -> None:
        self.args = args

    def format_bibtex(self):
        bibs = self._read_bibtex_from_file(self.args.input)
        bibs = self._remove_duplicates(bibs)

        if not self.args.no_online:
            bibs = self._online_check(bibs)

        bibs = self._select_keys(bibs)
        bibs = self._standardize_names(bibs)

        self._write_bibtex(bibs, self.args.output)

    # ========== Utils ==========
    def _remove_up_to(self, in_string, chars, times):
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

        return in_string[num_to_cut_before:-num_to_cut_after]

    # ========== IO ==========
    def _read_entry_from_lines(self, in_str: str):
        lines = in_str.splitlines()
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
                cite_type, cite_name = line.split("{")
                entry = {"cite_type": cite_type.replace(',', '').strip()}
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
                    entry[key.strip()] = self._remove_up_to(value.strip(), "{},", 1)

        return entry

    def _read_bibtex_from_file(self, in_file: str):
        with open(in_file, 'r') as f:
            lines = f.readlines()

        # add all bibtex entries to a dict with key=cite_name
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
                cite_type, cite_name = line.split("{")
                entry = {"cite_type": cite_type.replace(',', '').strip()}
                bibs[cite_name.replace(',', '').strip()] = entry
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
                    entry[key.strip()] = self._remove_up_to(value.strip(), "{},", 1)

        return bibs

    def _write_bibtex(self, bibs, out_file: str):
        with open(out_file, 'w') as f:
            for cite_name, bib in bibs.items():
                f.write(f"{bib.get('cite_type')}{{{cite_name},\n")
                for key in bib:
                    if key in ["cite_type", "cite_name"]:
                        continue
                    f.write(f"\t{key} = {{{bib[key]}}}")
                    if key == list(bib.keys())[-1]:
                        f.write("\n")
                    else:
                        f.write(",\n")
                f.write("}\n")

    # ========== Formatters ==========
    def _select_keys(self, bibs: list):
        for bib in bibs.values():
            for key in list(bib.keys()):
                if key not in ["cite_type"] + SELECTED_KEYS[bib["cite_type"]]:
                    del bib[key]

        return bibs

    def _online_check(self, bibs):
        """
        Check online database to search latest item
        """
        def auth_table():
            api_token = "8e3a52d6fcb48ab2e27e82d980d2303d759cb86e"
            base = Base(api_token, "https://table.nju.edu.cn")
            base.auth()
            return base

        table = auth_table()
        count = 0
        for bib_key, bib_item in bibs.items():
            bib_type = bib_item['cite_type']
            if (bib_type in ["@article", "@inproceedings"]):
                bib_title = bib_item['title'].replace("'", "\'")
                bib_title = bib_title.replace('"', '\"')
                if ("'" in bib_title) and ('"' in bib_title):
                    sentence = "select bib from BIB where 标题 = '{}'".format(bib_title)
                    continue
                if "'" in bib_title:
                    sentence = 'select bib from BIB where 标题 = "{}"'.format(bib_title)
                else:
                    sentence = "select bib from BIB where 标题 = '{}'".format(bib_title)
                query_result = table.query(sentence)
                if len(query_result) == 1:
                    bibs[bib_key] = self._read_entry_from_lines(query_result[0]['bib'])
                    count += 1
        print(f"Online check coverage:{count / len(bibs)}")
        return bibs

    def _remove_duplicates(self, bibs):
        duplicates = dict()
        for i in range(len(bibs) - 1):
            cite_name = list(bibs.keys())[i]
            bib = bibs[cite_name]

            # skip entries already in duplicates
            if any(cite_name in duplicates[dup] for dup in duplicates):
                continue

            dup = {cite_name: []}
            for j in range(i + 1, len(bibs)):
                another_cite_name = list(bibs.keys())[j]
                another_bib = bibs[another_cite_name]
                if bib['title'] == another_bib['title']:
                    dup[cite_name].append(another_cite_name)
            if dup[cite_name]:
                duplicates.update(dup)

        # actually delete entries
        remove_names = []
        for dup in duplicates.values():
            remove_names.extend(dup)
        for cite_name in remove_names:
            del bibs[cite_name]

        # log the event
        with open(self.args.log, 'w+') as f:
            for dup in duplicates:
                f.write(f"{dup} <- {duplicates[dup]}\n")

        return bibs

    def _standardize_names(self, bibs):

        def preprocess_string(string, chars_in='(){},:', char_out=''):
            for char in chars_in:
                string = string.replace(char, char_out)
            return string.lower().split()

        def lcs(sequence1: list, sequence2: list) -> int:
            """ compute longest common subsequence """
            m, n = len(sequence1), len(sequence2)
            dp = [[0] * (n + 1) for _ in range(m + 1)]

            for i, j in itertools.product(range(1, m + 1), range(1, n + 1)):
                dp[i][j] = dp[i - 1][j - 1] + 1 if sequence1[i - 1] == sequence2[
                    j - 1] else max(dp[i - 1][j], dp[i][j - 1])

            return dp[m][n]

        for cite_name, bib in bibs.items():
            if bib['cite_type'] == '@inproceedings':
                key_to_modify = 'booktitle'
            elif bib['cite_type'] == '@article':
                key_to_modify = 'journal'
            else:
                continue

            if key_to_modify not in bib:
                print(f"Error: {cite_name}   Required key {key_to_modify} not found")
                continue

            max_value, max_id = 0, -1
            for i, std_name in enumerate(STANDARD_NAMES):
                if key_to_modify in bib:
                    value = lcs(preprocess_string(bib[key_to_modify]),
                                preprocess_string(std_name))
                    if value > max_value:
                        max_value = value
                        max_id = i

            # only replace with confidence
            if max_value >= min(
                    len(preprocess_string(bib[key_to_modify])) * REPLACE_THRESHOLD,
                    len(preprocess_string(STANDARD_NAMES[max_id])) *
                    REPLACE_THRESHOLD):
                bib[key_to_modify] = STANDARD_NAMES[max_id]

        return bibs


def main():
    parser = ArgumentParser()
    parser.add_argument('input', type=str, help="input .bib filename", default='in.bib')
    parser.add_argument('-no', '--no_online', help="forbid doing online check", action='store_true')
    
    parser.add_argument('-o', '--output', type=str, help="output .bib filename", default='out.bib')
    parser.add_argument('-l', '--log', type=str, help="output log filename", default='logs.txt')

    args = parser.parse_args()
    formatter = BibTexFormatter(args)
    formatter.format_bibtex()
