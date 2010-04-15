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
        return self.date + ', ' + self.decription
    
class Booking(models.Model):
    trans = models.ForeignKey(Transaction)
    acc = models.ForeignKey(Account)
    value = models.FloatField()
    debORcred = models.BooleanField()
    def __unicode__(self):
        return '%.2f'%self.value
