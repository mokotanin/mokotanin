import os
import requests
import re

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

for year in range(2010, 2027):
    variables = {
        "login": USERNAME,
        "from": f"{year}-01-01T00:00:00Z",
        "to": f"{year + 1}-01-01T00:00:00Z",
    }

    response = requests.post(
        "https://api.github.com/graphql",
        headers=headers,
        json={
            "query": QUERY,
            "variables": variables,
        },
    )

    data = response.json()

    if "errors" in data:
        print(f"{year}: ERROR")
        print(data["errors"])
        continue

    count = data["data"]["user"]["contributionsCollection"][
        "contributionCalendar"
    ]["totalContributions"]

    print(f"{year}: {count}")
    total += count

print("----------------")
print(f"TOTAL: {total}")

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

readme = re.sub(
    r"<!-- CONTRIBUTIONS:START -->.*?<!-- CONTRIBUTIONS:END -->",
    content,
    readme,
    flags=re.DOTALL,
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)