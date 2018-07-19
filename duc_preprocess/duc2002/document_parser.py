import os
import re
import datetime


def get_normalized_sentences(text, nlp):
    text = re.sub(r"\r|\t", " ", text)
    text = re.sub(r"\s+", " ", text.strip())
    docs = nlp.pipe([text])
    ns = []
    for doc in docs:
        for sent in doc.sents:
            tokens_all = [w for w in sent 
                          if w.text.strip() != '']
            tokens = [w.text.strip().lower() for w in tokens_all]
            pos = [w.pos_ for w in tokens_all]
            ne = [w.ent_type_ for w in tokens_all]
            pretty_text = sent.text.strip()
            pretty_text = re.sub(r"\r|\n|\t", r" ", pretty_text)
            pretty_text = re.sub(r"\s+", r" ", pretty_text)
            ns.append({"tokens": tokens, "text": pretty_text, 
                       "pos": pos, "ne": ne})
    return ns    

def parse_perdocs_xml(path, nlp):

    with open(path, "r") as fp:
        xml = fp.read()

    header_patt = r'<SUM.*?TYPE="PERDOC"\s+SIZE="(.*?)"\s+DOCREF="\s*(.*?)"' \
        '\s+SELECTOR="(.*?)"\s+SUMMARIZER="(.*?)"\s*>'
    summary_patt = header_patt + r'(.*?)</SUM>'

    headers = [m for m in re.findall(header_patt, xml, flags=re.DOTALL)]
    headers_found = len(headers)

    data = {}
    for match in re.findall(summary_patt, xml, flags=re.DOTALL):
        size, doc_id, selector, summarizer, summary_text = match
        size = int(size)
        sentences = get_normalized_sentences(summary_text, nlp)
        data[doc_id] = {"input_ids": [doc_id], "sentences": sentences,
                        "selector": selector, "summarizer": summarizer,
                        "size": size}

    if len(data) != headers_found:
        raise Exception("Error in summary xml {}".format(path))
    return data


def parse_mds_xml(path, nlp):
    SUM_PATT = r'<SUM.*?TYPE="MULTI"\s+SIZE="(.*?)"\s+DOCREF="(.*?)"\s+SELECTOR="(.*?)"\s+SUMMARIZER="(.*?)"\s*>(.*?)</SUM>'

    with open(path, "r") as fp:
        xml = fp.read()

    match = re.search(SUM_PATT, xml, flags=re.DOTALL)
    
    if match is None:
        raise Exception(
            "Could not find summary xml tag for file: {}".format(path))

    size, docref_string, selector, summarizer, raw_text = match.groups()
    size = int(size)
    input_document_ids = re.split(r"\s+", docref_string)
    sentences = get_normalized_sentences(raw_text, nlp)
    return {"input_ids": input_document_ids, 
            "summarizer": summarizer,
            "selector": selector,
            "sentences": sentences,
            "size": size}

def parse_input_docs(paths, nlp):
    data = []
    for path in paths:
        
        _, fn = os.path.split(path)
        if fn.startswith("AP"):
            doc_id, sentences, date = parse_ap(path, nlp)
        elif fn.startswith("WSJ"):
            doc_id, sentences, date = parse_wsj(path, nlp)
        elif fn.startswith("SJMN"):
            doc_id, sentences, date = parse_sjmn(path, nlp)
        elif fn.startswith("FT"):
            doc_id, sentences, date = parse_ft(path, nlp)
        elif fn.startswith("LA"):
            doc_id, sentences, date = parse_la(path, nlp)
        elif fn.startswith("FBIS"):
            doc_id, sentences, date = parse_fbis(path, nlp)
        else:
            raise Exception()
       

        data.append(
            {"doc_id": doc_id, "sentences": sentences, "date": date})

    return data


def parse_ap(path, nlp):

    sentences = []

    with open(path, "r") as fp:
        xml = fp.read()

    doc_id_match = re.search(
        r"<DOCNO>\s*(AP\d\d\d\d\d\d-\d+)\s*</DOCNO>", xml, 
        flags=re.DOTALL)
    assert doc_id_match is not None
    doc_id = doc_id_match.groups()[0]

    date_match = re.search(
        r"<DOCNO>\s*AP(\d\d)(\d\d)(\d\d)-\d+\s*</DOCNO>", xml, 
        flags=re.DOTALL)
    assert date_match is not None

    year, month, day = date_match.groups()
    year = int("19" + year)
    month = int(month)
    day = int(day)
    date = datetime.date(year, month, day)

    body_text_match = re.search(
        r"<TEXT>(.*?)</TEXT>", xml, flags=re.DOTALL)
    assert body_text_match is not None

    for body_text in re.findall(r"<TEXT>(.*?)</TEXT>", xml, flags=re.DOTALL):
        for graf in re.split(r"^   ", body_text, flags=re.MULTILINE):
            sentences.extend(get_normalized_sentences(graf, nlp))
    
    return doc_id, sentences, date
 
def parse_wsj(path, nlp):

    sentences = []

    with open(path, "r") as fp:
        xml = fp.read()
    date_match = re.search(
        r"<DOCNO>\s*WSJ(\d\d)(\d\d)(\d\d)-\d+\s*</DOCNO>", xml, 
        flags=re.DOTALL)
    assert date_match is not None

    year, month, day = date_match.groups()
    year = int("19" + year)
    month = int(month)
    day = int(day)
    date = datetime.date(year, month, day)

    doc_id = re.search(
        r"<DOCNO>\s*(WSJ\d\d\d\d\d\d-\d+)\s*</DOCNO>", xml, 
        flags=re.DOTALL).groups()[0]
 
    lp_match = re.search(
        r"<LP>(.*?)</LP>", xml, flags=re.DOTALL)
    if lp_match is not None:
        lp_text = lp_match.groups()[0]

        for graf in re.split(r"^   ", lp_text, flags=re.MULTILINE):
            sentences.extend(get_normalized_sentences(graf, nlp))

    body_text_match = re.search(
        r"<TEXT>(.*?)</TEXT>", xml, flags=re.DOTALL)
    assert body_text_match is not None
    body_text = body_text_match.groups()[0]

    
    for graf in re.split(r"^   ", body_text, flags=re.MULTILINE):
        sentences.extend(get_normalized_sentences(graf, nlp))

    return doc_id, sentences, date

def parse_la(path, nlp):

    sentences = []

    with open(path, "r") as fp:
        xml = fp.read()
    date_match = re.search(
        r"<DOCNO>\s*LA(\d\d)(\d\d)(\d\d)-\d+\s*</DOCNO>", xml, 
        flags=re.DOTALL)
    assert date_match is not None
    month, day, year = date_match.groups()
    year = int("19" + year)
    month = int(month)
    day = int(day)
    date = datetime.date(year, month, day)

    doc_id_match = re.search(
        r"<DOCNO>\s*(LA\d\d\d\d\d\d-\d+)\s*</DOCNO>", xml, flags=re.DOTALL)
    doc_id = doc_id_match.groups()[0]

    for body_text in re.findall(r"<TEXT>(.*?)</TEXT>", xml, flags=re.DOTALL):
        for graf in re.findall(r"<P>(.*?)</P>", body_text, flags=re.DOTALL):
            sentences.extend(get_normalized_sentences(graf, nlp))
 
    return doc_id, sentences, date

def parse_ft(path, nlp):

    sentences = []

    with open(path, "r") as fp:
        xml = fp.read()

    doc_id_match = re.search(
        r"<DOCNO>\s*(FT.*?)\s*</DOCNO>", xml, flags=re.DOTALL)
    assert doc_id_match is not None
    doc_id = doc_id_match.groups()[0]

    date_match = re.search(
        r"<DATE>\s*(\d\d)(\d\d)(\d\d)\s*</DATE>", xml, flags=re.DOTALL)    
    assert date_match is not None

    year, month, day = date_match.groups()
    year = int("19" + year)
    month = int(month)
    day = int(day)
    date = datetime.date(year, month, day)
    body_text_match = re.search(
        r"<TEXT>(.*?)</TEXT>", xml, flags=re.DOTALL)
    assert body_text_match is not None
    body_text = body_text_match.groups()[0]

    sentences.extend(get_normalized_sentences(body_text, nlp))
            
    return doc_id, sentences, date  

def parse_sjmn(path, nlp):

    sentences = []

    with open(path, "r") as fp:
        xml = fp.read()

    doc_id_match = re.search(
        r"<DOCNO>\s*(.*?)\s*</DOCNO>", xml, flags=re.DOTALL)
    assert doc_id_match is not None
    doc_id = doc_id_match.groups()[0]

    pubdate_match = re.search(
        r"<PUBDATE>\s*(\d\d)(\d\d)(\d\d)\s*</PUBDATE>", xml)    
    assert pubdate_match is not None


    year, month, day = pubdate_match.groups()
    year = int("19" + year)
    month = int(month)
    day = int(day)
    date = datetime.date(year, month, day)

    lead_text_match = re.search(
        r"<LEADPARA>(.*?)</LEADPARA>", xml, flags=re.DOTALL)
    assert lead_text_match is not None
    lead_text = lead_text_match.groups()[0]

    for graf in lead_text.split(";"):
        sentences.extend(get_normalized_sentences(graf, nlp))
            

    body_text_match = re.search(
        r"<TEXT>(.*?)</TEXT>", xml, flags=re.DOTALL)
    assert body_text_match is not None
    body_text = body_text_match.groups()[0]

    for graf in body_text.split(";"):
        sentences.extend(get_normalized_sentences(graf, nlp))
            
    return doc_id, sentences, date

def parse_fbis(path, nlp):

    sentences = []

    with open(path, "r") as fp:
        xml = fp.read()

    doc_id_match = re.search(
        r"<DOCNO>\s*(FBIS.*?)\s*</DOCNO>", xml, flags=re.DOTALL)
    assert doc_id_match is not None
    doc_id = doc_id_match.groups()[0]

    date_match = re.search(
        r"<DATE1>\s*(\d+) ([A-Za-z]+) (\d\d\d\d)\s*</DATE1>", xml, 
        flags=re.DOTALL)    
    assert date_match is not None

    day, month, year = date_match.groups()
    year = int(year)
    
    if month == "Jan":
        month = 1
    elif month == "January":
        month = 1
    elif month == "Mar":
        month = 2
    elif month == "March":
        month = 2
    elif month == "Feb":
        month = 3
    elif month == "February":
        month = 3
    elif month == "Apr":
        month = 4
    elif month == "May":
        month = 5
    elif month == "Jun":
        month = 6
    elif month == "Jul":
        month = 7
    elif month == "Aug":
        month = 8
    elif month == "Sep":
        month = 9
    elif month == "Oct":
        month = 10
    elif month == "Nov":
        month = 11
    elif month == "Dec":
        month = 12
    else:
        raise Exception()

    day = int(day)
    date = datetime.date(year, month, day)

    body_text_match = re.search(
        r"<TEXT>(.*?)</TEXT>", xml, flags=re.DOTALL)
    assert body_text_match is not None
    body_text = body_text_match.groups()[0]
    body_text = re.sub(r"</?F.*?>", r" ", body_text) 

    for graf in re.split(r"^  ", body_text, flags=re.MULTILINE):
        sentences.extend(get_normalized_sentences(graf, nlp))

    return doc_id, sentences, date
