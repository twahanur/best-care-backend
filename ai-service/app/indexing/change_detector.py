"""
Content Hashing and Database Change Detector.
Prevents redundant embedding generation when database records are updated with unchanged semantic content.
"""
import hashlib

class ChangeDetector:
    @staticmethod
    def compute_hash(text: str) -> str:
        """
        Compute MD5 hash of canonical text content.
        """
        normalized_text = " ".join(text.strip().split())
        return hashlib.md5(normalized_text.encode("utf-8")).hexdigest()

    @classmethod
    def has_changed(cls, existing_hash: str, new_text: str) -> bool:
        """
        Returns True if content has materially changed and requires re-indexing.
        """
        new_hash = cls.compute_hash(new_text)
        return existing_hash != new_hash
