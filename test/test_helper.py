import os
import logging
import re
from rongcloud.api import ApiClient
import unittest



# Logging
logging.basicConfig(level=logging.INFO)

# Credential
app_key = ""
app_secret = ""

os.environ.setdefault('rongcloud-app-key', app_key)
os.environ.setdefault('rongcloud-app-secret', app_secret)

client = ApiClient()

