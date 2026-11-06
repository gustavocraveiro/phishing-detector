import argparse
import sys

from detector.predictor import predict_url


EXIT_COMMANDS = {"q", "quit", "exit"}


def analyze(url):
    """Run the prediction for a single URL and print the result."""
    try:
        result = predict_url(url)
    except ValueError as error:
        print(f"[ERROR] {error}")
        return False

    print(f"\nURL:        {result['url']}")
    print(f"Prediction: {result['prediction']}")

    if result["confidence"] is not None:
        print(f"Confidence: {result['confidence']}%")
    else:
        print(f"Reason:     {result.get('reason', 'N/A')}")
    print()

    return True


def interactive_mode():
    """Prompt for URLs repeatedly until the user quits."""
    print("===== PHISHING DETECTOR =====")
    print("Type a URL to analyze, or 'q' to quit.\n")

    while True:
        try:
            url = input("URL> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if url.lower() in EXIT_COMMANDS:
            break

        if not url:
            continue

        analyze(url)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze URLs and detect potential phishing."
    )
    parser.add_argument(
        "urls",
        nargs="*",
        help="One or more URLs to analyze. If omitted, interactive mode starts."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.urls:
        interactive_mode()
        return 0

    all_ok = True
    for url in args.urls:
        all_ok = analyze(url) and all_ok

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())