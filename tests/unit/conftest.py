#!/usr/bin/python3
import collections

import mock

import pytest


# If layer options are used, add this to ${fixture}
# and import layer in ${libfile}
@pytest.fixture
def mock_layers(monkeypatch):
    import sys
    # Mock any functions in layers that need to be mocked here
    sys.modules['charms.layer'] = mock.Mock()
    sys.modules['reactive'] = mock.Mock()

    get_info = collections.namedtuple('mock_info', 'registry_path image_username image_password')
    get_info.registry_path = 'mock_registry_path'
    get_info.username = 'mock_image_username'
    get_info.password = 'mock_image_password'

    mock_get_info = mock.Mock()
    mock_get_info.return_value = get_info

    def options(layer):
        # mock options for layers here
        if layer == 'example-layer':
            options = {'port': 9999}
            return options
        else:
            return None

    monkeypatch.setattr('${libfile}.layer.options', options)
    monkeypatch.setattr('${libfile}.layer.docker_resource.get_info', mock_get_info)


@pytest.fixture
def mock_hookenv_config(monkeypatch):
    import yaml

    def mock_config():
        cfg = {}
        yml = yaml.load(open('./config.yaml'))

        # Load all defaults
        for key, value in yml['options'].items():
            cfg[key] = value['default']

        # Manually add cfg from other layers
        # cfg['my-other-layer'] = 'mock'
        return cfg

    monkeypatch.setattr('${libfile}.hookenv.config', mock_config)


@pytest.fixture
def mock_remote_unit(monkeypatch):
    monkeypatch.setattr('${libfile}.hookenv.remote_unit', lambda: 'unit-mock/0')


@pytest.fixture
def mock_charm_dir(monkeypatch):
    monkeypatch.setattr('${libfile}.hookenv.charm_dir', lambda: '.')


@pytest.fixture
def ${fixture}(tmpdir, mock_layers, mock_hookenv_config, mock_charm_dir, monkeypatch):
    from $libfile import $libclass
    helper = ${libclass}()

    # Example config file patching
    cfg_file = tmpdir.join('example.cfg')
    with open('./tests/unit/example.cfg', 'r') as src_file:
        cfg_file.write(src_file.read())
    helper.example_config_file = cfg_file.strpath

    # Any other functions that load helper will get this version
    monkeypatch.setattr('${libfile}.${libclass}', lambda: helper)

    return helper
