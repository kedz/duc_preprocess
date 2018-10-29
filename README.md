duc_preprocess
==============

A library for preprocessing (sentence/word tokenizing and pos/ner tagging) 
the datasets from the Document Understanding Conference. 

This library uses spacy (https://spacy.io/) for all preprocessing.

Currently preprocesses single document 2001/2002 DUC data only but
planning on adding the multi-document data as well.

This package requires data from NIST that is publicly available but requires
signing a release and emailing with NIST to obtain dataset passwords. 

See https://duc.nist.gov/data.html for details on this process.

By email you should receive the following documents from NIST:

> DUC 2001: `DUC2001_Summarization_Documents.tgz`

> DUC 2002: `DUC2002_Summarization_Documents.tgz` 

To preprocess the DUC 2002 single document data you will also need to download
additional DUC 2002 test data from the NIST website using the script 
`scripts/duc2002_test_data.sh`

The usage is 
```
$ scripts/duc2002_test_data.sh UNAME PASS DATA_DIR
```

where UNAME and PASS are a username and password that NIST will give you
after you have sent them the release forms. 
The test data will be a tarball at 
`DATA_DIR/DUC2002_test_data.tar.gz`
`DATA_DIR` is optional and the script will use the current working 
directory if not supplied.


Example usage:

```python
from duc_preprocess import duc2001, duc2002

# Writes single document 2001 summarization data to duc2001_output.
duc2001_path="PATH/TO/DUC2001_Summarization_Document.tgz"
duc2001_output="PATH/TO/WRITE/DUC2001/DATA"
duc2001.preprocess_sds(duc2001_output, nist_data_path=duc2001_path)

# Writes single document 2002 summarization data to duc2002_output.
duc2002_path="PATH/TO/DUC2002_Summarization_Document.tgz"
duc2002_test_data="PATH/TO/DUC2002_test_data.tar.gz"
duc2002_output="PATH/TO/WRITE/DUC2002/DATA"
duc2002.preprocess_sds(
    duc2002_output, 
    nist_document_data_path=duc2002_path,
    nist_summary_data_path=duc2002_test_data)
```

### Notes
Single doc scripts does not create data for FBIS documents since 
these are very different in style and format from the other 
documents.
There are only a handful of FBIS documents so this shouldn't be a big deal.

Also for some reason, FT934-10911 does not have a single doc summary in the original summaries data so I skipped it.
