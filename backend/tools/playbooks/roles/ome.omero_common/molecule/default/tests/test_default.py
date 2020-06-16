import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_directory(host):
    d = host.file('/opt/omero')
    assert d.is_directory
    assert d.user == 'root'
    assert d.group == 'root'
