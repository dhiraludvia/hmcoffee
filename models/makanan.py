from odoo import models, fields, api

class Makanan(models.Model):
    _name = 'hmcoffee.makanan'
    _description = 'Makanan'

    name = fields.Char(string='Menu')
    harga = fields.Integer(string='Harga')
    detailmakanan_ids = fields.One2many('hmcoffee.detailmakanan', 'makanan_id', string='Detail Bahan')


class DetailMakanan(models.Model):
    _name = 'hmcoffee.detailmakanan'
    _description = 'Detail Makanan'

    bahan_id = fields.Many2one(comodel_name='hmcoffee.bahan', string='Nama Bahan')
    kebutuhan = fields.Integer(string='Kebutuhan')
    makanan_id = fields.Many2one(comodel_name='hmcoffee.makanan', string='Makanan')
    
    
    
    
