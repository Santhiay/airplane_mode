frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
		if (frm.doc.docstatus === 0 && !frm.is_new()) {
			frm.add_custom_button(
				__("Assign Seat"),
				() => {
					frappe.prompt(
						{
							fieldname: "seat",
							label: __("Seat Number"),
							fieldtype: "Data",
							reqd: 1,
						},
						(values) => {
							frm.set_value("seat", values.seat);
						},
						__("Assign Seat"),
						__("Assign")
					);
				},
				__("Actions")
			);
		}
	},
});
