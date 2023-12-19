# import library yang dibutuhkan
import csv
import base64
from io import StringIO
from odoo import models, fields, api, exceptions
from .json_field import JsonField
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

# definisikan class WizardReadCSV yang merupakan models.TransientModel
class WizardDataAkademikCSV(models.TransientModel):
    # nama tabel di database
    _name = 'wizard.dataakademik.csv'
    # nama yang ditampilkan di odoo
    _description = 'Wizard Baca Data Akademik Mahasiswa dari CSV'

    # definisikan field file_path yang bertipe Char
    file_csv = fields.Binary(string='File CSV', required=True)

    # definisikan fungsi untuk membaca data dari file .csv
    def read_csv(self):
        # ambil objek dari models mahasiswa.data
        akademik = self.env['mahasiswa.dataakademik']
        # ambil nilai dari field file_path
        file_csv = self.file_csv
        # panggil fungsi read_csv dari models mahasiswa.data dengan parameter file_path
        akademik.read_csv(file_csv)
        # kembalikan action untuk menutup wizard
        # akademik.action_akademik()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'mahasiswa.dataakademik',
            'view_mode': 'tree,form',
            'view_type': 'form'
        }

# definisikan class Mahasiswa yang merupakan models.Model
class DataAkademik(models.Model):
    # nama tabel di database
    _name = 'mahasiswa.dataakademik'
    # nama yang ditampilkan di odoo
    _description = 'Data Akademik Mahasiswa'

    # definisikan field-field yang ada di tabel
    nim_id = fields.Many2one('mahasiswa.data', string='NIMID', ondelete='cascade')
    nim = fields.Char(related='nim_id.nim', string='NIM')
    nama = fields.Char(related='nim_id.nama', string='Nama', store=True)
    kode_matkul_id = fields.Many2one('mahasiswa.data.matkul', string='MatakuliahID', ondelete='cascade')
    matkul = fields.Char(related='kode_matkul_id.matkul', string='Mata Kuliah', store=True)
    nilai = JsonField(string="Kumpulan Nilai")
    nilai2 = fields.Float(string='Nilai')
    # nilai_view = fields.Char(string="Kumpulan Nilai 2", compute='_viewnilai')
    prestasi = fields.Integer(related='nim_id.prestasi', string='Total Prestasi')
    kompen = fields.Integer(related='nim_id.kompen', string='Total Kompen')

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
            nilai = {}
            for n in range(2,len(header)-2):
                matrecord = self.env['mahasiswa.data.matkul'].search([('kode', '=', header[n])])
                nilai[matrecord.matkul] = float(row[n])

            for n in range(2,len(header)-2):
                mhsrecord = self.env['mahasiswa.data'].search([('nim', '=', nim)])
                if not mhsrecord:
                    _logger.info(f"No Record with NIM {nim}")
                else:
                    matrecord = self.env['mahasiswa.data.matkul'].search([('kode', '=', header[n])])
                    if not matrecord:
                        _logger.info(f"No Matkul with Kode {header[n]}")
                    else:
                        record = self.search([('nim_id', '=', mhsrecord.id),
                                              ('kode_matkul_id', '=', matrecord.id)])
                        if not record:
                            self.create({
                                'nim_id': mhsrecord.id,
                                # 'nama': nama,
                                'kode_matkul_id': matrecord.id,
                                'nilai': nilai,
                                'nilai2': float(row[n]),
                                # 'prestasi': prestasi,
                                # 'kompen': alpaku,
                            })
                        else:
                            record.write({
                                # 'nama': nama,
                                'nilai': nilai,
                                'nilai2': float(row[n]),
                                # 'prestasi': prestasi,
                                # 'kompen': alpaku,
                            })
            # buat record baru di tabel dengan data yang dibaca
            # record = self.search([('nim', '=', nim)])
            # # jika record tidak ditemukan, buat record baru dengan data yang dibaca
            # if not record:
            #     self.create({
            #         'nim': nim,
            #         'nama': nama,
            #         'nilai': nilai,
            #         'prestasi': prestasi,
            #         'kompen': alpaku,
            #     })
            # else:    
            #     record.write({
            #         'nama': nama,
            #         'nilai': nilai,
            #         'prestasi': prestasi,
            #         'kompen': alpaku,
            #     })

    # @api.depends('nilai')
    # def _viewnilai(self):
    #     self.nilai_view = False
    #     for item in self:
    #         item.nilai_view = str(item.nilai) + "\n" + item.nama

    def action_akademik(self):
        # kembalikan action yang sudah didefinisikan di views xml
        return self.env.ref('import_data_mahasiswa.action_akademik').read()[0]
    
    # definisikan fungsi untuk memanggil action untuk membuka wizard untuk read_csv
    def action_akademik_read_csv(self):
        # kembalikan action yang sudah didefinisikan di views xml
        return self.env.ref('import_data_mahasiswa.action_akademik_read_csv').read()[0]
