import mongoengine as db
import datetime
from flask import current_app


class Employee(db.Document):
    JOB_TYPE = ["A", "B"]
    id = db.SequenceField(primary_key=True)
    firstName = db.StringField(required=False)
    lastName = db.StringField(required=False)
    jobGroup = db.StringField(choices=JOB_TYPE)


class PayPeriod(db.EmbeddedDocument):
    id = db.SequenceField(primary_key=True)
    startDate = db.DateTimeField()
    endDate = db.DateTimeField()


class TimeReportLog(db.Document):
    id = db.SequenceField(primary_key=True)
    created_time = db.DateTimeField(default=datetime.datetime.now)
    file_name = db.StringField(required=True)

    @classmethod
    def file_exist(cls, file_name):
        current_app.logger.info("File name", file_name)
        csv_exist = cls.objects(file_name=file_name).first()
        current_app.logger.info("s csv exist name", csv_exist)

        if csv_exist:
            return True
        else:
            cls(file_name=file_name).save()
            return False


class Payroll(db.Document):
    id = db.SequenceField(primary_key=True)
    # employeeId = db.ReferenceField(Employee, required=True)
    employeeId = db.IntField(required=True)
    payPeriod = db.EmbeddedDocumentField(PayPeriod)
    amountPaid = db.DecimalField(precision=2, required=True, min_value=0)
