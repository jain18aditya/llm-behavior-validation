import re

def json_extractor(text: str):
    order_id = re.search(r"Order ID:\s*(\d+)", text)
    amount = re.search(r"\$(\d+)", text)
    status = re.search(r"Status:\s*(\w+)", text)

    return {
        "order_id": order_id.group(1) if order_id else None,
        "amount": amount.group(1) if amount else None,
        "status": status.group(1) if status else None
    }