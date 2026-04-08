from dataclasses import dataclass
import csv
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


@dataclass
class ModelOutput:
    is_scam: bool
    confidence: float


class ScamClassifier:
    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=3000)
        self.model = LogisticRegression(max_iter=1000)
        self._train_baseline()

    def _load_dataset_from_csv(self) -> tuple[list[str], list[int]]:
        dataset_path = Path("data/ai_generated_scam_dataset.csv")
        if not dataset_path.exists():
            return [], []

        texts: list[str] = []
        labels: list[int] = []
        with dataset_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                text = (row.get("text") or "").strip().lower()
                label = (row.get("label") or "").strip().lower()
                if not text:
                    continue
                texts.append(text)
                labels.append(1 if label == "scam" else 0)
        return texts, labels

    def _train_baseline(self) -> None:
        texts, labels = self._load_dataset_from_csv()
        if not texts:
            scam_samples = [
                "your bank account is suspended click now to verify",
                "urgent payment required avoid legal action",
                "send gift cards to claim your reward",
                "confirm your password and otp immediately",
                "wire transfer this amount today to secure your package",
                "you won crypto investment return in 24 hours",
            ]
            safe_samples = [
                "let us schedule a normal team meeting tomorrow",
                "your package will arrive on friday by noon",
                "please review the attached project proposal",
                "doctor appointment reminder for monday",
                "your support ticket has been resolved",
                "thanks for your payment your receipt is attached",
            ]
            texts = scam_samples + safe_samples
            labels = [1] * len(scam_samples) + [0] * len(safe_samples)

        labels_arr = np.array(labels)
        vectors = self.vectorizer.fit_transform(texts)
        self.model.fit(vectors, labels_arr)

    def predict(self, text: str) -> ModelOutput:
        vector = self.vectorizer.transform([text])
        prob = float(self.model.predict_proba(vector)[0][1])
        return ModelOutput(is_scam=prob >= 0.5, confidence=prob)


classifier = ScamClassifier()
