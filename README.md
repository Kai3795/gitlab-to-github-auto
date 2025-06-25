# GitLab to GitHub Auto Update
#### Author: Bocaletto Luca

**GitLab to GitHub Auto Update** is a Python tool that automates the import and synchronization of all your GitLab projects into GitHub. It will:

1. Fetch every project you’re a member of on GitLab.  
2. Create a matching GitHub repo if it doesn’t already exist.  
3. Invoke GitHub’s “Import Repository” API to pull from GitLab (using your GitLab credentials for private repos).

Ideal if you manage hundreds of repos and want a hands-free mirror on GitHub!

---

## Table of Contents

- [Features](#features)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Usage](#usage)  
- [How It Works](#how-it-works)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- **Bulk Sync:** Loops through all your GitLab projects in one go.  
- **Auto-Create:** Creates GitHub repos on demand (public or private).  
- **Seamless Imports:** Kicks off GitHub’s official Import API for mirroring.  
- **Handles Privacy:** Passes your GitLab token when importing private repos.  

---

## Requirements

- **Python 3.6+**  
- **`requests` library**  
  ```bash
  pip install requests
  ```
- **GitLab Personal Access Token** with **`api`** scope  
- **GitHub Personal Access Token** with **`repo`** scope  

---

## Installation

1. **Clone this repository**  
   ```bash
   git clone https://gitlab.com/bocaletto-luca/gitlab-to-github-auto.git
   cd gitlab-to-github-auto
   ```

2. **(Optional) Create & activate a virtual env**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**  
   ```bash
   pip install requests
   ```

---

## Configuration

Open `gitlab_to_github_auto_update.py` and set:

```python
# GitLab settings
GITLAB_URL      = "https://gitlab.com/api/v4"
GITLAB_TOKEN    = "your_gitlab_token_here"
GITLAB_USERNAME = "your-username"

# GitHub settings
GITHUB_API_URL  = "https://api.github.com"
GITHUB_TOKEN    = "your_github_token_here"
GITHUB_USERNAME = "your-username"
```

> **Security Note:**  
> Never commit your tokens in plaintext. Use environment variables or a `.env` file (excluded via `.gitignore`).

---

## Usage

Make the script executable and run:

```bash
chmod +x gitlab_to_github_auto_update.py
./gitlab_to_github_auto_update.py
```

Or simply:

```bash
python3 gitlab_to_github_auto_update.py
```

You’ll see console output for each project—whether it was created or already existed, and the status of the import trigger.

---

## How It Works

1. **Fetch Projects**  
   Requests `/projects?membership=true` on GitLab, handling pagination.  

2. **Check/Create on GitHub**  
   For each project name, checks `GET /repos/{user}/{project}`. Creates via `POST /user/repos` if missing.

3. **Trigger Import**  
   Calls `PUT /repos/{user}/{project}/import` on GitHub, passing the GitLab HTTP URL plus credentials for private repos.

---

## Contributing

Bug reports, feature requests, and pull requests are welcome!  
1. Fork the repo.  
2. Create a feature branch.  
3. Open a Merge Request here on GitLab.  

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Made with ❤️ by bocaletto-luca*
