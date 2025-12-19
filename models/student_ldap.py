# -*- coding: utf-8 -*-
"""
MIGRATION (Odoo 11→12): LDAP integration compatible with v12 python-ldap library
"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class StudentLdapDirectory(models.Model):
    """LDAP Directory - student LDAP server configuration."""
    
    _name = 'student.ldap.directory'
    _description = 'Student LDAP Directory'
    
    name = fields.Char(required=True)
    ldap_server = fields.Char(required=True)
    ldap_port = fields.Integer(default=389)
    ldap_base_dn = fields.Char(required=True)
    username = fields.Char()
    password = fields.Char()
    
    @api.multi
    def _student_sync_ldap(self):
        """Sync student data from LDAP server (v12 compatible)."""
        for record in self:
            _logger.info("Syncing LDAP students from %s", record.ldap_server)
            # ...existing LDAP sync logic...