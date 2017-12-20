from setuptools import setup

setup(
   name='duc_preprocess',
   version='1.0',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.com',
   packages=[],  #same as name
   dependency_links = [
       'git+https://github.com/kedz/simple_cnlp.git#egg=simple_cnlp'],
   install_requires = [
       'simple_cnlp'],
)
