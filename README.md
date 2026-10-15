# PZ QA Automation Framework (Playwright + Python)

A production-grade test automation framework built with Python, Pytest, and Playwright utilizing the Page Object Model (POM) design pattern to validate the [PZ QA Web Application](https://pzqa.vercel.app).

---

## Prerequisites

Ensure the following tools are installed on your workstation:
- **Python**: Version `3.12+` (with `pip`)
- **Git**: Version `2.x+`
- **Supported Operating Systems**: Windows 10/11, macOS, or Linux (Ubuntu 20.04+)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2. Create and Activate a Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies & Browser Binaries
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install --with-deps chromium
```

---

## Running Automation Tests

### Run the Complete Test Suite (Headless with HTML Report)
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run Tests in Headed Mode (Watch Execution in Browser)
```bash
pytest --headed
```

### Run Individual Test Suites
```bash
# Authentication & Access Control Suite
pytest tests/test_auth.py

# Product Catalog Browsing Suite
pytest tests/test_catalog.py

# Cart Actions, Stepper & Counter Verification Suite
pytest tests/test_cart_actions.py
```

### Run a Specific Test Case
```bash
pytest tests/test_cart_actions.py::TestCartInteractions::test_tc_act_01_initial_add_to_cart_counter_update
```

---

## Project Structure

```text
pzqa_test/
├── .github/
│   └── workflows/
│       └── playwright.yml         # GitHub Actions CI/CD pipeline
├── config/
│   ├── __init__.py
│   └── settings.py                # Environment configuration & test data
├── pages/
│   ├── __init__.py
│   ├── base_page.py               # Shared browser interactions & waits
│   ├── login_page.py              # Login POM actions & locators
│   └── catalog_page.py            # Catalog & Cart POM actions & locators
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures and browser context hooks
│   ├── test_auth.py               # Authentication tests (TC_AUTH_01 - 09)
│   ├── test_catalog.py            # Product catalog tests (TC_CAT_01 - 04)
│   └── test_cart_actions.py       # Cart operations tests (TC_ACT_01 - 05)
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## CI/CD Pipeline

The framework includes a GitHub Actions configuration at `.github/workflows/playwright.yml`. It runs automatically on pushes and pull requests to `main`, executes all tests in headless mode, and uploads the generated HTML test report as an artifact named `playwright-test-report`.