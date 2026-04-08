from sqlalchemy.orm import Session

from app.db import models
from app.db.schemas import DetectResponse
from app.ml.model_service import classifier
from app.services.preprocessing_service import extract_urls, preprocess_text
from app.services.rules_engine import run_rules


SUSPICIOUS_DOMAIN_FRAGMENTS = [".ru", ".tk", "bit.ly", "tinyurl", "verify-now", "secure-login"]


def _default_action(is_scam: bool) -> str:
    if is_scam:
        return "Do not click links or share personal information. Verify through official channels."
    return "No strong scam signals found. Still verify the sender before sharing sensitive data."


def _detect_suspicious_url_signals(urls: list[str]) -> list[str]:
    reasons: list[str] = []
    for url in urls:
        if any(fragment in url for fragment in SUSPICIOUS_DOMAIN_FRAGMENTS):
            reasons.append("Contains shortened or suspicious URL pattern")
            break
    return reasons


def analyze_and_store(db: Session, raw_text: str, channel: str | None) -> DetectResponse:
    cleaned = preprocess_text(raw_text)
    model_output = classifier.predict(cleaned)
    rule_reasons, suggested_type = run_rules(cleaned)
    urls = extract_urls(cleaned)
    url_reasons = _detect_suspicious_url_signals(urls)

    reasons = rule_reasons + url_reasons
    confidence = model_output.confidence
    is_scam = model_output.is_scam

    # Rules provide explainable confidence bumps for obvious scam patterns.
    if reasons:
        confidence = min(1.0, confidence + min(0.25, 0.05 * len(reasons)))
        is_scam = True if confidence >= 0.55 else is_scam

    scam_type = suggested_type or ("generic scam risk" if is_scam else "likely safe")
    recommended_action = _default_action(is_scam)

    message = models.Message(raw_text=raw_text, cleaned_text=cleaned, channel=channel)
    db.add(message)
    db.flush()

    detection = models.Detection(
        message_id=message.id,
        is_scam=is_scam,
        confidence=confidence,
        scam_type=scam_type,
        recommended_action=recommended_action,
    )
    db.add(detection)
    db.flush()

    final_reasons = reasons or ["No explicit rule matches; model-based classification only"]
    db.add_all([models.DetectionReason(detection_id=detection.id, reason=r) for r in final_reasons])
    db.commit()
    db.refresh(detection)
    db.refresh(message)

    return DetectResponse(
        message_id=message.id,
        is_scam=detection.is_scam,
        confidence=float(round(detection.confidence, 4)),
        scam_type=detection.scam_type,
        reasons=final_reasons,
        recommended_action=detection.recommended_action,
        created_at=detection.created_at,
    )
