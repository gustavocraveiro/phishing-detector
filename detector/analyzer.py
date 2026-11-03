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


def extract_features(url):

    url = str(url).strip()
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
        "has_https": int(urlsplit(url).scheme.lower() == "https"),
        "has_ip": has_ip,
        "has_suspicious_words": has_suspicious_words,
        "special_char_count": len(re.findall(r"[^a-zA-Z0-9]", url))
    }

    return features
