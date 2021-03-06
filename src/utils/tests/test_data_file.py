import time
from pathlib import Path

import pytest

import settings
from utils.data_file import DataFile

DATA_SPEC = (None, 'test')


@pytest.fixture(scope='module', name='data', autouse=True)
def make_temp_dir(tmpdir_factory):
    saved_path = settings.DATA_PATH
    temp_dir = tmpdir_factory.mktemp('data_file')
    settings.DATA_PATH = Path(temp_dir)
    yield
    settings.DATA_PATH = saved_path


def test_no_file():
    data = DataFile(*DATA_SPEC)
    assert data.value is None
    assert data.last_update is None
    assert data.data_path.parts[-1] == f'{DATA_SPEC[1]}.pickle4'
    assert data.data_path.parent == settings.DATA_PATH
    time0 = time.time()
    data.value = 1
    assert data.value == 1
    assert data.last_update > time0


def test_from_file():
    time0 = time.time()
    data = DataFile(*DATA_SPEC)
    assert data.value == 1
    assert data.last_update < time0


def test_data_path():
    data = DataFile('cat1', 'data1')
    assert data.data_path.parts[-1] == 'cat1.pickle4'
    assert data.data_path.parts[-2] == 'data1'
    assert data.data_path.parents[1] == settings.DATA_PATH


def test_data_path_no_cat():
    data = DataFile(None, 'data1')
    assert data.data_path.parts[-1] == 'data1.pickle4'
    assert data.data_path.parents[0] == settings.DATA_PATH


def test_str():
    result = 'DataFile(data_category=cat2, data_name=data3, data=Data(value=None, last_update=None))'
    assert str(DataFile('cat2', 'data3')) == result
