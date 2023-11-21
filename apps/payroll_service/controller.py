from flask import (
    Blueprint,
    request,
    jsonify,
)
from flask import current_app
from .csv_parser import CSVJSONConverter
from .models import Payroll, Employee, TimeReportLog
from .serializer import PayrollSerializer

payroll = Blueprint("payroll", __name__, url_prefix="/payroll")


@payroll.route("/list", methods=["GET"])
def payroll_list():
    serializer = PayrollSerializer()
    data = serializer.list()
    current_app.logger.info("payroll_report: %s", data)
    return jsonify(data), 200


@payroll.route("/upload-report", methods=["POST"])
def upload_report():
    """
    API - for upload employee timely report csv file for creating payroll.
    Payroll - Saving data to payroll collection
    MANDATORY FIELDS
        csv_file

    PROCESS
            Check if the file is already uploaded
            A valid csv sheet must be uploaded when calling the api
            The csv file data is converted to json
            Json data is serialized to save in payroll collection
    """
    try:
        if request.files.get("csv_file"):
            filename = request.files.get("csv_file").filename
            # CHECK IF A FILE IS ALREADY UPLOADED.
            check_file_exist = TimeReportLog.file_exist(filename)
            if check_file_exist:
                return (
                    jsonify(message=f"{filename} is already uploaded"),
                    400,
                )
            csv_file = request.files.get("csv_file")
            emp_report_list = CSVJSONConverter.build_json(csv_file)
            payroll = PayrollSerializer()
            # Saving to Database
            result = payroll.create(emp_report_list)
        else:
            # CHECK IF A FILE IS UPLOADED
            return (
                jsonify(message="Mandatory field Missing: CSV file missing"),
                400,
            )
        if result:
            current_app.logger.info(result)
            return jsonify(message="Timely report iss added successfully"), 201
    # A VALID CSV FILE MUST BE UPLOADED WHEN CALLING THE API
    except ValueError as error:
        current_app.logger.info(f"Invalid file format:{error}")
        return jsonify(message="Invalid file format"), 403
    except Exception as exc:
        current_app.logger.info(f"error general csv upload error:{exc}")
        return jsonify(message="Internal server error"), 500
