# Payroll service API with Docker

This repository contains a simple Flask API that can be run using Docker.

## Prerequisites

- Docker installed on your machine.

## Setup Instructions

1. Clone this repository:

    ```bash
     git clone https://github.com/ganeshcmohan/se-challenge-payroll.git
     cd se-challenge-payroll
    ```

2. Build and start the services with `docker-compose`:

    ```bash
    docker-compose up --build
    ```

This will build the Docker image for your Flask API and start it using `docker-compose`. The API will be accessible at `http://localhost:9001`.

### Shutting Down

To stop the running containers, press `Ctrl + C` in the terminal where `docker-compose up` is running. To remove the containers completely, run:

```bash
docker-compose down
    ```

## Endpoints

### Endpoint 1: `/payroll/list`

- **Method**: GET
- **Description**: Returns employess payroll report list
- **Usage**:

    ```bash
    curl http://localhost:9001/payroll/list
    ```

- **Response**:

    ```json
   {
    "payrollReport": {
        "employeeReports": [
            {
                "amountPaid": "$370.00",
                "employeeId": 1,
                "payPeriod": {
                    "endDate": "2023-11-15",
                    "startDate": "2023-11-01"
                }
            },
            {
                "amountPaid": "$930.00",
                "employeeId": 2,
                "payPeriod": {
                    "endDate": "2023-11-15",
                    "startDate": "2023-11-01"
                }
            },
            {
                "amountPaid": "$590.00",
                "employeeId": 3,
                "payPeriod": {
                    "endDate": "2023-11-15",
                    "startDate": "2023-11-01"
                }
            },
            {
                "amountPaid": "$600.00",
                "employeeId": 4,
                "payPeriod": {
                    "endDate": "2023-11-15",
                    "startDate": "2023-11-01"
                }
            }
        ]
    }
}
    ```

### Endpoint 2: `/payroll/upload-report`

- **Method**: POST
- **Description**: Upload a csv file contains employes timely report.Sample csv report file is included `time-report-42.csv`
- **Usage**:

- Use tools like `curl` or Postman to send a POST request to `http://localhost:9001/payroll/upload-report` with a file attached in form-data.

      In Postman:
        1. Set the request type to POST.
        2. Enter the URL: `http://localhost:9001/payroll/upload-report`.
        3. Select the Body tab and choose `form-data`.
        4. Add a key named `csv_file` and select a file to upload.

      In `curl`:

      ```bash
      curl -X POST -F "csv_file=@/path/to/your/file.csv" http://localhost:9001/payroll/upload-report
      ```

      Replace `/path/to/your/file.csv` with the path to the file you want to upload.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
