Welcome to SecondServe Backend Documentation
=============================================

.. image:: _static/doc_coverage.svg
   :alt: Documentation coverage badge
   :align: right

.. image:: _static/test_coverage.svg
   :alt: Test coverage badge
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

for running tests and generating badges from ./SecondServe/backend:
.. code-block:: bash

   # Run a coverage test
   
   coverage run -m pytest 

   # Generate and print a coverage report
   
   coverage xml -o coverage.xml
   
   coverage report -m

   # Generate test coverage badge
   
   coverage-badge -o docs/source/_static/test_coverage.svg -f

For generating documentation and badges from ./SecondServe/backend:
.. code-block:: bash

   # Source docs
   
   sphinx-apidoc -o docs/source . 

   # Generate HTML documentation
   
   sphinx-build -b html docs/source docs/build/html

   # Generate documentation coverage badge
   
   docstr-coverage . --skip-private --skip-magic --badge docs/source/_static/doc_coverage.svg

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
