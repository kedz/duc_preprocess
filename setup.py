from setuptools import setup

setup(
   name='duc_preprocess',
   version='1.0',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.com',
   packages=["duc_preprocess",
             "duc_preprocess.duc2001",
             "duc_preprocess.duc2002"],  
   dependency_links = [
       'git+https://github.com/kedz/simple_cnlp.git#egg=simple_cnlp',
       'git+https://github.com/kedz/rouge_papier.git#egg=rouge_papier'],
   install_requires = [
       'simple_cnlp', "rouge_papier", "spacy==2.0.11"],
)
