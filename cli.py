"""Command-line interface for the Password Strength Checker."""

import getpass
import sys

from .analyzer import analyze_password


def _print_report(report) -> None:
    print("\n" + "=" * 48)
    print("             PASSWORD SECURITY REPORT")
    print("=" * 48)
    print(f"Strength: {report.rating}")
    print(f"Score:    {report.score}/7")
    print("\nSecurity checks:")
    for label, passed in report.checks:
        status = "PASS" if passed else "NEEDS WORK"
        print(f"  [{status:10}] {label}")

    print("\nRecommendations:")
    for item in report.feedback:
        print(f"  - {item}")

    print("\nPrivacy: analysis was performed locally; no password was saved or sent.")
    print("=" * 48)


def main() -> int:
    print("=" * 48)
    print("             PASSWORD STRENGTH CHECKER")
    print("=" * 48)
    print("Your input is hidden and analyzed locally.")
    print("Press Ctrl+C to exit.\n")

    try:
        password = getpass.getpass("Enter a test password: ")
        if not password:
            print("No password entered. Please run the program again.")
            return 1

        report = analyze_password(password)
        _print_report(report)

        # Drop the local reference as soon as practical. Python strings cannot
        # be reliably zeroized, so this is not a secure-memory guarantee.
        password = None
        return 0

    except KeyboardInterrupt:
        print("\nExited safely.")
        return 130
    except (EOFError, OSError) as exc:
        print(f"\nUnable to read hidden input: {exc}", file=sys.stderr)
        print("Run this program in a terminal that supports hidden input.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
