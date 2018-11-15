.. highlight:: shell

============
Installation
============


Stable release
--------------

To install Chariot Privacy Engine, run this command in your terminal:

.. code-block:: console

    $ pip install chariot_base

This is the preferred method to install Chariot Base, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for Chariot Privacy Engine can be downloaded from the `Gitlab repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git@gitlab.com:chariot-h2020/chariot_base.git

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://gitlab.com/chariot-h2020/chariot_base/-/archive/master/chariot_base-master.zip

Then install requirements for a Debian like system, with the following command:

.. code-block:: console

 $ sudo apt-get install python-dev libgmp3-dev

Once you have a copy of the source and requirement are installed, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Gitlab repo: https://gitlab.com/chariot-h2020/chariot_base
.. _tarball: https://github.com/theofilis/chariot_privacy_engine/tarball/master
