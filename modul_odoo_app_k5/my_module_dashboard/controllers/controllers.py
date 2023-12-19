from odoo import http

class StudentAchievements(http.Controller):
    @http.route('/student_achievements/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/student_achievements/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('student_achievements.listing', {
            'root': '/student_achievements',
            'objects': http.request.env['student.achievement'].search([]),
        })

    @http.route('/student_achievements/objects/<model("student.achievement"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('student_achievements.object', {
            'object': obj
        })
