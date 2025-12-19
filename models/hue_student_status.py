# -*- coding: utf-8 -*-
"""
Student Status and Invoice Management.

MIGRATION (Odoo 11→12):
  - Removed print() statement
  - Added docstrings
  - Improved error handling
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
import werkzeug
_logger = logging.getLogger(__name__)

class HueStudentStatus(models.Model):
    """Student Status - track student's academic term status."""
    
    _name = 'hue.student.status'
    _description = 'Student Status'
    
    student_id = fields.Many2one('op.student', string="Student")
    academic_id = fields.Many2one('hue.academic.years', string="Academic Year")
    academic_term_id = fields.Many2one('hue.terms', string="Term")
    paid = fields.Boolean()
    assigned = fields.Boolean()
    one_time = fields.Boolean()
    invoice_id = fields.Integer()
    
    @api.multi
    def action_open_related_document(self):
        """Open related invoice in form view."""
        self.ensure_one()
        # CHANGED: print() → _logger.info() (Odoo 12 best practice)
        _logger.info("Opening related document for invoice ID: %s", self.invoice_id)
        
        if not self.invoice_id:
            raise UserError(_("No related invoice found for this student status record."))
        
        invoice = self.env['account.invoice'].browse(self.invoice_id)
        if not invoice.exists():
            raise UserError(_("Invoice %s no longer exists.") % self.invoice_id)
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Invoice: %s') % invoice.number,
            'res_model': 'account.invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'res_id': self.invoice_id,
            'target': 'current',
        }