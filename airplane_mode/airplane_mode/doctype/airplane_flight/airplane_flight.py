# Copyright (c) 2024, Kumkum Tiwari and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	# pass
    def on_submit(self):
        # Update the status to 'Completed' after submission
        self.db_set('status', 'Completed')
    def before_save(self):
        # Calculate the total crew members from the child table
        if self.crew_member:  # Check if child table has data
            total_crew = len(self.crew_member)  # Count the number of entries in the child table
            self.total_crew_members = total_crew  # Update the read-only field in the parent doctype
        else:
            self.total_crew_members = 0  # Default to 0 if no crew members        


