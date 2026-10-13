import os
import sys
import requests

if len(sys.argv) != 3:
    print("Usage: python github_repo.py <owner> <repo>")
    sys.exit(1)

owner = sys.argv[1]
repo = sys.argv[2]

token = os.getenv("GITHUB_TOKEN")

if not token:
    print("Error: GITHUB_TOKEN environment variable is not set.")
    sys.exit(1)

url = f"https://api.github.com/repos/{owner}/{repo}"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

try:
    response = requests.get(url, headers=headers, timeout=10)

    print("Status:", response.status_code)
    print("Rate limit:", response.headers.get("X-RateLimit-Limit"))
    print("Remaining:", response.headers.get("X-RateLimit-Remaining"))
    print("Rate limit used:", response.headers.get("X-RateLimit-Used"))
    print("Rate limit reset:", response.headers.get("X-RateLimit-Reset"))

    response.raise_for_status()

    data = response.json()

    print("Repository:", data["full_name"])
    print("Description:", data["description"])
    print("Visibility:", data["visibility"])
    print("Default branch:", data["default_branch"])
    print("Open issues:", data["open_issues_count"])

except requests.exceptions.HTTPError as error:
    print("HTTP error:", error)

except requests.exceptions.RequestException as error:
    print("Request failed:", error)
