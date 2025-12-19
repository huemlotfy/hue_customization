# -*- coding: utf-8 -*-
"""
MIGRATION (Odoo 11→12): OpenEducat student extension fully v12 compatible
"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
import random
import string
import datetime

try:
    import ldap3
    from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
    LDAP3_AVAILABLE = True
except ImportError:
    LDAP3_AVAILABLE = False
    _logger = logging.getLogger(__name__)
    _logger.warning("ldap3 library not installed. LDAP features will be disabled.")

_logger = logging.getLogger(__name__)

class OpStudentExt(models.Model):
    """OpenEducat Student Extension - additional student fields."""
    
    _inherit = 'op.student'
    _description = 'Student Extension'
    
    
    def randomStringwithDigitsAndSymbols(self, stringLength=8):
        """Generate a random string of letters, digits and special characters """
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))

    #collage = fields.Many2one('student_collage', 'Collage')
    faculty = fields.Many2one('hue.faculties', 'faculty', tracking=True)
    level = fields.Many2one('hue.faculties.levels', 'level', tracking=True)
    #programs = fields.Selection([])
    course_id = fields.Many2one('op.course', tracking=True  ,domain="[('parent_id', '=', course_id)]")
    previous_course_id = fields.Many2one('op.course', tracking=True)
    transfer_type = fields.Selection([('internal', 'internal'), ('external', 'external')])
    student_code = fields.Integer('Student Code', tracking=True)
    student_nationality = fields.Many2one('hue.nationalities', tracking=True)
    student_city = fields.Many2one('hue.cities', tracking=True , string="Student birth Country")
    student_birth_place = fields.Many2one('hue.cities', tracking=True)
    student_status = fields.Many2one('hue.std.data.status', tracking=True)
    student_certificates = fields.Many2one('hue.certificates', tracking=True)
    certificate_country = fields.Many2one('hue.nationalities', tracking=True)
    certificate_date =fields.Selection([(num, str(num)) for num in range( ((datetime.datetime.now().year)-34), ((datetime.datetime.now().year)+1) )])
    university_name = fields.Many2one('hue.university.transfer' , tracking=True)
    university_country = fields.Many2one('res.country' , tracking=True)
    special_case = fields.Boolean(tracking=True)
    join_year = fields.Many2one('hue.joining.years' , tracking=True , string="Join Year")
    join_term = fields.Many2one('op.semesters' , tracking=True , string='Join Term')
    timestamp= fields.Datetime()
    cgpa = fields.Float('cgpa', tracking=True)
    percentage =  fields.Float('Percentage', tracking=True)
    year = fields.Selection([(num, str(num)) for num in range( ((datetime.datetime.now().year)-15), ((datetime.datetime.now().year)+5) )])
    mc = fields.Boolean(tracking=True)
    father_discount = fields.Boolean(tracking=True , string='Staff discount')
    brother_discount = fields.Boolean(tracking=True , string='Sibling discount')
    syndicate_discount = fields.Boolean(tracking=True , string='Syndicate discount')
    martyrs_discount = fields.Boolean(tracking=True , string='Martyrs discount')
    early_discount = fields.Boolean(tracking=True , string='Early discount')
    extra_discount = fields.Boolean(tracking=True , string='Extra discount')
    syrian_egyptian = fields.Boolean(tracking=True)
    egyptian_expatriate = fields.Boolean(tracking=True)
    image_mc_discount = fields.Binary(string='Mc Image' ,attachment=True)
    image_brother_discount = fields.Binary(string='Sibling Discount Image',attachment=True)
    image_syndicate_discount = fields.Binary(string='Syndicate Image',attachment=True)
    image_martyrs_discount = fields.Binary(string='Martyrs Image',attachment=True)
    excellence_discount =fields.Selection([('3.50_3.76','from 3.50 to 3.76'),('3.76_4','from 3.76 to 4')], tracking=True)
    top_student_discount =fields.Selection([('50%','50%'),('25%','25%'),('15%','15%'),('5%','5%')], tracking=True)
    allow_registration = fields.Boolean(tracking=True)
    user_id = fields.Many2one('res.users', 'Related User')
    password = fields.Char()
    en_name = fields.Char(tracking=True)
    d_name = fields.Char( string="ID Name",tracking=True)
    registration_block_reason = fields.Many2one('hue.block.reason', 'Registration Block Reason', tracking=True)
    result_block_reason = fields.Many2one('hue.block.reason', 'Result Block Reason', tracking=True)
    national_id = fields.Char('National ID', tracking=True)
    military_status = fields.Selection([('ادي الخدمة','ادي الخدمة'),('معاف مؤقت','معاف مؤقت'),('معاف نهائي','معاف نهائي'),('مؤجل لسن 28','مؤجل لسن 28'),('مؤجل لسن 29','مؤجل لسن 29'),('تحت الطلب','تحت الطلب'),('تم تسوية الموقف التجنيدي نهائيا','تم تسوية الموقف التجنيدي نهائيا')], tracking=True)
    student_term = fields.Integer()
    # stu_photo_hide = fields.Boolean('Hide Photo')
    photo_hide = fields.Boolean('Hide Photo', tracking=True)
    specialneeds = fields.Boolean('Special Needs', tracking=True)
    new_gpa = fields.Float()
    original_gpa = fields.Float(digits=(16, 10))
    crh = fields.Float('Earned Hours') #, tracking=True
    new_crh = fields.Float('New Earned Hours') #, tracking=True
    core_crh = fields.Float('Core Hours') # tracking=True
    elective_crh = fields.Float('Elective Hours') #, tracking=True
    project_crh = fields.Float('Project Hours') #, tracking=True
    religion = fields.Selection([('مسلم','مسلم'),('مسيحى','مسيحى')] , string="Religion", tracking=True)
    prequaldegree = fields.Float('Degree', tracking=True)
    stumobile = fields.Char('Mobile', tracking=True)
    stutele = fields.Char('Phone', tracking=True)
    advisor = fields.Char(compute="_advisor")
    std_type = fields.Selection(
        [('regular', 'regular'), ('transferred', 'transferred'),
         ('scholarship', 'scholarship'), ('expatriate', 'expatriate'),('special_case', 'special case'),('special_case_transfer', 'special case transfer')])
    extra_national_id = fields.Char(tracking=True, string="Extra Nationail ID")
    seatno = fields.Char('Seat Number', tracking=True)
    qualyear = fields.Many2one('hue.joining.years', tracking=True , string="Qualification Year")
    militaryno = fields.Char('Military Number', tracking=True)
    decisionno = fields.Char('Decision Number', tracking=True)
    military_date = fields.Char('Military Date', tracking=True)
    admission_notes = fields.Char('Admission Notes', tracking=True)
    gardian_name = fields.Char('Guardian Name', tracking=True)
    gardian_type = fields.Selection([('أب','أب'),('أم','أم'),('خال','خال'),('عم','عم'),('أخ','أخ'),('أخت','أخت')] , tracking=True , string="Guardian Name")
    gardian_tele = fields.Char('Guardian Phone', tracking=True)
    gardian_mobile = fields.Char('Guardian Mobile', tracking=True)
    scholarship = fields.Selection([('5','Partial 5%'),('10','Partial 10%'),('15','Partial 15%'),('20','Partial 20%'),('25','Partial 25%')
        ,('30','Partial 30%'),('35','Partial 35%'),('40','Partial 40%'),('45','Partial 45%'),('50','Partial 50%'),('55','Partial 55%'),('60','Partial 60%'),('65','Partial 65%')
        ,('70','Partial 70%'),('75','Partial 75%'),('80','Partial 80%'),('85','Partial 85%'),('90','Partial 90%'),('95','Partial 95%'),('100','Full')
        ], tracking=True)
    sds_tobedeleted = fields.Boolean( tracking=True)
    special_needs =fields.Boolean()
    educational_mandate = fields.Boolean()
    postgraduate_code = fields.Char(tracking=True)
    new_high_school_certificate = fields.Boolean(string="New High School Certificate")
    def validate_student_code(self):
        for obj in self:
            domain = [
                ('student_code', '=', obj.student_code),
                ('id', '!=', obj.id),
            ]
            data = self.sudo().search_count(domain)
            if data:
                raise ValidationError(('Student Code alredy exist, Try again '))                
            return True

    def randomString(self,stringLength=6):
        return ''.join(random.choice(str(random.randint(1,9))) for i in range(stringLength))

    @api.model
    def diable_ldap_user(self):
        if not LDAP3_AVAILABLE:
            raise UserError(_("LDAP3 library is not installed. Please install python-ldap3 to use LDAP features."))
        
        ldap_conn = self.env["ldap.directory"]._ldap_connect()
        conn = ldap_conn[0]
        conn.start_tls()
        ldap_base = ldap_conn[1]
        print("11111111111")
        status_ids = self.env['hue.std.data.status'].sudo().search([('id', 'not in',[2,42,48,])])._ids
        i = 1
        for rec in self.search([('student_status', 'in', status_ids)]):
            ldap_base = 'OU=HUE-Faculties,DC=horus,DC=edu,DC=eg'
            search_dn = conn.search(format(ldap_base),search_filter='(|(sAMAccountName='+str(rec.student_code)+')(mail='+rec.email+'))',search_scope=SUBTREE,attributes=['distinguishedName','userAccountControl'])
            if search_dn:
                userdn = str(conn.response[0]['attributes']['distinguishedName'])
                userAccountControl = str(conn.response[0]['attributes']['userAccountControl'])
                if userAccountControl == '66048' :
                    conn.modify(userdn, {'userAccountControl': [('MODIFY_REPLACE', 2)]})
                    print("_________________________" + str(i) + "__________________________")
                    i = i+1
        #


    @api.multi
    def create_user(self):
        if not LDAP3_AVAILABLE:
            raise UserError(_("LDAP3 library is not installed. Please install python-ldap3 to use LDAP features."))
        
        ldap_conn = self.env["ldap.directory"]._ldap_connect()
        conn = ldap_conn[0]
        conn.start_tls()
        conn.raise_exceptions = True
        ldap_base = ldap_conn[1]
        # create user
        for rec in self:
            if rec.postgraduate_code :
                student_code = rec.postgraduate_code
            else :
                student_code = rec.student_code
            if not rec.password:
                userdn = 'CN=' + str(student_code) + ',' + rec.faculty.ldap_dn
                username = str(student_code)
                application_en_full_name = self.env['op.student'].search([('id', '=', rec.id)], limit=1).en_name
                ldap_base = 'OU=HUE-Faculties,DC=horus,DC=edu,DC=eg'
                search_dn = conn.search(format(ldap_base), search_filter='(|(sAMAccountName=' + str(
                    student_code) + ')(mail=' + rec.email + '))', search_scope=SUBTREE,
                                        attributes=['distinguishedName', 'userAccountControl'])
                for entry in conn.entries:
                    print(entry)
                if search_dn:
                    print(search_dn)
                    userdn = str(conn.response[0]['attributes']['distinguishedName'])
                    print(userdn)
                    password = self.randomString(6)
                    data = conn.extend.microsoft.modify_password(userdn, password)
                    # for entry in conn.entries:
                    #     print(entry)
                    data =  conn.modify(userdn, {'userAccountControl': [('MODIFY_REPLACE', 512)]})
                    data =  conn.modify(userdn, {'sTUGR': [('MODIFY_REPLACE', rec.student_status.id)]})
                    print('qqqqqqqqqqqqq')
                    print(data)
                    # for entry in conn.entries:
                    #     print(entry)
                    password_expire = {"pwdLastSet": [('MODIFY_REPLACE', 0)] }  # // use 0 instead of -1.
                    conn.modify(dn=userdn, changes=password_expire)
                    rec.password = password
                if not search_dn:
                    data = conn.add(userdn, attributes={
                        'objectClass': ['organizationalPerson', 'person', 'top', 'user'],
                        'sAMAccountName': username,
                        'userPrincipalName': "{}@{}".format(username, "horus.edu.eg"),
                        'displayName': application_en_full_name,
                        'mail': str(student_code) + "@horus.edu.eg"  # optional
                    })
                    # Print the resulting entries.
                    # for entry in conn.entries:
                    #     print(entry)
                    password = self.randomString(6)
                    data = conn.extend.microsoft.modify_password(userdn, password)
                    # for entry in conn.entries:
                    #     print(entry)
                    data =  conn.modify(userdn, {'userAccountControl': [('MODIFY_REPLACE', 512)]})
                    # for entry in conn.entries:
                    #     print(entry)
                    password_expire = {"pwdLastSet": [('MODIFY_REPLACE', 0)] }  # // use 0 instead of -1.
                    conn.modify(dn=userdn, changes=password_expire)
                    rec.password = password
            #return True
            else:
                ldap_conn = self.env["ldap.directory"]._ldap_connect()
                username = str(student_code)
                conn = ldap_conn[0]
                ldap_base = ldap_conn[1]
                # data =  conn.modify(userdn, {'studentsstaus': [('MODIFY_REPLACE', rec.student_status.id)]})
                search_dn = conn.search(format(ldap_base),search_filter= "(sAMAccountName="+username+")", search_scope=SUBTREE, attributes=['distinguishedName'])
                if search_dn:
                    userdn = str(conn.response[0]['dn'])
                    conn.modify(userdn, {'sTUGR': [('MODIFY_REPLACE', rec.student_status.id)]})
                    print('qqqqqqqqqqqqq')
                    # print(data)
            oauth_provider = self.env['auth.oauth.provider'].search([('enabled','=', True )],limit=1)
            if oauth_provider:
                provider = oauth_provider.id
            else:
                provider = 0

            if(student_code):
                if rec.last_name:
                    last_name = str(rec.last_name)
                else:
                    last_name = ''
                group_portal = self.env.ref('base.group_portal', False)
                values = {
                    'name': str(rec.name) +" "+ last_name,
                    'image': rec.image,
                    'partner_id': rec.partner_id.id,
                    'login': str(student_code)+"@horus.edu.eg",
                    'active': True,
                    'oauth_provider_id': provider,
                    'oauth_uid': str(student_code)+"@horus.edu.eg",
                    'is_student': True,
                    'groups_id': [(6, 0, [group_portal.id])]
                }
                if rec.user_id:
                    rec.user_id.write(values)
                    user_id = rec.user_id
                else:
                    new_user_id = self.env['res.users'].create(values)
                    rec.user_id = new_user_id.id

                rec.already_partner = True    
                # group_student = self.env.ref('base.group_portal', False)
                # group_user = self.env.ref('base.group_user', False)
                # group_student.sudo().write({'users': [(4, user_id.id)]})
                # group_user.sudo().write({'users': [(3, user_id.id)]})
                # if new_user_id:
                #     ldap_conn = self.env["student.ldap.directory"]._ldap_connect()  
                #     conn = ldap_conn[0]
                #     conn.start_tls()
                #     ldap_base = ldap_conn[1]
                #     # create user
                #     userdn = 'CN='+ str(rec.student_code)+','+rec.faculty.faculty_create_ou.dn
                #     print(userdn)
                #     username = str(rec.student_code)
                #     conn.add(userdn, attributes={
                #        'objectClass': ['organizationalPerson', 'person', 'top', 'user'],
                #        'sAMAccountName': username,
                #        'userPrincipalName': "{}@{}".format(username, 'hours.edu.eg'),
                #        'displayName': rec.en_name,
                #        'mail': str(rec.student_code)+"@horus.edu.eg"  # optional
                #     })
                #     password = self.randomStringwithDigitsAndSymbols(8)
                #     conn.extend.microsoft.modify_password(userdn, password)
                #     conn.modify(userdn, {'userAccountControl': [('MODIFY_REPLACE', 512)]})
                #     rec.password = password
                rec.already_partner = True
            else:
                raise UserError('Student code must be set!')                    
                # if user_id:
                #     group_student = self.env.ref('openeducat_core.group_op_student', False)
                #     group_portal = self.env.ref('base.group_portal', False)
                #     for group in user_id.groups_id :
                #         group.write({'users': [(3, user_id.id)]})
                #     group_student.write({'users': [(4, user_id.id)]})
                #     group_portal.write({'users': [(4, user_id.id)]})
                # rec.user_id.partner_id.is_student = True
            # else:
            #     raise UserError('Student code must be set!')


class PartnernData(models.Model):    
    _inherit = 'res.partner'
    #collage = fields.Many2one('student_collage', 'Collage')
    related_student=  fields.Many2one('op.student', 'Student',tracking=True)
    faculty = fields.Many2one('hue.faculties', 'faculty')
    mc = fields.Boolean()
    level = fields.Many2one('hue.faculties.levels', 'level')
    #programs = fields.Selection([])
    student_code = fields.Integer('Student Code')
    student_nationality = fields.Many2one('hue.nationalities')
    student_city = fields.Many2one('hue.cities')
    student_status = fields.Many2one('hue.std.data.status')    
    student_certificates = fields.Many2one('hue.certificates')
    join_year = fields.Many2one('hue.joining.years' , string="Join Year")    
    cgpa = fields.Float('cgpa')
    percentage =  fields.Float('Percentage')
    year = fields.Selection([(num, str(num)) for num in range( ((datetime.datetime.now().year)-15), ((datetime.datetime.now().year)+5) )])
    name = fields.Char(tracking=True)

    # join_term = fields.Many2one('op.semesters', string="Join Term")
    #student_academic_id = fields.One2many('hue.student.academic.years', 'student_academic_id',string="Terms")

 
    

class HUEBlockReason(models.Model):
    _name = 'hue.block.reason'
    _description = 'Block Reason'

    name = fields.Char('Name')
    

class WizardOpStudent(models.TransientModel):
    _inherit = 'wizard.op.student'
    _description = "Create User for selected Student(s)"

    def _get_students(self):
        if self.env.context and self.env.context.get('active_ids'):
            return self.env.context.get('active_ids')
        return []

    student_ids = fields.Many2many(
        'op.student', default=_get_students, string='Students')

    @api.multi
    def create_student_user(self):
        user_group = self.env.ref('openeducat_core.group_op_student')
        active_ids = self.env.context.get('active_ids', []) or []
        records = self.env['op.student'].browse(active_ids)
        print('___________________________________________ aa ____________________')
        for record in records:
            record.create_user()
        # self.env['res.users'].create_user(records, user_group)

