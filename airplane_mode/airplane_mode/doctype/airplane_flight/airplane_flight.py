# Copyright (c) 2026, santhiya and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirplaneFlight(WebsiteGenerator):
	def on_submit(self):
		self.db_set("status", "Completed")

	def before_save(self):
		if not self.route:
			self.route = f"flights/{frappe.scrub(self.airplane)}-{frappe.generate_hash(length=6)}"
