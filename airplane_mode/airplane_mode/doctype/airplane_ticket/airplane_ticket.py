# Copyright (c) 2024, Kumkum Tiwari and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random

class AirplaneTicket(Document):
    
    def validate(self):
        # Ensure no duplicate add-ons and calculate the total price
        total = self.flight_price
        if self.add_ons:
            unique_add_ons = set()
            valid_add_ons = []

            # Validate each add-on and calculate total price
            for add_on in self.add_ons:
                if add_on.add_on_type in unique_add_ons:
                    frappe.msgprint(f"Duplicate add-on: {add_on.add_on_type}")
                else:
                    unique_add_ons.add(add_on.add_on_type)
                    valid_add_ons.append(add_on)
                    total += add_on.amount
            
            # Set valid add-ons without duplicates
            self.add_ons = valid_add_ons
        # Set the total amount after add-ons
        self.total_amount = total
        self.validate_ticket_capacity()

    def before_submit(document):
    # Check if the status is not 'Boarded', throw an error
        if document.status != "Boarded":
            frappe.throw("This Airplane Ticket cannot be submitted because its status is not 'Boarded'.")
    
    def before_insert(self):
        # Assign a random available seat before inserting the document
        available_seats = self.get_available_seats()
        if not available_seats:
            frappe.throw(("All seats are booked or not available."))
        self.seat = random.choice(available_seats)

        random_integers = random.randint(1, 2)
        random_alphabets = random.choice(['A','B'])
        self.gate_number = f"{random_alphabets}{random_integers} Gate"

    def get_available_seats(self):
        """Generate random seat and check if it's already booked."""
        available_seats = []
        letters = ['A', 'B', 'C', 'D', 'E']

        # Create a list of all possible seat combinations
        for number in range(1, 21):  # Seat numbers from 1 to 20
            for letter in letters:
                seat = f"{number}{letter}"
                # Check if the seat is already booked for the same flight
                if not frappe.db.exists('Airplane Ticket', {'flight': self.flight, 'seat': seat}):
                    available_seats.append(seat)

        return available_seats

    def validate_ticket_capacity(self):
        # Fetch the associated flight document
        flight_doc = frappe.get_doc("Airplane Flight", self.flight)

        # Fetch the associated airplane's capacity
        airplane_doc = frappe.get_doc("Airplane", flight_doc.airplane)
        capacity = airplane_doc.capacity

        # Count how many tickets have been issued for this flight
        issued_tickets = frappe.db.count("Airplane Ticket", filters={"flight": self.flight})

        # If the number of issued tickets exceeds the capacity, throw an error
        if issued_tickets >= capacity:
            frappe.throw(f"Cannot create a new ticket. The number of issued tickets ({issued_tickets}) exceeds the airplane's capacity ({capacity}).")
