from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Recall:
    country: str
    city: str
    reason_for_recall: str
    classification: str
    product_description: str
    code_info: Optional[str]
    report_date: datetime
    recall_number: str
    recalling_firm: str
    initial_firm_notification: str
    status: str
    distribution_pattern: str
