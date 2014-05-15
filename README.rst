PokitDok Platform API Client for Python
=======================================

Installation
------------

Install from PyPI_ using pip_

.. code-block:: bash

    $ pip install pokitdok


Resources
---------

Report issues_ on GitHub


Quick start
-----------

.. code-block:: python

    import pokitdok

    client = pokitdok.api.PokitDokClient('<your client id>', '<your client secret>')

    #submit an eligibility request
    eligibility_response = client.eligibility({
        "trading_partner_id": "2",
        "member_id": "W00000000000",
        "provider_id": "1467560003",
        "provider_name": "AYA-AY",
        "provider_first_name": "JEROME",
        "provider_type": "Person",
        "member_name": "JANE DOE",
        "member_birth_date": "1970-01-01",
        "service_types": ["Health Benefit Plan Coverage"]
    })

    #Check on pending platform activities
    client.activities()

See the documentation_ for detailed information on all of the PokitDok Platform APIs

Supported Python Versions
-------------------------

This library aims to support and is tested against these Python versions:

* 2.7.6
* 3.4.0
* PyPy

You may have luck with other interpreters - let us know how it goes.

License
-------

Copyright (c) 2014 PokitDok, Inc.  See LICENSE for details.

.. _documentation:
.. _issues: https://github.com/PokitDokInc/pokitdok-python/issues
.. _PyPI: https://pypi.python.org/pypi
.. _pip: https://pypi.python.org/pypi/pip

