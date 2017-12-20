import argparse
import re
import os
from . import document_parser
import simple_cnlp


def fix_missing_summary_final_tag(release_path, port):
    path1 = os.path.join(
        release_path, "data", "test", "duplicate.summaries", "d43hc", "100")
    msg_template = "Could not find summary xml tag for file: {}"
    try:
        summary_data = document_parser.parse_mds_xml(path1, port)
        print("Correctly parsed {}".format(path1))
    except Exception as e:
        if str(e) == msg_template.format(path1):
            print("Fixing broken xml in {}".format(path1))
            with open(path1, "r") as fp:
                broken_xml = fp.read()
                fixed_xml = "{}</SUM>".format(broken_xml)
            with open(path1, "w") as fp:
                fp.write(fixed_xml)
        else:
            raise e

def fix_broken_summary_final_tag(release_path, port):
    path1 = os.path.join(
        release_path, "data", "training", "d35f", "d35ff", "perdocs")

    msg_template = "Error in summary xml {}"

    try: 
        document_parser.parse_perdocs_xml(path1, port)
        print("Correctly parsed {}".format(path1))
    except Exception as e:
        if str(e) == msg_template.format(path1):
            print("Fixing broken xml in {}".format(path1))
            with open(path1, "r") as fp:
                broken_xml = fp.read()
                fixed_xml = re.sub(
                    r'</SUM$', r'</SUM>', broken_xml, flags=re.MULTILINE)
            with open(path1, "w") as fp:
                fp.write(fixed_xml)
        else:
            raise e

def remove_duplicate_file(release_path):
    path1 = os.path.join(
        release_path, "data", "test", "docs", "d05a", "FBIS-41815~")
    if os.path.exists(path1):
        print("Removing duplicate file: {}".format(path1))
        os.remove(path1)
    else:
        print("Already deleted file: {}".format(path1))

def fix_summary_docref_listing(release_path):

    for size in ["100", "200", "400"]:
        path1 = os.path.join(
            release_path, "data", "test", "original.summaries", "d28ee", size)
        with open(path1, "r") as fp:
            xml = fp.read()
        if re.search(r"LA103089-0075", xml):
            print("Replacing bad docref \"LA103089-0075\" with correct " \
                  "docref \"LA050889-0075\"") 
            fixed_xml = re.sub(r"LA103089-0075", r"LA050889-0075", xml)
            with open(path1, "w") as fp:
                fp.write(fixed_xml)
        else:
            print("Already fixed bad docref in {}".format(path1))

        path2 = os.path.join(
            release_path, "data", "test", "original.summaries", "d39gg", size)
        with open(path2, "r") as fp:
            xml = fp.read()
        if re.search(r"FT934-11083 ", xml):
            print("Removing bad docref \"FT934-11083\"") 
            fixed_xml = re.sub(r"FT934-11083 ", r"", xml)
            with open(path2, "w") as fp:
                fp.write(fixed_xml)
        else:
            print("Already fixed bad docref in {}".format(path2))

    path3 = os.path.join(
        release_path, "data", "training", "d09b", "d09bb", "perdocs")
    with open(path3, "r") as fp:
        xml3 = fp.read()
    if re.search(r'SMN91-06154062', xml3):
        print("Replacing bad docref SMN91-06154062 with " \
            "SJMN91-06154062 in {}".format(path3))
        fixed_xml = re.sub(r'SMN91-06154062', r'SJMN91-06154062', xml3)
        with open(path3, "w") as fp:
            fp.write(fixed_xml)
    else:
        print("Already fixed bad docref in {}".format(path3))

    path4 = os.path.join(
        release_path, "data", "training", "d17c", "d17cc", "perdocs")
    with open(path4, "r") as fp:
        xml4 = fp.read()
    if re.search(r'AP870611-0085', xml4):
        print("Replacing bad docref AP870611-0085 with " \
            "WSJ870611-0085 in {}".format(path4))
        fixed_xml = re.sub(r'AP870611-0085', r'WSJ870611-0085', xml4)
        with open(path4, "w") as fp:
            fp.write(fixed_xml)
    else:
        print("Already fixed bad docref in {}".format(path4))

    path5 = os.path.join(
        release_path, "data", "training", "d23d", "d23dd", "perdocs")
    with open(path5, "r") as fp:
        xml5 = fp.read()
    if re.search(r'SJMN91-0605144', xml5):
        print("Replacing bad docref SJMN91-0605144 with " \
            "SJMN91-06015144 in {}".format(path5))
        fixed_xml5 = re.sub(r'SJMN91-0605144', r'SJMN91-06015144', xml5)
        with open(path5, "w") as fp:
            fp.write(fixed_xml5)
    else:
        print("Already fixed bad docref in {}".format(path5))

    path6 = os.path.join(
        release_path, "data", "training", "d38g", "d38gg", "perdocs")
    with open(path6, "r") as fp:
        xml6 = fp.read()
    if re.search(r'APP890515-0232', xml6):
        print("Replacing bad docref APP890515-0232 with " \
            "AP890515-0232 in {}".format(path6))
        fixed_xml6 = re.sub(r'APP890515-0232', r'AP890515-0232', xml6)
        with open(path6, "w") as fp:
            fp.write(fixed_xml6)
    else:
        print("Already fixed bad docref in {}".format(path6))

    path7 = os.path.join(
        release_path, "data", "training", "d49i", "d49ii", "perdocs")
    with open(path7, "r") as fp:
        xml7 = fp.read()
    if re.search(r'WSJ891125-0090', xml7):
        print("Replacing bad docref WSJ891125-0090 with " \
            "AP891125-0090 in {}".format(path7))
        fixed_xml7 = re.sub(r'WSJ891125-0090', r'AP891125-0090', xml7)
        with open(path7, "w") as fp:
            fp.write(fixed_xml7)
    else:
        print("Already fixed bad docref in {}".format(path7))

    path8 = os.path.join(
        release_path, "data", "training", "d49i", "d49ii", "perdocs")
    with open(path8, "r") as fp:
        xml8 = fp.read()
    if re.search(r'FT931-100514', xml8):
        print("Replacing bad docref FT931-100514 with " \
            "FT931-10514 in {}".format(path8))
        fixed_xml8 = re.sub(r'FT931-100514', r'FT931-10514', xml8)
        with open(path8, "w") as fp:
            fp.write(fixed_xml8)
    else:
        print("Already fixed bad docref in {}".format(path8))

    path9 = os.path.join(
        release_path, "data", "training", "d55k", "d55kk", "perdocs")
    with open(path9, "r") as fp:
        xml9 = fp.read()
    if re.search(r'FB153-57782', xml9):
        print("Replacing bad docref FB153-57782 with " \
            "FBIS3-57782 in {}".format(path9))
        fixed_xml9 = re.sub(r'FB153-57782', r'FBIS3-57782', xml9)
        with open(path9, "w") as fp:
            fp.write(fixed_xml9)
    else:
        print("Already fixed bad docref in {}".format(path9))

    path10 = os.path.join(
        release_path, "data", "test", "duplicate.summaries", "d05ac", 
        "perdocs")
    with open(path10, "r") as fp:
        xml10 = fp.read()
    if re.search(r'FBIS4-35908', xml10):
        print("Replacing bad docref FBIS4-35908 with " \
            "FBIS4-45908 in {}".format(path10))
        fixed_xml10 = re.sub(r'FBIS4-35908', r'FBIS4-45908', xml10)
        with open(path10, "w") as fp:
            fp.write(fixed_xml10)
    else:
        print("Already fixed bad docref in {}".format(path10))

    path11 = os.path.join(
        release_path, "data", "test", "original.summaries", "d59kk", 
        "perdocs")
    with open(path11, "r") as fp:
        xml11 = fp.read()
    if re.search(r'LA081489-0225', xml11):
        print("Replacing bad docref LA081489-0225 with " \
            "LA081489-0025 in {}".format(path11))
        fixed_xml11 = re.sub(r'LA081489-0225', r'LA081489-0025', xml11)
        with open(path11, "w") as fp:
            fp.write(fixed_xml11)
    else:
        print("Already fixed bad docref in {}".format(path11))

def remove_summary_with_missing_document(release_path):
    path1 = os.path.join(
        release_path, "data", "test", "original.summaries", "d31ff", 
        "perdocs")
    with open(path1, "r") as fp:
        xml1 = fp.read()
    if re.search(r'LA0902789-0067', xml1):
        print("Removing summary for missing documents LA0902789-0067.")
        fixed_xml1 = re.sub(
            r'<SUM.*?DOCREF="LA0902789-0067".*?</SUM>',
            r'',
            xml1,
            flags=re.DOTALL)
        with open(path1, "w") as fp:
            fp.write(fixed_xml1)
    else:
        print("Already removed bad summary in {}".format(path1))

    path2 = os.path.join(
        release_path, "data", "test", "original.summaries", "d31ff", 
        "perdocs")
    with open(path2, "r") as fp:
        xml2 = fp.read()
    if re.search(r'AP880927-0092', xml2):
        print("Removing summary for missing documents AP880927-0092.")
        fixed_xml2 = re.sub(
            r'<SUM.*?DOCREF="AP880927-0092".*?</SUM>',
            r'',
            xml2,
            flags=re.DOTALL)
        with open(path2, "w") as fp:
            fp.write(fixed_xml2)
    else:
        print("Already removed bad summary in {}".format(path2))

    path3 = os.path.join(
        release_path, "data", "test", "original.summaries", "d31ff", 
        "perdocs")
    with open(path3, "r") as fp:
        xml3 = fp.read()
    if re.search(r'LA051189-0216', xml3):
        print("Removing summary for missing documents LA051189-0216.")
        fixed_xml3 = re.sub(
            r'<SUM.*?DOCREF="LA051189-0216".*?</SUM>',
            r'',
            xml3,
            flags=re.DOTALL)
        with open(path3, "w") as fp:
            fp.write(fixed_xml3)
    else:
        print("Already removed bad summary in {}".format(path3))

def run_repairs(release_data_path, port):
    fix_missing_summary_final_tag(release_data_path, port)
    fix_broken_summary_final_tag(release_data_path, port)
    remove_duplicate_file(release_data_path)
    fix_summary_docref_listing(release_data_path)
    remove_summary_with_missing_document(release_data_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--release-data", type=str, required=True)
    parser.add_argument("--corenlp-port", type=int, default=9000)
    args = parser.parse_args()

    with simple_cnlp.Session(port=args.corenlp_port) as session: 
        run_repairs(args.release_data, args.corenlp_port)

if __name__ == "__main__":
    main()
