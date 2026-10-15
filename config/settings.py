import os
from dotenv import load_dotenv

# Automatically loads .env file if present
load_dotenv()

class Settings:
    BASE_URL = os.getenv("PZ_BASE_URL", "https://pzqa.vercel.app")
    LOGIN_URL = f"{BASE_URL}/login"
    CATALOG_URL = f"{BASE_URL}/"

    # Credentials read securely from .env (locally) or GitHub Secrets (in CI)
    VALID_USERNAME = os.getenv("PZ_USERNAME", "")
    VALID_PASSWORD = os.getenv("PZ_PASSWORD", "")

    # Edge Case & Negative Test Data
    WRONG_PASSWORD = "wrong_pass_123"
    UNREGISTERED_USER = "non_existent_user"

    # Verified Expected UI Text
    EXPECTED_HEADING = "Products"
    EXPECTED_SUBHEADING = (
        "Add items with the stepper on each card. The header shows how many different "
        "products are in your cart, not total units."
    )