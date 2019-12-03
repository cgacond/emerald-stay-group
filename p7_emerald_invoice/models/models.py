# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import collections, functools, operator 
class Account_invoice_extended(models.Model):

    _inherit = 'account.invoice'



    def get_analytic_name(self,inv):
        
        ans = ''
        stop = 0
        for i in inv.invoice_line_ids:

            if i.account_analytic_id:
                stop += 1
                if stop == 1:
                    ans = i.account_analytic_id.name
        return ans


    
    def design_line_item(self,inv):
        

        ans = {}    
        one_ans = []
        two_ans = []
        three_ans = []
        l1_amt = []
        count_of_d = 0
        t_vat = []
        gross_total = 0
        minus_total = 0

        for line in inv.invoice_line_ids:
            one = {}
            two = {}
            three = {}
            
            if line.product_id.name.upper() == 'GROSS':
                one['order'] = True
                one['name'] = line.name
                one['amount'] = line.price_subtotal
                gross_total += line.price_subtotal
                l1_amt.append(one['amount'])
                one_ans.append(one)

            if line.product_id.name.upper() == 'MINUS':
                
                one['order'] = False
                one['name'] = line.name
                one['amount'] = line.price_subtotal
                minus_total += abs(line.price_subtotal)
                l1_amt.append((one['amount']))
                one_ans.append(one)
            
            
            if line.product_id.name.upper() == 'MINUS: EMERALD STAY SHARE':
                
                two['name'] = line.name
                two['amount'] = line.price_subtotal
                two['percentage'] = str(line.quantity * 100) + ' ' + '%'
                two_ans.append(two)

            

            if line.product_id.name.upper() == 'DEDUCTIONS':
                three['name'] = line.name
                three['amount'] = line.price_subtotal
                three_ans.append(three)
                count_of_d += 1
                t_vat.append(three['amount'])

            

            # preparing vat


        t_dicts = []
        tax_dicts = []
        result = None
        if inv.tax_line_ids:

            for t in inv.tax_line_ids:

                
                t_dicts.append({t.tax_id.id:t.amount})

        if t_dicts:

            result = dict(functools.reduce(operator.add,map(collections.Counter, t_dicts))) 

        total_vat = 0
        if result != None:

            for x,y in zip(result.keys(),result.values()):
                total_vat += y
                tax_dicts.append({'name':'VAT' +' ' + self.env['account.tax'].sudo().browse(x).name,'amount':y})

        
            






        l1_ans = gross_total - minus_total
        
        ans['one'] = sorted(one_ans, key = lambda i: i['order'],reverse=True)

        ans['label1'] = [{'name': 'Net hospitality revenue over period', 'amount':round(l1_ans,2)}]
        
        
       
        ans['two'] = two_ans

        if two_ans:


            ans['label2'] = [{'name': 'Net rent to pay', 'amount': round(l1_ans - abs(two_ans[0]['amount']),2)}]
        else:
            ans['label2'] = [{'name': 'Net rent to pay', 'amount': round(l1_ans - 0,2)}]
        
        ans['label3'] = "Deductions (article" " " + str(count_of_d) + " of rent agreement)"

        ans['three'] = three_ans
        if two_ans:
            
            tot_ex_vat = (abs(l1_ans) - abs(two_ans[0]['amount'])) - abs(sum(t_vat))
        else:

            tot_ex_vat = (abs(l1_ans) - 0) - abs(sum(t_vat))

        ans['label4'] = [{'name':'Total excluding VAT','amount':round(tot_ex_vat,2)}]


        
        if t_dicts:

            ans['label5'] = tax_dicts
        else:
            ans['label5'] = [{'name':'VAT 0' ,'amount':0}]

        ans['label6'] = [{'name':'Total including VAT','amount': round(tot_ex_vat + total_vat,2)}]

        
        return ans