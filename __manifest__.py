# -*- coding: utf-8 -*-
{
    'name': "SWALAYAN SALES",

    'summary': """
        SWALAYAN SALES FIX AMIIIN""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sw_wh'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/customer_views.xml',
        'views/sales.xml',
        'views/discount_view.xml',
        'views/product_views.xml',
        'views/discpro_view.xml',
        'views/menu_view.xml',
    ],
}