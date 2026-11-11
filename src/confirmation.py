import re
from src.config.intention import intention


def _contains_keyword(text, keywords):
    for keyword in keywords:
        pattern = rf"\b{re.escape(keyword)}\b"
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
    return False


def request_confirmation(action_description):
    """Ask for confirmation and return CONFIRMED or REJECTED.

    Unrecognized replies are not treated as consent; the user is prompted again.
    """
    while True:
        response = input(
            f"Are you sure you want to {action_description}? (yes/no): "
        ).strip().lower()

        if _contains_keyword(response, intention["yes"]):
            return "CONFIRMED"

        if _contains_keyword(response, intention["no"]):
            return "REJECTED"

        print("Please answer yes or no.")
