import os
import logging
import re
from rongcloud.api import ApiClient
import unittest



# Logging
logging.basicConfig(level=logging.INFO)

# Credential
app_key = "8brlm7ufr6893"
app_secret = "LCLvqdWSupCzFH"

os.environ.setdefault('rongcloud-app-key', app_key)
os.environ.setdefault('rongcloud-app-secret', app_secret)

client = ApiClient()

