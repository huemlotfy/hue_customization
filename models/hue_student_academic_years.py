# -*- coding: utf-8 -*-
"""
MIGRATION (Odoo 11→12): Student academic tracking model v12 compatible
"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class HueStudentAcademicYears(models.Model):
    """Student Academic Years - track student's academic year history."""
    
    _name = 'hue.student.academic.years'
    _description = 'Student Academic Years'
    
    student_id = fields.Many2one('op.student', required=True)
    academic_year_id = fields.Many2one('hue.academic.years', required=True)
    status = fields.Selection([
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended')
    ])




