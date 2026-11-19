frappe.ui.form.on("Flight Passenger", {
	first_name(frm) {
		frm.trigger("set_full_name");
	},
	last_name(frm) {
		frm.trigger("set_full_name");
	},
	set_full_name(frm) {
		frm.set_value("full_name", [frm.doc.first_name, frm.doc.last_name].filter(Boolean).join(" "));
	},
});
