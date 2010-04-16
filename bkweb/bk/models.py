from django.db import models

# Create your models here.

class Account(models.Model):
    accno = models.IntegerField(primary_key=True)
    balance = models.FloatField()
    debinc = models.BooleanField()
    description = models.CharField(max_length=512)
    def __unicode__(self):
        return '%d, '%self.accno + self.description
    
class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=512)
 
    def __unicode__(self):
        return u'%d: %s'%(self.id,self.description)

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
    # this should automatically make Transaction.booking_set work
    trans = models.ForeignKey(Transaction)
    acc = models.ForeignKey(Account)
    debit = models.FloatField()
    credit = models.FloatField()
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
            
        
