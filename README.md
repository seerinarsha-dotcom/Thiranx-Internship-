# Password Strength Analyzer

A Python CLI tool that evaluates the strength of user-entered passwords.

Built as part of a Thiranex internship task. Follows the approach from a
Venlovo Academy Python password security tutorial.

---

## What it checks

| Check | Description |
|---|---|
| Length | Character count of the password |
| Complexity | Lowercase, uppercase, digits, and symbols |
| Entropy | Bits of unpredictability based on pool size and length |
| Common password list | Flags passwords found in a built-in list of weak passwords |
| Password reuse | Stores SHA-256 hashes in SQLite and warns if the same password is entered again |

## Verdict

The script combines complexity and entropy into a total score and returns one of:

- **Very Strong**
- **Strong**
- **Moderate**
- **Weak**

If the password is common, the verdict is automatically **Weak**.

## Suggestions

For **Weak** and **Moderate** passwords, the script prints:

- A numbered list of what the password is missing
- An example of a stronger version built from the same password

## Requirements

- Python 3.11 or newer
- No external packages — only the standard library (`string`, `math`, `hashlib`, `sqlite3`)

## How to run

```bash
py password_checker.py
```

On Windows with the Python launcher:

```powershell
py password_checker.py
```

Type a password when prompted. The script will print the analysis and verdict.

## Example output

```
Enter a password to check: Pass@1234

Password length: 9 characters
Complexity score: 40 / 40
Entropy: 58.99 bits
  [PASS] Has lowercase
  [PASS] Has uppercase
  [PASS] Has digits
  [PASS] Has symbols

Final verdict: Strong
```

If you enter the same password again:

```
Enter a password to check: Pass@1234

Password length: 9 characters
Complexity score: 40 / 40
Entropy: 58.99 bits

WARNING: You have used this password before!
  [PASS] Has lowercase
  [PASS] Has uppercase
  [PASS] Has digits
  [PASS] Has symbols

Final verdict: Strong
```

For a weak password such as `admin`:

```
Enter a password to check: admin

Password length: 5 characters
Complexity score: 10 / 40
Entropy: 23.5 bits

WARNING: This password is in the common password list!

  [PASS] Has lowercase
  [FAIL] Has uppercase
  [FAIL] Has digits
  [FAIL] Has symbols

Final verdict: Weak

Suggestions to make your password stronger:
  1. Make it at least 8 characters long (12+ is better)
  2. Add uppercase letters (A-Z)
  3. Add numbers (0-9)
  4. Add symbols (!@#$%^&* etc.)

Example of a stronger version: adminABC123!@#
```

## Files

| File | Purpose |
|---|---|
| `password_checker.py` | Main password checker script |
| `password_history.db` | Local SQLite database that stores password hashes to detect reuse (created automatically, not committed) |

The `password_history.db` file stays local and is **not** committed to the repository.

## Optional feature

The task mentioned an optional database integration to prevent reuse of old
passwords. This version implements that using SQLite and SHA-256 hashing, so
the database never stores the actual password text — only the hash.

## Author

Arsha — cybersecurity student
- GitHub: https://github.com/seerinarsha-dotcom
- Email: seerinarsha@gmail.com
