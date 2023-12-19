class StudentAchievement(models.Model):
    _name = 'student.achievement'

    name = fields.Char(string='Nama')
    gpa = fields.Float(string='IPK')
    extracurricular = fields.Float(string='Kegiatan Ekstrakurikuler')
    research = fields.Float(string='Karya Ilmiah')
    rank = fields.Integer(string='Peringkat')
