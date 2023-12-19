from odoo import api, models, fields, _
from odoo.exceptions import UserError

# definisikan class WizardReadCSV yang merupakan models.TransientModel
class WizardRefresh(models.TransientModel):
    # nama tabel di database
    _name = 'wizard.dashboard.refresh'
    # nama yang ditampilkan di odoo
    _description = 'Refresh Data Ranking di dashboard'



    # definisikan fungsi untuk membaca data dari file .csv
    def refresh_data(self):
        # ambil objek dari models mahasiswa.data
        dashboard = self.env['student.achievement']
        
        dashboard._write_records()
        # kembalikan action untuk menutup wizard
        # akademik.action_akademik()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'student.achievement',
            'view_mode': 'tree,form,graph',
            'view_type': 'tree'
        }



class StudentAchievement(models.Model):
    _name = 'student.achievement'
    _description = 'Student Achievement'

    name = fields.Char(string='Student Name', required=True)
    nlratio = fields.Float(string='Nilai Ratio')
    rank = fields.Integer(string='Peringkat')

    @api.model
    def _write_records(self):
        rank_model = self.env['rank.model'].search([], limit=10)
        self.search([]).unlink()  # Menghapus seluruh data sebelum menambahkan yang baru
        for record in rank_model:
            self.create({
                'name': record.name,
                'nlratio': record.ratio,
                'rank': record.rank
            })

    @api.model
    def _register_hook(self):
        super(StudentAchievement, self)._register_hook()
        self._write_records()

    def refresh_data(self):
        """
        Method untuk button "Refresh Data" yang akan menghapus seluruh data
        dan mengganti dengan data baru.
        """
        self._write_records()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',  # Untuk merefresh tampilan setelah pembaruan data
        }
