from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Penjualan(models.Model):
    _name = 'hmcoffee.penjualan'
    _description = 'Penjualan'

    name = fields.Char(string='Nama')
    tanggal_transaksi = fields.Datetime('Tanggal Transaksi', default=fields.Datetime.now())
    detailpenjualan_ids = fields.One2many(comodel_name='hmcoffee.detailpenjualan', 
                                          inverse_name='penjualan_id', string='Detail Penjualan')
    
    total_harga = fields.Integer(compute='_compute_total_harga', string='Total Harga Penjualan')
    
    @api.depends('detailpenjualan_ids')
    def _compute_total_harga(self):
        for rec in self:
            a = self.env['hmcoffee.detailpenjualan'].search([('penjualan_id', '=', rec.id)]).mapped('subtotal')
            rec.total_harga = sum(a)

    def unlink(self):
        if self.detailpenjualan_ids:
            a = []
            for detail in self:
                a = self.env['hmcoffee.detailpenjualan'].search([('penjualan_id','=',detail.id)])
            print (a)
            for bahannya in a:
                bahannya.bahan_id.stok += bahannya.quantity
        rec = super(Penjualan,self).unlink()

    
    # def write(self, vals):
    #     for rec in self:
    #         a = self.env['hmcoffee.detailpembelian'].search([('penjualan_id','=',rec.id)])
    #         for data in a:
    #             if data:
    #                 data.bahan_id.stok -= data.qty
    #     record = super(Pembelian, self).write(vals)        
    #     for recc in self:
    #         b = self.env['hmcoffee.detailpembelian'].search([('pembelian_id','=',recc.id)])
    #         for databaru in b:
    #             if databaru in a:
    #                 databaru.bahan_id.stok += databaru.qty
    #     return record

class DetailPenjualan(models.Model):
    _name = 'hmcoffee.detailpenjualan'
    _description = 'Detail Penjualan'

    penjualan_id = fields.Many2one(comodel_name='hmcoffee.penjualan', string='Penjualan')
    bahan_id = fields.Many2one(comodel_name='hmcoffee.bahan', string='Barang')
    harga_satuan = fields.Integer(compute='_compute_harga_satuan', string='Harga Satuan')
    quantity = fields.Integer(string='Quantity')
    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')
    
    @api.depends('bahan_id')
    def _compute_harga_satuan(self):
        for rec in self:
            rec.harga_satuan = rec.bahan_id.harga_modal
    
    @api.depends('harga_satuan','quantity')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.harga_satuan*rec.quantity  
    
    @api.constrains('quantity')
    def _checkQuantity(self):
        for rec in self:
            if rec.quantity < 1:
                raise ValidationError('Tidak bisa membeli {} {} pcs'. format(rec.bahan_id.nama_bahan, rec.quantity))
            elif(rec.quantity > rec.bahan_id.stok):
                raise ValidationError('Stok {} tidak mencukupi, maksimal pembelian {} pcs'. format(rec.bahan_id.nama_bahan, rec.bahan_id.stok))
                