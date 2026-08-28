import os
import re
import requests
from datetime import datetime, timezone
import time

USERNAME = os.environ["GITHUB_USERNAME"]
TOKEN = os.environ["GITHUB_TOKEN"]

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

def graphql_request(query, variables):
    """Fait une requête GraphQL et gère les erreurs."""
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers,
    )
    response.raise_for_status()
    data = response.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]

# --- 1. Récupérer tous les dépôts où vous avez commité ---
repo_query = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      commitContributionsByRepository(maxRepositories: 100) {
        repository {
          name
          owner { login }
        }
      }
    }
  }
}
"""

from_date = "2008-01-01T00:00:00Z"
to_date = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

data = graphql_request(repo_query, {
    "login": USERNAME,
    "from": from_date,
    "to": to_date,
})

repos = []
for entry in data["user"]["contributionsCollection"]["commitContributionsByRepository"]:
    repo = entry["repository"]
    repos.append(f"{repo['owner']['login']}/{repo['name']}")

print(f"📦 {len(repos)} dépôt(s) trouvé(s) à analyser.")

# --- 2. Pour chaque dépôt, récupérer tous vos commits et additionner les lignes ---
total_lines = 0

commit_query = """
query($owner: String!, $repo: String!, $from: GitTimestamp!, $to: GitTimestamp!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    defaultBranchRef {
      target {
        ... on Commit {
          history(since: $from, until: $to, first: 100, after: $cursor) {
            pageInfo {
              hasNextPage
              endCursor
            }
            nodes {
              additions
              deletions
            }
          }
        }
      }
    }
  }
}
"""

for repo_full in repos:
    owner, repo_name = repo_full.split("/")
    print(f"🔍 Analyse de {repo_full}...")
    
    cursor = None
    has_next = True
    repo_lines = 0

    while has_next:
        variables = {
            "owner": owner,
            "repo": repo_name,
            "from": from_date,
            "to": to_date,
            "cursor": cursor,
        }
        try:
            data = graphql_request(commit_query, variables)
            history = data["repository"]["defaultBranchRef"]["target"]["history"]
            
            for node in history["nodes"]:
                repo_lines += node["additions"] + node["deletions"]
            
            has_next = history["pageInfo"]["hasNextPage"]
            cursor = history["pageInfo"]["endCursor"]
            time.sleep(0.1)  # Éviter de saturer l'API
        except Exception as e:
            print(f"  ⚠️ Erreur sur {repo_full} : {e}")
            break

    total_lines += repo_lines
    print(f"  ➕ Lignes pour {repo_full} : {repo_lines}")

print(f"✅ Total des lignes modifiées (additions + suppressions) : {total_lines}")

# --- 3. Générer les GIFs et mettre à jour README ---
digits = str(total_lines)

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

pattern = r"<!-- CONTRIBUTIONS:START -->.*?<!-- CONTRIBUTIONS:END -->"
readme = re.sub(pattern, content, readme, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)

print("✅ README.md mis à jour avec le nouveau compteur de lignes !")