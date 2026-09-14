"""
Week 3 — Phishing Email Detection Model
=========================================
Step 1: Dataset + basic setup

Builds a small labeled email dataset and prepares it for ML.
"""

import pandas as pd
from sklearn.model_selection import train_test_split


# --- Step 1: Define the dataset ---

# Each entry: (email_text, label)
# Label: 1 = Phishing, 0 = Safe
emails = [
    # Phishing emails (label = 1)
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

    # Safe / legitimate emails (label = 0)
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


# --- Step 2: Load into a DataFrame ---

df = pd.DataFrame(emails, columns=["email_text", "label"])
df["label_name"] = df["label"].map({1: "Phishing", 0: "Safe"})


# --- Step 3: Split into features (X) and labels (y) ---

X = df["email_text"]   # The email content
y = df["label"]        # 1 = Phishing, 0 = Safe


# --- Step 4: Train/test split ---

# 80% training, 20% testing, fixed random state for reproducibility
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)


# --- Step 5: Print everything so we can see it ---

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
print("Step 1 complete — dataset loaded and split.")
print("Next: Step 2 — feature extraction.")
print("=" * 60)
