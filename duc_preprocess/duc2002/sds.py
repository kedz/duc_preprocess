import os
import re
import json
import argparse
from . import document_parser
import spacy


def validate_directory(path):
    if path != "" and not os.path.exists(path):
        os.makedirs(path)

def get_summaries(eval_root_path, nlp):

    summary_dir = os.path.join(eval_root_path, "summaries", "summaries")

    id2summaries = {}

    for fn in os.listdir(summary_dir):
        match = re.search("^(d\d+[a-z])[a-z]$", fn)
        if match is None:
            continue
        docset = match.groups()[0]
        print(docset, fn)
        summary_path = os.path.join(summary_dir, fn, "perdocs")
        if not os.path.exists(summary_path):
            continue
        summaries = document_parser.parse_perdocs_xml(summary_path, nlp)
        for doc_id, summary in summaries.items():
            key = (docset, doc_id)
            if key not in id2summaries:
                id2summaries[key] = []
            id2summaries[key].append(summary)
    for docset_id, doc_id in id2summaries.keys():
        print("Found {} summaries for doc {} {}".format(
            len(id2summaries[(docset_id, doc_id)]), docset_id, doc_id))
    print("Found at least 1 summary for {} docsets".format(len(id2summaries)))

    return id2summaries

def get_inputs(release_root_path, nlp):

    docset_ids = os.listdir(os.path.join(release_root_path, "docs"))

    id2input_data = {}
    for docset_id in docset_ids:
        print(docset_id)
        docset_dir = os.path.join(release_root_path, "docs", docset_id)
        input_paths = [os.path.join(docset_dir, fn)
                       for fn in os.listdir(docset_dir)]
        docs = document_parser.parse_input_docs(input_paths, nlp)
        for doc in docs:
            input_data = []
            for s, sentence in enumerate(doc["sentences"], 1):
                input_data.append({
                    "docset_id": docset_id,
                    "doc_id": doc["doc_id"],
                    "date": str(doc["date"]),
                    "sentence_id": s,
                    "text": sentence["text"],
                    "pos": sentence["pos"],
                    "ne": sentence["ne"],
                    "tokens": sentence["tokens"]})

            id2input_data[(docset_id, doc["doc_id"])] = input_data

    return id2input_data

def extract_sds_data(document_release_data_path, summary_release_data_path,
                     output_dir, nlp=None):
    if nlp is None:
        nlp = spacy.load('en', parser=False)

    summary_dir = os.path.join(output_dir, "targets")
    validate_directory(summary_dir)
    inputs_dir = os.path.join(output_dir, "inputs")
    validate_directory(inputs_dir)

    id2summaries = get_summaries(summary_release_data_path, nlp)
    id2inputs = get_inputs(document_release_data_path, nlp)

    for id, summaries in id2summaries.items():
        for summary in summaries:
            summary["docset_id"] = id[0]
        print(id)
        docset_id, doc_id = id
        assert id in id2inputs
        input_data = id2inputs[id]
        input_path = os.path.join(
            inputs_dir, "{}.{}.input.json".format(docset_id, doc_id))

        print("Writing input data {} ...".format(input_path))
        with open(input_path, "w") as fp:
            fp.write(json.dumps(input_data))

        summary_path = os.path.join(
            summary_dir, "{}.{}.target.json".format(docset_id, doc_id))
        print("Writing target data {} ...".format(summary_path))
        with open(summary_path, "w") as fp:
            fp.write(json.dumps(summaries))
