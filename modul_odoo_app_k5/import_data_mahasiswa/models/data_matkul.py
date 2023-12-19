# import library yang dibutuhkan
import csv
import base64
from odoo import models, fields, api, exceptions

# definisikan class WizardReadCSV yang merupakan models.TransientModel
class WizardReadCSVMatkul(models.TransientModel):
    # nama tabel di database
    _name = 'wizard.readcsv.matkul'
    # nama yang ditampilkan di odoo
    _description = 'Wizard Baca Data Akademik Mahasiswa dari CSV'

    # definisikan field file_path yang bertipe Char
    file_csv = fields.Binary(string='File CSV', required=True)

    # definisikan fungsi untuk membaca data dari file .csv
    def read_csv(self):
        # ambil objek dari models mahasiswa.data
        matkulmod = self.env['mahasiswa.data.matkul']
        # ambil nilai dari field file_path
        file_csv = self.file_csv
        # panggil fungsi read_csv dari models dengan parameter file_path
        matkulmod.read_csv(file_csv)
        # kembalikan action untuk menutup wizard
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mahasiswa.data.matkul',
            'view_mode': 'tree,form',
            'view_type': 'tree'
        }

# definisikan class Mahasiswa yang merupakan models.Model
class DataMatkul(models.Model):
    # nama tabel di database
    _name = 'mahasiswa.data.matkul'
    # nama yang ditampilkan di odoo
    _description = 'Data Mata Kuliah Akademik'

    # definisikan field-field yang ada di tabel
    kode = fields.Char(string='Kode', required=True)
    matkul = fields.Char(string='Mata Kuliah', required=True)
    sks = fields.Integer(string='SKS', required=True)
    jam = fields.Integer(string='Jam', required=True)

    # definisikan fungsi untuk membaca data dari file .csv
    @api.model
    def read_csv(self, file_csv):
        # buka file .csv dengan mode 'r' (read)
        csv_data = base64.b64decode(file_csv).decode("utf-8")
        reader = csv.reader(csv_data.splitlines(), delimiter=",")
        # lewati baris pertama yang berisi header
        header = next(reader)
        # iterasi setiap baris di file
        for row in reader:
            # ambil data dari setiap kolom
            kode = row[0]
            matkul = row[1]
            sks = int(row[2]) #sementara 1
            jam = int(row[3])
            # buat record baru di tabel dengan data yang dibaca
            record = self.search([('kode', '=', kode)])
            # jika record tidak ditemukan, buat record baru dengan data yang dibaca
            if not record:
                self.create({
                    'kode': kode,
                    'matkul': matkul,
                    'sks': sks,
                    'jam': jam,
                })
            else:    
                record.write({
                    'matkul': matkul,
                    'sks': sks,
                    'jam': jam,
                })

    def action_matkul_akademik(self):
        # kembalikan action yang sudah didefinisikan di views xml
        return self.env.ref('import_data_mahasiswa.action_matkul_akademik').read()[0]
    
    # definisikan fungsi untuk memanggil action untuk membuka wizard untuk read_csv
    def action_matkul_read_csv(self):
        # kembalikan action yang sudah didefinisikan di views xml
        return self.env.ref('import_data_mahasiswa.action_matkul_read_csv').read()[0]
