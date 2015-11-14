# paytrace_py

## paytrace_py is in ALPHA development and is not ready for production use.

paytrace_py is a python library to simplify and streamline interactions with the [PayTrace JSON API](http://help.paytrace.com/json).

# Install

```
git clone https://github.com/PayTrace/paytrace_py.git
cd paytrace_py
sudo python setup.py install
```

# Example usage

```
from paytrace_py.paytrace_connector import PayTraceConnector

# allow_insecure=True is set for the api test server only.
pt_connector = PayTraceConnector('demo123','demo123',allow_insecure=True)

data = {
      "amount": "1.00",
      "credit_card": {
        "number": "4111111111111111",
        "expiration_month": "12",
        "expiration_year": "2020"
      },
      "csc": "999",
      "billing_address": {
        "name": "Steve Smith",
        "street_address": "8320 E. West St.",
        "city": "Spokane",
        "state": "WA",
        "zip": "85284"
      }
    }

json_response = pt.keyed_sale(data)
print json_response
```
