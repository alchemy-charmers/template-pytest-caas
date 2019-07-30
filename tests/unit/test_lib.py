#!/usr/bin/python3
import yaml


class TestLib():
    def test_pytest(self):
        assert True

    def test_${fixture}(self, ${fixture}):
        ''' See if the helper fixture works to load charm configs '''
        assert isinstance(${fixture}.charm_config, dict)

    def test_make_pod_spec(self, ${fixture}):
        spec = ${fixture}.make_pod_spec()
        spec_yaml = yaml.safe_load(spec)
        assert spec_yaml['containers'][0]['imageDetails']['imagePath'] == 'mock_registry_path'
        assert spec_yaml['containers'][0]['imageDetails']['username'] == 'mock_image_username'
        assert spec_yaml['containers'][0]['imageDetails']['password'] == 'mock_image_password'
        assert spec_yaml['containers'][0]['command'] == ['sh', '-c', 'tail -f /dev/null']
        assert spec_yaml['containers'][0]['ports'][0]['containerPort'] == 22
        assert spec_yaml['containers'][0]['ports'][0]['name'] == 'ssh'

    # Include tests for functions in ${libfile}
