from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class Rank_Wizard(models.TransientModel):
    _name = "wizard.rank.stage"
    _description = "Wizard to read csv file as input for the selection calculation"

    def check_group_id_change(self,ch_last):
        lgroup = [a.group_id for a in self.env['rank.stage'].search([])]

        for index in range(len(lgroup)):
            # Cek jika ada record dengan group_id yang kosong
            if index+1 not in lgroup:
                bp = index+1
                # if not record.group_id:
                _logger.info(f"group id {bp} not found")
                sub_records = self.env['rank.stage'].search([('group_id', '=', bp+1)])
                for item in sub_records:
                    _logger.info(f"change {item.criteria} from {item.group_id} to {item.group_id - 1}")
                    item.write({'group_id': (item.group_id - 1)})
        if ch_last:
            last_record = self.env['rank.stage'].search([])[-1]
            _logger.info(f"change {last_record.criteria} from {last_record.group_id} to {last_record.group_id + 1}")
            last_record.write({'group_id': (last_record.group_id + 1)})
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        #     'params': {
        #         'menu_id': self.env.ref('dss_student_achievement.menu_stage_rank').id,
        #     },
        #     # 'type': 'ir.actions.act_window',
        #     # 'res_model': 'rank.stage',
        #     # 'view_mode': 'kanban',
        #     # 'view_type': 'kanban'
        # }

class Rank_stage(models.Model):
    _name = "rank.stage"
    _description = "Model to store the sequence stage"

    # name = fields.Char('Name', required=True)
    criteria = fields.Char('Criteria', required=True)
    # group_id = fields.Char('Group', default='Criteria')
    group_id = fields.Integer('Group', required=True)
    sequence = fields.Integer('Sequence')
    readonly = fields.Boolean('Readonly', default=False)
                
    # untuk mencegah kriteria tidak diubah rank ordernya
    @api.constrains('sequence')
    def _check_sequence(self):
        # stage_first_id = self.env.ref('dss_student_achievement.rank_stage_first').id 
        # stage_last_id = self.env.ref('dss_student_achievement.rank_stage_last').id 
        stage_first_id = self.env['rank.stage'].search([])[0].id
        stage_last_id = self.env['rank.stage'].search([])[-1].id
        for stage in self:
            if stage.id == stage_first_id:
                if stage.sequence != 1:
                    raise UserError(_(f'You cannot change the order of first stage. ID: {stage.id} sequence: {stage.sequence}'))
            if stage.id == stage_last_id:
                if stage.sequence != len(self.env['rank.stage'].search([])):
                    raise UserError(_(f'You cannot change the order of last stage. ID: {stage.id} sequence: {stage.sequence}'))
    
    def write(self,vals):
        # stage_first_id = self.env.ref('dss_student_achievement.rank_stage_first').id 
        # stage_last_id = self.env.ref('dss_student_achievement.rank_stage_last').id 
        stage_first_id = self.env['rank.stage'].search([])[0].id
        stage_last_id = self.env['rank.stage'].search([])[-1].id

        lgroup = [a.group_id for a in self.search([])]
        change_last = False

        if lgroup:
            _logger.info(f"list gid {lgroup}")
            _logger.info(f"vals {vals}")
            if 'group_id' in vals:
                _logger.info(f"vals:{vals['group_id']}")
                change_last = (vals['group_id'] == max(lgroup))
            lgroup.pop()
            _logger.info(f"list gid after pop {lgroup}")
            maxgroup = max(lgroup)
        # for stage in self:
            # _logger.info(f"Index {stage.criteria}")
        _logger.info(f"({self.id}) {vals}")
        if self.id == stage_first_id:
            if vals['group_id'] != 1:
                raise UserError(_(f'You cannot change the order of first stage. ID: {self.id} to group: {vals["group_id"]}'))
        elif self.id == stage_last_id:
            if vals['group_id'] != maxgroup+1:
                raise UserError(_(f'You cannot change the order of last stage. ID: {self.id} to group: {vals["group_id"]}'))
        override_write = super(Rank_stage,self).write(vals)
        self.env['wizard.rank.stage'].check_group_id_change(change_last)
    
    def get_stage_rank(self):
        datastage = self.env['rank.stage'].search_read([])
        arrstage = []
        for item in datastage:
            arrstage.append({
                'name':item['criteria'],
                'rank':item['sequence'],
            })
        return arrstage



