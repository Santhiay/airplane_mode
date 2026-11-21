# Copyright (c) 2026, santhiya and contributors
# For license information, please see license.txt

import random

import frappe
from frappe import _
from frappe.model.document import Document


class AirplaneTicket(Document):
	def before_insert(self):
		self.validate_capacity()
		self.seat = f"{random.randint(1, 99)}{random.choice('ABCDE')}"

	def validate(self):
		self.remove_duplicate_addons()
		self.calculate_total_amount()

	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw(_("Airplane Ticket can be submitted only when the status is Boarded"))

	def validate_capacity(self):
		airplane = frappe.db.get_value("Airplane Flight", self.flight, "airplane")
		capacity = frappe.db.get_value("Airplane", airplane, "capacity")
		ticket_count = frappe.db.count("Airplane Ticket", {"flight": self.flight})
		if ticket_count >= capacity:
			frappe.throw(_("No seats available. Tickets sold have reached the airplane capacity."))

	def remove_duplicate_addons(self):
		seen = set()
		unique_rows = []
		for row in self.add_ons:
			if row.item not in seen:
				seen.add(row.item)
				unique_rows.append(row)
		self.set("add_ons", unique_rows)

	def calculate_total_amount(self):
		addon_total = sum((row.amount or 0) for row in self.add_ons)
		self.total_amount = (self.flight_price or 0) + addon_total
