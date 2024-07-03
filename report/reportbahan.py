from odoo import models, fields, api

class ReportBahan(models.AbstractModel):
    _name = 'report.hmcoffee.report_bahan_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Bahan'

    def generate_xlsx_report(self, workbook, data, bahan):
        sheet = workbook.add_worksheet('Daftar Bahan')
        row = 1
        col = 0
        sheet.write(row,col,'Nama Bahan')
        sheet.write(row+1,col,'Stok')
        sheet.write(row+2,col,'Harga Modal')
        sheet.write(row+3,col,'Total Modal')
        for obj in bahan:
            row = 1
            col += 1
            sheet.write(row,col,obj.nama_bahan)
            sheet.write(row+1,col,obj.stok)
            sheet.write(row+2,col,obj.harga_modal)
            sheet.write(row+3,col,obj.total_modal)

    
