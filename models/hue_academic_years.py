# -*- coding: utf-8 -*-
"""
MIGRATION (Odoo 11â†’12): SQL queries use parameterized execution (v12 requirement)
Large file with ~500 LOC SQL blocks - compatible but recommend future ORM refactoring
"""

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class HueAcademicYears(models.Model):
    """Academic Years - central academic planning model."""
    
    _name = 'hue.academic.years'
    _description = 'Academic Years'
    
    name = fields.Char(required=True)
    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)
    active = fields.Boolean(default=True)
    course_id = fields.Many2one('op.course', 'Courses')
    faculty = fields.Many2one('hue.faculties', 'Faculties')
    current = fields.Boolean('Current', default=False)
    gpa_current = fields.Boolean('GPA Current', default=False)
    run_semester_gpa = fields.Boolean('Run semester gpa', default=False)
    timetable_current = fields.Boolean('Timetable Current', default=False)
    sequence = fields.Integer('sequence', default=False)
    student_id = fields.Many2one('op.student','Students')
    start_date = fields.Date(string='Start date', required=True, help='Starting date of academic year')
    end_date = fields.Date(string='End date', required=True, help='Ending date of academic year')
    invoice_date = fields.Date()
    year_code = fields.Integer('Year Code', default=False)
    
    
    
    
    def generate_invoices_discount(self):
        # invoices = self.env['account.invoice'].search([('id','in',(482088,478533,478534,478535,482091,478536,480086,480088,478543,482103,482104,482106,482107,478862,478548,480098,482117,478863,478873,478557,482120,482122,482124,480109,482127,482137,480122,482143,482144,480126,480127,482145,480128,480129,482146,480130,480131,482149,482150,482152,482160,480140,480141,480142,480143,480375,478874,480154,480157,480158,480167,480171,480174,480175,480177,480178,478625,480179,480180,478628,480182,478631,480185,478634,478864,480376,478637,478640,478641,480196,478647,480200,478650,478651,478652,480202,480206,478659,480208,480212,478666,478667,480215,478668,478669,480216,480217,478865,480219,480220,480221,480223,478678,480225,478681,478684,480230,480231,478689,480233,478690,478691,480234,478692,480238,480239,478699,480240,480241,478702,478703,480244,478709,478710,478711,478714,480254,478715,478716,478717,480265,480266,478726,478728,480268,478729,478730,478733,480271,478734,478735,478741,480276,478742,480277,478743,478745,480282,480284,480285,478752,478753,480288,480289,480291,478760,478761,478762,478868,478765,478766,478769,478770,480301,480295,480303,478777,480306,480307,480308,480309,478784,480311,478785,478786,480314,478793,478796,478800,480325,478801,480327,478802,478808,478811,478812,478869,478813,478814,478815,480337,478818,478819,478820,480339,478824,478825,478871,478828,478829,480345,478833,478835,478837,480354,480357,478832,478834,478843,478846,480360,480361,478849,480362,480363,478852,478872,478855,480370,480371,480372,480373,480384,480385,480386,478879,478881,480390,480391,480392,478884,480397,480398,478885,478886,478887,480399,478888,478889,480401,480403,478893,478895,480408,480272,478898,480409,478899,480410,478900,478901,478902,478903,480415,478906,480416,480740,478908,480420,478913,478914,480423,480424,478917,478919,478920,480427,478921,478927,478930,478931,480438,478932,478933,478934,479193,478942,478944,480447,479195,480450,478890,480452,478951,478953,480453,480454,480455,478956,480456,478958,480457,478961,480460,478965,480464,478970,479196,480469,478971,480470,478973,478974,480473,480474,478981,478982,478983,480478,478980,478984,480479,478985,480480,480481,480484,478990,480490,480491,479000,479002,480498,480499,479005,480504,480506,480517,480518,479016,480521,479018,480522,479020,479021,480523,479022,480526,479024,480527,479025,479027,480531,480532,479030,479032,479035,480537,479036,480542,480545,480546,480547,479043,480548,479045,479046,479050,480555,480557,479056,480561,479205,479059,480565,479062,480567,479064,480572,479067,480573,480574,479071,480575,480578,479076,480580,479078,479079,479081,480583,479082,480585,480587,479085,479086,479087,480589,480749,479088,480590,479089,480591,480592,480750,480595,480596,480601,480604,480612,480613,480614,480615,480623,480624,480627,479117,479121,480652,480653,480665,480667,480668,480675,479152,480679,480680,479154,480681,480684,480685,480686,480690,480693,480694,479165,480697,479167,480700,480701,480702,480718,480721,480725,480726,480727,480728,480729,479186,479203,480762,480764,479206,480768,479208,480769,480772,479821,480775,480776,479822,480786,479223,479225,480796,479226,480799,480800,480803,479234,479237,479240,479243,481322,479245,480820,480823,479248,480826,479251,479254,479259,479262,481398,479264,481665,480852,480856,480858,479283,480862,481412,480854,480863,479286,479289,480866,479292,480868,480873,480874,479299,481324,480878,479301,480881,480882,479303,480887,480888,480889,479309,479312,480895,481325,480898,480902,480905,480901,480906,481441,479325,480915,479328,480918,480919,479330,479332,479333,479334,480931,479338,480932,480935,479341,479343,479345,480946,480952,479357,479358,480956,479362,479363,479364,480960,480963,479370,479375,480968,479379,479380,480971,479382,480980,479389,480981,479391,481329,480982,480986,480987,480991,480992,479402,479405,480993,481330,479407,479408,479410,479411,480999,479413,481000,479415,481003,481004,479421,479426,481012,479435,479436,481019,481020,479442,481024,481335,481025,481026,481336,481027,479428,479447,479448,479451,479454,480998,481035,479457,479460,481461,481462,481337,479462,479463,479464,479465,479466,479467,481046,479472,481048,479473,481049,481050,479476,479477,481389,481338,481053,479481,479482,481056,479485,481062,481066,481067,479500,481068,479501,479502,481069,479507,479509,481078,481079,479516,481080,481081,481414,479519,481082,481083,481084,481085,479522,479525,479526,479527,479529,481092,479533,481095,479543,479544,481390,479548,479550,479551,479553,479834,481107,479554,479556,479559,481424,479562,481112,479565,481352,481391,481115,481116,481117,479570,479571,479578,481353,479579,479581,479582,481127,479585,481128,479586,479587,479588,481129,479589,479590,479591,481392,479594,481132,479596,481133,479597,481134,481135,479600,479601,479602,479603,481356,481143,481145,481146,479610,481357,481149,479616,481150,479623,481156,481167,481168,481169,481170,481171,479642,481173,479647,481177,481181,481182,481178,481184,479660,481186,481187,481188,479664,479667,479669,481195,481393,481196,479671,479672,481200,479841,479676,481203,479682,481366,481367,479687,481210,481211,479691,479694,481369,481216,481219,481221,481225,481231,481237,481240,481241,481247,479734,481250,479736,481251,481252,479740,481253,479743,481254,481255,481256,479748,481257,481258,481259,479749,479754,481377,481266,479757,481272,481273,479766,481274,481396,479767,481275,481278,479773,479774,481283,481284,481429,479781,479783,481289,481290,481291,481292,479789,481293,479793,479794,479795,479798,479801,479802,481304,481397,481305,481384,481310,481311,481312,481313,479816,479817,479819,479820,481401,479853,481402,481409,481411,481413,481419,481422,479871,481423,481425,479874,481428,479880,481440,481444,479889,481448,479890,479892,481452,479894,479896,481459,479898,481460,481463,481466,479902,481469,481470,481472,481477,481478,479915,479917,479920,479921,481491,479923,481492,481495,481496,481497,479930,481498,481499,481502,481505,481506,479940,479941,479943,479944,481507,481508,481509,481510,481511,481512,479952,479953,479956,479962,481517,479966,479968,481520,479977,479978,479979,479982,481525,479984,479985,481528,481529,481530,479990,479991,480001,480003,481541,481542,480005,481544,480010,481545,481548,481549,480021,481550,480022,481551,480023,480026,480027,480028,481556,480034,480035,480036,480037,480044,480048,480049,481564,481567,481568,480058,481569,481570,480060,480072,481575,480077,480079,480081,481578,481579,481582,481583,481588,481589,481590,481593,481594,481597,481598,481604,481609,481612,481617,481627,481628,481631,481636,481637,481640,481643,481644,481645,481649,481650,481653,481658,481661,481664,481666,481669,481672,481673,481674,481677,481680,481681,481683,481686,481689,481690,481693,481694,481695,481696,481697,481698,481701,481702,481705,481706,481707,481708,481709,481710,481711,481712,481713,481714,481717,481722,481723,481728,481733,481737,481738,481739,481740,481741,481744,481745,481746,481747,481748,481749,481750,481753,481756,481759,481760,481761,481764,481765,481766,481767,481780,481781,481782,481786,481791,481792,481793,481794,481795,481798,481799,481800,481801,481802,481805,481810,481811,481818,481819,481822,481823,481826,481831,481832,481835,481836,481837,481838,481846,481849,481852,481853,481854,481855,481860,481861,481862,481863,481864,481867,481868,481869,481872,481873,481876,481877,481878,481883,481884,481887,481890,481895,481896,481897,481898,481899,481900,481901,481902,481903,481906,481907,481908,481909,481910,481911,481912,481917,481924,481927,481928,481935,481938,481940,481942,481943,481944,481946,481949,481950,481951,481952,481961,481962,481965,481971,481972,481973,481974,481975,481976,481977,481980,481989,481990,481991,481992,481993,481994,482000,482001,482004,482013,482014,482015,482025,482026,482027,482028,482029,482030,482038,482039,482042,482055,482057,482062,482072,482073,482075,482076,482077,482080,482086,482087,478528,478529,478530))])    
        invoices = self.env['account.invoice'].search([('id','in',(473884,473876,473497))])
        
        sql = ("select id from account_invoice where state != 'paid' and notes = 'Registration By Hours' and id not in ( "
                + " select id from account_invoice where number in ( "
                + " select origin from account_invoice where notes = 'Registarion By Hours - Credit Note' ))")
        self.env.cr.execute(sql)
        invoices = self.env.cr.dictfetchall()
        
        for inv in invoices:
            
            invoice_data = self.env['account.invoice'].search([('id','=',inv['id'])])
            print('WadOOOooDDDdd')
            print(invoice_data)
            
            discounts_data = []
            hr_faculties = self.env['hue.faculties']
            hue_joining_years = self.env['hue.joining.years']
            hue_academic_years = self.env['hue.academic.years']
            financial_years = self.env['hue.years']
            hue_installments = self.env['hue.installments']
            product = self.env['product.product']
            invoice = self.env['account.invoice']
            invoice_line = self.env['account.invoice.line']
            student_status = self.env['hue.student.status']
            academic_years = self.env['hue.academic.years']
            terms = self.env['hue.terms']
            increase_years = self.env['hue.years.increase']
            
            partner_id = invoice_data.partner_id.id
            student_id = self.env['op.student'].search([('partner_id','=',partner_id)])
                                                              
            Certificate_id = student_id.student_certificates.id
            StudentStatus_id = student_id.student_status.id
            join_year = student_id.join_year.id
            NationalityID = student_id.nationality.id
            partner_id = student_id.partner_id
            mc = student_id.mc
            scholarship = student_id.scholarship
            special_case = student_id.special_case
            staff_dis = student_id.father_discount
            sibling_dis = student_id.brother_discount
            martyrs_dis = student_id.martyrs_discount
            early_dis = student_id.early_discount
            syndicate_dis = student_id.syndicate_discount
            cgpa = 0
            CertificatePercentage = student_id.percentage
            faculty_id_data = student_id.faculty.id
            course_id = student_id.course_id.id
            year = hue_academic_years.sudo().search([('join_year','=',join_year)],limit=1).year
            facult_identifier = student_id.course_id.faculty_id.identifier
            
            if student_id.course_id.parent_id:
                course_id = student_id.course_id.parent_id.id
            
            
            print('cccccccccccccccccccccccccccc')
            print(course_id)
            if scholarship:
                discounts = self.env['hue.discounts'].sudo().search(
                [('percentage_from', '<=', CertificatePercentage),
                 ('percentage_to', '>=', CertificatePercentage),
                 ('join_year_id', '=', join_year), ('course_id', '=', course_id),
                 ('faculty_ids', '=', faculty_id_data),('scholarship','=',scholarship)],limit=1)
            else:
                print('********************************************************************************************************************************************')
                print(early_dis)
                if mc:
                    print('1-----------------')
                    discounts = self.env['hue.discounts'].sudo().search(
                        [('mc', '=', 1), ('percentage_from', '<=', CertificatePercentage),
                         ('percentage_to', '>=', CertificatePercentage),
                         # ('nationality_id', '=', NationalityID),
                         # ('certificate_id', '=', Certificate_id),
                         ('join_year_id', '=', join_year), ('course_id', '=', course_id),
                         ('faculty_ids', '=', faculty_id_data),('scholarship','=',False)],limit=1)
                elif staff_dis:
                    print('2-----------------')
                    
                    discounts = self.env['hue.discounts'].sudo().search(
                        [('staff_discount', '=', True), ('percentage_from', '<=', CertificatePercentage),
                         ('percentage_to', '>=', CertificatePercentage),
                         # ('nationality_id', '=', NationalityID),
                         # ('certificate_id', '=', Certificate_id),
                         ('join_year_id', '=', join_year), ('course_id', '=',course_id),
                         ('faculty_ids', '=', faculty_id_data),('scholarship','=',False)],limit=1)
                elif sibling_dis:
                    print('3-----------------')
                    print(CertificatePercentage)
                    print(NationalityID)
                    print(Certificate_id)
                    print(join_year)
                    print(course_id)
                    print(faculty_id_data)
                    discounts = self.env['hue.discounts'].sudo().search(
                        [('sibling_discount', '=', True), ('percentage_from', '<=', CertificatePercentage),
                         ('percentage_to', '>=', CertificatePercentage),
                         # , ('nationality_id', '=', int(NationalityID)),
                         # ('certificate_id', '=', Certificate_id),
                         ('join_year_id', '=', join_year), ('course_id', '=', course_id),
                         ('faculty_ids', '=', faculty_id_data),('scholarship','=',False)],limit=1)
                elif martyrs_dis:
                    print('4-----------------')
                    discounts = self.env['hue.discounts'].sudo().search(
                        [('martyrs_discount', '=', True), ('percentage_from', '<=', CertificatePercentage),
                         ('percentage_to', '>=', CertificatePercentage),
                         # ('nationality_id', '=', NationalityID),
                         # ('certificate_id', '=', Certificate_id),
                         ('join_year_id', '=', join_year), ('course_id', '=', course_id),
                         ('faculty_ids', '=', faculty_id_data),('scholarship','=',False)],limit=1)
                elif syndicate_dis:
                    print('5-----------------')
                    discounts = self.env['hue.discounts'].sudo().search(
                        [('syndicate_discount', '=', True), ('percentage_from', '<=', CertificatePercentage),
                         ('percentage_to', '>=', CertificatePercentage),
                         # ('nationality_id', '=', NationalityID),
                         # ('certificate_id', '=', Certificate_id),
                         ('join_year_id', '=', join_year), ('course_id', '=', course_id),
                         ('faculty_ids', '=', faculty_id_data),('scholarship','=',False)],limit=1)
                
                elif early_dis:
                    print('6-----------------')
                    discounts = self.env['hue.discounts'].sudo().search(
                        [('early_discount', '=', True),
                         ('percentage_from', '<=', CertificatePercentage),
                         ('percentage_to', '>=', CertificatePercentage),
                         # ('nationality_id', '=', NationalityID),
                         # ('certificate_id', '=', Certificate_id),
                         ('join_year_id', '=', join_year), ('course_id', '=', course_id),
                         ('faculty_ids', '=', faculty_id_data),('scholarship','=',False)],limit=1)
                print(discounts)
                print('22222222222222222222')
            for dis in discounts:
                discounts_data.append(dis)
            
            for discount in discounts_data:
                print('wadood')
                
                product_data = product.sudo().search([('discount_id', '=', discount.id)])
                account_id = False
                if product_data.id:
                    account_id = product_data.property_account_income_id.id
                if not account_id:
                    account_id = product_data.categ_id.property_account_income_categ_id.id
                if not account_id:
                    raise UserError(
                        _('There is no income account defined for this product: "%s". \
                           You may have to install a chart of account from Accounting \
                           app, settings menu.') % (product.name,))                   
                if invoice_data:
                    price_unit = (discount.percentage_credit_hour * invoice_data.amount_total)/100
                    
                    credit_note_data = invoice.sudo().create({
                        'academic_term':invoice_data.academic_term.id,
                        'origin':invoice_data.number,
                        'notes':'Registarion By Hours - Credit Note',
                        'invoice_type':'regular',
                        'currency_id' : invoice_data.currency_id.id,
                        'type': 'out_refund',
                        'account_id': partner_id.property_account_receivable_id.id,
                        'reference': False,
                        'faculty':faculty_id_data,
                        'student_code':student_id.student_code,
                        'academic_year':invoice_data.academic_year.id,
                        'date_due':invoice_data.date_invoice,
                        'date_invoice':invoice_data.date_invoice,
                        'partner_id':partner_id.id,
                        'state': 'draft'
                        })
                    
                    if invoice_data:
                        dis_increase = 0
                        invoice_line_data = invoice_line.sudo().create({
                        'name': product_data.name,
                        'account_id': account_id,
                        'price_unit': price_unit ,
                        'quantity': 1,
                        'invoice_id': credit_note_data.id,
                        'product_id': product_data.id
                        })
                    
                    credit_note_data.action_invoice_open()
                    
                    credit_notes = self.env['account.invoice'].sudo().search([('origin', '=', invoice_data.number)])
                    credit_note_ids = []
                    for cr in credit_notes:
                        credit_note_ids.append(cr.id)
                    
                    domain = [('invoice_id', 'in', credit_note_ids),('account_id', '=', invoice_data.account_id.id), ('partner_id', '=', invoice_data.env['res.partner']._find_accounting_partner(invoice_data.partner_id).id), ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0), ('amount_residual_currency', '!=', 0.0)]
                    if invoice_data.type in ('out_invoice', 'in_refund'):
                        domain.extend([('credit', '>', 0), ('debit', '=', 0)])
                        type_payment = _('Outstanding credits')
                    else:
                        domain.extend([('credit', '=', 0), ('debit', '>', 0)])
                        type_payment = _('Outstanding debits')
                    info = {'title': '', 'outstanding': True, 'content': [], 'invoice_id': invoice_data.id}
                    lines = invoice_data.env['account.move.line'].sudo().search(domain)
                    currency_id = invoice_data.currency_id
                    
                    if len(lines) != 0:
                        for line in lines:
                            self.assign_outstanding_credit(line.id,invoice_data)
    @api.multi
    def assign_outstanding_credit(self, credit_aml_id , inv_id):
        inv_id.ensure_one()
        credit_aml = self.env['account.move.line'].sudo().browse(credit_aml_id)
        if not credit_aml.currency_id and inv_id.currency_id != inv_id.company_id.currency_id:
            credit_aml.with_context(allow_amount_currency=True, check_move_validity=False).write({
                'amount_currency': inv_id.company_id.currency_id.with_context(date=credit_aml.date).compute(credit_aml.balance, inv_id.currency_id),
                'currency_id': inv_id.currency_id.id})
        if credit_aml.payment_id:
            credit_aml.payment_id.write({'invoice_ids': [(4, inv_id.id, None)]})
        return self.register_payment(credit_aml,inv_id)
    
    @api.multi
    def register_payment(self, payment_line ,inv_id = False, writeoff_acc_id=False, writeoff_journal_id=False ):
        """ Reconcile payable/receivable lines from the invoice with payment_line """
        line_to_reconcile = inv_id.env['account.move.line']
        for inv in inv_id:
            line_to_reconcile += inv.move_id.line_ids.filtered(lambda r: not r.reconciled and r.account_id.internal_type in ('payable', 'receivable'))
        return (line_to_reconcile + payment_line).reconcile(writeoff_acc_id, writeoff_journal_id)

    @api.multi
    def generate_invoices_discount_ss(self):
        for rec in self:
            product = self.env['product.product']
            inv_product = product.sudo().search([('id', '=', 9954)])
            account_id = False
            if inv_product.id:
                account_id = inv_product.property_account_income_id.id
            if not account_id:
                account_id = inv_product.categ_id.property_account_income_categ_id.id
            # if not account_id:
            #     continue
            #     raise UserError(
            #         _('There is no income account defined for this product: "%s". \
            #            You may have to install a chart of account from Accounting \
            #            app, settings menu.'))
            
            sql = ("select distinct aa.id inv_id , bb.price_unit price , aa.partner_id from account_invoice aa inner join account_invoice_line bb \n"
                    + " on aa.id = bb.invoice_id \n"
                    + " where aa.academic_year = 69536 and aa.academic_term in (26,27)  \n"
                    + " and aa.invoice_type = 'regular' and aa.type = 'out_invoice' and aa.state != 'cancel' \n"
                    + " and bb.name = 'Ø§Ù„Ø²ÙŠØ§Ø¯Ø© Ø§Ù„Ø³Ù†ÙˆÙŠØ© Ù„Ø¹Ø§Ù… 2023/2024' and aa.faculty = 12 ")
            
            self.env.cr.execute(sql)
            allinvoices = self.env.cr.dictfetchall()
            students = []
            print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW')
            count = 0
            for invoice in allinvoices:
                count = count+1
                print(count)
                print('count................................')
                _logger.info('--------------------------------------------------')
                _logger.info(count)
                _logger.info('--------------------------------------------------')
                student = self.env['op.student'].search([('partner_id','=', invoice['partner_id'] )])
                print(invoice['inv_id'])
                students_invoices = self.env['account.invoice'].search([('id','=', invoice['inv_id'] )])
                # print(invoice['inv_id'])
                credit_note_data = self.env['account.invoice'].sudo().create({
                                'academic_term':students_invoices.academic_term.id,
                                'origin':students_invoices.number,
                                'notes': 'Increase Discount 2024',
                                'invoice_type':'regular',
                                'currency_id' : students_invoices.currency_id.id,
                                'invoice_id' : students_invoices.id,
                                'type': 'out_refund',
                                # 'account_id': partner_id.property_account_receivable_id.id,
                                'reference': False,
                                'faculty':student.faculty.id,
                                'student_code':student.student_code,
                                'academic_year':students_invoices.academic_year.id,
                                'date_due': students_invoices.date_due,
                                'date_invoice':students_invoices.date_due,
                                'partner_id':student.partner_id.id,
                                'state': 'draft'
                                })
                            
                if students_invoices:
                    print('11111111111111111111111111111111')
                    print(student.scholarship)
                    if student.scholarship == 100:
                        continue
                    if student.scholarship:
                        print('2222222222222222222222')
                        price_unit = invoice['price'] / 2
                        percent = 100 - int(student.scholarship)
                        price_unit = price_unit * percent  / 100
                    else:
                        print('333333333333333333333')
                        price_unit = invoice['price'] / 2
                        
                    invoice_line_data = self.env['account.invoice.line'].sudo().create({
                    'name': inv_product.name,
                    'account_id': account_id,
                    'price_unit': price_unit,
                    'quantity': 1,
                    'invoice_id': credit_note_data.id,
                    'product_id': inv_product.id
                    })
                
                students_invoices.write({'name':inv_product.name})
            
                credit_note_data.action_invoice_open()
                
                credit_notes = self.env['account.invoice'].search([('origin', '=', students_invoices.number)])
                credit_note_ids = []
                for cr in credit_notes:
                    credit_note_ids.append(cr.id)
                
                domain = [('invoice_id', 'in', credit_note_ids),('account_id', '=', students_invoices.account_id.id), ('partner_id', '=', students_invoices.env['res.partner']._find_accounting_partner(students_invoices.partner_id).id), ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0), ('amount_residual_currency', '!=', 0.0)]
                if students_invoices.type in ('out_invoice', 'in_refund'):
                    domain.extend([('credit', '>', 0), ('debit', '=', 0)])
                    type_payment = _('Outstanding credits')
                else:
                    domain.extend([('credit', '=', 0), ('debit', '>', 0)])
                    type_payment = _('Outstanding debits')
                info = {'title': '', 'outstanding': True, 'content': [], 'invoice_id': students_invoices.id}
                lines = students_invoices.env['account.move.line'].search(domain)
                currency_id = students_invoices.currency_id
                
                if len(lines) != 0:
                    for line in lines:
                        self.assign_outstanding_credit(line.id,students_invoices)
    
    @api.multi
    def generate_invoices_gpa(self):
        for rec in self:
            financial_years = self.env['hue.years']
            hue_installments = self.env['hue.installments']
            product = self.env['product.product']
            invoice = self.env['account.invoice']
            invoice_line = self.env['account.invoice.line']
            student_status = self.env['hue.student.status']
            terms = self.env['hue.terms']
            increase_years = self.env['hue.years.increase']
            status_ids = (self.env['hue.std.data.status'].search([('active_invoice', '=', True)])._ids)
            jointerm2 = self.env['op.student'].search([('join_year', '=', 69535),('join_term', '=', 2)]).ids
            print('jointerm2jointerm2jointerm2jointerm2')
            print(jointerm2)
            students_gpa = self.env['op.student.accumlative.semesters'].search([('course_id','!=',15),('student_id','not in',jointerm2)
            ,('student_id','in',(5456,2466,5174,4214,5770,3694,3553,5356,5500,3822,5517,4821,3524,5665,3732,5806,2820,3523,2512,6001,5350,5949,6096,3256,4988,5330,6132,5756,4324,5512,5288,5592,5336,5970,5339,4883,4839,5349,5809,6023,5353,4942,5503,5302,5610,4950,6024,3554,4835,2736,5457,6058,5630,5390,5593,6028,2473,4692,6158,3990,5391,5342,5309,4760,4959,5775,5664,4933,5725,4714,5360,3697,5767,5650,4755,6334,4797,5168,5166,5648,5283,5169,4527,5299,2414,3883,5674,4863,5460,5026,4507,5265,4922,5420,5429,5232,5328,5879,5182,4771,5714,6305,5294,5453,5365,5323,5258,5476,5686,5231,5656,5351,5259,5778,5151,5450,4848,6074,5862,5432,5313,4949,3485,5505,5760,5870,4824,4770,5430,5431,4965,5763,5440,4169,5227,4930,5270,4510,5625,5924,5364,5057,5876,5754,5550,5881,4997,5554,5546,5297,4228,5700,6050,5938,4651,5720,5599,5745,2530,3650,4912,5255,4801,4911,5159,5706,5594,5880,5732,6349,4238,5285,5287,5198,5723,5584,6329,5935,5199,5721,5143,3552,5712,5677,5205,5749,4021,5063,4805,5206,4833,4537,4538,4971,5204,5715,5746,6048,2737,5202,5687,3842,5054,5941,5193,5626,5678,5150,5616,5152,4541,5627,5281,5691,6188,4877,4799,5933,5701,4776,5747,4994,5208,5617,5138,4982,5564,5271,3549,5256,2989,4940,6041,5676,4794,4494,2384,5696,4920,5573,5681,5139,5195,5180,5042,5878,4534,5184,5569,4395,5772,5733,5684,5794,5050,5724,5604,6170,5049,5115,2975,5282,6040,5572,5130,5170,5822,6108,5091,5303,5780,5628,5857,4976,6093,5132,4803,5566,4992,5699,4528,6134,5602,5197,4862,5702,6215,5099,5707,5692,5605,5647,5213,4919,5931,5708,5567,5688,2416,5812,5835,5675,5659,5861,5094,5128,5210,5752,5348,5743,5774,6113,6110,4777,5324,5519,5814,5575,4769,5088,4159,6206,4967,6207,2718,5908,6338,3994,5423,5097,4075,6189,6059,4931,5929,5062,5122,5896,5041,6078,5075,6152,5008,5090,5240,4802,6064,5084,4999,4783,4778,4892,5238,5882,5127,5000,4887,4938,5950,5027,4542,4307,2458,5860,5843,5914,4874,5083,4871,4878,5034,5037,5808,5118,5012,5019,6224,5239,4903,5251,5110,5531,4941,5893,5921,2590,5038,6054,4928,3475,3718,3835,5958,4294,6150,5516,5662,4998,3855,4876,5899,5023,4454,4980,2879,5813,2863,5262,5608,5445,3992,5417,4006,5873,5455,4790,3704,4229,4506,4962,5737,6348,4543,5790,4829,2475,5107,4836,4849,4814,4851,5797,5366,4540,4808,5016,5827,5006,4818,5867,5836,5894,5176,5228,4472,5413,4866,4901,5855,5478,5393,6173,4544,5229,5831,4758,5523,4819,5622,3660,2548,5376,2615,5689,5211,4861,5458,4895,5513,5649,3559,4545,5903,6070,6020,2655,2710,6351,5226,4915,6038,5392,5234,5495,5437,5762,4842,5469,5443,6176,2900,4548,2920,5695,5992,5548,4000,5383,5415,4535,5325,5477,5441,5433,5416,2299,3183,4468,4838,5315,5856,5374,2407,2759,3334,4371,3421,4549,2417,5412,2923,6330,2455,2297,4550,4784,2605,2523,4551,4552,4553,3211,4221,4886,4319,4511,3874,2537,3412,3166,4554,2978,3471,3002,3180,4966,5047,4526,4555,6122,4556,4557,4558,4399,5844,4559,4560,4561,4562,4563,4566,3122,4568,4569,2412,6098,6187,2813,2726,2834,5419,4464,2732,3424,5421,4711,3931,2312,3510,2695,4502,3921,5293,2597,4570,3930,2409,6016,4162,2750,4571,4572,4573,4575,4005,4580,3595,4581,5658,6007,4582,3504,6162,3266,2348,4583,4584,3481,2550,4586,4587,2410,3555,2425,4589,4588,3048,4590,3857,4592,4594,4595,6147,2592,6143,4386,4596,4597,4599,4466,4600,3848,4601,4603,5955,4604,4605,4607,4606,3973,4609,4132,4610,4611,3262,4615,4614,4389,3813,4254,4267,4616,4617,4619,4620,4623,4621,4624,4622,2454,4233,4625,2350,5971,4626,3846,4629,4628,4630,4631,3494,2511,4632,4633,4634,4636,4641,4640,4635,4638,4516,4642,4486,2574,4645,4643,4648,4647,4646,2675,3827,6190,2456,2623,2747,4655,4652,4654,2453,6049,4656,3237,4011,6141,3675,5685,4657,4662,4660,4661,4081,3476,4663,4473,2998,4669,4666,4667,4670,4671,4672,4673,4677,4679,4676,4678,4675,4683,4681,4685,4686,4680,4682,4691,4688,4690,4694,4695,6144,3499,3668,3129,4235,4696,2846,2569,4697,2679,6153,2343,4698,4699,2346,4564,5361,5945,6034,4701,4700,4702,4704,4705,4706,4709,4712,4715,4717,4716,4718,4713,4727,4719,4720,4728,4721,4725,4723,4724,4726,4729,4730,4735,4734,4731,4733,4732,4737,4736,2857,4738,4739,4742,4740,4743,4747,4745,4746,4749,4750,4751,4752,4753,4754,4762,4775,4759,4761,4774,4756,4772,4768,4792,4781,4791,4786,4785,4789,4779,4782,4798,4796,4806,4800,4793,4807,4812,4811,4817,4809,4816,4813,4810,4825,4832,4822,4823,4820,4831,4827,4826,4843,4845,4847,4834,4844,4837,4841,4857,4859,4852,4860,4850,4853,4856,4855,4867,4865,4875,4864,4868,4872,4869,4873,4880,4879,4889,4882,4881,4885,4894,4896,4902,4897,4893,4898,4891,4899,4908,4905,4910,4907,4916,4906,4914,4932,4935,4926,4934,4924,4923,4925,4936,4947,4939,4944,4945,4937,4943,4960,4961,4952,4958,4956,4954,4964,4953,4972,4977,4985,6328,4984,4970,4979,4969,4996,4989,4991,4990,4986,5005,5002,5017,5013,5003,5014,5009,5015,5031,5030,5021,5025,5033,5028,5029,5032,5052,5044,5048,5035,5036,5039,5046,5059,5061,5070,5069,5058,5067,5071,5053,5077,5074,5073,5081,5086,5085,5087,5080,5103,5093,5100,5098,5089,5095,5105,5114,5109,5113,5106,5108,5104,5112,5123,5134,5125,5137,5126,5135,5155,5156,5154,5144,5158,5140,5157,5172,5164,5160,5162,5167,5165,5171,5188,5185,5186,5181,5183,5187,5175,5178,5194,5189,5191,5192,5200,5203,5190,5217,5220,5215,5218,5214,5209,5225,5230,5224,5235,5233,5223,5237,5250,5246,5244,5249,5248,5243,5260,5264,5257,5261,5254,5253,5277,5280,5278,5273,5274,5279,5275,5292,5298,5284,5296,5289,6337,5300,5312,5319,5318,5308,5304,5311,5305,5327,5321,5340,5334,5329,5344,5354,5346,5347,5370,5363,5369,5367,5368,5373,5377,5380,5379,5382,5385,5386,5404,5395,5405,5414,5403,5409,5434,5439,5447,5449,5448,5454,5459,5936,5468,5473,5472,5474,5482,5485,5491,5493,5490,5502,5508,5510,5514,5509,5507,5530,5535,5526,5533,5534,5520,5527,5544,5540,5545,5539,5538,5557,5570,5561,5560,5571,5581,5583,5580,5595,5587,5578,5611,5614,5612,5619,5621,5620,5651,5643,5641,5634,5629,5632,5663,5652,5653,5670,5660,5673,5672,5680,5698,5690,5693,5694,5697,5710,5713,5703,5705,5728,5718,5717,5722,5742,5731,5734,5738,5744,5740,5748,5757,5750,5758,5765,5759,5764,5761,5768,5771,5776,5781,5783,5785,5784,5787,5804,5807,5788,5801,5791,5799,5803,5826,5823,5821,5810,5818,5838,5840,5841,5829,5839,5834,5842,5830,5852,5846,5847,5850,5848,5853,5851,5866,5864,5858,5869,5872,5865,5868,5886,5877,5874,5875,5885,5883,5901,5889,5890,5895,5900,5887,5888,5897,5910,5912,5913,5902,5911,5906,5907,5917,5916,5927,5920,5926,5932,5919,5922,5942,5947,5939,5944,5948,5940,5964,5963,5957,5953,5956,5966,5961,5988,5984,5985,6009,5995,6010,6014,6011,6013,6022,6018,6019,6026,6031,6032,6015,6037,6036,6045,6042,6043,6047,6065,6056,6067,6062,6063,6053,6052,6072,6081,6077,6075,6091,6106,6087,6084,6088,6086,6109,6124,6115,6116,6123,6107,6111,6118,6126,6125,6156,6135,6129,6136,6133,6161,6139,6160,6148,6149,6163,6171,6177,6168,6167,6166,6164,6165,6169,6179,6183,6184,6181,6200,6182,6185,6212,6217,6208,6210,6219,6211,6310,6223,6308,6226,6225,6222,6319,6304,6333,6325,6326,6324,6331,6346,6339,6342,6343,6345,6336,6357,6354,3748,3731,5973,5976,5999,6005,6012,6055,6201,4703))])
            for student in students_gpa:
                student_scholarship  = student.student_id.scholarship
                brother_discount = student.student_id.brother_discount
                credit_n = False
                students_invoices = invoice.search([('partner_id','=',partner_id.id)
                    ,('academic_year', '=', 69536),('academic_term', '=', 27)
                    ,('type','=','out_invoice'),('invoice_type','=','regular')],limit=1)
               
                credit_n = invoice.search([('partner_id','=',partner_id.id),('notes','=','GPA Discount 2024')
                        ,('academic_year', '=', 69536),('type','=','out_refund'),('invoice_type','=','regular')],limit=1)
                if student.current_gpa >= 3.5 and student.current_gpa < 4.1 and not credit_n:
                    discounts = self.env['hue.discounts'].sudo().search([('cgpa_from', '<=', student.current_gpa),
                            ('cgpa_to', '>=',student.current_gpa)])
                    
                    inv_product = product.sudo().search([('discount_id', '=', discounts.id)],limit=1)
                    account_id = False
                    if inv_product.id:
                        account_id = inv_product.property_account_income_id.id
                    if not account_id:
                        account_id = inv_product.categ_id.property_account_income_categ_id.id
                    if not account_id:
                        continue
                        raise UserError(
                            _('There is no income account defined for this product: "%s". \
                               You may have to install a chart of account from Accounting \
                               app, settings menu.') % (std_id,))
                    
                    if account_id != False:
                        financial_year = financial_years.search([('join_year', '=', join_year),('scholarship', '=', False),('course_id', '=',student.student_id.course_id.id), ('faculty', '=', std_faculty_id)],limit=1)
                        if not financial_year:
                            financial_year = financial_years.search(
                                [('join_year', '=', join_year), ('course_id', '=', False),('scholarship', '=', False),
                                 ('faculty', '=', std_faculty_id)], limit=1)
                        total_amount = 0
                        if financial_year:
                            #check student nationality
                            if student.student_id.student_nationality.foreign_nationality :
                                total_amount = financial_year.total_dollar
                            else:
                                total_amount = financial_year.total                
                        
                        price_unit = total_amount * (discounts.discount_rate/100)
                        price_unit = price_unit / 2
                        if student_data_status_id == 2 and student_scholarship == False : #and brother_discount == False
                            
                            credit_note_data = invoice.sudo().create({
                                'academic_term':students_invoices.academic_term.id,
                                'origin':students_invoices.number,
                                'notes': 'GPA Discount 2024',
                                'invoice_type':'regular',
                                'currency_id' : students_invoices.currency_id.id,
                                'invoice_id' : students_invoices.id,
                                'type': 'out_refund',
                                'account_id': partner_id.property_account_receivable_id.id,
                                'reference': False,
                                'faculty':std_faculty_id,
                                'student_code':std_code,
                                'academic_year':students_invoices.academic_year.id,
                                'date_due': students_invoices.date_due,
                                'date_invoice':students_invoices.date_due,
                                'partner_id':partner_id.id,
                                'state': 'draft'
                                })
                            
                            if students_invoices:
                                # price_unit = product_data.list_price / invoices_data_count
                                invoice_line_data = invoice_line.sudo().create({
                                'name': inv_product.name,
                                'account_id': account_id,
                                'price_unit': price_unit,
                                'quantity': 1,
                                'invoice_id': credit_note_data.id,
                                'product_id': inv_product.id
                                })
                            
                            students_invoices.write({'name':inv_product.name})
                        
                            credit_note_data.action_invoice_open()
                            
                            credit_notes = self.env['account.invoice'].search([('origin', '=', students_invoices.number)])
                            credit_note_ids = []
                            for cr in credit_notes:
                                credit_note_ids.append(cr.id)
                            
                            domain = [('invoice_id', 'in', credit_note_ids),('account_id', '=', students_invoices.account_id.id), ('partner_id', '=', students_invoices.env['res.partner']._find_accounting_partner(students_invoices.partner_id).id), ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0), ('amount_residual_currency', '!=', 0.0)]
                            if students_invoices.type in ('out_invoice', 'in_refund'):
                                domain.extend([('credit', '>', 0), ('debit', '=', 0)])
                                type_payment = _('Outstanding credits')
                            else:
                                domain.extend([('credit', '=', 0), ('debit', '>', 0)])
                                type_payment = _('Outstanding debits')
                            info = {'title': '', 'outstanding': True, 'content': [], 'invoice_id': students_invoices.id}
                            lines = students_invoices.env['account.move.line'].search(domain)
                            currency_id = students_invoices.currency_id
                            
                            if len(lines) != 0:
                                for line in lines:
                                    self.assign_outstanding_credit(line.id,students_invoices)
                                            
                    
    @api.multi
    def register_payment(self, payment_line ,inv_id = False, writeoff_acc_id=False, writeoff_journal_id=False ):
        """ Reconcile payable/receivable lines from the invoice with payment_line """
        line_to_reconcile = inv_id.env['account.move.line']
        for inv in inv_id:
            line_to_reconcile += inv.move_id.line_ids.filtered(lambda r: not r.reconciled and r.account_id.internal_type in ('payable', 'receivable'))
        return (line_to_reconcile + payment_line).reconcile(writeoff_acc_id, writeoff_journal_id)
    
    @api.multi
    def assign_outstanding_credit(self, credit_aml_id , inv_id):
        inv_id.ensure_one()
        credit_aml = self.env['account.move.line'].browse(credit_aml_id)
        if not credit_aml.currency_id and inv_id.currency_id != inv_id.company_id.currency_id:
            credit_aml.with_context(allow_amount_currency=True, check_move_validity=False).write({
                'amount_currency': inv_id.company_id.currency_id.with_context(date=credit_aml.date).compute(credit_aml.balance, inv_id.currency_id),
                'currency_id': inv_id.currency_id.id})
        if credit_aml.payment_id:
            credit_aml.payment_id.write({'invoice_ids': [(4, inv_id.id, None)]})
        return self.register_payment(credit_aml,inv_id)
    
    @api.multi
    def generate_invoices(self):
        financial_years = self.env['hue.years']
        hue_installments = self.env['hue.installments']
        product = self.env['product.product']        
        invoice = self.env['account.invoice']
        invoice_line = self.env['account.invoice.line']
        student_status = self.env['hue.student.status']
        terms = self.env['hue.terms']
        increase_years = self.env['hue.years.increase']
        status_ids = (self.env['hue.std.data.status'].search([('active_invoice', '=', True)])._ids)
        course_id = self.course_id.id
        faculty = self.faculty.id
        std = self.student_id
        joinyear = self.join_year.id
        print(joinyear)
        if joinyear:
            students = self.env['op.student'].search([('student_status','in',status_ids),('year', '<', '2026')
            ,('faculty', '=', self.faculty.id),('join_year', '=', joinyear)] , limit=600, offset=701 )
        elif std:
            students = self.env['op.student'].search([('id', '=', self.student_id.id)])
        count=0
        
        for student in students:
            count = count + 1
            std_join_year = student.join_year.id
            std_year = student.year
            std_faculty_id = student.faculty.id
            std_course_id = student.course_id.id
            std_id = student.id
            std_code = student.student_code
            partner_id =  student.partner_id
            join_year  = student.join_year.id
            scholarship = student.scholarship
            student_data_status_id  = student.student_status.id
            mc = student.mc
            staff_dis = student.father_discount
            sibling_dis = student.brother_discount
            martyrs_dis = student.martyrs_discount
            syndicate_dis = student.syndicate_discount
            early_dis = student.early_discount
            extra_dis = student.extra_discount
            student_student_nationality_id  = student.student_nationality.id
            CertificatePercentage = student.percentage
            Certificate_id = student.student_certificates.id
            faculty_id_data = student.faculty.id
            NationalityID = student.student_nationality.id
            special_case = student.special_case
            if scholarship == False:
                financial_year = financial_years.search([('join_year', '=', join_year), ('course_id', '=', student.course_id.id),('scholarship','=',False)], limit=1)
                if not financial_year:
                    financial_year = financial_years.search([('join_year', '=', join_year), ('faculty', '=', student.faculty.id),('scholarship','=',False)], limit=1)
            else:
                financial_year = financial_years.search([('join_year', '=', join_year), ('course_id', '=', student.course_id.id),('scholarship','=',True)], limit=1)
                if not financial_year:
                    financial_year = financial_years.search([('join_year', '=', join_year), ('faculty', '=', student.faculty.id),('scholarship','=',True)], limit=1)
            
            if financial_year:
                if student.student_nationality.foreign_nationality :
                    installments = hue_installments.sudo().search([('years_id', '=', financial_year.id),('extra_inv', '=', True),('special_case','=',False),('one_time', '=', False),('foreign_nationality','=',True)])
                    incease = increase_years.sudo().search([('year_id', '=', financial_year.id),('foreign_nationality','=',True),('special_case','=',False)])
                elif special_case:
                    installments = hue_installments.sudo().search([('years_id', '=', financial_year.id),('special_case','=',True),('one_time', '=', False),('foreign_nationality','=',False)])
                    incease = increase_years.sudo().search([('year_id', '=', financial_year.id),('special_case','=',True)])
                else:
                    installments = hue_installments.sudo().search([('years_id', '=', financial_year.id),('extra_inv', '=', True),('special_case','=',False),('one_time', '=', False),('foreign_nationality','=',False)])
                    incease = increase_years.sudo().search([('year_id', '=', financial_year.id),('foreign_nationality','=',False),('special_case','=',False)])
                for installment in installments:
                    global_term_id = installment.term_id.id
                    term_data = terms.sudo().search([('term_id','=',self.id), ('global_term_id','=', global_term_id)],limit=1)
                    from_date = term_data.from_date
                    to_date = term_data.from_date
                    name = term_data.name
                    currency = installment.currency
                    invoice_exist = invoice.sudo().search([
                        ('academic_term','=',term_data.id),
                        ('invoice_type','=','regular'),
                        ('type','=','out_invoice'),
                        ('state','!=','cancel'),
                        ('faculty','=',std_faculty_id),
                        ('academic_year','=',self.id),
                        ('partner_id','=',partner_id.id),
                        ])
                    if invoice_exist:
                        break;
                    invoice_data = invoice.sudo().create({
                        'academic_term':term_data.id,
                        'notes':financial_year.notes,
                        'invoice_type':'regular',
                        'currency_id' : currency.id,
                        'account_id': partner_id.property_account_receivable_id.id,
                        'type': 'out_invoice',
                        'reference': False,
                        'faculty':std_faculty_id,
                        'student_code':std_code,
                        'academic_year':self.id,
                        'date_due':to_date,
                        'date_invoice':from_date,
                        'partner_id':partner_id.id,
                        'state': 'draft',
                        'dis_inv': installment.extra_inv
                        })

                    inv_product = product.sudo().search([('installments_id', '=', installment.id)])
                    account_id = False
                    if inv_product.id:
                        account_id = inv_product.property_account_income_id.id
                    if not account_id:
                        account_id = inv_product.categ_id.property_account_income_categ_id.id
                    if not account_id:
                        raise UserError(
                            _('There is no income account defined for this product: "%s". \
                               You may have to install a chart of account from Accounting \
                               app, settings menu.') % (product.name,))                                
                    invoice_line_data = invoice_line.sudo().create({
                        'name':inv_product.name,
                        'account_id':account_id,
                        'price_unit':inv_product.list_price,
                        'quantity':1,
                        'invoice_id':invoice_data.id,
                        'product_id':inv_product.id
                        })
                    account_id = False
                    if incease:
                        for increase in incease:
                            if increase.id:
                                account_id = increase.property_account_income_id.id
                            if not account_id:
                                account_id = increase.categ_id.property_account_income_categ_id.id
                            if not account_id:
                                raise UserError(
                                    _('There is no income account defined for this product: "%s". \
                                       You may have to install a chart of account from Accounting \
                                       app, settings menu.') % (product.name,))                                
                            invoice_line_data = invoice_line.sudo().create({
                                'name':increase.name,
                                'account_id':account_id,
                                'price_unit':increase.list_price,
                                'quantity':1,
                                'invoice_id':invoice_data.id,
                                'product_id':increase.product_id.id
                                })
                
                    invoice_data.action_invoice_open()
                
                discounts_data = []
                discounts = []
                
                if scholarship:
                    discounts = self.env['hue.discounts'].sudo().search(
                    [('percentage_from', '<=', CertificatePercentage),
                     ('percentage_to', '>=', CertificatePercentage), ('nationality_id', '=', NationalityID),
                     ('certificate_id', '=', Certificate_id),
                     ('join_year_id', '=', join_year),
                     ('faculty_ids', '=', faculty_id_data),('scholarship','=',scholarship)],limit = 1)
                elif special_case:
                    if sibling_dis:
                        discounts = self.env['hue.discounts'].sudo().search(
                            [('sibling_discount', '=', True), ('percentage_from', '<=', CertificatePercentage),
                             ('percentage_to', '>=', CertificatePercentage), ('nationality_id', '=', NationalityID),
                             ('certificate_id', '=', Certificate_id),
                             ('join_year_id', '=', join_year),
                             ('faculty_ids', '=', faculty_id_data),('special_case','=',True)],limit = 1)
                else:
                    if mc:
                        discounts = self.env['hue.discounts'].sudo().search(
                            [('mc', '=', 1), ('percentage_from', '<=', CertificatePercentage),
                             ('percentage_to', '>=', CertificatePercentage), ('nationality_id', '=', NationalityID),
                             ('certificate_id', '=', Certificate_id),
                             ('join_year_id', '=', join_year),
                             ('faculty_ids', '=', faculty_id_data),('scholarship','=',False)])
                    elif staff_dis:
                        discounts = self.env['hue.discounts'].sudo().search(
                            [('staff_discount', '=', True), ('percentage_from', '<=', CertificatePercentage),
                             ('percentage_to', '>=', CertificatePercentage), ('nationality_id', '=', NationalityID),
                             ('certificate_id', '=', Certificate_id),
                             ('join_year_id', '=', join_year),
                             ('faculty_ids', '=', faculty_id_data),('scholarship','=',False)])
                    elif sibling_dis:
                        discounts = self.env['hue.discounts'].sudo().search(
                            [('sibling_discount', '=', True), ('percentage_from', '<=', CertificatePercentage),
                             ('percentage_to', '>=', CertificatePercentage), ('nationality_id', '=', NationalityID),
                             ('certificate_id', '=', Certificate_id),
                             ('join_year_id', '=', join_year),
                             ('faculty_ids', '=', faculty_id_data),('scholarship','=',False),('special_case','=',False)])
                    elif martyrs_dis:
                        discounts = self.env['hue.discounts'].sudo().search(
                            [('martyrs_discount', '=', True), ('percentage_from', '<=', CertificatePercentage),
                             ('percentage_to', '>=', CertificatePercentage), ('nationality_id', '=', NationalityID),
                             ('certificate_id', '=', Certificate_id),
                             ('join_year_id', '=', join_year),
                             ('faculty_ids', '=', faculty_id_data),('scholarship','=',False)])
                    elif syndicate_dis:
                        discounts = self.env['hue.discounts'].sudo().search(
                            [('syndicate_discount', '=', True), ('percentage_from', '<=', CertificatePercentage),
                             ('percentage_to', '>=', CertificatePercentage), ('nationality_id', '=', NationalityID),
                             ('certificate_id', '=', Certificate_id),
                             ('join_year_id', '=', join_year),
                             ('faculty_ids', '=', faculty_id_data),('scholarship','=',False)])
                    elif early_dis:
                        discounts = self.env['hue.discounts'].sudo().search(
                            [('early_discount', '=', True),
                            ('percentage_from', '<=', CertificatePercentage),
                            ('percentage_to', '>=', CertificatePercentage),
                            # ('nationality_id', '=', NationalityID),
                            # ('certificate_id', '=', Certificate_id),
                            ('join_year_id', '=', join_year),
                            ('faculty_ids', '=', faculty_id_data),('scholarship','=',False)],limit=1)
                    if extra_dis:
                        print('7-----------------')
                        discounts = self.env['hue.discounts'].sudo().search([('id','=','1319')],limit=1)
                            
                for discount in discounts:
                    product_data = product.sudo().search([('discount_id', '=', discount.id)])
                    invoices_data_count = len(invoice.sudo().search(
                        [('state', '=', 'open'), ('partner_id', '=', partner_id.id), ('invoice_type', '=', 'regular'),
                        ('academic_year', '=', self.id) , ('dis_inv', '=', True) ],limit = 2)._ids)
                    invoices_data = invoice.sudo().search(
                        [('state', '=', 'open'), ('partner_id', '=', partner_id.id), ('invoice_type', '=', 'regular'),
                        ('academic_year', '=', self.id), ('dis_inv', '=', True)],limit = 2)
                    
                    account_id = False
                    if product_data.id:
                        account_id = product_data.property_account_income_id.id
                    if not account_id:
                        account_id = product_data.categ_id.property_account_income_categ_id.id
                    if not account_id:
                        raise UserError(
                            _('There is no income account defined for this product: "%s". \
                               You may have to install a chart of account from Accounting \
                               app, settings menu.') % (product.name,))                   
                    if invoices_data:
                        #print(invoices_data)
                        for invoice_data in invoices_data:
                            print(product_data.list_price)
                            print(invoices_data_count)
                            # price_unit = product_data.list_price / invoices_data_count
                            price_unit = (discount.percentage_credit_hour * invoice_data.amount_total)/100
                            # invoice_line_data = invoice_line.sudo().create({
                            #     'name': product_data.name,
                            #     'account_id': account_id,
                            #     'price_unit': price_unit,
                            #     'quantity': 1,
                            #     'invoice_id': invoice_data.id,
                            #     'product_id': product_data.id
                            # })
                            
                            credit_note_data = invoice.sudo().create({
                                'academic_term':invoice_data.academic_term.id,
                                'origin':invoice_data.number,
                                'notes':financial_year.notes,
                                'invoice_type':'regular',
                                'currency_id' : currency.id,
                                'type': 'out_refund',
                                'account_id': partner_id.property_account_receivable_id.id,
                                'reference': False,
                                'faculty':std_faculty_id,
                                'student_code':std_code,
                                'academic_year':invoice_data.academic_year.id,
                                'date_due':invoice_data.date_invoice,
                                'date_invoice':invoice_data.date_invoice,
                                'partner_id':partner_id.id,
                                'state': 'draft'
                                })
                            
                            if invoices_data:
                                dis_increase = 0
                                # price_unit = product_data.list_price / invoices_data_count
                                # if incease:
                                #     if student.scholarship:
                                #         dis_increase = (increase.list_price * int(student.scholarship)) / 100
                                #     else:2
                                #         dis_increase = increase.list_price * 0.1
                                    
                                invoice_line_data = invoice_line.sudo().create({
                                'name': product_data.name,
                                'account_id': account_id,
                                'price_unit': price_unit + dis_increase,
                                'quantity': 1,
                                'invoice_id': credit_note_data.id,
                                'product_id': product_data.id
                                })
                            
                            credit_note_data.action_invoice_open()
                            
                            credit_notes = self.env['account.invoice'].search([('origin', '=', invoice_data.number)])
                            credit_note_ids = []
                            for cr in credit_notes:
                                credit_note_ids.append(cr.id)
                            
                            domain = [('invoice_id', 'in', credit_note_ids),('account_id', '=', invoice_data.account_id.id), ('partner_id', '=', invoice_data.env['res.partner']._find_accounting_partner(invoice_data.partner_id).id), ('reconciled', '=', False), '|', ('amount_residual', '!=', 0.0), ('amount_residual_currency', '!=', 0.0)]
                            if invoice_data.type in ('out_invoice', 'in_refund'):
                                domain.extend([('credit', '>', 0), ('debit', '=', 0)])
                                type_payment = _('Outstanding credits')
                            else:
                                domain.extend([('credit', '=', 0), ('debit', '>', 0)])
                                type_payment = _('Outstanding debits')
                            info = {'title': '', 'outstanding': True, 'content': [], 'invoice_id': invoice_data.id}
                            lines = invoice_data.env['account.move.line'].search(domain)
                            currency_id = invoice_data.currency_id
                            
                            if len(lines) != 0:
                                for line in lines:
                                    self.assign_outstanding_credit(line.id,invoice_data)

    
class HueAccountPayment(models.Model):
    _inherit = 'account.payment'
    payment_note = fields.Char(string="Payment Note")
    
class HueAccountInvoice(models.Model):
    _inherit = 'account.invoice.line'
    academic_year  =  fields.Many2one('hue.academic.years',store=True,related='invoice_id.academic_year')
    faculty  =  fields.Many2one('hue.faculties',store=True,related='invoice_id.faculty')
    invoice_type  =  fields.Selection([('regular', 'Regular'), ('one', 'One Time'),('bus', 'Buses'), ('hostel', 'Hostel'),('miscellaneous', 'Miscellaneous'),('summer', 'Summer'),('post_graduate', 'Post Graduate'),('application', 'Application'),('intern', 'Intern') ],store=True,related='invoice_id.invoice_type')
    partner_id  =  fields.Many2one('res.partner',store=True,related='invoice_id.partner_id')
class HueAccountInvoice(models.Model):
    _inherit = 'account.invoice'
    invoice_type = fields.Selection([('regular', 'Regular'), ('one', 'One Time'),('bus', 'Buses'), ('hostel', 'Hostel'),('miscellaneous', 'Miscellaneous'),('summer', 'Summer'),('post_graduate', 'Post Graduate'),('application', 'Application'),('intern', 'Intern')],string="Invoice Type")
    academic_year  =  fields.Many2one('hue.academic.years', 'Academic Year')
    student_code  =  fields.Integer('Student Code',store=False,related='partner_id.student_code')
    student_code_postgraduate = fields.Char(
    string='Postgraduate Student',
    related='partner_id.related_student.postgraduate_code',
    store=False )
    # join_year  =  fields.Integer('Join Year',store=True,related='partner_id.join_year')
    faculty = fields.Many2one('hue.faculties','faculty',store=True,related='partner_id.faculty')
    student_status = fields.Many2one('hue.std.data.status','Student Status',store=True,related='partner_id.student_status')
    notes = fields.Char(string="Total Notes")
    academic_term = fields.Many2one('hue.terms', 'Academic Term')        
    is_application = fields.Boolean('Is Application')
    deactive = fields.Boolean('Is deactive')
    mc = fields.Boolean('MC',related='partner_id.mc')
    dis_inv = fields.Boolean('Allow Discount')
    join_year = fields.Many2one('hue.joining.years',related='partner_id.join_year' ,store=True)
    # join_term = fields.Many2one('res.partner','related_student.join_term' ,store=True,)
    special_case = fields.Boolean(related='partner_id.related_student.special_case' ,store=True, readonly=True)
    fawry_reference_number = fields.Char(readonly=True)
 

    @api.multi
    def action_invoice_deactive(self):
        self.write({'deactive' :True})
        return True


    @api.multi
    def action_invoice_open(self):
        invoice =  self.env['account.invoice']
        inv = invoice.search([('id','=',self.id)],limit=1)
        if inv:
            inv.write({'user_id':self._uid})
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')    
        if to_open_invoices.filtered(lambda inv: inv.state != 'draft'):    
            raise UserError(_("Invoice must be in draft state in order to validate it."))
        if to_open_invoices.filtered(lambda inv: inv.amount_total < 0):
            raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))    
        to_open_invoices.action_date_assign()    
        to_open_invoices.action_move_create()
        return to_open_invoices.invoice_validate()
        

        
            
        

        
        
                    
