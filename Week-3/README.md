# Week 3 - Phishing Email Detection Model

A machine learning model that classifies emails as **Phishing** or **Safe** using engineered features and scikit-learn.

## Task Requirements

Build a machine learning model using Scikit-learn that can:

- Train on a dataset of phishing and legitimate emails
- Extract and analyze email features (URLs, keywords, etc.)
- Classify emails as "Phishing" or "Safe"
- Display accuracy and confusion matrix

## What This Does

The model extracts **10 engineered features** from each email and trains a **Multinomial Naive Bayes** classifier:

### Feature Categories

**URL features:**
- `url_count` - number of URLs in the email
- `has_http` - whether HTTP is present (phishing sites rarely use HTTPS)
- `has_at_symbol` - whether @ symbol is present
- `suspicious_tld_count` - count of suspicious top-level domains (.xyz, .tk, .top, .loan, .gq, etc.)

**Keyword features:**
- `urgent_keyword_count` - urgent/scarcity words (urgent, immediate, act now, suspended, etc.)
- `verify_keyword_count` - verification words (verify, confirm, validate, login, sign in, etc.)
- `prize_keyword_count` - prize/winning words (winner, prize, claim, congratulations, free, etc.)

**Text features:**
- `generic_greeting` - whether the email uses a generic greeting ("Dear Customer", etc.)
- `email_length` - total length of the email text
- `uppercase_ratio` - ratio of uppercase characters (phishing often uses more caps)

## How to Run

### Prerequisites

- Python 3.14.7 (installed at `C:\Users\hp\AppData\Local\Python\pythoncore-3.14-64\python.exe`)
- Required libraries: `pandas`, `scikit-learn`, `numpy`

### Install dependencies

```bash
C:\Users\hp\AppData\Local\Python\pythoncore-3.14-64\python.exe -m pip install pandas scikit-learn numpy
```

### Run the script

```bash
cd C:\Users\hp\Thiranx-Internship-clone
C:\Users\hp\AppData\Local\Python\pythoncore-3.14-64\python.exe Week-3\phishing_detector.py
```

Or in VS Code: open `Week-3/phishing_detector.py`, select Python 3.14.7 interpreter, click **Run Python File** (▶️ button).

## Expected Output

The script runs in 4 steps:

1. **Dataset Overview** — shows 38 emails (18 phishing + 20 safe)
2. **Feature Extraction** — lists all 10 features and confirms the extractor is ready
3. **Step 3 — Small Dataset Model** — trains on 15 emails, shows 66.7% accuracy (limited data)
4. **Step 4 — Expanded Dataset Model** — trains on 38 emails, shows **100% test accuracy** with a clean confusion matrix (4 true negatives, 4 true positives, zero errors)

## Key Results

- **Test accuracy (expanded model):** 100% on 8 test samples
- **Confusion matrix:** TN=4, FP=0, FN=0, TP=4
- **Classification report:** precision=1.00, recall=1.00, f1-score=1.00 for both classes
- **Predictions on new emails:** 6 of 7 new emails classified correctly

## Limitations

- Small dataset: real phishing detection uses thousands of labeled emails
- Keyword features are English-only and can be evaded by changing wording
- URL features only work when URLs are present in email text
- No content-based features (e.g., CountVectorizer) — those can catch patterns the keyword list misses
- This is a learning exercise, not a production system

## Dataset

The dataset is defined inline in the script as a list of (email_text, label) pairs:

- **Label 1 = Phishing** (40 examples covering common phishing patterns)
- **Label 0 = Safe** (25 examples of legitimate emails)

In a real project, this would come from a CSV file or database.

## Files

| File | Description |
|---|---|
| `phishing_detector.py` | Main script — dataset, feature extraction, training, evaluation, predictions |

## Author

Arsha — Thiranex Internship Program
