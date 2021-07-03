import requests
import urllib3
import json

from threatingestor.sources import Source


class Plugin(Source):

    def __init__(self, name, search, username="", token=""):
        self.name = name
        self.search = search

        if username and token:
            self.auth = (username, token)
        else:
            self.auth = None


    def run(self, saved_state):
        # Read saved state and set HTTP headers.
        url = self.url

        data = { 
            "query": "malwareinfo", 
            "malware": self.q, 
            "limit": 1000,
            "days": 1
        }

        headers = {}
        if saved_state:
            # If both last modified and etag, set both.
            # Otherwise just interpret the whole field as last modified.
            last_modified = saved_state

            if len(saved_state.split(';')) == 2:
                last_modified, etag = saved_state.split(';')
                headers['If-None-Match'] = etag

            headers['If-Modified-Since'] = last_modified
        
        # Send head first to check 304.
        response = requests.head(self.url, headers=headers)
        
        # If not modified, return immediately.
        if response.status_code == 304:
            return saved_state, []

        response = requests.post(url+"/api/v1/", json=data, verify=False)
        # Form saved state.
        last_modified = response.headers.get('Last-Modified')
        etag = response.headers.get('Etag')

        if etag:
            saved_state = ';'.join([str(last_modified), etag])
        else:
            saved_state = last_modified

        # Process text.
        artifact_list = self.process_element(response.text, self.url, include_nonobfuscated=True)

        return saved_state, artifact_list
