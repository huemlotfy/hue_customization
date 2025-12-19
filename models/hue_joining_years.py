# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class HueJoiningYears(models.Model):
    """Joining Years - student enrollment years."""
    
    _name = 'hue.joining.years'
    _description = 'Joining Years'
    
    name = fields.Char()
    d_id = fields.Char(string="External ID")
    active = fields.Boolean(string="Active")
    #faculty = fields.Many2one('hue.faculties', 'faculty')
    #year_id = fields.Many2one('hue.years', 'year_id')	

