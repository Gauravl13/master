from django.db import models
from elasticsearch_dsl import Document, Keyword, Text
from elasticsearch_dsl.connections import connections
from django.conf import settings
import datetime


class Employee(models.Model):
    emp_id=models.IntegerField(primary_key=True)
    first_name=models.CharField(max_length=40)
    last_name=models.CharField(max_length=40)
    email=models.EmailField()
    mobileno=models.IntegerField()
    gender=models.TextField()
    created_at=models.DateTimeField(default=datetime.date.today)
    updated_at=models.DateTimeField()

    def indexing(self):
        obj = MyIndex(
            meta={'id': self.emp_id},
            emp_id=self.emp_id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            mobileno=self.mobileno,
            gender=self.gender,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        obj.save()

class MyIndex(Document):
    emp_id = Keyword()
    first_name = Text()
    last_name = Text()
    email = Text()
    mobileno = Text()
    gender = Text()
    created_at =Keyword()
    updated_at =Keyword()

    class Index:
        name = 'userinformation'






