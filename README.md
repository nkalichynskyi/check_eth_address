To set up environment run following commands(for unix env)
```commandline
python3 -m venv ./venv
source venv/bin/activate
pip install -r ./requirements.txt
```

To run script:
```commandline
python ./main.py <address>
```
Balance on the output is converted to Eth for readability.

Script also has optional dependency on etherscan, if api key is provided list of transactions for given address will be retrieved.
Retrieved list of transaction is just an example of what can be fetched.

To get number of total tx:
```commandline
python ./main.py <address> --api-key <api_key>
```