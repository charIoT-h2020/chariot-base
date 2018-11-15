======================
Chariot Base
======================

.. image:: https://img.shields.io/pypi/v/chariot-base.svg
        :target: https://pypi.python.org/pypi/chariot-base

.. image:: https://readthedocs.org/projects/chariot-base/badge/?version=latest
        :target: https://chariot-base.readthedocs.io/en/latest/?badge=latest

Base utilities for chariot micro-services.

* Free software: Eclipse Public License 1.0
* Documentation: https://chariot-northbound-dispatcher.readthedocs.io.

Development
-----------

Encrypt application secrets, with the folling command

.. code-block:: console
 
 $ gpg -c --batch --passphrase test config.json


Features
--------

* Connection to Influx DB
* Connection to MQTT broker
* Connection to Cloudant
* Connection to IBM Watson IoT service

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
