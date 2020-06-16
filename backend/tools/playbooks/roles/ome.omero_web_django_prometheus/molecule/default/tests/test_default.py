import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_django_exporter_metrics(host):
    out = host.check_output(
        'curl http://localhost/django_prometheus/metrics')
    assert "django_http_responses_body_total_bytes_count" in out
