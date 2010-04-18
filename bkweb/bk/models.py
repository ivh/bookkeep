from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat

class Account(models.Model):
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    accno = models.IntegerField(_('Account number'), help_text=_('Number of the account, according to BAS. This number is used for classifying accounts, e.g. when calculating income statemant.'),primary_key=True)
    balance = models.FloatField(_('Balance'), help_text=_('The current balance of the account'))
    debinc = models.BooleanField(_('Debit increases balance?'), help_text=_('General distinction of accounts, into which direction the balance goes for debit and credit.'))
    description = models.CharField(_('Description'), help_text=_('Describe the account.'),max_length=512)
    def __unicode__(self):
        return '%d, '%self.accno + self.description
    
class Transaction(models.Model):
    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    date = models.DateField(_('Date'), help_text=_('Date of the transaction'))
    description = models.CharField(_('Description'), help_text=_('Describe the transaction.'),max_length=512)
 
    def __unicode__(self):
        return u'%d, %s, %s'%(self.id,self.date.isoformat(),self.description)

    def isbalanced(self):
        csum,dsum=0.0,0.0
        for booking in self.booking_set.all():
            if booking.credit: csum+=booking.credit
            if booking.debit: dsum+=booking.debit
        bal=csum-dsum
        return (bal < 0.01) and (bal > -0.01)
    
    def save(self, *args, **kwargs):
        # dont save unbalanced transactions
        if self.isbalanced():
            super(Transaction, self).save(*args, **kwargs) 
        
    
class Booking(models.Model):
    class Meta:
        verbose_name = _('Booking')
        verbose_name_plural = _('Bookings')

    # this should automatically make Transaction.booking_set work
    trans = models.ForeignKey(Transaction)
    acc = models.ForeignKey(Account)
    debit = models.FloatField(_('Debit'), help_text=_('Debit value'))
    credit = models.FloatField(_('Credit'), help_text=_('Credit value'))
    credit.blank,debit.blank,credit.null,debit.null=(True,)*4
    def __unicode__(self):
        return u'Account:%d D:%.2f C:%.2f'%(self.acc.accno,self.debit or 0.0,self.credit or 0.0)

    def save(self, *args, **kwargs):
        super(Booking, self).save(*args, **kwargs) 

        if self.debit:
            if self.acc.debinc: self.acc.balance+=self.debit
            else: self.acc.balance-=self.debit
        if self.credit:
            if self.acc.debinc: self.acc.balance-=self.credit
            else: self.acc.balance+=self.credit
        self.acc.save()
            
        
class Counterpart(models.Model):
    class Meta:
        verbose_name = _('Counterpart')
        verbose_name_plural = _('Counterparts')

    isCustomer = models.BooleanField(_('Customer?'), help_text=_('Is this a customer? (Supplier otherwise)'))
    name = models.CharField(_('Name'), help_text=_('Counterpart name'),max_length=512)
    
    def save(self, *args, **kwargs):
        super(Counterpart, self).save(*args, **kwargs) 
        
    def __unicode__(self):
        #if self.isCustomer: prefix=_('Customer')
        #else: prefix=_('Supplier')
        #return u'%s: %s'%(prefix,self.name)
        return u'%s'%self.name


class Invoice(models.Model):
    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')

    date = models.DateField(_('Date'), help_text=_('Date of the invoice'))
    counterpart = models.ForeignKey(Counterpart)
    trans = models.OneToOneField(Transaction)
    paytrans = models.OneToOneField(Transaction,related_name='ispaymentfor')
    paytrans.null,paytrans.blank=(True,)*2

    description = models.CharField(_('Description'), help_text=_('Describe the invoice.'),max_length=512)

    def isPaid(self):
        if self.paytrans: return True
        else: return False

    def isCustomer(self):
        return self.counterpart.isCustomer

    def __unicode__(self):
        if self.isCustomer(): prefix=_('Customer Invoice')
        else: prefix=_('Supplier Invoice')
        if self.isPaid(): prefix=string_concat(prefix,_(' (paid)'))
        else: prefix=string_concat(prefix,_(' (unpaid)'))
        return u'%s: %s'%(prefix,self.description)
