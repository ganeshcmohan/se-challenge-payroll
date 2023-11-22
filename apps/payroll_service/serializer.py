from collections import defaultdict
from datetime import datetime, timedelta

from flask import current_app

from .models import PayPeriod, Payroll


class PayrollSerializer:
    """This is a Serializer class for Payroll model"""

    def __init__(self) -> None:
        self.payroll_report = {"payrollReport": {"employeeReports": []}}

    def serialize_data(self, payroll_list):
        for data in payroll_list:
            employee_id = data["employeeId"]
            start_date = data["payPeriod"]["startDate"]
            end_date = data["payPeriod"]["endDate"]
            amount_paid = data["amountPaid"]
            self.payroll_report["payrollReport"]["employeeReports"].append(
                {
                    "employeeId": employee_id,
                    "payPeriod": {
                        "startDate": start_date.strftime("%Y-%m-%d"),
                        "endDate": end_date.strftime("%Y-%m-%d"),
                    },
                    "amountPaid": f"${amount_paid:.2f}",
                }
            )
        return self.payroll_report

    def list(self) -> list:
        payroll = Payroll.objects()
        payroll_list = self.serialize_data(payroll)
        return payroll_list

    def create(self, data):
        """
        process the data based on Payroll model format and save to Database
        :param data:
        :return: json_data
        """

        # Group data by employee ID and pay period
        grouped_data = defaultdict(list)
        for entry in data:
            employee_id = entry["employee id"]
            date = datetime.strptime(entry["date"], "%d/%m/%Y")
            # Define your logic to determine pay periods based on dates
            # For example, assuming pay periods are 15 days:
            start_date = date - timedelta(days=date.day - 1)
            end_date = start_date + timedelta(days=14)
            pay_period = f"{start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}"

            # Add data to the grouped structure
            grouped_data[(employee_id, pay_period)].append(entry)
        self.payroll_save(grouped_data)
        current_app.logger.info("result: %s", self.payroll_report)
        return self.payroll_report

    @staticmethod
    def calculate_amount(hours_worked, job_group):
        # Calculate amount paid for each pay period
        rate = 20 if job_group == "A" else 30
        return hours_worked * rate

    def payroll_save(self, grouped_data):
        # pre-process grouped data  and save to database.
        try:
            for (employee_id, pay_period), entries in grouped_data.items():
                total_amount_paid = sum(
                    self.calculate_amount(
                        entry["hours worked"], entry["job group"]
                    )
                    for entry in entries
                )
                current_app.logger.info(
                    "total_amount_paid: %s", total_amount_paid
                )
                start_date, end_date = pay_period.split(" - ")
                pay_period_obj = PayPeriod(
                    **{"startDate": start_date, "endDate": end_date}
                )
                report_entry = {
                    "employeeId": int(employee_id),
                    "payPeriod": pay_period_obj,
                    # "amountPaid": f"${total_amount_paid:.2f}",  # Format amount as currency string
                    "amountPaid": total_amount_paid,
                }
                payroll = Payroll(**report_entry)
                payroll.save()
                self.payroll_report["payrollReport"]["employeeReports"].append(
                    report_entry
                )
            return True
        except Exception as exec:
            current_app.logger.info("payroll creation failed: %s", exec)
            return False
