from django.db import models

# Create your models here.

class Account(models.Model):
    accno = models.IntegerField()
    balance = models.FloatField()
    description = models.CharField(max_length=200)
    def __unicode__(self):
        return '%d, '%self.accno + self.description
    
class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=200)
    def __unicode__(self):
        return str(self.date) + ', ' + self.description
    
class Booking(models.Model):
    trans = models.ForeignKey(Transaction)
    debit = models.ForeignKey(Account, related_name='debit_acc')
    credit = models.ForeignKey(Account, related_name='credit_acc')
    value = models.FloatField()
    def __unicode__(self):
        return '%.2f'%self.value
