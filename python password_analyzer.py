import re
import hashlib

# Simulated database for old passwords (hashed)
old_password_hashes = set()

# Common weak passwords list
COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123",
    "password123", "admin", "welcome"
}

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_reuse(password):
    """Check if password was used before"""
    return hash_password(password) in old_password_hashes

def save_password(password):
    """Save password hash to history"""
    old_password_hashes.add(hash_password(password))

def analyze_password(password):
    score = 0
    feedback = []

    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8–12 characters.")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    # Numbers
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Include numbers.")

    # Special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Include special characters.")

    # Common password check
    if password.lower() in COMMON_PASSWORDS:
        feedback.append("This is a very common password.")
        score = 0

    # Reuse check
    if check_reuse(password):
        feedback.append("You have used this password before.")
        score = 0

    # Strength rating
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    elif score <= 6:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return strength, feedback

def suggest_password(password):
    """Generate a stronger suggestion"""
    suggestion = password

    if len(password) < 12:
        suggestion += "@" + str(len(password) * 7)

    if not re.search(r"[A-Z]", suggestion):
        suggestion = suggestion.capitalize()

    if not re.search(r"\d", suggestion):
        suggestion += "9"

    if not re.search(r"[!@#$%^&*]", suggestion):
        suggestion += "#"

    return suggestion


# -------- MAIN PROGRAM --------
if __name__ == "__main__":
    try:
        while True:
            pwd = input("\nEnter a password (or type 'exit'): ")

            if pwd.lower() == "exit":
                print("Exiting program...")
                break

            strength, feedback = analyze_password(pwd)

            print(f"\nStrength: {strength}")

            if feedback:
                print("Suggestions:")
                for f in feedback:
                    print(f"- {f}")
            else:
                print("Great password! 🎉")

            improved = suggest_password(pwd)
            print(f"Suggested stronger password: {improved}")

            save_password(pwd)

    except OSError:
        # Fallback if input() fails
        print("\n⚠ Input not supported. Running test cases instead...\n")

        test_passwords = ["hello", "Password123", "Strong@456"]

        for pwd in test_passwords:
            print(f"\nTesting: {pwd}")

            strength, feedback = analyze_password(pwd)
            print(f"Strength: {strength}")

            if feedback:
                print("Suggestions:")
                for f in feedback:
                    print(f"- {f}")

            improved = suggest_password(pwd)
            print(f"Suggested stronger password: {improved}")

            save_password(pwd)