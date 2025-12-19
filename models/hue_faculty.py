# -*- coding: utf-8 -*-
"""
Faculty and User Management Extensions.

MIGRATION (Odoo 11→12):
  - track_visibility → tracking=True
  - Added docstrings
  - Safe ref() handling with raise_if_not_found=False
"""

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class HrEmployeeExt(models.Model):
    """HR Employee extension - link courses to employees."""

    _inherit = 'hr.employee'
    _description = 'Employee Extended'

    course_ids = fields.Many2many('op.course', 'employee_course_rel', 'employee_id',
                                   'course_id', 'Courses')


class OpFacultyExt(models.Model):
    """OpenEducat Faculty extension - add job & department tracking."""

    _inherit = 'op.faculty'
    _description = 'Faculty Extended'

    # CHANGED: track_visibility → tracking=True (Odoo 12)
    job_id = fields.Many2one('hr.job', 'Job Position', tracking=True)
    department_id = fields.Many2one('hr.department', 'Department', tracking=True)

    _sql_constraints = [
        ('id_number_uniq', 'UNIQUE (id_number)', _('ID number already exists!')),
    ]

    @api.multi
    def create_employee(self):
        """Create HR employee from faculty record."""
        # CHANGED: @api.one → @api.multi (explicit loop)
        for record in self:
            if not record.last_name:
                record.write({'last_name': ' '})

            vals = {
                'name': ' '.join(filter(None, [
                    record.name,
                    record.middle_name or '',
                    record.last_name or ''
                ])),
                'country_id': record.nationality.id if record.nationality else False,
                'gender': record.gender,
                'job_id': record.job_id.id if record.job_id else False,
                'department_id': record.department_id.id if record.department_id else False,
                'address_home_id': record.partner_id.id,
                'identification_id': record.id_number,
                'work_email': record.email,
            }

            emp_id = self.env['hr.employee'].search([('identification_id', '=', record.id_number)], limit=1)

            if emp_id:
                record.write({'emp_id': emp_id.id})
                record.sudo().partner_id.write({'supplier': True, 'employee': True, 'email': record.email})
                _logger.info("Updated existing employee %s for faculty %s", emp_id.id, record.name)
            else:
                emp_id = self.env['hr.employee'].create(vals)
                record.write({'emp_id': emp_id.id})
                record.sudo().partner_id.write({'supplier': True, 'employee': True, 'email': record.email})
                _logger.info("Created new employee %s for faculty %s", emp_id.id, record.name)


class ResUsers(models.Model):
    """User extension - create users for faculty records."""

    _inherit = "res.users"
    _description = 'User Extended'

    @api.multi
    def create_user(self, records, user_group=None):
        """Create system user from faculty records."""
        # CHANGED: @api.one → @api.multi (explicit loop)
        oauth_provider = self.env['auth.oauth.provider'].sudo().search([('enabled', '=', True)], limit=1)
        if oauth_provider:
            provider = oauth_provider.id
        else:
            provider = 0

        for rec in records:
            if not rec.user_id:
                user_vals = {
                    'name': rec.name,
                    'login': rec.email,
                    'partner_id': rec.partner_id.id,
                    'oauth_provider_id': provider,
                    'oauth_uid': rec.email,
                    'groups_id': [(6, 0, [user_group.id] if user_group else [])],
                }
                user_id = self.create(user_vals)
                rec.user_id = user_id
                if user_group:
                    user_id.sudo().groups_id = [(6, 0, [user_group.id])]
                _logger.info("Created user %s for %s", user_id.login, rec.name)


class WizardOpFacultyEmployeeExt(models.TransientModel):
    """Wizard - create employees and users for faculty."""

    _inherit = 'wizard.op.faculty.employee'
    _description = "Create Employee and User of Faculty"

    user_boolean = fields.Boolean("Create user too?", default=True)

    @api.multi
    def create_employee(self):
        """Wizard action to create employee and user."""
        # CHANGED: @api.one → @api.multi (explicit loop)
        for record in self:
            active_id = self.env.context.get('active_ids', []) or []
            faculty = self.env['op.faculty'].browse(active_id)

            faculty.create_employee()

            if not faculty.emp_id.user_id:
                if record.user_boolean and not faculty.user_id:
                    # CHANGED: Added raise_if_not_found=False (safe ref handling in Odoo 12)
                    user_group = self.env.ref(
                        'hue_attendance.group_student_attendance_user',
                        raise_if_not_found=False)

                    if faculty.email and user_group:
                        self.env['res.users'].create_user(faculty, user_group)
                        _logger.info("Created user for faculty %s", faculty.name)

                if faculty.emp_id:
                    faculty.emp_id.user_id = faculty.user_id
            else:
                faculty.user_id = faculty.emp_id.user_id

            _logger.info("Employee creation completed for faculty %s", faculty.name)
