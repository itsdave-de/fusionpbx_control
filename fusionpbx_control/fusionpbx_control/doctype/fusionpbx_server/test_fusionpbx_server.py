# Copyright (c) 2023, Luiz Costa and Contributors
# See license.txt

import re
import requests
import frappe
from frappe.tests.utils import FrappeTestCase


class TestFusionPBXServer(FrappeTestCase):
	pass


@frappe.whitelist()
def check_endpoint(api_url, api_token):
    headers = {
        'Authorization': api_token
    }
    response = requests.get(f"{api_url}/ping", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        frappe.throw("Connection error !<br />%s" % (
		    str(re.search(r'<pre>(.*?)</pre>', response.content.decode('utf-8'), re.DOTALL).group(1))
	    ))

