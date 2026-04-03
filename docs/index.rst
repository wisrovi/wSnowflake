wSnowflake Documentation
=========================

|Version| |License| |Python|

wSnowflake is a Python library that provides a high-level interface for Snowflake operations.
It simplifies working with Snowflake databases, warehouses, and data processing.

.. |Version| image:: https://img.shields.io/pypi/v/wSnowflake.svg
   :target: https://pypi.org/project/wSnowflake/
   :alt: PyPI Version

.. |License| image:: https://img.shields.io/pypi/l/wSnowflake.svg
   :target: https://pypi.org/project/wSnowflake/
   :alt: License

.. |Python| image:: https://img.shields.io/pypi/pyversions/wSnowflake.svg
   :target: https://pypi.org/project/wSnowflake/
   :alt: Python Versions

Quick Start
-----------

.. code-block:: bash

   pip install wSnowflake

.. code-block:: python

   from wSnowflake import Snowflake

   sf = Snowflake(account="my-account", user="myuser", password="pass", warehouse="my_wh")
   result = sf.query("SELECT * FROM my_table")

Key Capabilities
----------------

- **Connection Management** - Easy connection setup and pooling
- **Query Execution** - Execute queries with type conversion
- **Stage Operations** - Manage file stages
- **Streamlit Support** - Built-in Streamlit components
- **Type Safety** - Pydantic models for snowpark

.. toctree::
   :maxdepth: 2
   :caption: Contents

   getting_started/index
   api_reference/index
   tutorials/index
   faq
   glossary

.. toctree::
   :maxdepth: 1
   :caption: Additional

   License <license>
   bibliography

.. toctree::
   :maxdepth: 1
   :caption: External Links

   GitHub <https://github.com/wisrovi/wSnowflake>
   PyPI <https://pypi.org/project/wSnowflake/>
   LinkedIn <https://www.linkedin.com/in/william-steve-rodriguez-villamizar>

Indices and tables
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`