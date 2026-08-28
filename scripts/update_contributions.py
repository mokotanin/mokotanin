import os
import requests

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