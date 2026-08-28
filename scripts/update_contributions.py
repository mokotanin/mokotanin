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

# --- 1. Récupérer tous les dépôts où vous avez commité, en itérant par année ---
current_year = datetime.now().year
start_year = 2008  # année de création de GitHub

repo_set = set()

for year in range(start_year, current_year + 1):
    from_date = f"{year}-01-01T00:00:00Z"
    to_date = f"{year}-12-31T23:59:59Z"
    
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
    
    try:
        data = graphql_request(repo_query, {
            "login": USERNAME,
            "from": from_date,
            "to": to_date,
        })
        for entry in data["user"]["contributionsCollection"]["commitContributionsByRepository"]:
            repo = entry["repository"]
            repo_set.add(f"{repo['owner']['login']}/{repo['name']}")
    except Exception as e:
        print(f"⚠️ Erreur pour l'année {year} : {e}")

print(f"📦 {len(repo_set)} dépôt(s) trouvé(s) à analyser.")

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

from_date_all = "2008-01-01T00:00:00Z"
to_date_all = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

for repo_full in repo_set:
    owner, repo_name = repo_full.split("/")
    print(f"🔍 Analyse de {repo_full}...")
    
    cursor = None
    has_next = True
    repo_lines = 0

    while has_next:
        variables = {
            "owner": owner,
            "repo": repo_name,
            "from": from_date_all,
            "to": to_date_all,
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