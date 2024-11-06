# Copyright (c) 2024, Kumkum Tiwari and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	# pass
    def on_submit(self):
        # Update the status to 'Completed' after submission
        self.db_set('status', 'Completed')

        


