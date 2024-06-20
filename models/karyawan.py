from odoo import models, fields, api

class Karyawan(models.Model):
    _inherit = 'hr.employee'

    usia = fields.Integer(string='Usia')
    # jabatan = fields.Selection(string='Jabatan', 
    #                            selection=[('kasir', 'Kasir'), 
    #                                       ('accounting', 'Accounting'),
    #                                       ('kebersihan','Kebersihan'),],
    #                                       required=True)
    # foto = fields.Binary(string='Foto', help='choose foto')
    tanggal_lahir = fields.Datetime(string='Tanggal Lahir', default=fields.Datetime.now())
    status = fields.Char(string='Status')
    is_menikah = fields.Boolean(string='Menikah', default=True)

    @api.onchange('usia')
    def _tentukan_status(self):
            if self.usia > 30:
                self.status = 'tua'
            else:
                self.status = 'muda'
