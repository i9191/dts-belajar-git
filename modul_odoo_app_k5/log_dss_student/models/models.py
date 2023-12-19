from odoo import models, fields

class MyModel(models.Model):
    _name = 'x_my_model'
    _description = 'My Model'

    name1 = fields.Char(string='Name 1')
    value1 = fields.Float(string='Value 1')
    name2 = fields.Char(string='Name 2')
    value2 = fields.Float(string='Value 2')
    name3 = fields.Char(string='Name 3')
    value3 = fields.Float(string='Value 3')
    name4 = fields.Char(string='Name 4')
    value4 = fields.Float(string='Value 4')
    name5 = fields.Char(string='Name 5')
    value5 = fields.Float(string='Value 5')