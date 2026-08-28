import os
import requests
from datetime import datetime, timedelta, timezone

USERNAME = os.environ["GITHUB_USERNAME"]
TOKEN = os.environ["GITHUB_TOKEN"]

query = """
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

now = datetime.now(timezone.utc)
one_year_ago = now - timedelta(days=365)

variables = {
    "login": USERNAME,
    "from": one_year_ago.isoformat(),
    "to": now.isoformat(),
}

response = requests.post(
    "https://api.github.com/graphql",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    },
    json={
        "query": query,
        "variables": variables,
    },
)

data = response.json()

if "errors" in data:
    print(data["errors"])
    raise SystemExit(1)

total = data["data"]["user"]["contributionsCollection"][
    "contributionCalendar"
]["totalContributions"]

print(f"All-time contributions: {total}")