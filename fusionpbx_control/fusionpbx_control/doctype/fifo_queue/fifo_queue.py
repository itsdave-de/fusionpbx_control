# Copyright (c) 2023, Luiz Costa and contributors
# For license information, please see license.txt

import os
import re
import json
import datetime
import requests
import frappe
from frappe.model.document import Document


class FIFOQueue(Document):
	pass


@frappe.whitelist()
def sync_data(doc: str):
    # load data from doctype
    doc_dict = json.loads(doc)
    print(json.dumps(doc_dict, indent=2))
    #
    # Model of json
    #
    output_data = {
        'queue': doc_dict['queue_name'],
        'fifo': []
    }
    
    pbx_server = frappe.get_doc('FusionPBX Server', doc_dict['fusionpbx'])

    # load items from FIFO table
    
    files_upload = []

    print(json.dumps(doc_dict, indent=2))

    for fifo in frappe.get_all("Fifo Warteschlange Ansage", filters={'queue': doc_dict['queue_name']}):
        fifo_dict = frappe.get_doc('Fifo Warteschlange Ansage', fifo['name'])

        # Make json item
        data = {}
        data['audio_file'] = os.path.basename(fifo_dict.audio)
        data['publish_from'] = fifo_dict.date_from.strftime('%Y-%m-%d')
        data['publish_to'] = fifo_dict.date_to.strftime('%Y-%m-%d')
        data['priority'] = int(fifo_dict.priority)
        data['enable'] = True if (fifo_dict.enable == 1) else False
        # append fifo
        output_data['fifo'].append(data)
        # Array of audios
        files_upload.append(os.path.basename(fifo_dict.audio))

    # Proccess files
    files = []
    for do_file in files_upload:
        files.append((
            'audio[]', (
                do_file, open(
                    os.path.join(
                        frappe.utils.file_manager.get_file_path(do_file)
                    ), 'rb'
                )
            )
        ))
    # Connect with endpoint
    resp = requests.post(
        f"{pbx_server.api_url}/sync",
        headers = { 'Authorization': pbx_server.api_token },
        data = { 'config': json.dumps(output_data) },
        files = files
    )
    if resp.status_code == 200:
        frappe.msgprint('Data updated successfully!<hr /><pre>%s</pre>' % (
            json.dumps(output_data, indent=2)
        ))
    else:
        frappe.msgprint('Error on syncronize data<br />%s' % (
            str(re.search(r'<pre>(.*?)</pre>', resp.content.decode('utf-8'), re.DOTALL).group(1))
        ))

