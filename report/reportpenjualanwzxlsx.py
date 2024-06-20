from odoo import models, fields, api

class ReportPenjualanWizardXlsx(models.AbstractModel):
    _name = 'report.hmcoffee.report_penjualan_wizard_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Penjualan Wizard Xlsx'

    def generate_xlsx_report(self, workbook, data, laporannya):
        #print((data['laporannya']))  
        #print(obj = data['laporannya'])      
        sheet = workbook.add_worksheet('Daftar Penjualan')
        row = 1
        col = 0
        sheet.write(row,col,'Nama Bahan')
        sheet.write(row+1,col,'Tanggal')
        for obj in laporannya:
            row = 1
            col += 1
            sheet.write(row,col,obj.name)
            sheet.write(row+1,col,obj.tanggal_penjualan)

    
