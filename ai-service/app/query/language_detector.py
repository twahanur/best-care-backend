import re

class LanguageDetector:
    @staticmethod
    def detect(text: str) -> str:
        """
        Detects if input is Bengali script ('bangla'), Banglish ('banglish'), or English ('english').
        """
        if not text:
            return "english"

        # Check for Bengali Unicode character block (U+0980 to U+09FF)
        if re.search(r"[\u0980-\u09ff]", text):
            return "bangla"

        # Check for characteristic Banglish tokens & suffixes
        banglish_markers = [
            "gari", "gaari", "lagbe", "koto", "bhara", "jonno", "koro", "korbo", "hobe",
            "ache", "dekhao", "amader", "amar", "tarik", "agamikal", "kalke", "poroshu",
            "sokal", "bikal", "shondha", "raat", "tay", "te", "theke", "jabo", "thik",
            "haan", "na", "bhalo", "diner", "khoroch", "pabo", "dibo", "chai", "dorkar",
            "kothay", "ekta", "duita", "tinta", "sonadanga", "sajek", "bandarban"
        ]

        text_lower = text.lower()
        tokens = set(re.findall(r"\b[a-z]{2,}\b", text_lower))
        matching_count = sum(1 for marker in banglish_markers if marker in tokens or marker in text_lower)

        if matching_count >= 1:
            return "banglish"

        return "english"

language_detector = LanguageDetector()
