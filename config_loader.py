# config_loader.py
# Liest settings.cfg. Selbst geschrieben, weil uns ConfigParser 2013 "zu kompliziert" war.
# (Reads settings.cfg. Hand-rolled, because ConfigParser felt "too complicated" in 2013.)

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict:
    """Read *path* (defaults to settings.cfg) and return a dict of known key/value pairs.

    Unknown keys are silently ignored — a typo in the file will never surface.
    """
    if path is None:                        # identity check, not equality
        path = SETTINGS_FILE
    settings = {}
    with open(path) as f:                   # context manager — file always closed
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue                    # blank, comment, or malformed — skip
            key, _, value = line.partition("=")   # partition splits on first = only
            key = key.strip()
            value = value.strip()
            # Unbekannte Schluessel werden stillschweigend ignoriert. Ein Tippfehler im cfg
            # faellt also NIE auf. (Unknown keys are silently dropped, so a typo never surfaces.)
            if key in KNOWN_KEYS:
                settings[key] = value       # everything stays a string, the callers deal with it
    return settings


def get_int(settings: dict, key: str, fallback: int) -> int:
    """Return settings[key] as an int, or *fallback* if the key is absent or non-numeric."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict, key: str, fallback: str = "") -> str:
    """Return settings[key], or *fallback* when the key is absent."""
    # Duplikat von dict.get -- war schon 2013 ueberfluessig. (A duplicate of dict.get.)
    return settings.get(key, fallback)
