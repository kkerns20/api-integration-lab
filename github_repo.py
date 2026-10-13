import os
import sys
import requests


def build_headers():
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        sys.exit(1)

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_repository(owner, repo, headers):
    url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(url, headers=headers, timeout=10)

    print("Status:", response.status_code)
    print("Rate limit:", response.headers.get("X-RateLimit-Limit"))
    print("Remaining:", response.headers.get("X-RateLimit-Remaining"))
    print("Rate limit used:", response.headers.get("X-RateLimit-Used"))
    print("Rate limit reset:", response.headers.get("X-RateLimit-Reset"))

    response.raise_for_status()

    return response.json()


def print_repository_summary(data):
    print("Repository:", data["full_name"])
    print("Description:", data["description"])
    print("Visibility:", data["visibility"])
    print("Default branch:", data["default_branch"])
    print("Open issues:", data["open_issues_count"])


def main():
    if len(sys.argv) != 3:
        print("Usage: python github_repo.py <owner> <repo>")
        sys.exit(1)

    owner = sys.argv[1]
    repo = sys.argv[2]

    headers = build_headers()

    try:
        data = get_repository(owner, repo, headers)
        print_repository_summary(data)

    except requests.exceptions.HTTPError as error:
        print("HTTP error:", error)

    except requests.exceptions.RequestException as error:
        print("Request failed:", error)


if __name__ == "__main__":
    main()
