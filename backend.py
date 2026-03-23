"""
backend.py – ML logic for FakeShield
======================================
Handles feature extraction, data generation, and model training.
Import this in frontend.py.
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from textblob import TextBlob
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

try:
    import emoji
    HAS_EMOJI = True
except ImportError:
    HAS_EMOJI = False


# ─────────────────────────────────────── Feature extraction ──────────────────

def count_emojis(text: str) -> int:
    if HAS_EMOJI:
        return sum(1 for ch in text if ch in emoji.EMOJI_DATA)
    return 0


def extract_features(text: str, rating: int = 5, verified: int = 0) -> dict:
    words  = text.split()
    wc     = max(len(words), 1)
    length = len(text)
    blob   = TextBlob(text)
    return {
        "word_count":             wc,
        "unique_word_ratio":      len(set(w.lower() for w in words)) / wc,
        "capital_ratio":          sum(1 for c in text if c.isupper()) / max(length, 1),
        "exclamation_count":      text.count("!"),
        "review_length":          length,
        "sentiment_polarity":     (blob.sentiment.polarity + 1) / 2,
        "sentiment_subjectivity": blob.sentiment.subjectivity,
        "extreme_rating":         1 if rating in (1, 5) else 0,
        "verified_purchase":      verified,
        "emoji_count":            count_emojis(text),
        "punctuation_ratio":      sum(1 for c in text if c in "!?.,;:") / max(length, 1),
    }


FEATURE_COLS = [
    "word_count", "unique_word_ratio", "capital_ratio", "exclamation_count",
    "review_length", "sentiment_polarity", "sentiment_subjectivity",
    "extreme_rating", "verified_purchase", "emoji_count", "punctuation_ratio",
]


# ─────────────────────────────────────── Data generation ─────────────────────

def _generate_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)

    fake_samples = [
        "AMAZING PRODUCT!!! BEST PURCHASE OF MY LIFE!!!! BUY THIS NOW!!!",
        "WOW!! This changed my life! INCREDIBLE quality! 5 STARS 10/10!!",
        "PERFECT PERFECT PERFECT!!! Recommended to EVERYONE!!! BEST EVER!!!",
        "FANTASTIC PRODUCT! SO HAPPY!!! WILL BUY AGAIN AND AGAIN!!!",
        "BEST PRODUCT EVER!!! CHANGED MY LIFE!!! 5 STARS NO DOUBT!!!",
        "INCREDIBLE QUALITY SO FAST SHIPPING 10/10 WOULD BUY AGAIN!!!",
        "LOVE LOVE LOVE THIS PRODUCT!!! NO COMPLAINTS AT ALL!!!",
        "OMG THIS IS AMAZING!!! SUPER FAST DELIVERY!!! HIGHLY RECOMMEND!!!",
        "AMAZING!!! Ordered 10 for my whole family!!! Seller is SUPERB!!!",
        "Zero issues absolutely flawless buy immediately best product love it",
    ]
    real_samples = [
        "I've been using this for three weeks. Quite satisfied with build quality.",
        "Decent product for the price. Installation was straightforward.",
        "After reading reviews I decided to purchase. Quality is decent.",
        "Ordered for my home office. Works perfectly fine. Instructions were clear.",
        "Bought as a gift. The person loved it. Quality seems solid.",
        "Good product overall. Arrived on time. Packaging was intact.",
        "Works as described. Not the best quality but acceptable for the price.",
        "Setup was easy. It does the job. Nothing fancy but reliable.",
        "I am satisfied with this purchase. Minor issues but nothing major.",
        "Product is okay. Delivery took a bit longer than expected.",
    ]

    rows = []
    for _ in range(500):
        f = extract_features(fake_samples[rng.integers(10)], int(rng.integers(4, 6)), int(rng.integers(0, 2)))
        f["label"] = 1
        rows.append(f)
    for _ in range(500):
        f = extract_features(real_samples[rng.integers(10)], int(rng.integers(2, 6)), int(rng.integers(0, 2)))
        f["label"] = 0
        rows.append(f)

    df = pd.DataFrame(rows)
    for col in [c for c in FEATURE_COLS if c not in ("extreme_rating", "verified_purchase")]:
        df[col] = (df[col] + rng.normal(0, df[col].std() * 0.08, len(df))).clip(lower=0)
    return df


# ─────────────────────────────────────── Model training ──────────────────────

def train_model():
    """Train a RandomForest on synthetic data. Returns (model, accuracy%)."""
    df  = _generate_data()
    X   = df[FEATURE_COLS].values
    y   = df["label"].values
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42)
    clf.fit(X_tr, y_tr)
    acc = round(accuracy_score(y_te, clf.predict(X_te)) * 100, 1)
    return clf, acc


# ─────────────────────────────────────── Prediction ──────────────────────────

def predict(clf, text: str, rating: int = 5, verified: int = 0, threshold: float = 0.5) -> dict:
    """Return prediction result dict with fake_prob, label, and features."""
    feats = extract_features(text, rating, verified)
    row   = np.array([feats[c] for c in FEATURE_COLS]).reshape(1, -1)
    prob  = float(clf.predict_proba(row)[0][1])
    return {
        "fake_prob": prob,
        "label":     int(prob >= threshold),
        "features":  feats,
    }
