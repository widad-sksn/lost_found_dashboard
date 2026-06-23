from odoo import models, fields
class ItemTag(models.Model):
    _name = "item.tag"
    _description = "Item Tags"
    name  = fields.Char(string = "Tag Name", required = True)
    color = fields.Integer(string = "Color")
