from __future__ import absolute_import
import csv
import time


import threatingestor.artifacts
from threatingestor.operators import Operator


class Plugin(Operator):
    """Operator for output to flat CSV file."""
    def __init__(self, filename, artifact_types=None, filter_string=None, allowed_sources=None):
        """CSV operator."""
        self.filename = filename

        super(Plugin, self).__init__(artifact_types, filter_string, allowed_sources)
        self.artifact_types = artifact_types or [
            threatingestor.artifacts.Domain,
            threatingestor.artifacts.Hash,
            threatingestor.artifacts.IPAddress,
            threatingestor.artifacts.URL,
        ]


    def handle_artifact(self, artifact):
        """Operate on a single artifact."""
        with open("__input_to_scan/"+time.strftime("%Y%m%d-")+self.filename, 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            artifact_type = artifact.__class__.__name__
            writer.writerow([str(artifact)])

