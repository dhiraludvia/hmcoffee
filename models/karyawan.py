from odoo import models, fields, api

class Karyawan(models.Model):
    _inherit = 'hr.employee'

    tanggal_lahir = fields.Datetime(string='Tanggal Lahir', default=fields.Datetime.now())
    is_menikah = fields.Boolean(string='Menikah', default=True)

