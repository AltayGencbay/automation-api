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

## HTML raporu oluşturma

Konsoldan takip etmek yerine pytest-html eklentisiyle çıktı almak için aşağıdaki komutu çalıştırın:

```
pytest -sv --html=reports/petstore.html
```

Komut tamamlandığında `reports/petstore.html` dosyasını tarayıcıda açarak detaylı test raporunu görüntüleyebilirsiniz.
