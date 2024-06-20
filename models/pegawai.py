from odoo import models, fields, api

class Pegawai(models.Model):
    _name = 'hmcoffee.pegawai'
    _description = 'Pegawai'

    name = fields.Char(string='Nama')
    usia = fields.Integer(string='Usia')
    jabatan = fields.Selection(string='Jabatan', 
                               selection=[('kasir', 'Kasir'), 
                                          ('accounting', 'Accounting'),
                                          ('kebersihan','Kebersihan'),],
                                          required=True)
    foto = fields.Binary(string='Foto', help='choose foto')
    tanggal_lahir = fields.Datetime(string='Tanggal Lahir', default=fields.Datetime.now())
    status = fields.Char(string='Status')
    
    @api.onchange('usia')
    def _tentukan_status(self):
            if self.usia > 30:
                self.status = 'tua'
            else:
                self.status = 'muda'
    
    

