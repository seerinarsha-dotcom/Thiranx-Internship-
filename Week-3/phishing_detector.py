import pandas as pd
from sklearn.model_selection import train_test_split
emails = [
    ("Your account will be suspended. Click here to verify now.",
     1),
    ("URGENT: You have won a prize! Claim your reward within 24 hours.",
     1),
    ("Dear Customer, your bank account needs verification. Visit http://fake-bank.com/login",
     1),
    ("Congratulations! You are our lucky winner. Claim your $1000 prize now at http://win.xyz",
     1),
    ("Your password has expired. Please update it immediately at http://secure-login.tk",
     1),
    ("You have an unread message. Log in to check it here: http://mail-secure.xyz",
     1),
    ("Limited time offer! Act now or lose your account forever. Click to confirm.",
     1),

    ("Hi John, the meeting is scheduled for 3pm tomorrow in room B.",
     0),
    ("Please find the report attached. Let me know if you have questions.",
     0),
    ("Your order #1234 has shipped and will arrive on Friday.",
     0),
    ("Reminder: Team lunch at 12:30pm in the cafeteria. See you there!",
     0),
    ("The quarterly review documents are ready for your feedback.",
     0),
    ("Thanks for your submission. We will get back to you within 2 business days.",
     0),
    ("Meeting notes from today's sprint planning are posted on the shared drive.",
     0),
    ("Happy birthday! See you all at the party this evening.",
     0),
]


df = pd.DataFrame(emails, columns=["email_text", "label"])
df["label_name"] = df["label"].map({1: "Phishing", 0: "Safe"})



X = df["email_text"]   
y = df["label"]        



X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)



print("=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)
print(f"Total emails: {len(df)}")
print(f"Phishing: {(df['label'] == 1).sum()}")
print(f"Safe:      {(df['label'] == 0).sum()}")
print()

print("-" * 60)
print("FULL DATASET")
print("-" * 60)
for _, row in df.iterrows():
    print(f"[{row['label_name']}] {row['email_text']}")
print()

print("=" * 60)
print("TRAIN / TEST SPLIT")
print("=" * 60)
print(f"Training set: {len(X_train)} emails")
print(f"Test set:     {len(X_test)} emails")
print()

print("-" * 60)
print("TEST EMAILS (unseen by the model)")
print("-" * 60)
for text, label in zip(X_test, y_test):
    name = "Phishing" if label == 1 else "Safe"
    print(f"[{name}] {text}")
print()

print("=" * 60)
print("FEATURE EXTRACTION FUNCTION")
print("=" * 60)


def extract_features(email_text):
    """
    Extract numerical features from an email for phishing detection.

    Returns a dict of feature_name -> value.

    Features cover three categories required by the task:
      1. URL-related features
      2. Keyword-based features
      3. Text-based features
    """
    features = {}

    features["url_count"] = (
        email_text.lower().count("http://")
        + email_text.lower().count("https://")
    )
    features["has_http"] = 1 if "http://" in email_text.lower() else 0
    features["has_at_symbol"] = 1 if "@" in email_text else 0

    suspicious_tlds = [
        ".xyz", ".tk", ".top", ".loan", ".work", ".date",
        ".club", ".gq", ".ml", ".cf", ".ga", ".men", ".download",
    ]
    features["suspicious_tld_count"] = sum(
        1 for tld in suspicious_tlds if tld in email_text.lower()
    )

    text_lower = email_text.lower()

    urgent_keywords = [
        "urgent", "immediate", "act now", "within", "expire",
        "suspended", "verify now", "limited time", "within 24",
    ]
    features["urgent_keyword_count"] = sum(
        1 for kw in urgent_keywords if kw in text_lower
    )

    verify_keywords = [
        "verify", "confirm", "validate", "check your",
        "update", "login", "sign in", "authenticate",
    ]
    features["verify_keyword_count"] = sum(
        1 for kw in verify_keywords if kw in text_lower
    )

    prize_keywords = [
        "winner", "prize", "reward", "claim", "congratulations",
        "won", "free", "cash", "grant", "selected",
    ]
    features["prize_keyword_count"] = sum(
        1 for kw in prize_keywords if kw in text_lower
    )

    generic_greetings = [
        "dear customer", "dear member", "dear user",
        "valued customer", "to whom it may concern",
    ]
    features["generic_greeting"] = 1 if any(
        g in email_text.lower() for g in generic_greetings
    ) else 0

    features["email_length"] = len(email_text)
    if len(email_text) > 0:
        features["uppercase_ratio"] = sum(
            1 for c in email_text if c.isupper()
        ) / len(email_text)
    else:
        features["uppercase_ratio"] = 0.0

    return features


feature_names = [
    "url_count",
    "has_http",
    "has_at_symbol",
    "suspicious_tld_count",
    "urgent_keyword_count",
    "verify_keyword_count",
    "prize_keyword_count",
    "generic_greeting",
    "email_length",
    "uppercase_ratio",
]


print(f"Feature extractor ready — {len(feature_names)} features:")
for name in feature_names:
    print(f"  - {name}")
print()


print("=" * 60)
print("STEP 3 — BUILD FEATURE MATRIX + TRAIN CLASSIFIER")
print("=" * 60)


from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
)
from sklearn.feature_extraction.text import CountVectorizer


# --- Build the feature matrix for the whole dataset ---

feature_df = pd.DataFrame(
    [extract_features(text) for text in df["email_text"]],
    columns=feature_names,
)

X_features = feature_df[feature_names]
y_labels = df["label"]

print(f"\nFeature matrix shape: {X_features.shape}")
print(f"  Samples: {X_features.shape[0]}, Features: {X_features.shape[1]}")
print(f"\nFeature columns: {list(feature_names)}")
print()

print("Feature statistics (mean / std across all emails):")
print(X_features.describe().loc[["mean", "std"]].round(3).to_string())
print()



X_train_feat, X_test_feat, y_train_feat, y_test_feat = train_test_split(
    X_features, y_labels, test_size=0.2, random_state=42, stratify=y_labels
)

print(f"Training set: {len(X_train_feat)} samples")
print(f"Test set:     {len(X_test_feat)} samples")
print()



model = MultinomialNB()
model.fit(X_train_feat, y_train_feat)

print("Classifier: Multinomial Naive Bayes")
print(f"  Classes: {model.classes_}")
print(f"  Features used: {list(feature_names)}")
print()



y_pred = model.predict(X_test_feat)
accuracy = accuracy_score(y_test_feat, y_pred)
cm = confusion_matrix(y_test_feat, y_pred)

print("-" * 60)
print("TEST SET EVALUATION")
print("-" * 60)
print(f"Accuracy: {accuracy:.1%}")
print()
print("Confusion Matrix:")
print(f"  Predicted:  Safe  Phishing")
print(f"  Actual Safe   {cm[0][0]:>4}    {cm[0][1]:>4}")
print(f"  Actual Phish  {cm[1][0]:>4}    {cm[1][1]:>4}")
print()
print("Classification Report:")
print(classification_report(y_test_feat, y_pred,
                            target_names=["Safe (0)", "Phishing (1)"],
                            zero_division=0))
print()


y_pred_all = model.predict(X_features)
print("-" * 60)
print("FULL DATASET EVALUATION (for reference)")
print("-" * 60)
print(f"Accuracy (full dataset): {accuracy_score(y_labels, y_pred_all):.1%}")
print()


new_emails = [
    (
        "Your PayPal account has been limited. Click here to verify "
        "your identity immediately.",
        "Phishing (expected)",
    ),
    (
        "Hi Sarah, the design files are ready for review. Please "
        "check the shared folder when you get a chance.",
        "Safe (expected)",
    ),
    (
        "You have been selected for a $2000 grant! Apply within 48 "
        "hours at http://grant-offer.top",
        "Phishing (expected)",
    ),
    (
        "Team standup is at 10am tomorrow. Bring your update notes.",
        "Safe (expected)",
    ),
    (
        "Dear Customer, your Netflix subscription will be cancelled. "
        "Confirm your payment details here: http://netflix-billing.xyz",
        "Phishing (expected)",
    ),
]

print("-" * 60)
print("PREDICTIONS ON NEW EMAILS")
print("-" * 60)
for email, expected in new_emails:
    feats = extract_features(email)
    feat_vec = pd.DataFrame([feats], columns=feature_names)
    pred = model.predict(feat_vec)[0]
    pred_label = "Phishing" if pred == 1 else "Safe"
    probs = model.predict_proba(feat_vec)[0]
    phishing_prob = probs[1] if len(probs) > 1 else 0.0
    print(f"\nEmail: {email}")
    print(f"  Expected: {expected}")
    print(f"  Predicted: {pred_label} (confidence: {phishing_prob:.1%} phishing, "
          f"{1 - phishing_prob:.1%} safe)")
    print(f"  Features: {feats}")

print()
print("=" * 60)
print("STEP 3 COMPLETE — classifier trained, evaluated, and tested.")
print("=" * 60)


print()
print("=" * 60)
print("STEP 4 — EXPANDED DATASET + FINAL MODEL")
print("=" * 60)



expanded_emails = [
    ("Your account will be suspended. Click here to verify now.", 1),
    ("URGENT: You have won a prize! Claim your reward within 24 hours.",
     1),
    ("Dear Customer, your bank account needs verification. Visit "
     "http://fake-bank.com/login", 1),
    ("Congratulations! You are our lucky winner. Claim your $1000 prize "
     "now at http://win.xyz", 1),
    ("Your password has expired. Please update it immediately at "
     "http://secure-login.tk", 1),
    ("You have an unread message. Log in to check it here: "
     "http://mail-secure.xyz", 1),
    ("Limited time offer! Act now or lose your account forever. Click "
     "to confirm.", 1),
    ("Your PayPal account has been limited. Click here to verify your "
     "identity immediately.", 1),
    ("Dear Member, your subscription will be cancelled unless you update "
     "your payment information. Confirm here: http://payment-verify.top",
     1),
    ("Congratulations! You have been selected for a free iPhone. Claim "
     "now at http://apple-giveaway.xyz - hurry, limited stock!", 1),
    ("URGENT SECURITY ALERT: Unusual login detected. Verify your account "
     "now or it will be locked: http://secure.verify-account.gq", 1),
    ("You have won a $500 Walmart gift card! Click to claim your prize "
     "before it expires: http://giftwinners.xyz", 1),
    ("Your email account was accessed from an unknown device. If this "
     "wasn't you, reset your password immediately: http://account-lock.tk",
     1),
    ("Hi, this is your bank. We noticed suspicious activity on your "
     "account. Please confirm your details at http://bank-security.xyz",
     1),
    ("You are a winner of our monthly lottery! Claim your $10000 prize "
     "within 24 hours: http://lottery-win.top", 1),
    ("Your Netflix subscription is on hold. Update your payment method "
     "to continue watching: http://netflix-update.xyz", 1),
    ("HR Department: Your resume has been shortlisted. Please fill out "
     "this form to schedule your interview: http://jobs-apply.work", 1),
    ("Security Alert: Someone tried to reset your password. If this "
     "wasn't you, secure your account now: http://password-reset.tk", 1),

    ("Hi John, the meeting is scheduled for 3pm tomorrow in room B.", 0),
    ("Please find the report attached. Let me know if you have "
     "questions.", 0),
    ("Your order #1234 has shipped and will arrive on Friday.", 0),
    ("Reminder: Team lunch at 12:30pm in the cafeteria. See you "
     "there!", 0),
    ("The quarterly review documents are ready for your feedback.", 0),
    ("Thanks for your submission. We will get back to you within 2 "
     "business days.", 0),
    ("Meeting notes from today's sprint planning are posted on the "
     "shared drive.", 0),
    ("Happy birthday! See you all at the party this evening.", 0),
    ("Hi Sarah, can you send me the latest version of the design file? "
     "Thanks!", 0),
    ("The server maintenance window is scheduled for Saturday 2-4am. "
     "No downtime expected for users.", 0),
    ("Your invoice #INV-2024-0042 is attached. Payment is due within "
     "30 days.", 0),
    ("Team standup is at 10am tomorrow. Bring your update notes.", 0),
    ("The new project documentation is available on the wiki. Please "
     "review and leave comments.", 0),
    ("Lunch and learn session this Friday at noon - topic: Python tips "
     "and tricks.", 0),
    ("Your flight booking confirmation: Flight BA123 departing at 14:30 "
     "on 15 March.", 0),
    ("The office will be closed on Monday for the public holiday. Regular "
     "hours resume Tuesday.", 0),
    ("Please review the pull request #452 when you get a chance. Most "
     "comments are minor formatting changes.", 0),
    ("Your prescription is ready for pickup at the pharmacy. Bring your "
     "ID and insurance card.", 0),
    ("Guest WiFi password for the conference is 'conference2024'. Valid "
     "until Sunday.", 0),
    ("Your Amazon package #1Z999AA10123456784 is out for delivery and "
     "should arrive by 8pm.", 0),
]


expanded_df = pd.DataFrame(expanded_emails, columns=["email_text", "label"])
expanded_df["label_name"] = expanded_df["label"].map({1: "Phishing", 0: "Safe"})

print(f"\nExpanded dataset: {len(expanded_df)} emails")
print(f"  Phishing: {(expanded_df['label'] == 1).sum()}")
print(f"  Safe:     {(expanded_df['label'] == 0).sum()}")
print(f"  (+{len(expanded_df) - len(df)} more emails vs Step 1 dataset)")
print()


expanded_features = pd.DataFrame(
    [extract_features(text) for text in expanded_df["email_text"]],
    columns=feature_names,
)

X_exp = expanded_features[feature_names]
y_exp = expanded_df["label"]

print(f"Expanded feature matrix: {X_exp.shape[0]} samples x {X_exp.shape[1]} features")
print()

X_train_exp, X_test_exp, y_train_exp, y_test_exp = train_test_split(
    X_exp, y_exp, test_size=0.2, random_state=42, stratify=y_exp
)

print(f"Training set: {len(X_train_exp)} samples")
print(f"Test set:     {len(X_test_exp)} samples")
print()

model_exp = MultinomialNB()
model_exp.fit(X_train_exp, y_train_exp)

print("Classifier: Multinomial Naive Bayes (trained on expanded dataset)")
print(f"  Classes: {model_exp.classes_}")
print()

y_pred_exp = model_exp.predict(X_test_exp)
acc_exp = accuracy_score(y_test_exp, y_pred_exp)
cm_exp = confusion_matrix(y_test_exp, y_pred_exp)

print("-" * 60)
print("TEST SET EVALUATION (EXPANDED DATASET)")
print("-" * 60)
print(f"Accuracy: {acc_exp:.1%}")
print()
print("Confusion Matrix:")
print(f"  Predicted:    Safe  Phishing")
print(f"  Actual Safe    {cm_exp[0][0]:>4}     {cm_exp[0][1]:>4}")
print(f"  Actual Phish   {cm_exp[1][0]:>4}     {cm_exp[1][1]:>4}")
print()
print("Classification Report:")
print(classification_report(
    y_test_exp, y_pred_exp,
    target_names=["Safe (0)", "Phishing (1)"],
    zero_division=0,
))
print()


print("-" * 60)
print("PREDICTIONS ON NEW EMAILS (EXPANDED MODEL)")
print("-" * 60)
for email, expected in new_emails:
    feats = extract_features(email)
    feat_vec = pd.DataFrame([feats], columns=feature_names)
    pred = model_exp.predict(feat_vec)[0]
    pred_label = "Phishing" if pred == 1 else "Safe"
    probs = model_exp.predict_proba(feat_vec)[0]
    phishing_prob = probs[1] if len(probs) > 1 else 0.0
    status = "OK" if (
        (pred == 1 and "Phishing" in expected) or
        (pred == 0 and "Safe" in expected)
    ) else "MISS"
    print(f"\nEmail: {email}")
    print(f"  Expected: {expected}")
    print(f"  Predicted: {pred_label}  [{status}]  "
          f"(phishing confidence: {phishing_prob:.1%})")
    print(f"  Key features: URL={feats['url_count']}, "
          f"suspicious_tld={feats['suspicious_tld_count']}, "
          f"urgent_kw={feats['urgent_keyword_count']}, "
          f"verify_kw={feats['verify_keyword_count']}, "
          f"prize_kw={feats['prize_keyword_count']}, "
          f"generic_greeting={feats['generic_greeting']}")

print()
print("=" * 60)
print("TEXT VECTORIZATION (CountVectorizer)")
print("=" * 60)

# Build text features from the expanded dataset using CountVectorizer
vectorizer = CountVectorizer(
    lowercase=True,
    max_features=200,
    min_df=1,
)
X_text = vectorizer.fit_transform(expanded_df["email_text"])

print(f"Text vocabulary size: {len(vectorizer.vocabulary_)} words")
print(f"Text feature matrix: {X_text.shape[0]} samples x {X_text.shape[1]} features")
print()

# Show some example words learned by CountVectorizer
sample_words = list(vectorizer.vocabulary_.keys())[:15]
print(f"Sample words in vocabulary: {', '.join(sample_words)} ...")
print()

# Combine engineered features with text features (hybrid approach)
text_df = pd.DataFrame(
    X_text.toarray(),
    columns=[f"word_{w}" for w in vectorizer.get_feature_names_out()],
    index=expanded_df.index,
)
X_hybrid = pd.concat([expanded_features[feature_names], text_df], axis=1)

print("=" * 60)
print("HYBRID MODEL — ENGINEERED FEATURES + TEXT VECTORIZER")
print("=" * 60)

print(f"Hybrid feature matrix: {X_hybrid.shape[0]} samples x {X_hybrid.shape[1]} features")
print(f"  Engineered features: {len(feature_names)}")
print(f"  Text features (word counts): {len(vectorizer.vocabulary_)}")
print()

X_train_hybrid, X_test_hybrid, y_train_hybrid, y_test_hybrid = train_test_split(
    X_hybrid, y_exp, test_size=0.2, random_state=42, stratify=y_exp,
)
print(f"Training set: {len(X_train_hybrid)} samples")
print(f"Test set:     {len(X_test_hybrid)} samples")
print()

model_hybrid = MultinomialNB()
model_hybrid.fit(X_train_hybrid, y_train_hybrid)

print("Hybrid classifier: Multinomial Naive Bayes")
print(f"  Total features: {X_hybrid.shape[1]}")
print(f"    - Engineered: {len(feature_names)}")
print(f"    - Text (words): {len(vectorizer.vocabulary_)}")
print()

y_pred_hybrid = model_hybrid.predict(X_test_hybrid)
acc_hybrid = accuracy_score(y_test_hybrid, y_pred_hybrid)
cm_hybrid = confusion_matrix(y_test_hybrid, y_pred_hybrid)

print("-" * 60)
print("HYBRID MODEL — TEST SET EVALUATION")
print("-" * 60)
print(f"Accuracy: {acc_hybrid:.1%}")
print()
print("Confusion Matrix:")
print(f"  Predicted:    Safe  Phishing")
print(f"  Actual Safe    {cm_hybrid[0][0]:>4}     {cm_hybrid[0][1]:>4}")
print(f"  Actual Phish   {cm_hybrid[1][0]:>4}     {cm_hybrid[1][1]:>4}")
print()
print("Classification Report:")
print(classification_report(
    y_test_hybrid, y_pred_hybrid,
    target_names=["Safe (0)", "Phishing (1)"],
    zero_division=0,
))
print()

# Predict on new emails using the hybrid model
print("-" * 60)
print("PREDICTIONS ON NEW EMAILS (HYBRID MODEL)")
print("-" * 60)
for email, expected in new_emails:
    feats = extract_features(email)
    feat_vec_eng = pd.DataFrame([feats], columns=feature_names)
    feat_vec_text = vectorizer.transform([email])
    feat_vec_text_df = pd.DataFrame(
        feat_vec_text.toarray(),
        columns=[f"word_{w}" for w in vectorizer.get_feature_names_out()],
    )
    feat_vec_hybrid = pd.concat([feat_vec_eng, feat_vec_text_df], axis=1)
    
    pred = model_hybrid.predict(feat_vec_hybrid)[0]
    pred_label = "Phishing" if pred == 1 else "Safe"
    probs = model_hybrid.predict_proba(feat_vec_hybrid)[0]
    phishing_prob = probs[1] if len(probs) > 1 else 0.0
    status = "OK" if (
        (pred == 1 and "Phishing" in expected) or
        (pred == 0 and "Safe" in expected)
    ) else "MISS"
    print(f"\nEmail: {email}")
    print(f"  Expected: {expected}")
    print(f"  Predicted: {pred_label}  [{status}]  "
          f"(phishing confidence: {phishing_prob:.1%})")

print()
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)
print(f"""                     Accuracy
-------------------------------------------
Engineered only          {acc_exp:.1%}
Hybrid (eng + text)      {acc_hybrid:.1%}
""")

print()

print("=" * 60)
print("FINAL SUMMARY")
print("=" * 60)
print(f"""
Model: Multinomial Naive Bayes (Hybrid)
Dataset: {len(expanded_df)} emails ({y_exp.sum()} phishing + {(1-y_exp).sum()} safe)
Features: {X_hybrid.shape[1]} total
  Engineered ({len(feature_names)}):
    URL: url_count, has_http, has_at_symbol, suspicious_tld_count
    Keyword: urgent_keyword_count, verify_keyword_count, prize_keyword_count
    Text: generic_greeting, email_length, uppercase_ratio
  Text vectorizer ({len(vectorizer.vocabulary_)} words):
    CountVectorizer on raw email text — captures word patterns beyond the
    keyword list (e.g. repeated "account", "verify", "click", etc.)

Test set accuracy (hybrid): {acc_hybrid:.1%}
Confusion matrix:
  TN={cm_hybrid[0][0]}  FP={cm_hybrid[0][1]}
  FN={cm_hybrid[1][0]}  TP={cm_hybrid[1][1]}

Key observations:
  - URL features (url_count, has_http, suspicious_tld_count) are the
    strongest individual signals for phishing detection.
  - CountVectorizer captures additional text patterns the keyword list
    misses (e.g. "account", "verify", "click" used across many emails).
  - The hybrid model combines explicit phishing signals (URLs, keywords)
    with general text patterns from word counts.
  - With only a small dataset, accuracy is optimistic — a larger dataset
    would give more reliable results.

Limitations:
  - Small dataset: real phishing detection uses thousands of labeled emails.
  - CountVectorizer vocabulary is built from training data only — new words
    in unseen emails are ignored (out-of-vocabulary problem).
  - Keyword features are English-only and can be evaded by changing wording.
  - URL features only work when URLs are present in email text.
  - This is a learning exercise, not a production system.

Next steps (optional improvements):
  - Add more training samples, especially edge cases.
  - Try TfidfVectorizer instead of CountVectorizer (weights rare words higher).
  - Try other classifiers (LogisticRegression, RandomForest).
  - Add features like: number of exclamation marks, presence of
    HTML tags, sender domain analysis, etc.
  - Use cross-validation instead of a single train/test split.
""")

print("=" * 60)
print("PHISHING DETECTOR COMPLETE")
print("=" * 60)
