OMERO Common
============

[![Build Status](https://travis-ci.org/ome/ansible-role-omero-common.svg)](https://travis-ci.org/ome/ansible-role-omero-common)
[![Ansible Role](https://img.shields.io/ansible/role/41042.svg)](https://galaxy.ansible.com/ome/omero_common/)

Common variables and handlers for other OMERO application Ansible roles.


Role Variables
--------------

All variables are optional.
You should use the defaults unless you have a good reason not to.
- `omero_common_basedir`: The parent directory for OMERO applications.


Handlers
--------

This role includes standalone handlers which can be use to restart `omero-server` and `omero-web` without depending on the corresponding Ansible roles.
This may be useful when modifying the configuration of OMERO after installation.

If you know that the component you wish to restart is installed you can notify:
- `restart omero-server`
- `restart omero-web`
- `restart nginx`

If the component may or may not be installed you can notify:
- `restart omero-server if installed`
- `restart omero-web if installed`
- `restart nginx if installed`

Note that in the latter case the installation check is done when this role is run, not when the handlers are run, so there is a potential race condition.


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
