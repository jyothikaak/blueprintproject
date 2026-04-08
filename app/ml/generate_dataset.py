import csv
import random
from pathlib import Path


SCAM_TEMPLATES = [
    "urgent your {target} will be suspended click now",
    "confirm your {secret} immediately to avoid closure",
    "send {payment} today to release your package",
    "limited offer transfer {payment} now for guaranteed return",
    "job approved pay {payment} to start work",
]

SAFE_TEMPLATES = [
    "hello team our meeting is at {time}",
    "your order is out for delivery and arrives {time}",
    "please review the attached project update",
    "doctor appointment reminder for {time}",
    "thanks for your payment your receipt is attached",
]

TARGETS = ["bank account", "email account", "subscription"]
SECRETS = ["otp", "password", "pin"]
PAYMENTS = ["gift card", "wire transfer", "crypto payment"]
TIMES = ["tomorrow", "friday", "next week", "monday morning"]


def _fill(template: str) -> str:
    return template.format(
        target=random.choice(TARGETS),
        secret=random.choice(SECRETS),
        payment=random.choice(PAYMENTS),
        time=random.choice(TIMES),
    )


def build_dataset(rows_per_class: int = 50) -> None:
    out_path = Path("data/ai_generated_scam_dataset.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for _ in range(rows_per_class):
        rows.append({"text": _fill(random.choice(SCAM_TEMPLATES)), "label": "scam"})
        rows.append({"text": _fill(random.choice(SAFE_TEMPLATES)), "label": "safe"})

    random.shuffle(rows)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    build_dataset()
