// Copyright (c) 2024, Kumkum Tiwari and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
        // Add a custom button to the form
        frm.add_custom_button(__('Set Seat Number'), function() {
            // Open a dialog to input the seat number
            let d = new frappe.ui.Dialog({
                title: __('Enter Seat Number'),
                fields: [
                    {
                        label: 'Seat Number',
                        fieldname: 'seat_number',
                        fieldtype: 'Data',
                        reqd: 1 // Makes the field required
                    }
                ],
                primary_action_label: 'Submit',
                primary_action(values) {
                    // Set the seat number to the Seat field in the form
                    frm.set_value('seat', values.seat_number);
                    // Close the dialog
                    d.hide();
                }
            });

            // Show the dialog to the user
            d.show();
        });

	},
});
