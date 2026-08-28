import os
import requests
from datetime import datetime, timezone

USERNAME = os.environ["GITHUB_USERNAME"]
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""

now = datetime.now(timezone.utc)

# GitHub's "last year" calendar starts 1 year ago
# but we use the calendar dates themselves rather than
# simply summing API contribution types.
from_date = now.replace(year=now.year - 1)

variables = {
    "login": USERNAME,
    "from": from_date.isoformat(),
    "to": now.isoformat(),
}

response = requests.post(
    "https://api.github.com/graphql",
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    },
    json={
        "query": QUERY,
        "variables": variables,
    },
)

response.raise_for_status()
data = response.json()

if "errors" in data:
    print("GitHub GraphQL error:")
    print(data["errors"])
    raise SystemExit(1)

calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]

total = calendar["totalContributions"]

print(f"All-time contributions: {total}")