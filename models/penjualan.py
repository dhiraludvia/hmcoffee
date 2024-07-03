from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Penjualan(models.Model):
    _name = 'hmcoffee.penjualan'
    _description = 'Penjualan'

    ref = fields.Char(string='No. Referensi', required=True,
                          readonly=True, default=lambda self: _('New'))
    
    member = fields.Boolean(string='Apakah member ?')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Nama member')
    name = fields.Char(string='Nama Customer')
    tanggal_transaksi = fields.Datetime('Tanggal Transaksi', default=fields.Datetime.now())
    detailpenjualan_ids = fields.One2many(comodel_name='hmcoffee.detailpenjualan', 
                                          inverse_name='penjualan_id', string='Detail Penjualan')
    
    total_harga = fields.Integer(compute='_compute_total_harga', string='Total Harga Penjualan')
    
    state = fields.Selection([
        ('draft', 'draft'),
        ('confirm', 'confirm'),
        ('done', 'done'),
        ('cancel', 'cancel'),
    ], string='state',
    readonly=True, default="draft")

    def action_confirm(self):
        self.write({'state':'confirm'})

    def action_done(self):
        self.write({'state':'done'})

    def action_cancel(self):
        self.write({'state':'cancel'})
    
    def action_draft(self):
        self.write({'state':'draft'})

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

    def write(self, vals):
        for rec in self:
            a = self.env['hmcoffee.detailpenjualan'].search([('penjualan_id', '=', rec.id)])
            for data in a:
                if data:
                    data.bahan_id.stok -= data.quantity
        record = super(Penjualan, self).write(vals)
        for recc in self:
            b = self.env['hmcoffee.detailpenjualan'].search([('penjualan_id', '=', recc.id)])
            for databaru in b:
                if databaru in a:
                    databaru.bahan_id.stok += databaru.quantity
        return record
    
    @api.model
    def create(self, vals):
        if vals.get('ref', _("New")) == _("New"):
            member = vals.get('member', False)
            if member == True:
                vals['ref'] = self.env['ir.sequence'].next_by_code('referensi.penjualanmember') or _("New")
            else:
                vals['ref'] = self.env['ir.sequence'].next_by_code('referensi.penjualannonmember2') or _("New")
        record = super(Penjualan, self).create(vals)
        return record


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

    @api.model
    def create(self, vals):
        record = super(DetailPenjualan, self).create(vals)
        if record.quantity:
            self.env['hmcoffee.bahan'].search([('id', '=', record.bahan_id.id)]).write({'stok': record.bahan_id.stok - record.quantity})
        return record
