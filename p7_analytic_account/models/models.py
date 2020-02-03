# -*- coding: utf-8 -*-

from odoo import models, fields, api

class P7_account_invoice_inherited(models.Model):

    _inherit = 'account.invoice.line'


    is_pl = fields.Boolean(default=False)


    @api.onchange('account_id')
    def _onchange_account_id(self):

        # This function inherited from account module
        if not self.account_id:
            return
        if not self.product_id:
            fpos = self.invoice_id.fiscal_position_id
            if self.invoice_id.type in ('out_invoice', 'out_refund'):
                default_tax = self.invoice_id.company_id.account_sale_tax_id
            else:
                default_tax = self.invoice_id.company_id.account_purchase_tax_id
            self.invoice_line_tax_ids = fpos.map_tax(self.account_id.tax_ids or default_tax, partner=self.partner_id)
        elif not self.price_unit:
            self._set_taxes()

            
        # Below is P7 code for checking whether selected account is P&L or not. If P&L means we need make analytic account as mandatory.

        if self.account_id:
            if self.account_id.user_type_id.name in ['Other Income','Income','Depreciation','Expenses','Cost of Revenue']:
                self.is_pl = True
            else:
                self.is_pl = False
        else:
            self.is_pl = False




class P7_account_move_line(models.Model):

    _inherit = 'account.move.line'

    is_pl = fields.Boolean(default=False)


    @api.onchange('amount_currency', 'currency_id', 'account_id')
    def _onchange_amount_currency(self):
        '''Recompute the debit/credit based on amount_currency/currency_id and date.
        However, date is a related field on account.move. Then, this onchange will not be triggered
        by the form view by changing the date on the account.move.
        To fix this problem, see _onchange_date method on account.move.
        '''
        # NOTE This function is inherited from account module
        for line in self:
            company_currency_id = line.account_id.company_id.currency_id
            amount = line.amount_currency
            if line.currency_id and company_currency_id and line.currency_id != company_currency_id:
                amount = line.currency_id._convert(amount, company_currency_id, line.company_id, line.date or fields.Date.today())
                line.debit = amount > 0 and amount or 0.0
                line.credit = amount < 0 and -amount or 0.0
        
            # Below P7 code
            if line.account_id:
                if line.account_id.user_type_id.name in ['Other Income','Income','Depreciation','Expenses','Cost of Revenue']:
                    line.is_pl = True
                else:
                    line.is_pl = False



class P7_hr_expense(models.Model):

    _inherit = 'hr.expense'

    is_pl = fields.Boolean(default=False)

    
    @api.onchange('account_id')
    def onchange_account_id(self):

        if self.account_id:
            print("-if account---------")
            if self.account_id.sudo().user_type_id.name in ['Other Income','Income','Depreciation','Expenses','Cost of Revenue']:
                print("-if condition---------")
                self.is_pl = True
            else:
                print("-else account---------")
                self.is_pl = False
        