# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, ValidationError
from dateutil.relativedelta import relativedelta

# Owner details

class P7_owner(models.Model):
    
    _name = "p7.owner"

    _description = "Creating owner in this table"

    _sql_constraints = [('name_unique', 'unique(name,last_name)', 'This owner already exist.!'),('mail_unique', 'unique(email_address)', 'This email already exist')]

    name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    company_name = fields.Char(string="Company Name")
    registration_number = fields.Char(string="Registration Number")
    registration_place = fields.Char(string="Registration Place")
    registration_date = fields.Date(string="Registration Date")
    registration_capital = fields.Char(string="Registration Capital")
    address_1 = fields.Char(string="Address")
    address_2 = fields.Char(string="Address 2")
    state_id = fields.Many2one('res.country.state')
    city = fields.Char(string="City")
    country = fields.Many2one('res.country', string="Country")
    zip = fields.Char(string="Zip")
    email_address = fields.Char('Email', required=True)
    bank_details = fields.Char(string="Bank Detail")
    bank_ids = fields.One2many('p7.res.partner.bank', 'owner_id', string="Bank details",)
    line_ids = fields.One2many('p7.owner.line', 'owner_id', string="Home Details")
    partner_id = fields.Many2one('res.partner', string="vendor", readonly=True)
    is_partner = fields.Boolean(default=False)
    odoo_id = fields.Many2one('account.analytic.account', string="Analytic Account",)
    company_type = fields.Selection([('person', 'Individual'), ('company', 'Company')], default='person')
    

    @api.multi
    def name_get(self):

        if 1 == 1 :
            res = []
            for order in self:
                if order.name and order.last_name:
                    name = '%s  %s' % (str(order.name), str(order.last_name))
                if order.company_name:
                    name = '%s' % (str(order.company_name))
                res.append((order.id, name))
            return res
        return super(P7_owner, self).name_get()





    @api.multi
    def create_vendor(self):
        """ 
            This function allow us to create a vendor from the owener form
        """
        

        vendor = self.env['res.partner'].create(
            {
                'name': str(self.name) + ' ' + str(self.last_name) if self.company_type == 'person' else self.company_name,
                'supplier': True,
                'customer': False,
                'user_id': self.env.user.id,
                'email': self.email_address if self.email_address else False,
                'street': self.address_1 if self.address_1 else False,
                'street2': self.address_2 if self.address_2 else False,
                'city': self.city if self.city else False,
                'state_id': self.state_id.id if self.state_id else False,
                'zip': self.zip if self.zip else False,
                'country_id': self.country.id if self.country else False,
                'company_id': self.env.user.company_id.id,
            })

            

        if vendor:

            self.partner_id = vendor.id
            self.is_partner = True
            if self.bank_ids:
                for i in self.bank_ids:
                    bank = self.env['res.partner.bank'].create({
                        'bank_id': i.bank_id.id if i.bank_id else False,
                        'acc_number': i.acc_number,
                        'partner_id': vendor.id
                    })

       


        
        return True


class P7_owner_line(models.Model):

    _name = 'p7.owner.line'

    _description = "This table is using for supporting the owner table"

    name = fields.Char()
    home_id = fields.Many2one('p7.home', string="Home")
    contract_id = fields.Many2one('p7.contracts', string="Active Contracts")
    end_date = fields.Date(string="Ending Date")
    owner_id = fields.Many2one('p7.owner')


class P7_res_bank(models.Model):

    _name = 'p7.res.partner.bank'

    _description = "Gathering bank details for vendor creation"

    bank_id = fields.Many2one('res.bank', string="Bank")
    acc_number = fields.Char(string="Account Number")
    owner_id = fields.Many2one('p7.owner', string="Owner")




# Home detials
class P7_home(models.Model):

    _name = "p7.home"

    _description = "Creating homes"

    _sql_constraints = [('name_unique', 'unique(name)', 'This home already exist.!'),('odoo_id_unique','unique(odoo_id)','This Analytic Account already occupied')]


    name = fields.Char(string="Home name", required=True)
    owner_id = fields.Many2one('p7.owner', string="Owner Name", required=True)
    odoo_id = fields.Many2one('account.analytic.account', string="Analytic Account",required=True)
    distribution_name = fields.Char(string="Distribution Name", required=True)
    contractual_name = fields.Char(string="Contractual Name", required=True)
    address_1 = fields.Char(string="Address", required=True)
    address_2 = fields.Char(string="Address 2")
    cluster = fields.Char(string="Cluster", required=True)
    country = fields.Many2one('res.country', string="Country", required=True)
    interior_area = fields.Char(string="Interior Area")
    exterior_area = fields.Char(string="Exterior Area")
    home_description = fields.Text(string="Description")
    zoning_number = fields.Char(string="Zoning Number")
    zoning_section = fields.Char(string="Zoning Section")
    zoning_area = fields.Char(string="Zoning Area")



   



class P7_contracts(models.Model):

    _name = 'p7.contracts'

    _description = "Creating contracts"

    _sql_constraints = [('name_unique', 'unique(name)', 'This contract already exist.!')]

    name = fields.Char(string="Contracts Name", required=True)
    home_id = fields.Many2one('p7.home', string="Home", required=True)
    begin_date = fields.Date(string="Begin Date",required=True)
    payment_date = fields.Date(string="Starting date of payment",required=True)
    next_payment_date = fields.Date(string="Next payment date",readonly=True)
    periodicity = fields.Selection([('month','Per Month'),('quarter','Per Quarter'),('year','Per Year')],required=True)
    end_date = fields.Date(string="End Date", required=True)
    notice_period = fields.Integer(string="Notice Period")
    break_possibility = fields.Char(string="Break Possibility")
    deposit = fields.Char(string="Deposit")
    fixed_annual_rent_ht = fields.Char(string="Fixed Annual Rent")
    variable_base = fields.Char(String="Variable Base")
    variable_percentage = fields.Float(string="Variable")
    vat_rate = fields.Many2one('account.tax', string="Vat Rate")
    expense_electricity = fields.Char(string="Electricity Expense")
    expense_water = fields.Char(string="Water Expense")
    expense_gas = fields.Char(string="Gas Expense")
    expense_internet = fields.Char(string="Internet Expense")
    expense_ownershiptax = fields.Char(string="Ownership Tax Expense")
    owner_use = fields.Text(string="Owner uses")
    attachment = fields.Many2many('ir.attachment','contract_attachment_rel','aid','cid', string="PDF Upload")



    @api.model
    def create(self, vals):


        res = super(P7_contracts, self).create(vals)


        owner_dashboard = self.env['p7.owner.line'].create({
            'home_id': res.home_id.id,
            'contract_id': res.id,
            'end_date': res.end_date,
            'owner_id': res.home_id.owner_id.id
        })
        return res


    @api.onchange('periodicity')
    def checking_periodicity(self):


        if self.periodicity:
            if not self.payment_date:
                raise UserError(_('Please choose the Starting date of payment'))
            
            else:
                
                if self.periodicity == 'month':

                    self.next_payment_date = self.payment_date + relativedelta(months=1)
                    
                elif self.periodicity == 'quarter':

                    self.next_payment_date = self.payment_date + relativedelta(months=3)
                    
                elif self.periodicity == 'year':
                    
                    self.next_payment_date = self.payment_date + relativedelta(months=12)

                else:
                    pass
    
    
        
# Below are Configuration Masters

class P7_rent(models.Model):

    _name = 'rent.payments'

    _description = "Maintaining the rent details"


    contract_id = fields.Many2one('p7.contracts', string="Contract", required=True)
    rent_date = fields.Date(string="rent")
    name = fields.Char(string="Label", required=True)
    amount_ht = fields.Float(string="HT Amount", required=True)
    amount_vat = fields.Float(string="Vat Amount")
    amount_ttc = fields.Float(string="TTC Amount", required=True)
    attachment = fields.Many2many('ir.attachment','rent_attachment_rel','aid','rid', string="PDF Upload")


class P7_variable_expense_estimate(models.Model):

    _name = 'variable.expense.estimate'

    _description = "Master for variable expense and estimate of it"

    _sql_constraints = [('home_unique', 'unique(home_id)', 'Variable expense for this home is already exist.!')]


    home_id = fields.Many2one('p7.home', string="Home")
    welcome_pack = fields.Char(string="Welcome Pack")
    cleaning_per_stay = fields.Char(string="Cleaning per Stay")
    linen_per_stay = fields.Char(string="Linen per Stay")
    mid_week_per_stay = fields.Char(string="Mid Week per Stay")
    hot_tub_per_stay = fields.Char(string="Hot Tub per Stay")


class P7_fixed_expense_estimate(models.Model):

    _name = 'fixed.expense.estimate'

    _description = "Master for fixed expense estimate"

    _sql_constraints = [('home_unique', 'unique(home_id)', 'Fixed expense for this home is already exist.!')]


    name = fields.Char()
    home_id = fields.Many2one('p7.home', string="Home", required=True)
    counci_tax = fields.Many2one('p7.tax', string="Counci Tax")
    sejour_tax = fields.Many2one('p7.tax', string="Sejour Tax")
    rubbish_tax = fields.Many2one('p7.tax', string="Rubbish Tax")




class P7_property_expense(models.Model):

    _name = 'property.expense'

    _description = "Maintaining expense for Home"


    name = fields.Many2one('product.product',string="Item Name",required=True, domain=[('purchase_ok','=', True)])
    contract_id = fields.Many2one('p7.contracts', string="Contract", required=True)
    odoo_id = fields.Many2one('account.analytic.account', string="Analytic Account", required=True)
    supplier = fields.Many2one('res.partner',string="Supplier", required=True, domain=[('supplier','=', True)])
    amount_ht = fields.Float(string="HT Amount", required=True)
    vat_rate = fields.Many2one('account.tax', string="Vat Rate")
    amount_ttc = fields.Float(string="TTC Amount", required=True)
    currency = fields.Many2one('res.currency', string="Currency")
    type = fields.Selection([('maintenance','Maintenance'),('onboarding','On Boarding')])
    account = fields.Selection([('owner','Owner'),('emerald','Emerald')])
    status = fields.Selection([('added','Added'),('done','Done')])
    attachment = fields.Many2many('ir.attachment','property_attachment_rel','aid','pid', string="PDF Upload")



class P7_tax(models.Model):

    _name = 'p7.tax'

    _description = "This is a customized tax table for Fixed Expense Estimate"

    _sql_constraints = [('name_unique', 'unique(name)', 'Already this vat value is exist!')]


    name = fields.Float(string="Vat Value", required=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self : self.env.user.company_id.currency_id.id, required=True)



    @api.multi
    def name_get(self):

        if 1 == 1 :
            res = []
            for tax in self:
                if tax.name and tax.currency_id:
                    name = '%s  %s' % (str(tax.name), str(tax.currency_id.name))
               
                res.append((tax.id, name))
            return res
        return super(P7_tax, self).name_get()

