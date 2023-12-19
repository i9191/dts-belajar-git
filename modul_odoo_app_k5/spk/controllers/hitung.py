from .model import mapres

class StudentAchievement(models.Model):
    _name = 'student.achievement'

    name = fields.Char(string='Nama')
    gpa = fields.Float(string='IPK')
    extracurricular = fields.Float(string='Kegiatan Ekstrakurikuler')
    research = fields.Float(string='Karya Ilmiah')

    def calculate_rank(self):
        # Membaca prioritas kriteria dari pengguna
        priorities = [
            request.env['ir.config_parameter'].sudo().get('priority_gpa'),
            request.env['ir.config_parameter'].sudo().get('priority_extracurricular'),
            request.env['ir.config_parameter'].sudo().get('priority_research')
        ]

        # Melakukan pembobotan dengan metode ROC
        roc_weights = self.roc_weights(priorities)

        # Melakukan perangkingan dengan metode MOORA
        scores = self.score_matrix(roc_weights)
        ranks = moora(scores)

        # Menyimpan peringkat ke database
        for rank, student in zip(ranks, self):
            student.rank = rank

    def roc_weights(self, priorities):
        # Menghitung bobot ROC untuk setiap kriteria
        roc_weights = []
        for i in range(len(priorities)):
            roc_weights.append(1 / (1 + (priorities[i] / priorities[i - 1])))
        return roc_weights

    def score_matrix(self, weights):
        # Menghitung matriks skor untuk setiap kriteria
        scores = []
        for student in self:
            scores.append([
                student.gpa * weights[0],
                student.extracurricular * weights[1],
                student.research * weights[2]
            ])
        return scores
