Welcome to SecondServe Backend Documentation
=============================================

.. image:: _static/doc_coverage.svg
   :alt: Documentation coverage badge
   :align: right

Overview
--------

Welcome to the developer documentation for the **SecondServe Backend**.
This documentation covers the Django backend architecture, API endpoints,
data models, and utility modules used throughout the project.

The backend provides:

- User authentication and management
- API endpoints for client communication
- Integration with external services
- Database models and business logic

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Documentation Structure:

   modules

Developer Notes
---------------

For generating documentation and badges:

.. code-block:: bash

   # Source docs
   sphinx-apidoc -o docs/source . 

   # Generate HTML documentation
   sphinx-build -b html docs/source docs/build/html

   # Generate documentation coverage badge
   docstr-coverage backend/ --skip-private --skip-magic --badge docs/source/_static/doc_coverage.svg

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
