#!/usr/bin/env python3
import requests
import time

# ─── CONFIG ────────────────────────────────────────────────────────────────
GITLAB_URL       = "https://gitlab.com/api/v4"
GITLAB_TOKEN     = "YOUR_GITLAB_TOKEN"        # GitLab PAT with 'api' scope
GITLAB_USERNAME  = "your-username"           # Your GitLab username

GITHUB_API_URL   = "https://api.github.com"
GITHUB_TOKEN     = "YOUR_GITHUB_TOKEN"        # GitHub PAT with 'repo' scope
GITHUB_USERNAME  = "your-username"           # Your GitHub username

HEADERS_GL = { "Private-Token": GITLAB_TOKEN }
HEADERS_GH = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept":        "application/vnd.github.v3+json"
}

# ─── STEP 1: FETCH ALL GITLAB PROJECTS ────────────────────────────────────
def get_gitlab_projects():
    projects, page, per_page = [], 1, 100
    while True:
        r = requests.get(
            f"{GITLAB_URL}/projects",
            headers=HEADERS_GL,
            params={"membership": "true", "page": page, "per_page": per_page}
        )
        if r.status_code != 200:
            raise RuntimeError(f"GitLab fetch error: {r.status_code} {r.text}")
        data = r.json()
        if not data:
            break
        projects.extend(data)
        page += 1
    return projects

# ─── STEP 2: GITHUB REPO HELPERS ───────────────────────────────────────────
def github_repo_exists(name):
    r = requests.get(f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{name}", headers=HEADERS_GH)
    return r.status_code == 200

def create_github_repo(name, private=True):
    payload = {"name": name, "private": private}
    r = requests.post(f"{GITHUB_API_URL}/user/repos", headers=HEADERS_GH, json=payload)
    if r.status_code not in (201, 202):
        raise RuntimeError(f"GitHub create repo failed: {r.status_code} {r.text}")

# ─── STEP 3: TRIGGER GITHUB IMPORT ────────────────────────────────────────
def trigger_import(name, gitlab_http_url, is_private):
    url = f"{GITHUB_API_URL}/repos/{GITHUB_USERNAME}/{name}/import"
    data = {
        "vcs":     "git",
        "vcs_url": gitlab_http_url
    }
    if is_private:
        data["vcs_username"] = GITLAB_USERNAME
        data["vcs_password"] = GITLAB_TOKEN

    r = requests.put(url, headers=HEADERS_GH, json=data)
    if r.status_code not in (201, 202):
        print(f"[!] Import error for '{name}': {r.status_code} {r.text}")
    else:
        print(f"[✓] Import started for '{name}'")

# ─── MAIN ─────────────────────────────────────────────────────────────────
def main():
    print("Fetching GitLab projects…")
    projects = get_gitlab_projects()
    print(f"Found {len(projects)} projects on GitLab.\n")

    for proj in projects:
        name       = proj["path"]
        http_url   = proj["http_url_to_repo"]
        is_private = proj["visibility"] != "public"

        print(f"→ Processing '{name}':", end=" ")

        # 1) ensure GitHub repo exists
        if not github_repo_exists(name):
            print("creating repo…", end=" ")
            create_github_repo(name, private=is_private)
            # GitHub sometimes needs a moment to propagate
            time.sleep(1)
        else:
            print("repo exists…", end=" ")

        # 2) trigger import/mirror
        trigger_import(name, http_url, is_private)
        # optional: throttle imports so you don’t hit rate limits
        time.sleep(0.5)

if __name__ == "__main__":
    main()
