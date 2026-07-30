import csv
import io
from app import models


def generate_expenses_csv_string(expenses: list[models.Expense]) -> str:
    # 1. Create an in-memory string buffer to hold the CSV text
    output = io.StringIO()
    writer = csv.writer(output)

    # Write the header row
    writer.writerow([
        "Expense ID",
        "Description",
        "Category",
        "Amount (Cents)",
        "Paid By User ID",
        "Created At",
    ])

    # Write each expense row
    for exp in expenses:
        writer.writerow([
            exp.id,
            exp.description,
            exp.category,
            exp.amount_cents,
            exp.paid_by,
            exp.created_at,
        ])

    # Move the buffer pointer back to the beginning and return value
    output.seek(0)
    return output.getvalue()