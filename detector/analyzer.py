from urllib.parse import urlsplit
import ipaddress
import re
import tldextract


FEATURE_COLUMNS = [
    "url_length",
    "domain_length",
    "path_length",
    "dot_count",
    "hyphen_count",
    "at_count",
    "digit_count",
    "subdomain_count",
    "has_https",
    "has_ip",
    "has_suspicious_words",
    "special_char_count"
]

extractor = tldextract.TLDExtract(suffix_list_urls=())

SUSPICIOUS_WORDS = [
    "login",
    "verify",
    "update",
    "secure",
    "account",
    "banking",
    "password",
    "signin",
    "confirm",
    "wallet"
]


def validate_url(url):
    if not isinstance(url, str):
        return False

    url = url.strip()

    if not url or any(char.isspace() for char in url):
        return False

    try:
        parsed = urlsplit(url if "://" in url else f"//{url}")

        if "://" in url and parsed.scheme.lower() not in ("http", "https"):
            return False

        hostname = parsed.hostname

        if not hostname or len(hostname) > 253:
            return False

        # Validate port syntax and range
        try:
            parsed.port
        except ValueError:
            return False

        # Accept valid IP addresses
        try:
            ipaddress.ip_address(hostname)
            return True
        except ValueError:
            pass

        # Validate domain labels
        if "." not in hostname:
            return False

        labels = hostname.split(".")

        for label in labels:
            if not label or len(label) > 63:
                return False

            if label.startswith("-") or label.endswith("-"):
                return False

            if not re.fullmatch(r"[a-zA-Z0-9-]+", label):
                return False

        return True

    except ValueError:
        return False


def extract_features(url):

    if not validate_url(url):
        raise ValueError("Invalid URL provided.")

    url = url.strip()
    parsed = urlsplit(url if "://" in url else f"//{url}")

    hostname = parsed.hostname or ""
    domain = hostname.lower()
    path = parsed.path

    try:
        ipaddress.ip_address(domain)
        has_ip = 1
    except ValueError:
        has_ip = 0

    extracted = extractor(domain)

    subdomain_count = (
        len(extracted.subdomain.split("."))
        if extracted.subdomain and not has_ip
        else 0
    )

    has_suspicious_words = int(
        any(word in url.lower() for word in SUSPICIOUS_WORDS)
    )

    features = {
        "url_length": len(url),
        "domain_length": len(domain),
        "path_length": len(path),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "at_count": url.count("@"),
        "digit_count": sum(char.isdigit() for char in url),
        "subdomain_count": subdomain_count,
        "has_https": int(parsed.scheme.lower() == "https"),
        "has_ip": has_ip,
        "has_suspicious_words": has_suspicious_words,
        "special_char_count": len(re.findall(r"[^a-zA-Z0-9]", url))
    }

    return features
