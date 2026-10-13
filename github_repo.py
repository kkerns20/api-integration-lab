import sys
import requests

if len(sys.argv) != 3:
    print("Usage: python github_repo.py <owner> <repo>")
    sys.exit(1)

owner = sys.argv[1]
repo = sys.argv[2]

url = f"https://api.github.com/repos/{owner}/{repo}"

try:
    response = requests.get(url, timeout=10)

    print("Status:", response.status_code)

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
