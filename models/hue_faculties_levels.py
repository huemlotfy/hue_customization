# -*- coding: utf-8 -*-
"""
MIGRATION (Odoo 11→12): Faculty levels configuration model v12 compatible
"""

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class HueFacultiesLevels(models.Model):
    """Faculties Levels - educational level definitions."""
    
    _name = 'hue.faculties.levels'
    _description = 'Faculties Levels'
    
    name = fields.Char(required=True)
    faculty = fields.Many2one('hue.faculties', required=True)
    d_id = fields.Char()
