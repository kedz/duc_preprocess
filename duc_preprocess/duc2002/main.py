import os
import tempfile
import tarfile
import shutil
from .sds import extract_sds_data


def preprocess_sds(output_directory, nist_document_data_path=None, 
                   nist_summary_data_path=None):
    '''
    Preprocess DUC 2002 single document summarization data.
    Gathers documents and multiple 100 word human reference abstracts.
    If nist_document_data_path is None, fall back to env variable
    DUC2002_ORIGINAL_DOCS and fail if that is not set.
    If nist_summary_data_path is None, fall back to env variable
    DUC2002_ORIGINAL_SUMMARIES and fail if that is not set.
    '''
    
    if nist_document_data_path is None:
        print("Checking environment variable 'DUC2002_ORIGINAL_DOCS' ...")
        nist_document_data_path = os.getenv('DUC2002_ORIGINAL_DOCS', None)

        if nist_document_data_path is None:
            raise Exception(
                "DUC2002_ORIGINAL_DOCS is not set and nist_document_data_path "
                "is None.")

    if nist_summary_data_path is None:
        print("Checking environment variable 'DUC2002_ORIGINAL_SUMMARIES' ...")
        nist_summary_data_path = os.getenv('DUC2002_ORIGINAL_SUMMARIES', None)

        if nist_summary_data_path is None:
            raise Exception(
                "DUC2002_ORIGINAL_SUMMARIES is not set and "
                "nist_summaries_data_path is None.")

    try:

        tmpdir = tempfile.mkdtemp()
        
        with tarfile.open(nist_document_data_path) as fp:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(fp, tmpdir)
        
        doc_workspace = os.path.join(tmpdir, "DUC2002_Summarization_Documents")

        inner_tar  = os.path.join(doc_workspace, "duc2002testdocs.tar")
        with tarfile.open(inner_tar) as fp:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(fp, doc_workspace)

        with tarfile.open(nist_summary_data_path) as fp:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(fp, tmpdir)
        
        sum_workspace = os.path.join(tmpdir, "DUC2002_test_data")
 
        print("Writing duc 2002 sds data to {} ...".format(output_directory))
        extract_sds_data(doc_workspace, sum_workspace, output_directory)
    
    finally:
        shutil.rmtree(tmpdir)
