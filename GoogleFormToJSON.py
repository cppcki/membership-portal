# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 17:54:06 2022

@author: Madison and Andrew
"""
from __future__ import print_function
from apiclient import discovery
from httplib2 import Http
from oauth2client import service_account, file, tools
import json

SCOPES = "https://www.googleapis.com/auth/forms.responses.readonly"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage('token.json')
creds = service_account.ServiceAccountCredentials.from_json_keyfile_name("token.json", SCOPES)

service = discovery.build('forms', 'v1', http=creds.authorize(Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

# Prints the responses of your specified form:
form_id = '1A00qyrXoONftiloR7HaFwf-VOf8c0Yb2NxOkvET3-Vg'
result = service.forms().responses().list(formId=form_id).execute()

result_form = json.dumps(result, indent=2)

with open('data.json', 'w') as outfile:
    outfile.write(result_form)
    