# import library yang dibutuhkan
import csv
import base64
from odoo import models, fields, api

# definisikan class WizardReadCSV yang merupakan models.TransientModel
class WizardDataMahasiswaCSV(models.TransientModel):
    # nama tabel di database
    _name = 'wizard.datamahasiswa'
    # nama yang ditampilkan di odoo
    _description = 'Wizard Baca Data Mahasiswa dari CSV'

    # definisikan field file_path yang bertipe Char
    file_csv = fields.Binary(string='File CSV', required=True)

    # definisikan fungsi untuk membaca data dari file .csv
    def read_csv(self):
        # ambil objek dari models mahasiswa.data
        mhs = self.env['mahasiswa.data']
        # ambil nilai dari field file_path
        file_csv = self.file_csv
        # panggil fungsi read_csv dari models mahasiswa.data dengan parameter file_path
        mhs.read_csv(file_csv)
        # kembalikan action untuk menutup wizard
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mahasiswa.data',
            'view_mode': 'tree,form',
            'view_type': 'form'
        }

# definisikan class Mahasiswa yang merupakan models.Model
class DataMahasiswa(models.Model):
    # nama tabel di database
    _name = 'mahasiswa.data'
    # nama yang ditampilkan di odoo
    _description = 'Data Mahasiswa'

    # definisikan field-field yang ada di tabel
    nim = fields.Char(string='NIM', required=True)
    nama = fields.Char(string='Nama', required=True)
    prestasi = fields.Integer(string='Total Prestasi', required=True)
    kompen = fields.Integer(string='Total Kompen', required=True)

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
            nim = row[0]
            nama = row[1]
            prestasi = 1 #sementara 1
            alpaku = int(row[len(row)-1])
            # buat record baru di tabel dengan data yang dibaca
            record = self.search([('nim', '=', nim)])
            # jika record tidak ditemukan, buat record baru dengan data yang dibaca
            if not record:
                self.create({
                    'nim': nim,
                    'nama': nama,
                    'prestasi': prestasi,
                    'kompen': alpaku,
                })
            else:    
                record.write({
                    'nama': nama,
                    'prestasi': prestasi,
                    'kompen': alpaku,
                })

    # @api.depends('nilai')
    # def _viewnilai(self):
    #     self.nilai_view = False
    #     for item in self:
    #         item.nilai_view = str(item.nilai) + "\n" + item.nama

    def action_mahasiswa(self):
        # kembalikan action yang sudah didefinisikan di views xml
        return self.env.ref('import_data_mahasiswa.action_mahasiswa').read()[0]
    
    # definisikan fungsi untuk memanggil action untuk membuka wizard untuk read_csv
    def action_mahasiswa_read_csv(self):
        # kembalikan action yang sudah didefinisikan di views xml
        return self.env.ref('import_data_mahasiswa.action_mahasiswa_read_csv').read()[0]
