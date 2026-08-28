import os
import re
import requests
from datetime import datetime, timezone, timedelta
import time

USERNAME = os.environ["GITHUB_USERNAME"]
TOKEN = os.environ["GITHUB_TOKEN"]
CACHE_FILE = "counter_cache.txt"

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

def load_cache():
    """Charge le total et la dernière date depuis le cache."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            lines = f.read().strip().splitlines()
            if len(lines) >= 2:
                try:
                    total = int(lines[0])
                    last_date = lines[1]
                    print(f"📂 Cache trouvé : total={total}, dernière date={last_date}")
                    return total, last_date
                except:
                    pass
    print("📂 Pas de cache valide, on part de zéro.")
    return 0, "2008-01-01T00:00:00Z"

def save_cache(total, last_date):
    """Sauvegarde le total et la date dans le cache."""
    with open(CACHE_FILE, "w") as f:
        f.write(f"{total}\n{last_date}")

# --- 1. Charger l'état précédent ---
total_so_far, last_run = load_cache()

# On décale d'1 seconde pour ne pas recalculer le dernier commit
last_run_dt = datetime.fromisoformat(last_run.replace("Z", "+00:00"))
# On ajoute 1 seconde pour être sûr de ne pas reprendre le même commit
new_since = (last_run_dt + timedelta(seconds=1)).isoformat().replace("+00:00", "Z")
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

print(f"🔍 Recherche des commits depuis {new_since} jusqu'à {now}")

# --- 2. Récupérer TOUS les dépôts (une seule fois, on garde la liste) ---
repos = []
cursor = None
has_next = True

print("📡 Récupération de tous vos dépôts...")
while has_next:
    repo_query = """
    query($login: String!, $cursor: String) {
      user(login: $login) {
        repositories(first: 100, after: $cursor, ownerAffiliations: OWNER, isFork: false) {
          pageInfo { hasNextPage endCursor }
          nodes { name owner { login } }
        }
      }
    }
    """
    variables = {"login": USERNAME, "cursor": cursor}
    try:
        data = graphql_request(repo_query, variables)
        page = data["user"]["repositories"]
        for repo in page["nodes"]:
            repos.append(f"{repo['owner']['login']}/{repo['name']}")
        has_next = page["pageInfo"]["hasNextPage"]
        cursor = page["pageInfo"]["endCursor"]
        time.sleep(0.05)
    except Exception as e:
        print(f"⚠️ Erreur dépôts : {e}")
        break

print(f"📦 {len(repos)} dépôt(s) trouvé(s).")

# --- 3. Pour chaque dépôt, récupérer UNIQUEMENT les nouveaux commits ---
new_lines = 0

commit_query = """
query($owner: String!, $repo: String!, $from: GitTimestamp!, $to: GitTimestamp!, $cursor: String) {
  repository(owner: $owner, name: $repo) {
    defaultBranchRef {
      target {
        ... on Commit {
          history(since: $from, until: $to, first: 100, after: $cursor) {
            pageInfo { hasNextPage endCursor }
            nodes { additions deletions }
          }
        }
      }
    }
  }
}
"""

for repo_full in repos:
    owner, repo_name = repo_full.split("/")
    cursor_commit = None
    has_next_commit = True
    repo_new_lines = 0

    while has_next_commit:
        variables = {
            "owner": owner,
            "repo": repo_name,
            "from": new_since,
            "to": now,
            "cursor": cursor_commit,
        }
        try:
            data = graphql_request(commit_query, variables)
            history = data["repository"]["defaultBranchRef"]["target"]["history"]
            for node in history["nodes"]:
                # 🔥 On compte seulement les AJOUTS (pas les suppressions)
                repo_new_lines += node["additions"]
            has_next_commit = history["pageInfo"]["hasNextPage"]
            cursor_commit = history["pageInfo"]["endCursor"]
            time.sleep(0.1)
        except Exception as e:
            print(f"  ⚠️ Erreur sur {repo_full} : {e}")
            break

    if repo_new_lines > 0:
        print(f"  ➕ {repo_new_lines} nouvelles lignes ajoutées dans {repo_full}")
    new_lines += repo_new_lines

# --- 4. Mettre à jour le total et le cache ---
new_total = total_so_far + new_lines
print(f"✅ Ancien total : {total_so_far}")
print(f"✅ Nouvelles lignes : {new_lines}")
print(f"✅ Nouveau total : {new_total}")

save_cache(new_total, now)

# --- 5. Mettre à jour le README ---
digits = str(new_total)
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

print("✅ README.md mis à jour avec le compteur incrémentiel !")