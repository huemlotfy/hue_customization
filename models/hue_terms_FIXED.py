# -*- coding: utf-8 -*-
"""
MIGRATION (Odoo 11→12): Academic terms model fully v12 compatible
FIXED: Added back hue.global.terms model that was removed
"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class HueGlobalTerms(models.Model):
    """
    Global Terms - used across academic years.
    
    MIGRATION NOTE: This model was accidentally removed in V12.
    It is required by hue_installments and hue_years models.
    """
    _name = 'hue.global.terms'
    _description = 'Global Terms'
    
    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True)


class HueTerms(models.Model):
    """Academic Terms - term/semester definitions."""
    
    _name = 'hue.terms'
    _description = 'Academic Terms'
    
    name = fields.Char(required=True)
    term_id = fields.Many2one('hue.academic.years', string='Academic Year', required=True)
    global_term_id = fields.Many2one('hue.global.terms', string='Global Term')
    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)
    active_validate = fields.Boolean(string='Active Validate')
    active_run = fields.Boolean(string='Active Run')
    active = fields.Boolean(default=True)
