import csv
import sys
import os
from fpdf import FPDF

def download_csv(user, fields, rows, tipo):
    if tipo == 1:
        filename = "historial_visitas_{0}.csv".format(user)
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

def download_pdf(user, fields, rows, tipo):
    pdf = FPDF(orientation = 'L')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    header = "| "
    for x in fields:
        header = header + x + ' | '
    pdf.cell(0, 10, txt = header, ln = 1, align = 'C')
    pdf.set_font("Arial", size = 12)
    for l in rows:
        r = "| "
        for x in l:
            r = r + str(x) + ' | '
        pdf.cell(0, 10, txt = r, ln = 1, align = 'C')
    if tipo == 1:
        filename = "historial_visitas_{0}.pdf".format(user)
    pdf.output(filename)
