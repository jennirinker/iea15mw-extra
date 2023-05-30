"""Simple module to define/check path to 15-MW git repo.

You must update to match the path on your machine in order to
run the scripts in this folder.
"""
from pathlib import Path


IEA15MW_GIT_DIR = Path('C:/Users/rink/git/G-iea/IEA-15-240-RWT')

# check path is correct
if not IEA15MW_GIT_DIR.is_dir():
    raise ValueError('The path to the 15-MW git repo defined in _functions.py is not correct! Path defined:\n'
                     + IEA15MW_GIT_DIR.as_posix())
