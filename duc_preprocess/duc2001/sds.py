import os
import re
import json
import argparse
from . import document_parser
import spacy


def get_training_summaries(docset_ids, release_path, nlp):
    id2summary = {}
    for docset_id in docset_ids:
        docset_path = os.path.join(
            release_path, "data", "training", docset_id)
        summary_ids = [dn for dn in os.listdir(docset_path)
                       if dn.startswith(docset_id)]
        assert len(summary_ids) == 1
        summary_id = summary_ids[0]
        summary_path = os.path.join(
            docset_path, summary_id, "perdocs")
        
        summaries = document_parser.parse_perdocs_xml(summary_path, nlp)
        print("Found {} summaries for docset {} ...".format(
            len(summaries), docset_id))    

        for doc_id, summary in summaries.items():
            summary["docset_id"] = docset_id
            id2summary[(docset_id, doc_id)] = [summary]

    return id2summary

def get_test_summaries(docset_ids, release_path, nlp):

    orig_summary_path = os.path.join(
        release_path, "data", "test", "original.summaries")
    all_orig_summary_ids = [fn for fn in os.listdir(orig_summary_path)]
    dupl_summary_path = os.path.join(
        release_path, "data", "test", "duplicate.summaries")
    all_dupl_summary_ids = [fn for fn in os.listdir(dupl_summary_path)]

    id2summary = {}
    for docset_id in docset_ids:

        orig_summary_ids = [fn for fn in all_orig_summary_ids 
                            if fn.startswith(docset_id)]
        dupl_summary_ids = [fn for fn in all_dupl_summary_ids 
                            if fn.startswith(docset_id) and 
                            fn not in orig_summary_ids]
        for orig_summary_id in orig_summary_ids:
            orig_summary_path = os.path.join(
                release_path, "data", "test", "original.summaries", 
                orig_summary_id, "perdocs")
            if not os.path.exists(orig_summary_path):
                continue
            summary_data = document_parser.parse_perdocs_xml(
                orig_summary_path, nlp)
            for doc_id, summary in summary_data.items():
                assert (docset_id, doc_id) not in id2summary
                summary["docset_id"] = docset_id
                id2summary[(docset_id, doc_id)] = [summary]
        for dupl_summary_id in dupl_summary_ids:
            dupl_summary_path = os.path.join(
                release_path, "data", "test", "duplicate.summaries", 
                dupl_summary_id, "perdocs")
            if not os.path.exists(dupl_summary_path):
                continue
            summary_data = document_parser.parse_perdocs_xml(
                dupl_summary_path, nlp)
            for doc_id, summary in summary_data.items():
                summary["docset_id"] = docset_id
                if (docset_id, doc_id) not in id2summary:
                    id2summary[(docset_id, doc_id)] = []
                id2summary[(docset_id, doc_id)].append(summary)
        
    for key, summaries in id2summary.items():
        print("Found {} summaries for doc id {}".format(
            len(summaries), key))

    return id2summary

def make_train_data_from_release_data(root_path, output_root_path, nlp):

    docset_ids = get_docset_ids_from_dir(
        os.path.join(root_path, "data", "training"))
    
    print("Creating training set input and target directories...")
    train_summary_dir = os.path.join(output_root_path, "train", "targets")
    validate_directory(train_summary_dir)
    train_inputs_dir = os.path.join(output_root_path, "train", "inputs")
    validate_directory(train_inputs_dir)

    print("Reading training summaries...")
    id2summary = get_training_summaries(
        docset_ids, root_path, nlp)
   
    docs = get_training_inputs(docset_ids, root_path, nlp)

    for key, summaries in id2summary.items():
        print(key)
        assert key in docs
        doc = docs[key]

        datestr = str(doc["date"])
        input_data = []
        for s, sentence in enumerate(doc["sentences"], 1):
            input_data.append(
                {"docset_id": key[0],
                 "doc_id": key[1],
                 "date": datestr,
                 "sentence_id": s,
                 "text": sentence["text"],
                 "pos": sentence["pos"],
                 "ne": sentence["ne"],
                 "tokens": sentence["tokens"]})
        
        input_path = os.path.join(
            train_inputs_dir, "{}.{}.input.json".format(key[0], key[1]))
        
        print("Writing input data {} ...".format(input_path))
        with open(input_path, "w") as fp:
            fp.write(json.dumps(input_data))

        summary_path = os.path.join(
            train_summary_dir, "{}.{}.target.json".format(key[0], key[1]))
        print("Writing target data {} ...".format(summary_path))
        with open(summary_path, "w") as fp:
            fp.write(json.dumps(summaries))


    return

def get_training_inputs(docset_ids, root_path, nlp):

    docs = {}
    for docset_id in docset_ids:
        docset_dir = os.path.join(
            root_path, "data", "training", docset_id, "docs")
        paths = [os.path.join(docset_dir, fn) 
                 for fn in os.listdir(docset_dir)]
        docset_docs = document_parser.parse_input_docs(paths, nlp)
        for doc in docset_docs:
            docs[(docset_id, doc["doc_id"])] = doc
        print("Found {} docs for docset {}".format(
            len(docset_docs), docset_id))
    return docs

def make_test_data_from_release_data(root_path, output_root_path, nlp):

    docset_ids = get_docset_ids_from_dir(
        os.path.join(root_path, "data", "test", "docs"))
    
    print("Creating test set input and target directories...")
    test_summary_dir = os.path.join(output_root_path, "test", "targets")
    validate_directory(test_summary_dir)
    test_inputs_dir = os.path.join(output_root_path, "test", "inputs")
    validate_directory(test_inputs_dir)

    print("Reading test summaries...")
    id2summaries = get_test_summaries(docset_ids, root_path, nlp)

    docs = get_test_inputs(docset_ids, root_path, nlp)

    for key, summaries in id2summaries.items():
        print(key)
        assert key in docs
        doc = docs[key]

        datestr = str(doc["date"])
        input_data = []
        for s, sentence in enumerate(doc["sentences"], 1):
            input_data.append(
                {"docset_id": key[0],
                 "doc_id": key[1],
                 "date": datestr,
                 "sentence_id": s,
                 "text": sentence["text"],
                 "pos": sentence["pos"],
                 "ne": sentence["ne"],
                 "tokens": sentence["tokens"]})
        
        input_path = os.path.join(
            test_inputs_dir, "{}.{}.input.json".format(key[0], key[1]))
        
        print("Writing input data {} ...".format(input_path))
        with open(input_path, "w") as fp:
            fp.write(json.dumps(input_data))

        summary_path = os.path.join(
            test_summary_dir, "{}.{}.target.json".format(key[0], key[1]))
        print("Writing target data {} ...".format(summary_path))
        with open(summary_path, "w") as fp:
            fp.write(json.dumps(summaries))



def get_test_inputs(docset_ids, root_path, nlp):
    docs = {}
    for docset_id in docset_ids:
        docset_dir = os.path.join(
            root_path, "data", "test", "docs", docset_id) 
        
        input_paths = [os.path.join(docset_dir, fn) 
                       for fn in os.listdir(docset_dir)]

        docset_docs = document_parser.parse_input_docs(input_paths, nlp)
        for doc in docset_docs:
            docs[(docset_id, doc["doc_id"])] = doc

        print("Found {} docs for docset {}".format(
            len(docset_docs), docset_id))
    return docs

def validate_directory(path):
    if path != "" and not os.path.exists(path):
        os.makedirs(path)

def get_docset_ids_from_dir(path):

    docset_ids = [dn for dn in os.listdir(path)
                  if re.search(r"^d\d\d[a-z]", dn)]
    assert len(docset_ids) == 30
    return docset_ids

def extract_sds_data(release_data_path, output_dir, nlp=None):
    if nlp is None:
        nlp = spacy.load('en', parser=False)

    make_train_data_from_release_data(
        release_data_path, output_dir, nlp)
    make_test_data_from_release_data(
        release_data_path, output_dir, nlp)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--release-data", type=str, required=True)
    parser.add_argument("--output-path", type=str, required=True)

    args = parser.parse_args()
    
    extract_sds_data(args.release_data, args.output_path)
        
if __name__ == "__main__":
    main()
