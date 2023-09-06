# Copyright (c) 2023, Luiz Costa and contributors
# For license information, please see license.txt

import hashlib
import os
import frappe
from frappe.model.document import Document


class FifoWarteschlangeAnsage(Document):
	pass


# Rename file with hash
@frappe.whitelist()
def before_save(doc, method):
    if doc.audio:
        file_doc = frappe.get_doc("File", {"file_url": doc.audio})

        base_name = os.path.basename(file_doc.file_name)
        name_without_extension, extension = os.path.splitext(base_name)
        hash_name = hashlib.md5((name_without_extension + str(frappe.utils.now())).encode()).hexdigest()
        new_file_name = f"{hash_name}{extension}"
        
        # rename file on filesystem
        old_path = frappe.get_site_path('public', 'files', base_name)
        new_path = frappe.get_site_path('public', 'files', new_file_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            # update doctype
            file_doc.file_name = new_file_name
            file_doc.file_url = f"/files/{new_file_name}"
            file_doc.save()
            # update field on doctype
            doc.audio = file_doc.file_url
