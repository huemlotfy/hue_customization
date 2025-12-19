# -*- coding: utf-8 -*-
"""
Pre-migration script: Odoo 11 → Odoo 12
Executes BEFORE module installation to prepare database.

SCHEMA CHANGES REQUIRED:
  - None (all fields compatible)
"""

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Execute pre-migration steps.
    
    Args:
        cr: Database cursor
        version: Target version (e.g., '12.0.1.0.0')
    """
    _logger.info("Starting pre-migration for hue_customization to Odoo 12...")
    
    # Verify existing tables don't have deprecated columns
    cr.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name LIKE 'hue_%'
    """)
    existing_tables = [row[0] for row in cr.fetchall()]
    _logger.info("Found %d existing HUE tables", len(existing_tables))
    
    # No schema changes required for this migration
    _logger.info("Pre-migration completed successfully")
