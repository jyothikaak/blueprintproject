from collections.abc import Callable


Rule = tuple[Callable[[str], bool], str, str]


def _contains_any(text: str, words: list[str]) -> bool:
    return any(word in text for word in words)


def run_rules(cleaned_text: str) -> tuple[list[str], str | None]:
    rules: list[Rule] = [
        (
            lambda t: _contains_any(t, ["urgent", "act now", "immediately", "final warning"]),
            "Urgent pressure language detected",
            "urgent payment scam",
        ),
        (
            lambda t: _contains_any(t, ["otp", "password", "pin", "verification code"]),
            "Requests sensitive security credentials",
            "account takeover phishing",
        ),
        (
            lambda t: _contains_any(t, ["gift card", "itunes card", "steam card"]),
            "Gift-card payment request is a common scam signal",
            "gift card scam",
        ),
        (
            lambda t: _contains_any(t, ["wire transfer", "crypto", "bitcoin", "usdt"]),
            "Unrecoverable payment method requested",
            "investment/payment scam",
        ),
        (
            lambda t: _contains_any(t, ["bank account locked", "account suspended", "verify account"]),
            "Impersonation of financial institution patterns detected",
            "bank phishing",
        ),
        (
            lambda t: _contains_any(t, ["upfront fee", "processing fee", "pay to start job"]),
            "Job-related upfront payment language detected",
            "job scam",
        ),
    ]
    reasons: list[str] = []
    suggested_type: str | None = None

    for check, reason, scam_type in rules:
        if check(cleaned_text):
            reasons.append(reason)
            if suggested_type is None:
                suggested_type = scam_type
    return reasons, suggested_type
