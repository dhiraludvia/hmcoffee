from odoo import models, fields, api

class StokOpname(models.Model):
    _name = 'hmcoffee.stokopname'
    _description = 'hmcoffee.stokopname'

    name = fields.Char('Nama Petugas')
    tanggal_stokopname = fields.Datetime('Tanggal Stokopname')
    detailstokopname_ids = fields.One2many('hmcoffee.detailstokopname', 'stokopname_id', string='detailstokopname')
    
    @api.model
    def default_get(self, fields):
        res = super(StokOpname, self).default_get(fields)
        bahan_record = self.env['hmcoffee.bahan'].search([])
        detail_vals = []
        for bahan in bahan_record:
            detail_vals.append((0,0,{
                'bahan_id': bahan.id,
                'check' : False,
                'catatan' : ''
            }))
        res['detailstokopnmae_ids'] = detail_vals
        return res
        

class DetailStokOpname(models.Model):
    _name = 'hmcoffee.detailstokopname'
    _description = 'model.technical.name'

    name = fields.Char(compute='_compute_name', string='name')
    stok = fields.Char(compute='_compute_stok', string='stok')
    bahan_id = fields.Many2one('hmcoffee.bahan', string='bahan')
    check = fields.Boolean('Check')
    catatan = fields.Char('Catatan')
    stokopname_id = fields.Many2one('hmcoffee.stokopname', string='stokopname')


    @api.depends('bahan_id')
    def _compute_stok(self):
        for rec in self:
            rec.stok = rec.bahan_id.stok

    @api.depends('bahan_id')
    def _compute_name(self):
        for i in self:
            i.name = i.bahan_id.nama_bahan
