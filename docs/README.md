# HUE Customization

**Module Name:** `hue_customization`  
**Version:** 12.0.1.0.0  
**Category:** Education  
**License:** LGPL-3

## 📋 Overview

HUE customization for Ibn Elhaytham Data


        Customization module for Horus University of Education (HUE)
        providing academic year management, invoicing, discounts, and student data handling.
    

## ✨ Key Features

- **hue.block.reason**: 102 fields, 7 methods
- **hue.discounts**: 25 fields, 4 methods
- **student_collage**: 4 fields, 2 methods
- **hue.nationalities**: 4 fields, 0 methods
- **hue.installments**: 16 fields, 1 methods
- **{} / {} / {} / {}**: 16 fields, 1 methods
- **hue.academic.years**: 38 fields, 10 methods
- **hue.terms**: 6 fields, 0 methods
- **hue.alumni.fees**: 32 fields, 3 methods
- **hue.alumni.installment**: 32 fields, 3 methods
- **hue.years**: 32 fields, 3 methods
- **hue.years.increase**: 32 fields, 3 methods
- **hue.student.academic.years**: 3 fields, 0 methods
- **hue.certificates**: 16 fields, 3 methods
- **hue.cities**: 16 fields, 3 methods
- **hue.std.data.status**: 16 fields, 3 methods
- **hue.certificates.conditions**: 16 fields, 3 methods
- **hue.faculties**: 3 fields, 1 methods
- **hue.faculties.levels**: 3 fields, 0 methods
- **student.ldap.directory**: 6 fields, 1 methods
- **hue.student.status**: 7 fields, 1 methods
- **hue.joining.years**: 5 fields, 0 methods

## 🔧 Installation

### Prerequisites
- Odoo 12.0 or higher
- Required modules:
  - account
  - mail
  - openeducat_core
  - web

### Installation Steps

1. **Download the module:**
   ```bash
   cd /opt/odoo/custom/addons
   # Copy module files here
   ```

2. **Update module list:**
   ```bash
   # Restart Odoo server
   sudo systemctl restart odoo
   ```

3. **Install via UI:**
   - Go to Apps menu
   - Remove "Apps" filter
   - Search for "HUE Customization"
   - Click Install

## 📚 Documentation

- [Technical Guide](TECHNICAL_GUIDE.md) - Complete technical reference
- [Business Logic](BUSINESS_LOGIC.md) - Business processes and workflows
- [Testing Checklist](TESTING_CHECKLIST.md) - QA and testing procedures
- [Changelog](CHANGELOG.md) - Version history and updates

## 🏗️ Module Structure

```
hue_customization/
├── models/          # 22 models
├── views/           # 3 view files
├── security/        # Access rights and rules
├── data/            # Initial data
└── __manifest__.py  # Module configuration
```

## 📊 Statistics

- **Models**: 22
- **Fields**: 430
- **Methods**: 52
- **Views**: 3
- **Dependencies**: 4

## 👥 Support

**Author:** HUE IT  
**Website:** https://horus.edu.eg

For support and questions, please contact the HUE IT department.

## 📄 License

This module is licensed under LGPL-3 license.

---

*Generated on November 25, 2025*
