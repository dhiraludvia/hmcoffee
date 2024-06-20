from odoo import models, fields

# class Pelanggan(models.Model):
#     _name = 'hmcoffee.pelanggan'
#     _description = 'Pelanggan'

#     name = fields.Char(string='Nama')
#     alamat = fields.Char(string='Alamat')
    

class Pelanggan(models.Model):
    _inherit = 'res.partner'

    level = fields.Selection([
        ('nonlevel', 'Non Level'),
        ('bronze','Bronze'),
        ('silver','Silver'),\
        ('gold','Gold'),
    ], string='Level')
    
