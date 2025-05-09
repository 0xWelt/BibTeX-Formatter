import itertools
import os
from argparse import ArgumentParser

from seatable_api import Base

CITE_TYPES = ["@article", "@book", "@inproceedings", "comment"]
SELECTED_KEYS = {
    "@article": ["author", "title", "journal", "volume", "pages", "year"],  # , "number"
    "@book": ["author", "title", "publisher", "year"],
    "@inproceedings": ["author", "title", "booktitle", "pages", "year"],
}
# keep this alphabetically
STANDARD_NAMES = []
REPLACE_THRESHOLD_RAW = 0.2  # only replace names with "similarity of raw" >= threshold
REPLACE_THRESHOLD_STD = (
    0.7  # only replace names with "similarity of standard" >= threshold
)


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
        with open(self.args.log, "w", encoding="utf-8") as f:
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
        with open(self.args.log, "r", encoding="utf-8") as f:
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
        with open(in_file, "r", encoding="utf-8") as f:
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
                bib = BibEntry(
                    cite_type.replace(",", "").strip().lower(),
                    cite_name.replace(",", "").strip(),
                )
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
                    bib.fields[key.strip()] = self._remove_up_to(
                        value.strip(), "{},", 1
                    )

        return bibs

    def _write_bibtex(self, bibs, out_file: str):
        with open(out_file, "w", encoding="utf-8") as f:
            for bib in bibs:
                f.write(bib.make_string())

    # ====================== Formatters (order matters) ======================
    def _remove_duplicates(self, bibs):
        duplicates = {}
        for i, bib in enumerate(bibs[:-1]):
            # skip entries with no title (comment) || already in duplicates
            if "title" not in bib.fields or any(
                bib.name in duplicates[dup] for dup in duplicates
            ):
                continue

            dup = [
                bib2
                for bib2 in bibs[i + 1 :]
                if "title" in bib2.fields
                and bib.fields["title"] == bib2.fields["title"]
            ]
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
            with open(self.args.log, "w", encoding="utf-8") as f:
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
                if "journal" not in bib.fields:
                    print(f"Fatal Error: {bib} missing key 'journal'")
                    quit()
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
                bib.fields["journal"] = f"arXiv preprint arXiv:{bib.fields['eprint']}"

        return bibs

    def _standardize_names(self, bibs):
        def preprocess_string(string, chars_in="(){},:.", char_out=""):
            for char in chars_in:
                string = string.replace(char, char_out)
            return string.lower().split()

        def same_name(in_str, ref_str, mode="fuzzy"):
            if mode == "fuzzy":
                return ref_str.startswith(in_str)
            elif mode == "precise":
                return in_str == ref_str

        def lcs(input: list, reference: list) -> int:
            """compute longest common subsequence"""
            m, n = len(input), len(reference)
            dp = [[0] * (n + 1) for _ in range(m + 1)]

            for i, j in itertools.product(range(1, m + 1), range(1, n + 1)):
                dp[i][j] = (
                    dp[i - 1][j - 1] + 1
                    if same_name(input[i - 1], reference[j - 1])
                    else max(dp[i - 1][j], dp[i][j - 1])
                )

            return dp[m][n]

        for bib in bibs:
            if bib.type == "@inproceedings":
                key_to_modify = "booktitle"
            elif bib.type == "@article":
                key_to_modify = "journal"
                if "arXiv" in bib.fields["journal"]:
                    continue
            else:
                continue

            if key_to_modify not in bib.fields:
                continue

            records = []  # (index, abs_value, rel_raw, rel_std)
            for i, std_name in enumerate(STANDARD_NAMES):
                abs_value = lcs(
                    preprocess_string(bib.fields[key_to_modify]),
                    preprocess_string(std_name),
                )
                relative_values_raw = abs_value / len(
                    preprocess_string(bib.fields[key_to_modify])
                )
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
            with open(self.args.log, "a", encoding="utf-8") as f:
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
            if (
                bib.type == "@inproceedings"
                and bib.fields["booktitle"]
                == "International Conference on Learning Representations"
            ):
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
            with open(self.args.log, "a", encoding="utf-8") as f:
                f.write(f"=============== Found Missing ===============\n")
                f.write(f"{missing_keys_count}\n")
                for name, miss in missing_keys.items():
                    f.write(f"{name}: {miss}\n")
                f.write("\n")

        return bibs


def main():
    parser = ArgumentParser()
    parser.add_argument("input", type=str, help="input .bib filename", default="in.bib")
    parser.add_argument(
        "-d",
        "--use_database",
        help="doing online check with database",
        action="store_true",
    )

    parser.add_argument(
        "-o", "--output", type=str, help="output .bib filename", default="out.bib"
    )
    parser.add_argument(
        "-l", "--log", type=str, help="output log filename", default="logs.txt"
    )
    args = parser.parse_args()

    # make STANDARD_NAMES
    root = os.path.dirname(os.path.abspath(__file__))
    for file_name in os.listdir(os.path.join(root, "data")):
        if file_name.endswith(".txt"):
            with open(
                os.path.join(root, "data", file_name), "r", encoding="utf-8"
            ) as f:
                for line in f:
                    if not line.startswith("#"):
                        STANDARD_NAMES.append(line.strip())

    formatter = BibTexFormatter(args)
    formatter.format_bibtex()
