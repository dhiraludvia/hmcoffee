from odoo import models, fields, api

class KategoriBahan(models.Model):
    _name = 'hmcoffee.kategoribahan'
    _description = 'KategoriBahan'


    name = fields.Selection(string='Nama Kategori', 
                               selection=[('kopi', 'Kopi'), 
                                          ('makanan', 'Makanan'),
                                          ('minuman','Minuman'),])
    
    no_rak = fields.Integer(string='Nomor Rak')
    bahan_ids = fields.One2many('hmcoffee.bahan', 
                                   'kategori_bahan_id', 
                                   string='Daftar Bahan')
    
    
