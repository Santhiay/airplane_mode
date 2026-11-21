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

	def on_update(self):
		if self.has_value_changed("gate_number"):
			frappe.enqueue(
				"airplane_mode.airplane_mode.doctype.airplane_flight.airplane_flight.update_ticket_gate_numbers",
				flight=self.name,
				gate_number=self.gate_number,
				enqueue_after_commit=True,
			)


def update_ticket_gate_numbers(flight, gate_number):
	frappe.db.set_value("Airplane Ticket", {"flight": flight}, "gate_number", gate_number)
