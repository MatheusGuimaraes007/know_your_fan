# models/profile_links_validator.py
import requests

class ProfileLinksValidator:
    def __init__(self):
        self.domains = {
            "csgo": [
                "hltv.org",
                "faceit.com",
                "esportal.com",
                "steamcommunity.com",
                "csgo-stats.com",
                "csgostats.gg",
                "scope.gg",
                "leetify.com",
                "aimlab.com"
            ],
            "valorant": [
                "tracker.gg",
                "valorant.op.gg",
                "dak.gg",
                "blitz.gg",
                "mobalytics.gg",
                "aimlab.com"
            ],
            "lol": [
                "op.gg",
                "lolpros.gg",
                "u.gg",
                "leagueofgraphs.com",
                "mobalytics.gg",
                "porofessor.gg"
            ],
            "fps_genérico": [
                "tracker.gg",
                "blitz.gg",
                "overwolf.com",
                "fortnitetracker.com",
                "cod.tracker.gg",
                "apex.tracker.gg",
                "r6.tracker.gg"
            ],
            "multijogos": [
                "liquipedia.net",
                "esports.espn.com",
                "esportscharts.com",
                "gamerzclass.com"
            ],
            "social": [
                "twitter.com",
                "twitch.tv",
                "youtube.com",
                "kick.com",
                "discord.gg",
                "instagram.com"
            ]
        }

    def validate(self, links):
        all_domains = [d for sublist in self.domains.values() for d in sublist]
        valid_links = []
        for link in links:
            if not link.startswith("http"):
                link = "https://" + link
            for domain in all_domains:
                if domain in link:
                    try:
                        response = requests.get(link, timeout=5)
                        if response.status_code == 200:
                            valid_links.append(link)
                            break
                    except:
                        continue
        return valid_links
