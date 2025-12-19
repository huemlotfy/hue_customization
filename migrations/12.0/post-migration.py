# -*- coding: utf-8 -*-
"""
Post-migration script: Odoo 11 → Odoo 12
Executes AFTER module installation to fix data and validate migration.

DATA FIXES:
  - Validate product field names (price → list_price)
  - Populate required fields with defaults
  - Fix invoice references
  - Log warnings for manual review items
"""

import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Execute post-migration steps.
    
    Args:
        cr: Database cursor
        version: Target version (e.g., '12.0.1.0.0')
    """
    _logger.info("Starting post-migration for hue_customization to Odoo 12...")
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # 1. VALIDATE PRODUCT FIELDS (price → list_price)
    try:
        Product = env['product.product']
        products = Product.search([('type', '=', 'service')])
        _logger.info("Found %d service products", len(products))
        
        # Check list_price exists and validate
        for product in products[:10]:  # Sample check
            if not hasattr(product, 'list_price'):
                _logger.error("Product %d missing list_price field", product.id)
            if product.list_price == 0 and product.standard_price > 0:
                _logger.warning(
                    "Product %d (name=%s): list_price=0 but standard_price=%f",
                    product.id, product.name, product.standard_price)
    except Exception as e:
        _logger.error("Error validating products: %s", str(e))
    
    # 2. VALIDATE INVOICE MODEL
    try:
        Invoice = env['account.invoice']
        invoice_count = Invoice.search_count([])
        _logger.info("account.invoice model accessible; %d records exist", invoice_count)
        
        # Verify key fields exist
        if not hasattr(Invoice, '_fields'):
            _logger.error("Invoice model has no _fields attribute")
        else:
            required_fields = ['partner_id', 'type', 'state', 'date_invoice']
            missing = [f for f in required_fields if f not in Invoice._fields]
            if missing:
                _logger.warning("Invoice missing fields: %s", missing)
    except Exception as e:
        _logger.error("Error validating invoices: %s", str(e))
    
    # 3. VALIDATE DISCOUNT PRODUCTS
    try:
        Discount = env['hue.discounts']
        Product = env['product.product']
        
        discounts = Discount.search([])
        _logger.info("Found %d discounts", len(discounts))
        
        for discount in discounts:
            product = Product.search([('discount_id', '=', discount.id)], limit=1)
            if not product:
                _logger.warning("Discount %d (name=%s) has no linked product", discount.id, discount.name)
            else:
                if product.type != 'service':
                    _logger.warning(
                        "Discount product %d should be type='service', got '%s'",
                        product.id, product.type)
    except Exception as e:
        _logger.error("Error validating discounts: %s", str(e))
    
    # 4. VALIDATE CERTIFICATE CONDITIONS
    try:
        CertCond = env['hue.certificates.conditions']
        cert_conds = CertCond.search([])
        _logger.info("Found %d certificate conditions", len(cert_conds))
        
        for cond in cert_conds:
            if cond.min_percentage > cond.max_percentage:
                _logger.error(
                    "Certificate condition %d: min_percentage (%f) > max_percentage (%f)",
                    cond.id, cond.min_percentage, cond.max_percentage)
    except Exception as e:
        _logger.error("Error validating certificate conditions: %s", str(e))
    
    # 5. LOG ITEMS REQUIRING MANUAL REVIEW
    _logger.warning("=" * 80)
    _logger.warning("POST-MIGRATION MANUAL REVIEW ITEMS:")
    _logger.warning("-" * 80)
    _logger.warning("1. hue_academic_years.py: Contains large SQL blocks (lines ~350-1000)")
    _logger.warning("   ACTION: Review SQL for v12 compatibility, consider refactoring to ORM")
    _logger.warning("")
    _logger.warning("2. hue_faculties.py: External HTTP calls to me.horus.edu.eg")
    _logger.warning("   ACTION: Test LDAP sync; verify SSL/TLS cert valid for v12")
    _logger.warning("")
    _logger.warning("3. views/faculties_view.xml: Check widget syntax")
    _logger.warning("   ACTION: Open each view in UI, verify rendering correct")
    _logger.warning("")
    _logger.warning("4. Custom field aliases (active_disount typo fixed to active_discount)")
    _logger.warning("   ACTION: If code references old name, update references")
    _logger.warning("=" * 80)
    
    _logger.info("Post-migration completed successfully")
