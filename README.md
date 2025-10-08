# Petstore API Automation

Automated tests for the Swagger Petstore API (https://petstore.swagger.io/v2) using pytest and Requests.

## Structure

```
api_tests/
  tests/
    test_pet_crud_positive.py
    test_pet_crud_negative.py
  schemas/
    pet_schema.json
  utils/
    logger.py
  conftest.py
  requirements.txt
  README.md
```

## Getting started

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the test suite: `pytest -sv`

The tests hit the public sandbox API and may intermittently fail if the service is unreachable. Each test logs requests and responses to help troubleshooting.

## Generating an HTML Report

Instead of monitoring the results in the console, you can generate an output using the pytest-html plugin by running the following command:

```
pytest -sv --html=reports/petstore.html
```

Once the command completes, open the reports/petstore.html file in your browser to view the detailed test report.
