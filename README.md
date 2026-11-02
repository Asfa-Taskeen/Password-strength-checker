# Password Strength Checker

A Python cybersecurity portfolio project with a terminal interface and a desktop GUI. It evaluates password length, character diversity, common-password matches, repeated characters, and predictable sequences, then provides actionable feedback.

> **Important:** This project uses a transparent educational heuristic. It is not a password-cracking simulator, a breach database lookup, or a guarantee that a password is secure. For production systems, use a vetted password-strength estimator and follow current authentication guidance.

## Features

- Desktop GUI with live assessment, show/hide control, score meter, checklist, and recommendations.
- Command-line interface with hidden password entry.
- Length and character-class checks.
- Detection of a small, bundled list of common passwords.
- Basic detection of repeated characters and predictable sequences.
- Local-only analysis: no network requests and no password file/database.
- Automated unit tests using Python's standard library.

## Requirements

- Python 3.9 or newer.
- Tkinter (included with most standard Windows Python installations).
- No third-party Python packages.

## Run the desktop application

Open a terminal in the repository root and run:

```bash
python -m password_checker.gui
```

On some systems, use `python3` instead of `python`.

## Run the command-line application

```bash
python -m password_checker
```

The CLI hides typed input. The GUI updates its assessment as you type. Use a made-up test password; do not enter a password you currently use for an important account.

## Run tests

```bash
python -m unittest discover -v
```

## Project structure

```text
password-strength-checker/
├── password_checker/
│   ├── __init__.py
│   ├── __main__.py
│   ├── analyzer.py
│   ├── cli.py
│   └── gui.py
├── tests/
│   ├── __init__.py
│   └── test_analyzer.py
├── .gitignore
├── LICENSE
└── README.md
```

## How the scoring works

The analyzer assigns points for password length and the presence of lowercase letters, uppercase letters, digits, and symbols. It applies penalties for selected predictable patterns and checks a small local list of commonly used passwords. The final score is capped at 7.

| Score | Rating |
|---:|---|
| 0–2 | Weak |
| 3–5 | Moderate |
| 6 | Strong |
| 7 | Very Strong |

This is a demonstration model, not a formal entropy calculation. It does not account for every dictionary, personal-information pattern, password reuse, or attacker strategy.

## Privacy and safe use

- The application does not write the entered password to disk.
- The application does not send the password over the network.
- The CLI uses `getpass` to hide typed input in a supported terminal.
- The GUI includes a show/hide control; the password remains visible in the local application only when that option is enabled.
- Python strings cannot be reliably zeroized from memory; this project does not claim secure-memory handling.
- The bundled common-password list is intentionally small and is not comprehensive.
- Use only fictional test passwords while demonstrating the project.

## Future improvements

- Replace the heuristic with a vetted estimator such as zxcvbn.
- Add localization and accessibility improvements.
- Package the desktop application as a Windows executable.
- Add continuous integration and expanded test coverage.

## Author

**Your Name** — Computer Science / Cybersecurity Portfolio Project

Update this section with your preferred name and portfolio links before publishing.
