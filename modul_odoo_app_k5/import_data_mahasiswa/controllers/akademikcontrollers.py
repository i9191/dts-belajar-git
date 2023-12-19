from odoo import http

import logging
_logger = logging.getLogger(__name__)

class AkademikControllers(http.Controller):
    # @http.route('/student_academic_data/<string:id>', type='json', auth='user', methods=['GET'])
    # def index(self, nim):
    #     # get data from model
    #     data = http.request.env['mahasiswa.dataakademik'].search(['nim','=',nim])
    #     # return data as json
    #     return {
    #         'nim': data.nim,
    #         'nama': data.nama,
    #         'nilai': str(data.nilai),
    #         'prestasi': data.prestasi,
    #         'kompen': data.kompen,
    #     }
    
    @http.route('/academic_data/mahasiswa', type='json', auth='user', methods=['GET'])
    def get_mahasiswa(self, **kwargs):
        _logger.info("API Data Mahasiswa...")
        # get the parameter from the request
        nim = kwargs.get('nim')
        # get the model object from the environment
        mahasiswa_model = http.request.env['mahasiswa.dataakademik']
        # search the data from the model based on the parameter
        if nim:
            if 'like' in nim:
                # use like operator with wildcard
                nim = nim.replace('like', '')
                mahasiswa_data = mahasiswa_model.search([('nim', 'like', nim)])
            else:
                # use equal operator
                mahasiswa_data = mahasiswa_model.search([('nim', '=', nim)])
        else:
            mahasiswa_data = mahasiswa_model.search([])
        # convert the data to a list of dictionaries
        mahasiswa_list = []
        for data in mahasiswa_data:
            mahasiswa_list.append({
                'nim': data.nim,
                'nama': data.nama,
                'nilai': data.nilai,
                'prestasi': data.prestasi,
                'kompen': data.kompen,
            })
        # return the data as json
        return {
            'count': len(mahasiswa_list),
            'data': mahasiswa_list
        }

