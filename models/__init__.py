# -*- coding: utf-8 -*-
"""
Odoo 12 compatible model imports.

MIGRATION NOTES (Odoo 11 → Odoo 12):
  - Organized imports in logical order (base models first, then extensions)
  - Verified all imported modules exist (no orphaned imports)
  - Added docstring (Odoo 12 convention)
"""

# Base models
from . import hue_faculties
from . import hue_faculties_levels
from . import hue_joining_years
from . import hue_years
from . import hue_installments
from . import hue_discounts
from . import hue_certificates
from . import hue_nationalities
from . import hue_student_status

# Model extensions & related modules
from . import hue_faculty
from . import student_extension_data
from . import student_extension
from . import student_ldap
from . import hue_academic_years
from . import hue_terms
from . import hue_student_academic_years

