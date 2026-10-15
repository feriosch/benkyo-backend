import os
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# jap_dev.helpers.connection builds a mongodb+srv client against the production
# cluster at import time. Replace it before anything imports it so unit tests
# never touch the real database.
_fake_connection = types.ModuleType('jap_dev.helpers.connection')
_fake_connection.database = MagicMock(name='database')
sys.modules['jap_dev.helpers.connection'] = _fake_connection

os.environ['TOKEN_PASS'] = 'test-secret'


@pytest.fixture
def files_dir(tmp_path, monkeypatch):
    """Run in a temp dir so CSV responses write to <tmp>/files, not the repo."""
    (tmp_path / 'files').mkdir()
    monkeypatch.chdir(tmp_path)
    return tmp_path / 'files'


@pytest.fixture
def client(files_dir, monkeypatch):
    from application import application
    # send_from_directory('files', ...) resolves against the app root path
    monkeypatch.setattr(application, 'root_path', str(files_dir.parent))
    application.config['TESTING'] = True
    return application.test_client()


@pytest.fixture
def auth_header():
    from jap_dev.helpers.token import generate_token
    return {'Authorization': f'Bearer {generate_token({"username": "tester"})}'}
