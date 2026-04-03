Installation
============

Requirements
------------

* Python 3.8+
* Snowflake account with appropriate credentials

Install via pip
---------------

.. code-block:: bash

    pip install wsnowflake

Install with development dependencies
-------------------------------------

.. code-block:: bash

    pip install wsnowflake[dev]

Install from source
-------------------

.. code-block:: bash

    git clone https://github.com/wisrovi/wSnowflake.git
    cd wSnowflake
    pip install -e .

Dependencies
~~~~~~~~~~~~

Required dependencies:

* ``snowflake-connector-python>=2.8.0`` - Official Snowflake Python connector

Optional dependencies:

* ``pytest>=7.0.0`` - Testing framework
* ``pytest-cov>=4.0.0`` - Coverage plugin
* ``pytest-asyncio>=0.21.0`` - Async test support
* ``ruff>=0.1.0`` - Linter
* ``mypy>=1.0.0`` - Type checker