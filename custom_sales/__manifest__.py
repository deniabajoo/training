# -*- coding: utf-8 -*-
{
    'name': 'Custom Sales Extension',
    
    'summary': 'Modul custom untuk perubahan dan penambahan pada model Sales Order',
    
    'description': """
Custom Sales Extension
======================
Modul ini digunakan sebagai kerangka dasar untuk setiap perubahan dan penambahan 
pada model sales.order. Modul ini inherit dari sale.order dan dapat dikembangkan 
sesuai kebutuhan bisnis.
    """,
    
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    
    'category': 'Sales/Sales',
    'version': '18.0.1.0.0',
    
    # Module yang diperlukan untuk modul ini berfungsi
    'depends': ['sale_management'],
    
    # File data yang akan dimuat
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
    ],
    
    # Data demo (opsional)
    'demo': [
        # 'demo/demo.xml',
    ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

