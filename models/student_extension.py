# -*- coding: utf-8 -*-

from odoo import models, fields , api, _
from odoo.exceptions import UserError, ValidationError
import logging
import json
import ssl
try:
    # Python 2
    import urllib2
    from urllib2 import Request, urlopen
except ImportError:
    # Python 3
    from urllib.request import Request, urlopen
_logger = logging.getLogger(__name__)

class StudentExtension(models.Model):
    """Student Extension - additional student data and methods."""
    
    _inherit = 'op.student'
    _description = 'Student Extension'
    
    collage = fields.Many2one('student_collage', 'Collage')
    programs = fields.Selection([])
    student_code = fields.Integer('student_code')
    
    @api.onchange('collage')
    def onchange_collage(self):
        print("######################")
        url = "https://me.horus.edu.eg/WebServiceHorus?index=GetStudentBasicData&userName=myd777myd&password=lo@stmm&collegeID=3"
        req = Request(url, headers={ 'X-Mashape-Key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' })
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        webURL = urlopen(req, context=gcontext)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        data = json.loads(data.decode(encoding))
        return {'value': {'programs': data[1]['Studentname']}}
    
    @api.multi
    def create_user(self):
        print("______________Create user for student")
        student_group = self.env['res.groups'].search([('name','=','Student')])
        print(student_group.id)
        """Creating the employee for the faculty"""
        
        oauth_provider = self.env['auth.oauth.provider'].search([('enabled','=', True )],limit=1)
        if oauth_provider:
            provider = oauth_provider.id
        else:
            provider = 0
        for rec in self:
            if(rec.student_code):
                values = {
                    'name': rec.name +" "+ rec.last_name,
                    'image': rec.image,
                    'partner_id': rec.partner_id,
                    'login': str(rec.student_code)+"@horus.edu.eg",
                    'active': True,
                    'oauth_provider_id': provider,
                    'oauth_uid': str(rec.student_code)+"@horus.edu.eg",
                    # 'is_student': True,
                }
                user_id = self.env['res.users'].create(values)
                rec.user_id = user_id.id
                
                group_student = self.env.ref('base.group_portal', False)
                for group in user_id.groups_id :
                    group.write({'users': [(3, user_id.id)]})
                group_student.write({'users': [(4, user_id.id)]})
                # rec.user_id.partner_id.is_student = True
            else:
                raise UserError('Student code must be set!')

class CollageModel(models.Model):
    _name = "student_collage"
    _description = "Student Collage"
    _description = "Collage"
    name = fields.Char('collage_name')