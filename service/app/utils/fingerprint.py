import re
import unicodedata
import hashlib
from models.word import Entry

def _canon_text(s: str) -> str:
    """Return a canonicalized string for hashing.
    - Unicode NFKC normalization (unify width & symbols)
    - Trim leading/trailing whitespace
    - Collapse consecutive whitespace into a single space
    - Lowercase for ASCII letters (language-agnostic, safe for English words)
    """
    # Normalize Unicode (e.g., full-width -> half-width, compatibility forms)
    s = unicodedata.normalize("NFKC", s)
    # Strip leading/trailing whitespace
    s = s.strip()
    # Collapse all whitespace sequences to a single space
    s = re.sub(r"\s+", " ", s)
    # Lowercase (affects Latin letters; Japanese etc. remains unchanged)
    s = s.lower()
    return s

def entry2fingerprint(entry: Entry) -> str:
    """Create a deterministic fingerprint for an Entry.
    Uses BLAKE2b-128 over a versioned, canonical payload.
    """
    parts = [
        _canon_text(entry.word),
        _canon_text(entry.meaning),
        _canon_text(entry.example_sentence),
        _canon_text(entry.example_sentence_translation),
    ]
    # Versioned payload to allow future changes without breaking old items
    payload = "entry:v1\n" + "\n".join(parts)

    # blake2b with 16-byte digest (128-bit) is short & collision-resistant for this use
    digest = hashlib.blake2b(payload.encode("utf-8"), digest_size=16).hexdigest()
    return digest
