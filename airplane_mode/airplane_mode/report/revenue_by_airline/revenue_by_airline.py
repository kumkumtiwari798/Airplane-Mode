# Copyright (c) 2024, Kumkum Tiwari and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt

def execute(filters=None):
    columns, data = get_columns(), get_data()
    total_revenue = sum([row['revenue'] for row in data])
    
    chart = get_chart_data(data)
    report_summary = get_report_summary(total_revenue)

    return columns, data, None, chart, report_summary

def get_columns():
    return [
        {"label": "Airline", "fieldname": "airline", "fieldtype": "Link", "options": "Airline", "width": 200},
        {"label": "Revenue", "fieldname": "revenue", "fieldtype": "Currency", "width": 150}
    ]

def get_data():
    airlines = frappe.get_all("Airline", fields=["name"])
    data = []
    for airline in airlines:
        revenue = frappe.db.sql("""
            SELECT SUM(at.total_amount)
            FROM `tabAirplane Ticket` at
            JOIN `tabAirplane Flight` af ON at.flight = af.name
            JOIN `tabAirplane` a ON af.airplane = a.name
            WHERE a.airline = %s
        """, (airline.name,))
        
        revenue = revenue[0][0] if revenue and revenue[0][0] is not None else 0
        data.append({
            "airline": airline.name,
            "revenue": flt(revenue)
        })
    return data

def get_chart_data(data):
    labels = [row["airline"] for row in data]
    values = [row["revenue"] for row in data]
    return {
        "data": {
            "labels": labels,
            "datasets": [{"name": "Revenue", "values": values}]
        },
        "type": "donut"
    }

def get_report_summary(total_revenue):
    return [
        {"label": "Total Revenue", "value": frappe.utils.fmt_money(total_revenue), "indicator": "Green"}
    ]


# import frappe

# def execute(filters=None):
#     # Define the columns for the report
#     columns = [
#         {'fieldname': "airline", 'label': "Airline", 'fieldtype': "Link", 'options': "Airplane", 'width': "150"},
#         {'fieldname': "total_revenue", 'label': "Total Revenue", 'fieldtype': "Currency", 'options': "AED", 'width': "150"}
#     ]

#     # Fetch all airlines
#     airlines = frappe.get_all("Airline", fields=["name"])

#     # Fetch the total revenue grouped by airline (corrected SQL query)
#     revenue_data = frappe.db.sql("""
#         SELECT 
#             airplane.airline AS airline, 
#             SUM(airplane_ticket.total_amount) AS total_revenue
#         FROM `tabAirplane Ticket` AS airplane_ticket
#         JOIN `tabAirplane` AS airplane ON airplane.name = airplane_ticket.airplane
#         WHERE airplane_ticket.docstatus = 1
#         GROUP BY airplane.airline
#     """, as_dict=True)
    
#     # Convert the revenue data to a dictionary for easier lookup
#     revenue_dict = {row["airline"]: row["total_revenue"] for row in revenue_data}

#     # Prepare the final data by including airlines with 0 revenue
#     data = []
#     total_revenue = 0
#     for airline in airlines:
#         # Get revenue for the airline, default to 0 if not found
#         revenue = revenue_dict.get(airline.name, 0)
#         data.append({"airline": airline.name, "total_revenue": revenue})
#         total_revenue += revenue

#     # Add a total row to the data
#     data.append({"airline": "Total", "total_revenue": total_revenue})

#     # Prepare the chart data
#     chart = {
#         "data": {
#             "labels": [x["airline"] for x in data[:-1]],  # Exclude the total row from the chart
#             "datasets": [{"values": [x["total_revenue"] for x in data[:-1]]}],
#         },
#         "type": "donut",
#     }

#     # Add a summary section for total revenue
#     summary = [{"label": "Total Revenue", "value": total_revenue, "datatype": "Currency"}]

#     # Return the columns, data, chart, and summary
#     return columns, data, None, chart, summary
