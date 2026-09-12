import string
import math
import hashlib
import sqlite3


DB_PATH = "password_history.db"


def get_password():
    """Ask the user for a password and return it."""
    password = input("Enter a password to check: ")
    return password


def check_length(password):
    """Return the length of the password."""
    return len(password)


def check_lowercase(password):
    """Return True if password has at least one lowercase letter."""
    return any(c.islower() for c in password)


def check_uppercase(password):
    """Return True if password has at least one uppercase letter."""
    return any(c.isupper() for c in password)


def check_digits(password):
    """Return True if password has at least one digit."""
    return any(c.isdigit() for c in password)


def check_symbols(password):
    """Return True if password has at least one symbol."""
    symbols = set(string.punctuation)
    return any(c in symbols for c in password)


def complexity_score(password):
    """Give a complexity score out of 40 (10 points per check)."""
    score = 0
    if check_lowercase(password):
        score += 10
    if check_uppercase(password):
        score += 10
    if check_digits(password):
        score += 10
    if check_symbols(password):
        score += 10
    return score


def calculate_entropy(password):
    """Calculate the entropy (in bits) of the password."""
    pool_size = 0

    if any(c.islower() for c in password):
        pool_size += 26
    if any(c.isupper() for c in password):
        pool_size += 26
    if any(c.isdigit() for c in password):
        pool_size += 10
    if any(c in string.punctuation for c in password):
        pool_size += len(string.punctuation)

    if pool_size == 0 or len(password) == 0:
        return 0

    entropy = len(password) * math.log2(pool_size)
    return round(entropy, 2)


COMMON_PASSWORDS = {
    "admin",
    "password",
    "password123",
    "123456",
    "12345678",
    "qwerty",
    "letmein",
    "welcome",
    "monkey",
    "dragon",
}


def is_common_password(password):
    """Return True if password is in the common passwords list."""
    return password.lower() in COMMON_PASSWORDS


def get_verdict(complexity, entropy, common):
    """Return a verdict string based on all three scoring methods."""
    if common:
        return "Weak"

    entropy_score = min(entropy / 2, 40)

    total = complexity + entropy_score

    if total >= 72:
        return "Very Strong"
    elif total >= 56:
        return "Strong"
    elif total >= 40:
        return "Moderate"
    else:
        return "Weak"


def suggest_improvements(password):
    """Return a list of suggestions based on what the password is missing."""
    suggestions = []

    if len(password) < 8:
        suggestions.append("Make it at least 8 characters long (12+ is better)")

    if not any(c.islower() for c in password):
        suggestions.append("Add lowercase letters (a-z)")

    if not any(c.isupper() for c in password):
        suggestions.append("Add uppercase letters (A-Z)")

    if not any(c.isdigit() for c in password):
        suggestions.append("Add numbers (0-9)")

    if not any(c in string.punctuation for c in password):
        suggestions.append("Add symbols (!@#$%^&* etc.)")

    return suggestions


def generate_suggestion(password):
    """Generate a stronger version of the password as an example."""
    result = password

    if not any(c.islower() for c in result):
        result += "abc"
    if not any(c.isupper() for c in result):
        result += "ABC"
    if not any(c.isdigit() for c in result):
        result += "123"
    if not any(c in string.punctuation for c in result):
        result += "!@#"

    while len(result) < 12:
        result += "X"

    return result


def init_db():
    """Create the database table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            password_hash TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def hash_password(password):
    """Return the SHA-256 hash of a password."""
    return hashlib.sha256(password.encode()).hexdigest()


def has_been_used(password):
    """Return True if this password (by hash) is already in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    h = hash_password(password)
    cursor.execute("SELECT 1 FROM passwords WHERE password_hash = ?", (h,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def store_password(password):
    """Store the hash of this password in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        h = hash_password(password)
        cursor.execute(
            "INSERT INTO passwords (password_hash) VALUES (?)",
            (h,)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # already exists
    finally:
        conn.close()


# --- Main program ---
if __name__ == "__main__":
    init_db()
    pwd = get_password()
    length = check_length(pwd)
    comp = complexity_score(pwd)
    entropy = calculate_entropy(pwd)
    common = is_common_password(pwd)

    print(f"\nPassword length: {length} characters")
    print(f"Complexity score: {comp} / 40")
    print(f"Entropy: {entropy} bits")

    if common:
        print("\nWARNING: This password is in the common password list!")

    if has_been_used(pwd):
        print("\nWARNING: You have used this password before!")

    checks = {
        "Has lowercase": check_lowercase(pwd),
        "Has uppercase": check_uppercase(pwd),
        "Has digits": check_digits(pwd),
        "Has symbols": check_symbols(pwd),
    }

    for name, result in checks.items():
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {name}")

    verdict = get_verdict(comp, entropy, common)
    print(f"\nFinal verdict: {verdict}")

    if verdict in ("Weak", "Moderate"):
        suggestions = suggest_improvements(pwd)
        print("\nSuggestions to make your password stronger:")
        for i, s in enumerate(suggestions, 1):
            print(f"  {i}. {s}")

        example = generate_suggestion(pwd)
        print(f"\nExample of a stronger version: {example}")

    store_password(pwd)
