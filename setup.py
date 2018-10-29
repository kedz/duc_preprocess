from setuptools import setup

setup(
   name='duc_preprocess',
   version='1.0',
   description='Preprocess DUC summarization data.',
   author='Chris Kedzie',
   author_email='kedzie@cs.columbia.edu',
   packages=["duc_preprocess",
             "duc_preprocess.duc2001",
             "duc_preprocess.duc2002"],  
   scripts=["scripts/duc2002-test-data.sh"],
   dependency_links = [
       'git+https://github.com/kedz/rouge_papier.git#egg=rouge_papier'],
   install_requires = [
       "rouge_papier", "spacy==2.0.11"],
)
