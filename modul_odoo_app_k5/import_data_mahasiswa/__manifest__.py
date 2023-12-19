{
    "name": "Import Data Mahasiswa",
    "version": "1.0.1",
    "category": "Tools",
    "author": "Ibnu Tsalis Assalam",
    "summary": "A module to manage academic data imported from CSV files",
    "depends": ["base"],
    'assets': {
        'web.assets_backend': [
            'import_data_mahasiswa/static/src/xml/custom_button.xml',
            'import_data_mahasiswa/static/src/js/custom_button.js',
            # 'import_data_mahasiswa/static/src/js/kanban_button.js',
            # 'import_data_mahasiswa/static/src/xml/kanban_button.xml',
        ],
    },
    "data": [
        # "views/csv_import_view.xml",
        "views/akademik_view.xml",
        "views/mahasiswa_view.xml",
        "views/matkul_view.xml",
        "security/ir.model.access.csv",
        "demo/demo.xml"
    ],
    "installable": True,
    "application": False,
}
