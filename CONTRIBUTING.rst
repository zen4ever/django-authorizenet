Contributing
============

Below is a list of tips for submitting issues and pull requests.  These are
suggestions and not requirements.

Submitting Issues
-----------------

Issues are often easier to reproduce/resolve when they have:

- A pull request with a failing test demonstrating the issue
- A code example that produces the issue consistently
- A traceback (when applicable)

Pull Requests
-------------

When creating a pull request, try to:

- Write tests if applicable
- Update the `README`_ file if needed
- Update the documentation if needed

.. _README: README.rst

Testing
-------

Please add tests for your code and ensure existing tests don't break.  To run
the tests against your code::

    python setup.py test

Please use tox to test the code against supported Python and Django versions.
First install tox::

    pip install tox

To run tox and generate a coverage report (in ``htmlcov`` directory)::

    make test

Generating documentation
------------------------

To regenerate the documentation use::

    make docs

The generated documentation HTML files can be found in ``docs/_build/html``.
