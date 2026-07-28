import re


def normalize_year(value):
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    # Handle 2024.0
    if value.endswith(".0"):
        value = value[:-2]

    # 2024
    if value.isdigit() and len(value) == 4:
        return value

    # 24
    if value.isdigit() and len(value) == 2:
        return "20" + value

    # FY24
    if value.upper().startswith("FY"):
        yy = value[-2:]
        if yy.isdigit():
            return "20" + yy

    # Mar-24
    match = re.search(r"(\d{2})$", value)
    if match:
        return "20" + match.group(1)

    return None
