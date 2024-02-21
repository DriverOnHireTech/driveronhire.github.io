from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def generate_pdf_response(data):
    # Create a response object
    response = HttpResponse(content_type='application/pdf')

    # Set the filename
    response['Content-Disposition'] = 'attachment; filename="invoice_report.pdf"'

    # Create a PDF object
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Add data to the PDF
    table_data = [
        ['ID', 'Name', 'Amount'],
        [data['data']['id'], data['data']['name'], data['data']['amount']]
    ]

    # Create a table
    table = Table(table_data)

    # Add style to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Build the PDF
    pdf.build([table])

    return response