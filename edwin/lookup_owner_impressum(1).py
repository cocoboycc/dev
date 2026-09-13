
import json
import re
import time
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

GENERIC_PROVIDERS = {
    "t-online.de", "web.de", "gmx.de", "gmx.net", "aol.com", "yahoo.de",
    "yahoo.com", "gmail.com", "googlemail.com", "freenet.de", "arcor.de",
    "online.de", "hotmail.com", "hotmail.de", "email.de", "outlook.de",
    "outlook.com", "icloud.com", "live.de", "mail.de",
}

IMPRESSUM_PATHS = ["/impressum", "/impressum/", "/impressum.html", "/kontakt", "/imprint"]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; GymOwnerLookup/1.0)"}

OWNER_PATTERNS = [
    r"Verantwortlich für den Inhalt.*?:\s*([A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß\.\-]+)",
    r"Inhaber(?:in)?\s*:?\s*([A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß\.\-]+)",
    r"Geschäftsführer(?:in)?\s*:?\s*([A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß\.\-]+)",
    r"Vertreten durch\s*:?\s*([A-ZÄÖÜ][a-zäöüß]+\s+[A-ZÄÖÜ][a-zäöüß\.\-]+)",
]


def get_company_domain(email):
    """Domain zurückgeben, außer sie gehört zu einem generischen Anbieter."""
    if not email or "@" not in email:
        return None
    domain = email.split("@")[1].lower().strip()
    return None if domain in GENERIC_PROVIDERS else domain


def is_allowed_by_robots(url):
    """robots.txt der Seite respektieren, bevor wir sie abrufen.
    RobotFileParser.read() kennt selbst keinen Timeout-Parameter, daher
    holen wir die robots.txt manuell mit requests (das hat einen) und
    füttern den Text erst danach in den Parser."""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()
    try:
        resp = requests.get(robots_url, headers=HEADERS, timeout=5)
        if resp.status_code != 200:
            return True  # keine robots.txt -> Zugriff gilt als erlaubt
        rp.parse(resp.text.splitlines())
        return rp.can_fetch(HEADERS["User-Agent"], url)
    except requests.RequestException:
        return True  # nicht erreichbar -> Zugriff gilt als erlaubt


def find_impressum_text(domain):
    """Probiert bekannte Impressum-Pfade und gibt den reinen Text der
    ersten erreichbaren Seite zurück (oder None)."""
    for scheme in ["https://", "http://"]:
        for path in IMPRESSUM_PATHS:
            url = scheme + domain + path
            if not is_allowed_by_robots(url):
                continue
            try:
                resp = requests.get(url, headers=HEADERS, timeout=5)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    return soup.get_text(separator=" ")
            except requests.RequestException:
                continue
    return None


def extract_owner_from_text(text):
    for pattern in OWNER_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None


def lookup_owner(gym):
    """Für ein einzelnes Gym-Dict den Owner nachschlagen."""
    domain = get_company_domain(gym.get("email"))
    if not domain:
        return None

    text = find_impressum_text(domain)
    if not text:
        return None

    return extract_owner_from_text(text)


def main():
    with open("gyms_final.json", "r", encoding="utf-8") as f:
        gyms = json.load(f)

    to_process = [g for g in gyms if g["owner"] is None]
    print(f"{len(to_process)} Gyms ohne Owner werden durchsucht...")

    found = 0
    for i, gym in enumerate(to_process):
        owner = lookup_owner(gym)
        if owner:
            gym["owner"] = owner
            found += 1

        #if i % 50 == 0:
        print(f"{i}/{len(to_process)} bearbeitet, {found} Owner gefunden")

        time.sleep(1)  # höflich sein - nicht zu schnell hintereinander anfragen

    with open("gyms_final_enriched.json", "w", encoding="utf-8") as f:
        json.dump(gyms, f, ensure_ascii=False, indent=2)

    print(f"\nFertig! {found} neue Owner gefunden.")


if __name__ == "__main__":
    main()
