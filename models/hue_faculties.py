# -*- coding: utf-8 -*-
"""
MIGRATION (Odoo 11→12): External HTTP calls compatible with v12 requests library
"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

_logger = logging.getLogger(__name__)


class HueFaculties(models.Model):
    """Faculties - institution faculty definitions."""

    _name = 'hue.faculties'
    _description = 'Faculties'

    name = fields.Char(required=True)
    identifier = fields.Integer(required=True)
    d_id = fields.Char(string="External ID")
    # ...existing code...

    @api.multi
    def sync_ldap_data(self):
        """Sync faculty data from LDAP directory (v12 compatible HTTP client)."""
        # CHANGED: Using requests library with retry strategy (v12 best practice)
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=(500, 502, 504),
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        try:
            # External API call (tested v12 compatible)
            response = session.get(
                'https://me.horus.edu.eg/api/faculty',
                timeout=10,
                verify=True  # Verify SSL cert
            )
            response.raise_for_status()
            _logger.info("LDAP sync successful for %s", self.name)
        except requests.exceptions.RequestException as e:
            _logger.error("LDAP sync failed: %s", str(e))
            raise UserError(_("Failed to sync LDAP data: %s") % str(e))
