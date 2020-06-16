OMERO.web django-prometheus
===========================

[![Build Status](https://travis-ci.org/ome/ansible-role-omero-web-django-prometheus.svg)](https://travis-ci.org/ome/ansible-role-omero-web-django-prometheus)
[![Ansible Role](https://img.shields.io/ansible/role/42003.svg)](https://galaxy.ansible.com/ome/omero_web_django_prometheus/)

Install and configure Django Prometheus exporter for OMERO.web.
Assumes OMERO.web 5.6+ Python 3 has been installed using the [ome.omero_web](https://galaxy.ansible.com/ome/omero_web) role.

See https://github.com/korfuri/django-prometheus

Note: metric endpoint `/django_prometheus/metrics` is not authenticated.


Role Variables
--------------

Optional:
- `omero_web_django_prometheus_config_web`: Automatically set `omero.web.*` configuration properties, default `True`.
- `omero_web_django_prometheus_stats_dir`: Prometheus temporary statistics directory

**Warning** This will make configuration changes to the OMERO.web and Gunicorn configurations, see [`templates/omero-web-config-django-prometheus-omero.j2`](templates/omero-web-config-django-prometheus-omero.j2) and [`defaults/main.yml`](defaults/main.yml) for details.

If you have customised your OMERO.web installation such as installing other web apps or setting `omero.web` configuration properties ensure the configuration changes made by this role are compatible.


Example playbook
----------------

    - hosts: localhost
      roles:
      - role: ome.omero_web
      - role: ome.omero_web_django_prometheus


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
