import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data()
	chart = get_chart(data)
	report_summary = get_summary(data)
	return columns, data, None, chart, report_summary


def get_columns():
	return [
		{"label": _("Airline"), "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 200},
		{"label": _("Revenue"), "fieldname": "revenue", "fieldtype": "Currency", "width": 150},
	]


def get_data():
	airlines = frappe.get_all("Airline", pluck="name")
	revenue = {a: 0 for a in airlines}

	tickets = frappe.get_all(
		"Airplane Ticket",
		filters={"docstatus": 1},
		fields=["flight", "total_amount"],
	)
	for t in tickets:
		airplane = frappe.db.get_value("Airplane Flight", t.flight, "airplane")
		airline = frappe.db.get_value("Airplane", airplane, "airline")
		if airline in revenue:
			revenue[airline] += t.total_amount or 0

	data = [{"airline": a, "revenue": r} for a, r in revenue.items()]
	data.append({"airline": _("Total"), "revenue": sum(revenue.values())})
	return data


def get_chart(data):
	rows = [d for d in data if d["airline"] != _("Total")]
	return {
		"data": {
			"labels": [d["airline"] for d in rows],
			"datasets": [{"values": [d["revenue"] for d in rows]}],
		},
		"type": "donut",
	}


def get_summary(data):
	total = sum(d["revenue"] for d in data if d["airline"] != _("Total"))
	return [{"value": total, "label": _("Total Revenue"), "datatype": "Currency"}]
