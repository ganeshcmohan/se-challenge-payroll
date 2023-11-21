import pandas as pd
import json
import io

from flask import current_app


class CSVJSONConverter:
    """
    Convert csv to json and parse the fields to save in Payroll model
    """

    @classmethod
    def build_json(cls, filename=None):
        if not filename:
            return None
        file_buffer = filename.read()
        file_stream = io.BytesIO(file_buffer)
        df = pd.read_csv(file_stream)
        json_data = df.to_json(orient="records")
        data = json.loads(json_data)
        return data
