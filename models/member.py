from odoo import models, fields, api

class Member(models.Model):
    _inherit = 'hmcoffee.manusia'

    no_member = fields.Char(string='No Member')
    
