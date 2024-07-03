from odoo.http import request
from odoo import models, fields, api

class ReportPenjualanWizardXlsx(models.AbstractModel):
    _name = 'report.hmcoffee.report_penjualan_wizard_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Penjualan Wizard Xlsx'

    def generate_xlsx_report(self, workbook, data, laporannya):
        obj=data['laporannya']
        print(len(obj))
        sheet = workbook.add_worksheet('Data Penjualan')
        bold_format = workbook.add_format({'bold': True})
        sheet.write('A1', 'Nama', bold_format)
        sheet.write('B1', 'Tanggal Transaksi', bold_format)
        sheet.write('C1', 'Total Harga', bold_format)

        row = 1
        for x in obj:
            col = 1
            sheet.write(row, 0, x['name'])
            sheet.write(row, 1, x['tanggal_transaksi'])
            sheet.write(row, 2, x['total_harga'])
            row += 1

    
class ReportPenjualanXlsx(models.AbstractModel):
    _name = 'report.hmcoffee.report_penjualan_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Penjualan'

    def generate_xlsx_report(self, workbook, data, penjualan):
        sheet = workbook.add_worksheet('Daftar Penjualan')
        # row = 1
        col = 0
        sheet.write(1,col,'Nama Customer')
        sheet.write(2,col,'Tanggal Transaksi')
        sheet.write(3,col,'Total Harga')
        for obj in penjualan:
            row = 1
            col += 1
            sheet.write(row,col,obj.name)
            sheet.write(row+1,col,obj.tanggal_transaksi)
            sheet.write(row+2,col,obj.total_harga)
        
        # sheet.write(row+4,0,'Barang')
        # sheet.write(row+4,1,'Harga Satuan')
        # sheet.write(row+4,2,'Quantity')
        # sheet.write(row+4,3,'Sub Total')
        
        # row = 8
        record_line = request.env['hmcoffee.penjualan'].search([('detailpenjualan_ids','=',obj.id)])
        for line in record_line:
            row = 8
            # sheet.write(row+3,col+1,line.detailpenjualan_ids.bahan_id)
            sheet.write(row,1,line.detailpenjualan_ids.harga_satuan)
            sheet.write(row,2,line.detailpenjualan_ids.quantity)
            sheet.write(row,3,line.detailpenjualan_ids.subtotal)
            row += 1
