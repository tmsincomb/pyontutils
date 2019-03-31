import unittest
from pathlib import Path
from pyontutils.utils import get_working_dir
from pyontutils.config import devconfig, checkout_ok
from pyontutils.integration_test_helper import TestScriptsBase, Folders, Repo
import neurondm


class TestScripts(Folders, TestScriptsBase):
    """ woo! """


ont_repo = Repo(devconfig.ontology_local_repo)
post_load = lambda : (ont_repo.remove_diff_untracked(), ont_repo.checkout_diff_tracked())
post_main = lambda : (ont_repo.remove_diff_untracked(), ont_repo.checkout_diff_tracked())

### handle ontology branch behavior
neurons = ('neurondm/core',
           'neurondm/lang',
           'neurondm/example',
           'neurondm/phenotype_namespaces',
           'neurondm/models/allen_cell_types',
           'neurondm/models/phenotype_direct',
           'neurondm/models/basic_neurons',
           'neurondm/models/huang2017',
           'neurondm/models/ma2015',
           'neurondm/models/cuts',
           'neurondm/build',
           'neurondm/sheets',
          )
print('checkout ok:', checkout_ok)
ont_branch = ont_repo.active_branch.name
skip = tuple()
lasts = tuple()
if not checkout_ok and ont_branch != 'neurons':
    skip += tuple(n.split('/')[-1] for n in neurons)  # FIXME don't use stem below
else:
    lasts += tuple(f'pyontutils/{s}.py' for s in neurons)

### build mains
mains = {}

module_parent = Path(__file__).resolve().parent.parent.as_posix()
working_dir = get_working_dir(__file__)
if working_dir is None:
    # python setup.py test will run from the module_parent folder
    # I'm pretty the split was only implemented because I was trying
    # to run all tests from the working_dir in one shot, but that has
    # a number of problems with references to local vs installed packages
    working_dir = module_parent

print(module_parent)
print(working_dir)

TestScripts.populate_tests(neurondm, working_dir, mains, lasts=lasts,
                           module_parent=module_parent, only=[], do_mains=True)
