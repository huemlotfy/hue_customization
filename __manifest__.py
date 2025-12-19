# -*- coding: utf-8 -*-
{
    'name': "HUE Customization",
    'summary': "HUE customization for Ibn Elhaytham Data",
    'description': """
        Customization module for Horus University of Education (HUE)
        providing academic year management, invoicing, discounts, and student data handling.
    """,
    'author': "HUE IT",
    'website': "https://horus.edu.eg",
    'version': '12.0.1.0.0',
    'category': 'Education',
    'license': 'LGPL-3',
    'depends': [
        'openeducat_core',
        'account',
        'mail',
        'web',
    ],
    'data': [
        'security/hue_security.xml',
        'security/ir.model.access.csv',
        'views/ldap_directory_view.xml',
        'views/faculties_view.xml',
        'views/student_extension_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'web_icon': 'hue_customization,static/description/icon.png',
}
