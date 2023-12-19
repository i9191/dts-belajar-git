{
    'name': 'Student Achievements Dashboard',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Dashboard for Student Achievements',
    'sequence': 10,
    'license': 'LGPL-3',
    'website': 'https://www.yourcompany.com',
    'description': """
                    Student Achievements Dashboard
                    ==============================
                    This module provides a dashboard to display student achievements. This module allows you to track and manage student achievements,
                    and provides a dashboard for easy visualization of their accomplishments.
                    """,
    'author': 'Khosyi Nasywa Imanda',
    'depends': ['base'],

    'assets': {
        'web.assets_backend': [
            'my_module_dashboard/static/src/xml/refresh_button.xml',
            'my_module_dashboard/static/src/js/refresh_button.js',
            # 'import_data_mahasiswa/static/src/js/kanban_button.js',
            # 'import_data_mahasiswa/static/src/xml/kanban_button.xml',
        ],
    },

    'data': [
        'security/security.xml',  # Tambahkan baris ini
        'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/menu.xml',  # File baru Anda
        #'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
