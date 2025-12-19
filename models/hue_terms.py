# -*- coding: utf-8 -*-
"""
HUE Terms and Global Terms Models

FIXED: Restored hue.global.terms model that was accidentally removed in V12.
This model is required by:
  - hue_installments.py (term_id field)
  - hue_years.py (term_id field)
  - hue_terms.py (global_term_id field)
"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class HueGlobalTerms(models.Model):
    """
    Global Terms - Semester/Term definitions used across academic years.
    
    Example: Fall, Spring, Summer
    """
    _name = 'hue.global.terms'
    _description = 'Global Terms'
    
    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string='Active', default=True)
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Global Term name must be unique!')
    ]


class HueTerms(models.Model):
    """
    Academic Terms - Specific term instances for each academic year.
    
    Links a global term (e.g., "Fall") to a specific academic year
    with start and end dates.
    """
    _name = 'hue.terms'
    _description = 'Academic Terms'
    
    name = fields.Char(string='Name', required=True)
    term_id = fields.Many2one(
        'hue.academic.years', 
        string='Academic Year', 
        required=True
    )
    global_term_id = fields.Many2one(
        'hue.global.terms', 
        string='Global Term'
    )
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    active_validate = fields.Boolean(string='Active Validate')
    active_run = fields.Boolean(string='Active Run')
    active = fields.Boolean(string='Active', default=True)
    
    @api.constrains('from_date', 'to_date')
    def _check_dates(self):
        for record in self:
            if record.from_date and record.to_date:
                if record.from_date > record.to_date:
                    raise ValidationError(_('From Date must be before To Date!'))
