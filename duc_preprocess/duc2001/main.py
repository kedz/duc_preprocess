import os
import tempfile
import tarfile
import shutil
from .repair import run_repairs
from .sds import extract_sds_data


def preprocess_sds(output_directory, nist_data_path=None):
    '''
    Preprocess DUC 2001 single document summarization data.
    Gathers documents and multiple 100 word human reference abstracts.
    If nist_data_path is None, fall back to env variable DUC2001_ORIGINAL
    and fail if that is not set.
    '''
    
    if nist_data_path is None:
        print("Checking environment variable 'DUC2001_ORIGINAL' ...")
        nist_data_path = os.getenv('DUC2001_ORIGINAL', None)

        if nist_data_path is None:
            raise Exception(
                "DUC2001_ORIGINAL is not set and nist_data_path is None.")

    try:

        tmpdir = tempfile.mkdtemp()
        
        with tarfile.open(nist_data_path) as fp:
            fp.extractall(tmpdir)
        
        workspace = os.path.join(tmpdir, "DUC2001_Summarization_Documents")

        run_repairs(workspace)
        print("Writing duc 2001 sds data to {} ...".format(output_directory))
        extract_sds_data(workspace, output_directory)
    
    finally:
        shutil.rmtree(tmpdir)
