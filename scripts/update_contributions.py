import os
import re
import requests
from datetime import datetime

USERNAME = os.environ["GITHUB_USERNAME"]
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

total = 0
current_year = datetime.now().year

for year in range(2008, current_year + 1):
    variables = {
        "login": USERNAME,
        "from": f"{year}-01-01T00:00:00Z",
        "to": f"{year}-12-31T23:59:59Z",
    }

    response = requests.post(
        "https://api.github.com/graphql",
        json={
            "query": QUERY,
            "variables": variables,
        },
        headers=headers,
    )

    response.raise_for_status()
    data = response.json()

    if "errors" in data:
        raise RuntimeError(data["errors"])

    total += data["data"]["user"]["contributionsCollection"][
        "contributionCalendar"
    ]["totalContributions"]

print(f"All-time contributions: {total}")

# Génère les GIFs correspondant à chaque chiffre
digits = str(total)

images = "\n".join(
    f'<img src="./counter-images/{digit}.gif" alt="{digit}">'
    for digit in digits
)

content = f"""<!-- CONTRIBUTIONS:START -->
<p align="center">
{images}
</p>
<!-- CONTRIBUTIONS:END -->"""

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

# Remplace uniquement le bloc entre les marqueurs
pattern = r"<!-- CONTRIBUTIONS:START -->.*?<!-- CONTRIBUTIONS:END -->"

readme = re.sub(
    pattern,
    content,
    readme,
    flags=re.DOTALL,
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)
