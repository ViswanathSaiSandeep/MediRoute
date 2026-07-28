"""
Security scan — detects hardcoded API keys and secrets in the codebase.
Runs during CI to prevent accidental credential leaks.
"""

import os
import re
import sys

# Ensure UTF-8 output encoding for Windows compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Patterns that indicate a hardcoded API key or secret
PATTERNS = [
    # Google API key (actual keys start with AIzaSy)
    (r'AIzaSy[A-Za-z0-9_-]{33}', "Google API Key"),
    # OpenAI key
    (r'sk-[A-Za-z0-9]{48}', "OpenAI API Key"),
    # Firebase specific patterns (actual keys, not placeholders)
    (r'(?<!YOUR_)(?<!placeholder)apiKey:\s*["\'][A-Za-z0-9_-]{30,}["\']', "Firebase API Key"),
    # Generic secret patterns with actual values
    (r'(?:api_key|apikey|secret|password|token)\s*[:=]\s*["\'][A-Za-z0-9+/=_-]{20,}["\']', "Potential Secret"),
    # AWS access key
    (r'AKIA[A-Z0-9]{16}', "AWS Access Key"),
    # Private key
    (r'-----BEGIN\s+(RSA |EC |DSA )?PRIVATE KEY-----', "Private Key"),
]

# Files/directories to skip
SKIP_DIRS = {
    '.git', 'node_modules', '__pycache__', '.dart_tool',
    'build', '.pub-cache', '.pub', '.idea', 'venv', '.venv',
}

SKIP_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg',
    '.woff', '.woff2', '.ttf', '.eot',
    '.zip', '.tar', '.gz', '.jar',
    '.lock', '.pyc', '.class',
}

# Known safe patterns (placeholders, not real keys)
SAFE_PATTERNS = [
    'YOUR_FIREBASE_API_KEY',
    'YOUR_GOOGLE_MAPS_API_KEY',
    'YOUR_API_KEY',
    'PLACEHOLDER',
    'String.fromEnvironment',
    'secrets.',
    'os.environ',
    'process.env',
]


def scan_for_secrets(root_dir: str = ".") -> list[str]:
    """Scan the codebase for hardcoded secrets. Returns list of issues found."""
    issues = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in SKIP_EXTENSIONS:
                continue

            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)

            # Skip .env files (they should be gitignored)
            if filename.endswith('.env') or filename.endswith('.env.local'):
                continue

            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except (OSError, IOError):
                continue

            for pattern, description in PATTERNS:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Get the line containing the match
                    line_start = content.rfind('\n', 0, match.start()) + 1
                    line_end = content.find('\n', match.end())
                    if line_end == -1:
                        line_end = len(content)
                    line_content = content[line_start:line_end].strip()

                    # Check if it's a safe pattern (placeholder, env var, etc.)
                    is_safe = any(safe in line_content for safe in SAFE_PATTERNS)
                    if is_safe:
                        continue

                    # Calculate line number
                    line_num = content[:match.start()].count('\n') + 1

                    issues.append(
                        f"[WARN] {description} in {rel_path}:{line_num} — "
                        f"'{line_content[:80]}...'" if len(line_content) > 80
                        else f"[WARN] {description} in {rel_path}:{line_num} — '{line_content}'"
                    )

    return issues


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    issues = scan_for_secrets(root)
    if issues:
        print("[FAIL] SECURITY ISSUES DETECTED:")
        for issue in issues:
            print(f"  {issue}")
        sys.exit(1)
    else:
        print("[PASS] No hardcoded API keys or secrets detected.")
