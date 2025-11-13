## Overview
This project demonstrates automated map-testing using Selenium & Python.
It covers panning, zooming, movement simulation, JS execution reliability, and location based cases.

## High-Level Architecture
   Tests(Python tests) -> Page Objects(MapPage interactions) -> Core Framework(driver factory, waits) -> Selenium Webdriver -> Maps Application

## Installation:

## 1️⃣ Install dependencies
```
pip install -r requirements.txt
```
## 2️⃣ Add project to PYTHONPATH
```
export PYTHONPATH="$PWD"
```
##  Running the Tests

Run all tests:
```
pytest -v
```
Run a single test:
```
pytest tests/test_google_maps.py::test_search_city_and_verify_zoom
```


