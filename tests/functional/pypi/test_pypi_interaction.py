import configparser
from os.path import expanduser
from pathlib import Path

import requests


def get_cx_index_url() -> str:
    pip_config_path = Path(f"{expanduser('~')}/.config/pip/pip.conf")
    if not pip_config_path.exists():
        pip_config_path = Path(f"{expanduser('~')}/Library/Application Support/pip/pip.conf")
        if not pip_config_path.exists():
            raise RuntimeError("Cannot find pip.conf")

    config = configparser.RawConfigParser()
    config.read(pip_config_path)

    return f"{config['global']['extra-index-url']}/canvasxpress/"


def test_index_search():
    r = requests.get(get_cx_index_url())
    assert r.status_code == 200
