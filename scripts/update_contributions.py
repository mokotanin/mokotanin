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

# ─────────────────────────────────────────
# Update Cat Girl Counter in README
# ─────────────────────────────────────────

README = "README.md"

with open(README, "r", encoding="utf-8") as f:
    content = f.read()

pattern = r'(<cat-girl-counter\s+count=")\d+("></cat-girl-counter>)'

new_content, replacements = re.subn(
    pattern,
    rf"\g<1>{total}\g<2>",
    content,
)

if replacements == 0:
    print("Cat Girl Counter not found in README.")
else:
    with open(README, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Cat Girl Counter updated to {total}.")