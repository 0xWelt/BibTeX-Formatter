import itertools
from argparse import ArgumentParser
from seatable_api import Base

CITE_TYPES = ["@article", "@book", "@inproceedings", "comment"]
SELECTED_KEYS = {
    "@article": ["author", "title", "journal", "volume", "pages", "year"],  # , "number"
    "@book": ["author", "title", "publisher", "year"],
    "@inproceedings": ["author", "title", "booktitle", "pages", "year"],
}
# keep this alphabetically
STANDARD_NAMES = [
    "AAAI Conference on Artificial Intelligence",
    "ACM Special Interest Group on Data Communication",
    "Advances in Neural Information Processing Systems",
    "AIAA Aviation Technology, Integration, and Operations Conference",
    "AIAA Guidance, Navigation, and Control Conference",
    "AIAA Journal on Guidance, Control, and Dynamics",
    "Allerton Conference on Communication, Control, and Compution",
    "American Control Conference",
    "Annual Conference of the International Speech Communication Association",
    "Artificial Intelligence",
    "Canadian Journal of Electrical and Computer Engineering",
    "Communications of the ACM",
    "Computer",
    "Computing in Science & Engineering",
    "Conference on Empirical Methods in Natural Language Processing",
    "Conference on Uncertainty in Artificial Intelligence",
    "Digital Avionics Systems Conference",
    "European Conference on Machine Learning",
    "IEEE Access",
    "IEEE Aerospace & Electronics Systems Magazine",
    "IEEE Aerospace Conference",
    "IEEE Annals of the History of Computing",
    "IEEE Antennas & Propagation Magazine",
    "IEEE Antennas and Wireless Propagation Letters",
    "IEEE Biometrics Compendium",
    "IEEE Circuits & Devices Magazine",
    "IEEE Circuits and Systems Magazine",
    "IEEE Communications Letters",
    "IEEE Communications Magazine",
    "IEEE Communications Surveys and Tutorials",
    "IEEE Computational Intelligence magazine",
    "IEEE Computer Architecture Letters",
    "IEEE Computer Graphics and Applications",
    "IEEE Computer Society Conference on Computer Vision and Pattern Recognition",
    "IEEE Conference on Decision and Control",
    "IEEE Consumer Electronics Magazine",
    "IEEE Control Systems Magazine",
    "IEEE Design & Test of Computers",
    "IEEE Distributed Systems Online",
    "IEEE Electrical Insulation Magazine",
    "IEEE Electron Device Letters",
    "IEEE Embedded Systems Letters",
    "IEEE Engineering in Medicine & Biology Magazine",
    "IEEE Engineering Management Review",
    "IEEE Geoscience and Remote Sensing Letters",
    "IEEE Industrial Electronics Magazine",
    "IEEE Industry Applications Magazine",
    "IEEE Instrumentation & Measurement Magazine",
    "IEEE Intelligent Systems",
    "IEEE Intelligent Transportation Systems Conference",
    "IEEE Intelligent Transportation Systems Magazine",
    "IEEE International Conference on Robotics and Automation",
    "IEEE International Conference on Soft Robotics"
    "IEEE Internet Computing",
    "IEEE Journal of Biomedical and Health Informatics",
    "IEEE Journal of Emerging and Selected Topics in Circuits and Systems",
    "IEEE Journal of Oceanic Engineering",
    "IEEE Journal of Photovoltaics",
    "IEEE Journal of Quantum Electronics",
    "IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing",
    "IEEE Journal of Selected Topics in Quantum Electronics",
    "IEEE Journal of Selected Topics in Signal Processing",
    "IEEE Journal of Solid-State Circuits",
    "IEEE Journal on Project Safety Engineering",
    "IEEE Journal on Selected Areas in Communications",
    "IEEE Latin America Transactions",
    "IEEE Magnetics Letters",
    "IEEE Micro",
    "IEEE Microwave and Wireless Components Letters",
    "IEEE Microwave Magazine",
    "IEEE MultiMedia",
    "IEEE Nanotechnology Magazine",
    "IEEE Network",
    "IEEE Open Journal of Circuits and Systems",
    "IEEE Pervasive Computing",
    "IEEE Photonics Journal",
    "IEEE Photonics Technology Letters",
    "IEEE Potentials",
    "IEEE Power & Energy Magazine",
    "IEEE Power Electronics Letters",
    "IEEE Pulse",
    "IEEE Reviews in Biomedical Engineering",
    "IEEE Robotics & Automation Magazine",
    "IEEE Security & Privacy Magazine",
    "IEEE Sensors Journal",
    "IEEE Signal Processing Letters",
    "IEEE Signal Processing Magazine",
    "IEEE Software",
    "IEEE Solid State Circuits Magazine",
    "IEEE Spectrum",
    "IEEE Systems Journal",
    "IEEE Technology & Society Magazine",
    "IEEE Transactions on Advanced Packaging",
    "IEEE Transactions on Aerospace and Electronic Systems",
    "IEEE Transactions on Affective Computing",
    "IEEE Transactions on Antennas and Propagation",
    "IEEE Transactions on Applied Superconductivity",
    "IEEE Transactions on Artificial Intelligence",
    "IEEE Transactions on Audio and Electroacoustic",
    "IEEE Transactions on Audio, Speech, and Language Processing",
    "IEEE Transactions on Automatic Control",
    "IEEE Transactions on Automation Science and Engineering",
    "IEEE Transactions on Autonomous Mental Development",
    "IEEE Transactions on Big Data",
    "IEEE Transactions on Biomedical Circuits and Systems",
    "IEEE Transactions on Biomedical Engineering",
    "IEEE Transactions on Biometrics, Behavior, and Identity Science",
    "IEEE Transactions on Broadcasting",
    "IEEE Transactions on Cable Television",
    "IEEE Transactions on Circuit Theory",
    "IEEE Transactions on Circuits and Systems for Video Technology",
    "IEEE Transactions on Circuits and Systems I: Regular Papers",
    "IEEE Transactions on Circuits and Systems II: Express Briefs",
    "IEEE Transactions on Cloud Computing",
    "IEEE Transactions on Cognitive and Developmental Systems",
    "IEEE Transactions on Cognitive Communications and Networking",
    "IEEE Transactions on Communications",
    "IEEE Transactions on Components and Packaging Technologies",
    "IEEE Transactions on Computational Intelligence and AI in Games",
    "IEEE Transactions on Computational Social Systems",
    "IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems",
    "IEEE Transactions on Computers",
    "IEEE Transactions on Consumer Electronics",
    "IEEE Transactions on Control Systems Technology",
    "IEEE Transactions on Dependable and Secure Computing",
    "IEEE Transactions on Device and Materials Reliability",
    "IEEE Transactions on Dielectrics and Electrical Insulation",
    "IEEE Transactions on Education",
    "IEEE Transactions on Electromagnetic Compatibility",
    "IEEE Transactions on Electron Devices",
    "IEEE Transactions on Electronics Packaging Manufacturing",
    "IEEE Transactions on Emerging Topics on Computing",
    "IEEE Transactions on Energy Conversion",
    "IEEE Transactions on Engineering Management",
    "IEEE Transactions on Evolutionary Computation",
    "IEEE Transactions on Fuzzy Systems",
    "IEEE Transactions on Games",
    "IEEE Transactions on Geoscience and Remote Sensing",
    "IEEE Transactions on Haptics",
    "IEEE Transactions on Image Processing",
    "IEEE Transactions on Industrial Electronics",
    "IEEE Transactions on Industrial Informatics",
    "IEEE Transactions on Industry Applications",
    "IEEE Transactions on Information Forensics and Security",
    "IEEE Transactions on Information Technology in Biomedicine",
    "IEEE Transactions on Information Theory",
    "IEEE Transactions on Instrumentation and Measurement",
    "IEEE Transactions on Intelligent Transportation Systems",
    "IEEE Transactions on Knowledge and Data Engineering",
    "IEEE Transactions on Learning Technologies",
    "IEEE Transactions on Magnetics",
    "IEEE Transactions on Manufacturing Technology",
    "IEEE Transactions on Medical Imaging",
    "IEEE Transactions on Microwave Theory and Techniques",
    "IEEE Transactions on Mobile Computing",
    "IEEE Transactions on Multimedia",
    "IEEE Transactions on Nanobioscience",
    "IEEE Transactions on Nanotechnology",
    "IEEE Transactions on Network and Service Management",
    "IEEE Transactions on Network Science and Engineering",
    "IEEE Transactions on Neural Networks and Learning Systems",
    "IEEE Transactions on Neural Systems and Rehabilitation Engineering",
    "IEEE Transactions on Nuclear Science",
    "IEEE Transactions on Parallel and Distributed Systems",
    "IEEE Transactions on Pattern Analysis and Machine Intelligence",
    "IEEE Transactions on Plasma Science",
    "IEEE Transactions on Power Delivery",
    "IEEE Transactions on Power Electronics",
    "IEEE Transactions on Power Systems",
    "IEEE Transactions on Professional Communication",
    "IEEE Transactions on Quantum Engineering",
    "IEEE Transactions on Reliability",
    "IEEE Transactions on Robotics",
    "IEEE Transactions on Semiconductor Manufacturing",
    "IEEE Transactions on Services Computing",
    "IEEE Transactions on Signal Processing",
    "IEEE Transactions on Smart Grid",
    "IEEE Transactions on Software Engineering",
    "IEEE Transactions on Sustainable Energy",
    "IEEE Transactions on Systems, Man and Cybernetics",
    "IEEE Transactions on Terahertz Science and Technology",
    "IEEE Transactions on Ultrasonics, Ferroelectrics and Frequency Control",
    "IEEE Transactions on Vehicular Technology",
    "IEEE Transactions on Very Large Scale Integration (VLSI) Systems",
    "IEEE Transactions on Visualization and Computer Graphics",
    "IEEE Transactions on Wireless Communications",
    "IEEE Vehicular Technology Magazine",
    "IEEE Wireless Communications Letters",
    "IEEE Wireless Communications",
    "IEEE Women in Engineering Magazine",
    "IEEE/ACM Transactions on Computational Biology and Bioinformatics",
    "IEEE/ACM Transactions on Networking",
    "IEEE/ASME Transactions on Mechatronics",
    "IEEE/CAA Journal of Automatica Sinica",
    "IEEE/OSA Journal of Optical Communications and Networking",
    "IEEE/RSJ International Conference on Intelligent Robots and Systems",
    "IEEE/TMS Journal of Electronic Materials",
    "International Conference on Acoustics, Speech, and Signal Processing",
    "International Conference on Agents and Artificial Intelligence",
    "International Conference on Automated Planning and Scheduling",
    "International Conference on Autonomous Agents and Multiagent Systems",
    "International Conference on Learning Representations",
    "International Conference on Machine Learning and Applications",
    "International Conference on Machine Learning",
    "International Conference on Spoken Language Processing",
    "International Conference on Tools and Algorithms for the Construction and Analysis of Systems",
    "International Joint Conference on Artificial Intelligence",
    "IT Professional",
    "Journal of Aerospace Computing, Information, and Communication",
    "Journal of Artificial Intelligence Research",
    "Journal of Autonomous Agents and Multi-Agent Systems",
    "Journal of Display Technology",
    "Journal of Economic Theory",
    "Journal of Intelligent Information Systems",
    "Journal of Lightwave Technology",
    "Journal of Machine Learning Research",
    "Journal of Microelectromechanical Systems",
    "Journal of Optimization Theory and Applications",
    "Learning and Intelligent Optimization",
    "Machine Learning",
    "Massachusetts Institute of Technology, Department of Aeronautics and Astronautics",
    "Massachusetts Institute of Technology, Department of Electrical Engineering and Computer Science",
    "Massachusetts Institute of Technology, Department of Mechanical Engineering",
    "Massachusetts Institute of Technology",
    "Mathematics of Operations Research",
    "Nature",
    "Neural Computing and Applications",
    "Operations Research",
    "Proceedings of the IEEE",
    "Robotics: Science and Systems",
    "Stanford University, Department of Aeronautics and Astronautics",
    "Stanford University, Department of Electrical Engineering",
    "Stanford University, Department of Mechanical Engineering",
]
REPLACE_THRESHOLD_RAW = 0.2  # only replace names with "similarity of raw" >= threshold
REPLACE_THRESHOLD_STD = 0.7  # only replace names with "similarity of standard" >= threshold


class BibEntry:
    def __init__(self, type: str, name: str):
        self.type = type
        self.name = name
        self.fields = {}

    def __repr__(self):
        return self.name

    def make_string(self) -> str:
        if self.type == "comment":
            return f"{self.name}\n"

        entry_string = f"{self.type}{{{self.name},\n"
        for key in sorted(self.fields):
            entry_string += f"  {key} = {{{self.fields[key]}}},\n"
        entry_string += "}\n"
        return entry_string


class BibTexFormatter:
    def __init__(self, args) -> None:
        self.args = args

    def format_bibtex(self):
        # read .bib file
        bibs = self._read_bibtex_from_file(self.args.input)

        # process bibtex entries
        with open(self.args.log, 'w') as f:
            pass
        bibs = self._remove_duplicates(bibs)
        # if self.args.use_database:
        #     bibs = self._online_check(bibs)
        bibs = self._format_arXiv(bibs)
        bibs = self._standardize_names(bibs)
        bibs = self._standardize_pages(bibs)
        bibs = self._select_keys(bibs)

        # write .bib file
        self._write_bibtex(bibs, self.args.output)
        with open(self.args.log, 'r') as f:
            print(f.read())

    # ====================== Utils ======================
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

    # ====================== IO ======================
    # def _read_entry_from_lines(self, in_str: str):
    #     lines = in_str.splitlines()
    #     previous_line = ""
    #     for line in lines:
    #         # skip comments and empty lines
    #         line = line.strip()
    #         if not line or line.startswith("%") or line.startswith("}"):
    #             continue

    #         # concatenate lines within a {}
    #         line = f"{previous_line} {line}" if previous_line else line

    #         # find a new entry
    #         if line.startswith("@"):
    #             assert previous_line == ""
    #             cite_type, cite_name = line.split("{")
    #             entry = {"cite_type": cite_type.replace(',', '').strip()}
    #             continue
    #         else:
    #             # inside an entry
    #             assert "=" in line
    #             if line.count("{") > line.count("}"):
    #                 previous_line = line
    #                 continue
    #             else:
    #                 previous_line = ""
    #                 key, value = line.split("=", 1)
    #                 entry[key.strip()] = self._remove_up_to(
    #                     value.strip(), "{},", 1)

    #     return entry

    def _read_bibtex_from_file(self, in_file: str):
        with open(in_file, 'r') as f:
            lines = f.readlines()

        # add all bibtex entries to a dict with key=cite_name
        bibs = []
        previous_line = ""
        for line in lines:
            # skip empty lines
            line = line.strip()
            if not line or line.startswith("}"):
                continue

            # for comment
            if line.startswith("%"):
                bib = BibEntry("comment", line)
                bibs.append(bib)
                continue

            # concatenate lines within a {}
            line = f"{previous_line} {line}" if previous_line else line

            # find a new entry
            if line.startswith("@"):
                assert previous_line == ""
                cite_type, cite_name = line.split("{")
                bib = BibEntry(cite_type.replace(',', '').strip(), cite_name.replace(',', '').strip())
                bibs.append(bib)
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
                    bib.fields[key.strip()] = self._remove_up_to(value.strip(), "{},", 1)

        return bibs

    def _write_bibtex(self, bibs, out_file: str):
        with open(out_file, 'w') as f:
            for bib in bibs:
                f.write(bib.make_string())

    # ====================== Formatters (order matters) ======================
    def _remove_duplicates(self, bibs):
        duplicates = {}
        for i, bib in enumerate(bibs[:-1]):
            # skip entries with no title (comment) || already in duplicates
            if "title" not in bib.fields or any(bib.name in duplicates[dup] for dup in duplicates):
                continue

            dup = [bib2 for bib2 in bibs[i + 1:] if "title" in bib2.fields and bib.fields['title'] == bib2.fields['title']]
            if dup:
                duplicates[bib] = dup

        # actually delete entries
        remove_bibs = []
        for dup in duplicates.values():
            remove_bibs.extend(dup)
        for bib in remove_bibs:
            bibs.remove(bib)

        # log the event
        if duplicates:
            with open(self.args.log, 'w') as f:
                f.write("=============== Found Duplicate ===============\n")
                for dup, value in duplicates.items():
                    f.write(f"{dup} <- {value}\n")
                f.write("\n")

        return bibs

    # def _online_check(self, bibs):
    #     """
    #     Check online database to search latest item
    #     """
    #     def auth_table():
    #         api_token = "8e3a52d6fcb48ab2e27e82d980d2303d759cb86e"
    #         base = Base(api_token, "https://table.nju.edu.cn")
    #         base.auth()
    #         return base

    #     print("Scanning database...")

    #     table = auth_table()
    #     count = 0
    #     for bib_key, bib_item in bibs.items():
    #         bib_type = bib_item['cite_type']
    #         if (bib_type in ["@article", "@inproceedings"]):
    #             bib_title = bib_item['title'].replace("'", "\'")
    #             bib_title = bib_title.replace('"', '\"')
    #             if ("'" in bib_title) and ('"' in bib_title):
    #                 sentence = "select bib from BIB where 标题 = '{}'".format(
    #                     bib_title)
    #                 continue
    #             if "'" in bib_title:
    #                 sentence = 'select bib from BIB where 标题 = "{}"'.format(
    #                     bib_title)
    #             else:
    #                 sentence = "select bib from BIB where 标题 = '{}'".format(
    #                     bib_title)
    #             query_result = table.query(sentence)
    #             if len(query_result) == 1:
    #                 bibs[bib_key] = self._read_entry_from_lines(
    #                     query_result[0]['bib'])
    #                 count += 1
    #     print(f"Online check coverage:{count / len(bibs)}")
    #     return bibs

    def _format_arXiv(self, bibs):
        for bib in bibs:
            if bib.type == "@article":
                # 1. google style, keep the same
                if "arXiv" in bib.fields["journal"]:
                    continue
                # 2. arXiv dblp style, convert to google style
                if "CoRR" in bib.fields["journal"]:
                    vol = bib.fields["volume"].replace("abs/", "")
                    bib.fields["journal"] = f"arXiv preprint arXiv:{vol}"
            # 3. arXiv API export style, convert to google style
            if bib.type == "@misc":
                bib.type = "@article"
                bib.fields['journal'] = f"arXiv preprint arXiv:{bib.fields['eprint']}"

        return bibs

    def _standardize_names(self, bibs):

        def preprocess_string(string, chars_in='(){},:.', char_out=''):
            for char in chars_in:
                string = string.replace(char, char_out)
            return string.lower().split()

        def same_name(in_str, ref_str, mode='fuzzy'):
            if mode == "fuzzy":
                return ref_str.startswith(in_str)
            elif mode == 'precise':
                return in_str == ref_str

        def lcs(input: list, reference: list) -> int:
            """ compute longest common subsequence """
            m, n = len(input), len(reference)
            dp = [[0] * (n + 1) for _ in range(m + 1)]

            for i, j in itertools.product(range(1, m + 1), range(1, n + 1)):
                dp[i][j] = dp[i - 1][j - 1] + 1 if same_name(
                    input[i - 1], reference[j - 1]) else max(dp[i - 1][j], dp[i][j - 1])

            return dp[m][n]

        for bib in bibs:
            if bib.type == '@inproceedings':
                key_to_modify = 'booktitle'
            elif bib.type == '@article':
                key_to_modify = 'journal'
                if "arXiv" in bib.fields["journal"]:
                    continue
            else:
                continue

            if key_to_modify not in bib.fields:
                continue

            records = []  # (index, abs_value, rel_raw, rel_std)
            for i, std_name in enumerate(STANDARD_NAMES):
                abs_value = lcs(preprocess_string(bib.fields[key_to_modify]), preprocess_string(std_name))
                relative_values_raw = abs_value / len(preprocess_string(bib.fields[key_to_modify]))
                relative_values_std = abs_value / len(preprocess_string(std_name))
                records.append((i, abs_value, relative_values_raw, relative_values_std))
            records.sort(key=lambda x: (x[2], x[3]), reverse=True)

            # only replace with confidence
            max_id, max_abs, max_raw, max_std = records[0]
            if max_raw >= REPLACE_THRESHOLD_RAW and max_std >= REPLACE_THRESHOLD_STD:
                bib.fields[key_to_modify] = STANDARD_NAMES[max_id]

        return bibs

    def _standardize_pages(self, bibs):
        # log wrong pages
        wrong_pages = {}

        for bib in bibs:
            if "pages" in bib.fields:
                bib.fields["pages"] = bib.fields["pages"].replace("--", "-")
                if bib.fields["pages"].count("-") != 1:
                    wrong_pages[bib.name] = bib.fields["pages"]

        if wrong_pages:
            with open(self.args.log, 'a') as f:
                f.write(f"=============== Found Wrong Pages ===============\n")
                for name, pages in wrong_pages.items():
                    f.write(f"{name}: {pages}\n")
                f.write("\n")

        return bibs

    def _select_keys(self, bibs: list):
        # log missing
        missing_keys = {}
        missing_keys_count = {}

        for bib in bibs:
            if bib.type not in SELECTED_KEYS:
                continue

            needed_keys = SELECTED_KEYS[bib.type].copy()
            # ICLR has no pages
            if bib.type == "@inproceedings" and bib.fields["booktitle"] == "International Conference on Learning Representations":
                needed_keys.remove("pages")
            # Google stgle arXiv only have these keys
            if bib.type == "@article" and "arXiv" in bib.fields["journal"]:
                needed_keys = ["title", "journal", "year", "author"]

            # remove redundent keys
            for key in list(bib.fields.keys()):
                if key not in needed_keys:
                    del bib.fields[key]

            # mark missing keys
            for key in needed_keys:
                if key not in bib.fields:
                    bib.fields[key] = ""
                if bib.fields[key] == "":
                    missing_keys[bib.name] = missing_keys.get(bib.name, [])
                    missing_keys[bib.name].append(key)
                    missing_keys_count[key] = missing_keys_count.get(key, 0) + 1

        if missing_keys:
            with open(self.args.log, 'a') as f:
                f.write(f"=============== Found Missing ===============\n")
                f.write(f"{missing_keys_count}\n")
                for name, miss in missing_keys.items():
                    f.write(f"{name}: {miss}\n")
                f.write("\n")

        return bibs


def main():
    parser = ArgumentParser()
    parser.add_argument('input', type=str,
                        help="input .bib filename", default='in.bib')
    parser.add_argument('-d', '--use_database',
                        help="doing online check with database", action='store_true')

    parser.add_argument('-o', '--output', type=str,
                        help="output .bib filename", default='out.bib')
    parser.add_argument('-l', '--log', type=str,
                        help="output log filename", default='logs.txt')

    args = parser.parse_args()
    formatter = BibTexFormatter(args)
    formatter.format_bibtex()
