Remediate S3

Remediate S3 is a python function to scan for all of the unencrypted S3 buckets in the selected AWS region within a single account and optionally apply default AES256 encryption
Usage

To unit test locally run the included stub.py file, to enable auto-remediation add the "Enable": True event

python stub.py

For dev/test create a lambda function with the appropriate test events, additional events can be added as needed (e.g. lifecycle as event = {"lifecycle" : "test"}