from django.db import models
from multiselectfield import MultiSelectField
# Create your models here.

class Tool(models.Model):
    REQUESTED = 'REQUESTED'
    REJECTED = 'REJECTED'
    NEW = 'NEW'
    IN_PROGRESS = 'IN_PROGRESS'
    POSTPONED = 'POSTPONED'
    DONE = 'DONE'
    STATUS_CHOICES = [
        (REQUESTED,   'Requested'),
        (REJECTED,    'Rejected'),
        (NEW,         'New'),
        (IN_PROGRESS, 'In progress'),
        (POSTPONED,   'Postponed'),
        (DONE,        'Done'),
        (POSTPONED,   'Graduate'),
    ]
    HEX = 'HEX'
    ARXML = 'ARXML'
    DBC = 'DBC'
    LOGS = 'LOGS'
    EXCEL = 'EXCEL'
    CATEGORY_CHOICES = [
        (HEX,   'hex'),
        (ARXML, 'arxml'),
        (DBC,   'dbc'),
        (LOGS,  'logs'),
        (EXCEL, 'excel'),
    ]

    ICON_CHOICES = [
        (HEX,   'ni ni-archive-2'),
        (ARXML, 'ni ni-collection'),
        (DBC,   'ni ni-money-coins'),
        (LOGS,  'ni ni-single-copy-04'),
        (EXCEL, 'ni ni-books'),
    ]
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    request_date = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length = 11, choices = STATUS_CHOICES, default = REQUESTED)
    category = MultiSelectField(choices = CATEGORY_CHOICES)
    category_icon = MultiSelectField(choices = ICON_CHOICES)