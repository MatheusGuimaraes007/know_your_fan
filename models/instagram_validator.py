import requests
import re

class InstagramValidator:
    def __init__(self):
        self.pattern = re.compile(r"^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{1,28}[^\W]$")
        self.banned_words = ["admin", "furiaoficial", "support"]

    def validate(self, username):
        if not username:
            return False
        username = username.replace("@", "").strip().lower()
        if not self.pattern.match(username):
            return False
        if any(banned in username for banned in self.banned_words):
            return False

        try:
            response = requests.get(f"https://www.instagram.com/{username}/", timeout=5)
            return response.status_code == 200
        except:
            return False