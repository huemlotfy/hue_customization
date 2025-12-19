# HUE Customization - Technical Guide

**Module:** `hue_customization`  
**Version:** 12.0.1.0.0  
**Last Updated:** November 25, 2025

---

## 📑 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Data Models](#data-models)
3. [Business Logic](#business-logic)
4. [Security & Permissions](#security--permissions)
5. [Integration Points](#integration-points)
6. [API Reference](#api-reference)

---

## 🏗️ Architecture Overview

### Module Information
- **Name**: HUE Customization
- **Technical Name**: `hue_customization`
- **Version**: 12.0.1.0.0
- **Category**: Education
- **License**: LGPL-3

### Dependencies
This module depends on the following Odoo modules:

- `account`
- `mail`
- `openeducat_core`
- `web`

### Architecture Pattern
This module follows Odoo's MVC (Model-View-Controller) architecture:
- **Models** (Python): Business logic and data structure
- **Views** (XML): User interface definitions
- **Controllers** (Python): HTTP request handling

---

## 📊 Data Models

### Model Overview


#### `hue.academic.years`

**File:** `models/hue_academic_years.py`

**Statistics:**
- Fields: 38
- Methods: 10

**Fields:**
- `name` (Char)
- `from_date` (Date)
- `to_date` (Date)
- `active` (Boolean)
- `course_id` (Many2one)
- `faculty` (Many2one)
- `current` (Boolean)
- `gpa_current` (Boolean)
- `run_semester_gpa` (Boolean)
- `timetable_current` (Boolean)
- ... and 28 more

**Key Methods:**
- `generate_invoices_discount()`
- `assign_outstanding_credit()`
- `register_payment()`
- `generate_invoices_discount_ss()`
- `generate_invoices_gpa()`
- `register_payment()`
- `assign_outstanding_credit()`
- `generate_invoices()`
- `action_invoice_deactive()`
- `action_invoice_open()`


#### `hue.alumni.fees`

**File:** `models/hue_years.py`

**Statistics:**
- Fields: 32
- Methods: 3

**Fields:**
- `name` (Char)
- `total` (Integer)
- `total_dollar` (Integer)
- `total_special` (Integer)
- `status_ids` (Many2many)
- `faculty` (Many2one)
- `academic_year` (Many2one)
- `installment_ids` (One2many)
- `alumni_fees_id` (Many2one)
- `term_id` (Many2one)
- ... and 22 more

**Key Methods:**
- `generate_invoices()`
- `create()`
- `create()`


#### `hue.alumni.installment`

**File:** `models/hue_years.py`

**Statistics:**
- Fields: 32
- Methods: 3

**Fields:**
- `name` (Char)
- `total` (Integer)
- `total_dollar` (Integer)
- `total_special` (Integer)
- `status_ids` (Many2many)
- `faculty` (Many2one)
- `academic_year` (Many2one)
- `installment_ids` (One2many)
- `alumni_fees_id` (Many2one)
- `term_id` (Many2one)
- ... and 22 more

**Key Methods:**
- `generate_invoices()`
- `create()`
- `create()`


#### `hue.block.reason`

**File:** `models/student_extension_data.py`

**Statistics:**
- Fields: 102
- Methods: 7

**Fields:**
- `collage` (Many2one)
- `faculty` (Many2one)
- `level` (Many2one)
- `programs` (Selection)
- `course_id` (Many2one)
- `previous_course_id` (Many2one)
- `transfer_type` (Selection)
- `student_code` (Integer)
- `student_nationality` (Many2one)
- `student_city` (Many2one)
- ... and 92 more

**Key Methods:**
- `randomStringwithDigitsAndSymbols()`
- `validate_student_code()`
- `randomString()`
- `diable_ldap_user()`
- `create_user()`
- `create_student_user()`


#### `hue.certificates`

**File:** `models/hue_certificates.py`

**Statistics:**
- Fields: 16
- Methods: 3

**Fields:**
- `name` (Char)
- `d_id` (Char)
- `certificate_active` (Boolean)
- `certtype` (Selection)
- `enroll_code` (Char)
- `name` (Char)
- `d_id` (Char)
- `name` (Char)
- `en_name` (Char)
- `d_id` (Char)
- ... and 6 more

**Key Methods:**


#### `hue.certificates.conditions`

**File:** `models/hue_certificates.py`

**Statistics:**
- Fields: 16
- Methods: 3

**Fields:**
- `name` (Char)
- `d_id` (Char)
- `certificate_active` (Boolean)
- `certtype` (Selection)
- `enroll_code` (Char)
- `name` (Char)
- `d_id` (Char)
- `name` (Char)
- `en_name` (Char)
- `d_id` (Char)
- ... and 6 more

**Key Methods:**


#### `hue.cities`

**File:** `models/hue_certificates.py`

**Statistics:**
- Fields: 16
- Methods: 3

**Fields:**
- `name` (Char)
- `d_id` (Char)
- `certificate_active` (Boolean)
- `certtype` (Selection)
- `enroll_code` (Char)
- `name` (Char)
- `d_id` (Char)
- `name` (Char)
- `en_name` (Char)
- `d_id` (Char)
- ... and 6 more

**Key Methods:**


#### `hue.discounts`

**File:** `models/hue_discounts.py`

**Statistics:**
- Fields: 25
- Methods: 4

**Fields:**
- `name` (Char)
- `dataa` (Selection)
- `certificate_id` (Many2many)
- `nationality_id` (Many2many)
- `join_year_id` (Many2one)
- `faculty_ids` (Many2one)
- `course_id` (Many2one)
- `cgpa_from` (Float)
- `cgpa_to` (Float)
- `percentage_credit_hour` (Float)
- ... and 15 more

**Key Methods:**
- `create()`
- `write()`
- `unlink()`
- `generate_discount()`


#### `hue.faculties`

**File:** `models/hue_faculties.py`

**Statistics:**
- Fields: 3
- Methods: 1

**Fields:**
- `name` (Char)
- `identifier` (Integer)
- `d_id` (Char)

**Key Methods:**
- `sync_ldap_data()`


#### `hue.faculties.levels`

**File:** `models/hue_faculties_levels.py`

**Statistics:**
- Fields: 3
- Methods: 0

**Fields:**
- `name` (Char)
- `faculty` (Many2one)
- `d_id` (Char)


#### `hue.installments`

**File:** `models/hue_installments.py`

**Statistics:**
- Fields: 16
- Methods: 1

**Fields:**
- `name` (Char)
- `installments` (Integer)
- `years_id` (Many2one)
- `term_id` (Many2one)
- `one_time` (Boolean)
- `extra_inv` (Boolean)
- `foreign_nationality` (Boolean)
- `special_case` (Boolean)
- `currency` (Many2one)
- `installments_id` (Many2one)
- ... and 6 more

**Key Methods:**
- `create()`


#### `hue.joining.years`

**File:** `models/hue_joining_years.py`

**Statistics:**
- Fields: 5
- Methods: 0

**Fields:**
- `name` (Char)
- `d_id` (Char)
- `active` (Boolean)
- `faculty` (Many2one)
- `year_id` (Many2one)


#### `hue.nationalities`

**File:** `models/hue_nationalities.py`

**Statistics:**
- Fields: 4
- Methods: 0

**Fields:**
- `name` (Char)
- `en_name` (Char)
- `d_id` (Char)
- `foreign_nationality` (Boolean)


#### `hue.std.data.status`

**File:** `models/hue_certificates.py`

**Statistics:**
- Fields: 16
- Methods: 3

**Fields:**
- `name` (Char)
- `d_id` (Char)
- `certificate_active` (Boolean)
- `certtype` (Selection)
- `enroll_code` (Char)
- `name` (Char)
- `d_id` (Char)
- `name` (Char)
- `en_name` (Char)
- `d_id` (Char)
- ... and 6 more

**Key Methods:**


#### `hue.student.academic.years`

**File:** `models/hue_student_academic_years.py`

**Statistics:**
- Fields: 3
- Methods: 0

**Fields:**
- `student_id` (Many2one)
- `academic_year_id` (Many2one)
- `status` (Selection)


#### `hue.student.status`

**File:** `models/hue_student_status.py`

**Statistics:**
- Fields: 7
- Methods: 1

**Fields:**
- `student_id` (Many2one)
- `academic_id` (Many2one)
- `academic_term_id` (Many2one)
- `paid` (Boolean)
- `assigned` (Boolean)
- `one_time` (Boolean)
- `invoice_id` (Integer)

**Key Methods:**
- `action_open_related_document()`


#### `hue.terms`

**File:** `models/hue_terms.py`

**Statistics:**
- Fields: 6
- Methods: 0

**Fields:**
- `name` (Char)
- `term_id` (Many2one)
- `global_term_id` (Integer)
- `from_date` (Date)
- `to_date` (Date)
- `active` (Boolean)


#### `hue.years`

**File:** `models/hue_years.py`

**Statistics:**
- Fields: 32
- Methods: 3

**Fields:**
- `name` (Char)
- `total` (Integer)
- `total_dollar` (Integer)
- `total_special` (Integer)
- `status_ids` (Many2many)
- `faculty` (Many2one)
- `academic_year` (Many2one)
- `installment_ids` (One2many)
- `alumni_fees_id` (Many2one)
- `term_id` (Many2one)
- ... and 22 more

**Key Methods:**
- `generate_invoices()`
- `create()`
- `create()`


#### `hue.years.increase`

**File:** `models/hue_years.py`

**Statistics:**
- Fields: 32
- Methods: 3

**Fields:**
- `name` (Char)
- `total` (Integer)
- `total_dollar` (Integer)
- `total_special` (Integer)
- `status_ids` (Many2many)
- `faculty` (Many2one)
- `academic_year` (Many2one)
- `installment_ids` (One2many)
- `alumni_fees_id` (Many2one)
- `term_id` (Many2one)
- ... and 22 more

**Key Methods:**
- `generate_invoices()`
- `create()`
- `create()`


#### `student.ldap.directory`

**File:** `models/student_ldap.py`

**Statistics:**
- Fields: 6
- Methods: 1

**Fields:**
- `name` (Char)
- `ldap_server` (Char)
- `ldap_port` (Integer)
- `ldap_base_dn` (Char)
- `username` (Char)
- `password` (Char)

**Key Methods:**


#### `student_collage`

**File:** `models/student_extension.py`

**Statistics:**
- Fields: 4
- Methods: 2

**Fields:**
- `collage` (Many2one)
- `programs` (Selection)
- `student_code` (Integer)
- `name` (Char)

**Key Methods:**
- `onchange_collage()`
- `create_user()`


#### `{} / {} / {} / {}`

**File:** `models/hue_installments.py`

**Statistics:**
- Fields: 16
- Methods: 1

**Fields:**
- `name` (Char)
- `installments` (Integer)
- `years_id` (Many2one)
- `term_id` (Many2one)
- `one_time` (Boolean)
- `extra_inv` (Boolean)
- `foreign_nationality` (Boolean)
- `special_case` (Boolean)
- `currency` (Many2one)
- `installments_id` (Many2one)
- ... and 6 more

**Key Methods:**
- `create()`


---

## 🔐 Security & Permissions

### Access Rights
Total access rules: 32

### Security Groups
Total groups defined: 2

### Record Rules
Total record rules: 0


---

## 🔗 Integration Points

### Internal Dependencies
- `account`
- `mail`
- `openeducat_core`
- `web`

### External Systems
- LDAP integration for user authentication
- Office 365 for email services
- Custom API endpoints

---

## 📞 Support

For technical support, please contact:
- **Team:** HUE IT Department
- **Website:** https://horus.edu.eg

---

*This is an automatically generated technical guide. For more details, refer to the source code.*
