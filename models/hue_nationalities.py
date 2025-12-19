# -*- coding: utf-8 -*-
"""
MIGRATION (Odoo 11→12): Nationalities reference data model v12 compatible
"""

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class HueNationalities(models.Model):
    """Nationalities - student nationality definitions."""
    
    _name = 'hue.nationalities'
    _description = 'Nationalities'
    
    name = fields.Char(required=True)
    en_name = fields.Char(string="English Name")
    d_id = fields.Char(string="External ID")
    foreign_nationality = fields.Boolean(default=True)


