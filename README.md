# httpie-lcp-auth
LCP auth plugin for HTTPie http://httpie.org


Installation
------------

.. code-block:: bash

    $ pip install git+https://github.com/pts-ferdinandcardoso/httpie-lcp-auth

You should now see ``alcp-hmac`` under ``--auth-type`` in ``$ http --help`` output.

Usage
-----

.. code-block:: bash

    $ http --auth-type=lcp-hmac --auth='mac identifier:mac secret_key' example.org
    
Example
-------
An example of a request would be as follows

.. code-block:: curl

    └─ $ ▶ http  -v --auth 2a6493171757427fa90813b69f8db464:CHB6KCeUFeaG9Q_Or8Z_YSHmPFAljr5YKC84dWa9D8g --auth-type=lcp-hmac POST https://staging.lcp.points.com/v1/offers/  offerTye=BUY name=Offer
     POST /v1/offers/ HTTP/1.1
     Accept: application/json, */*
     Accept-Encoding: gzip, deflate
     Authorization: MAC id="2a6493171757427fa90813b69f8db464", ts="1516889122", nonce="QXZFqptAI8w=", ext="b7f5f8e24650b540aeccf2fa36ba6e9c9a935427", mac="53XvvtDQ4+w77SlwKie9AGhVutc="
     Connection: keep-alive
     Content-Length: 36
     Content-Type: application/json
     Host: staging.lcp.points.com
     User-Agent: HTTPie/0.9.9

     {
        "name": "Offer", 
        "offerTye": "BUY"
     }

