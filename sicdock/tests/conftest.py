import pytest, os, sys, _pickle
from os.path import join, dirname, abspath, exists

from sicdock import data
from sicdock.rosetta.triggers_init import get_pose_cached
from sicdock.motif import ResPairData, HierScore
from sicdock.search.result import dummy_result

# addoption doesn't work for me
# def pytest_addoption(parser):
#     parser.addoption(
#         "--runslow", action="store_true", default=False, help="run slow tests"
#     )
#
#
# def pytest_collection_modifyitems(config, items):
#     if config.getoption("--runslow"):
#         # --runslow given in cli: do not skip slow tests
#         return
#     skip_slow = pytest.mark.skip(reason="need --runslow option to run")
#     for item in items:
#         if "slow" in item.keywords:
#             item.add_marker(skip_slow)

@pytest.fixture(scope="session")
def datadir():
   print('fixture datadir', data.datadir)
   assert exists(data.datadir)
   return data.datadir

@pytest.fixture(scope="session")
def pdbdir(datadir):
   d = join(datadir, "pdb")
   assert exists(d)
   return d

@pytest.fixture(scope="session")
def C2_3hm4(pdbdir):
   return get_pose_cached("C2_3hm4_1.pdb.gz", pdbdir)

@pytest.fixture(scope="session")
def C3_1nza(pdbdir):
   return get_pose_cached("C3_1nza_1.pdb.gz", pdbdir)

@pytest.fixture(scope="session")
def top7(pdbdir):
   return get_pose_cached("top7.pdb.gz", pdbdir)

@pytest.fixture(scope="session")
def C5_1ojx(pdbdir):
   return get_pose_cached("C5_1ojx.pdb.gz", pdbdir)

@pytest.fixture(scope="session")
def respairdat(datadir):
   return data.small_respairdat()

@pytest.fixture(scope="session")
def respairscore(datadir):
   return data.small_respairscore()

@pytest.fixture(scope="session")
def hscore():
   return data.small_hscore()

@pytest.fixture(scope="session")
def body():
   return data.body_dhr14()

@pytest.fixture(scope="session")
def plug():
   return data.body_dhr64()

@pytest.fixture(scope="session")
def hole():
   return data.body_small_c3_hole()

@pytest.fixture(scope="session")
def body_c3_mono():
   return data.body_c3_mono()

@pytest.fixture(scope="session")
def result():
   return dummy_result()
