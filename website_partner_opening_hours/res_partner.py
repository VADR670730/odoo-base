# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2017 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, _
import math
import logging
_logger = logging.getLogger(__name__)


class OpeningHours(models.Model):
    _name = 'opening.hours'

    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner')
    dayofweek = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string='Day of week', required=True)
    open_time = fields.Float(string='Open Time')
    close_time = fields.Float(string='Close Time')
    break_start = fields.Float(string='Break Start')
    break_stop = fields.Float(string='Break Stop')
    close = fields.Boolean(string='Close')
    opening_hours = fields.Char(string='Opening Hours', compute='_opening_hours')

    @api.one
    def _opening_hours(self):
        if not self.close:
            if self.break_start == 0.0 or self.break_stop == 0.0:
                self.opening_hours = '%s-%s' %(self.get_float_time(self.open_time), self.get_float_time(self.close_time))
            else:
                self.opening_hours = '%s-%s %s-%s' %(self.get_float_time(self.open_time), self.get_float_time(self.break_start), self.get_float_time(self.break_stop), self.get_float_time(self.close_time))
        else:
            self.opening_hours = _('Close')


    @api.model
    def get_float_time(self, time):
        return ("%.2f" %(math.floor(float(time)) + (float(time)%1)*0.6)) if time else 0.0

class res_partner(models.Model):
    _inherit = 'res.partner'

    opening_hours_ids = fields.One2many(comodel_name='opening.hours', inverse_name='partner_id', string='Openning Hours')
