# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2017 Vertel AB (<http://vertel.se>).
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
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)

class mail_nodup(models.Model):
    _inherit='mail.nodup'

    recipent = fields.Char()
    subject  = fields.Char()
    date     = fields.Date(default=fields.Date.today())
    
    @api.model
    def check_dup(self,recipent,subject):
        for dup in self.env['mail.nodup'].search([('recipient','=',recipent),('subject','=',subject)]):
            if dup.date >= fields.Datetime.to_string(today + timedelta(days=int(self.env['ir.config_parameter'].get_param('mail_nodup days','7'))):
                dup.unlink()
        dups = self.env['mail.nodup'].search([('recipient','=',recipent),('subject','=',subject)])
        if not len(dups) > 0:
            self.env['mail.nodup'].create({'recipient': recipent,'subject':subject})
            return False
        else:
            return True
    
    