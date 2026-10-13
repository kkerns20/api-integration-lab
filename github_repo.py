import os
import sys
from datetime import datetime, timedelta, timezone

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


def get_rate_limit(headers):
    url = "https://api.github.com/rate_limit"

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    core = data["resources"]["core"]

    reset_time = datetime.fromtimestamp(
        core["reset"],
        tz=timezone.utc,
    ).astimezone()

    print("\nAPI Rate Limit")
    print("Limit:", core["limit"])
    print("Used:", core["used"])
    print("Remaining:", core["remaining"])
    print("Reset:", reset_time.strftime("%Y-%m-%d %H:%M:%S %Z"))


def get_user_repositories(headers):
    url = "https://api.github.com/user/repos"

    params = {
        "per_page": 100,
        "sort": "updated",
    }

    repositories = []

    while url:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10,
        )

        print("\nRepository list request:", response.status_code)

        response.raise_for_status()

        page_data = response.json()
        repositories.extend(page_data)

        url = response.links.get("next", {}).get("url")

        # The next URL already contains its query parameters.
        params = None

    return repositories


def print_repository_list(repositories):
    print("\nRepositories")

    for repo in repositories:
        print(
            f"- {repo['full_name']} "
            f"(private={repo['private']}, "
            f"updated={repo['updated_at']})"
        )


def find_stale_repositories(repositories, stale_days=365):
    cutoff = datetime.now(timezone.utc) - timedelta(days=stale_days)

    stale_repositories = []

    for repo in repositories:
        updated_at = datetime.fromisoformat(
            repo["updated_at"].replace("Z", "+00:00")
        )

        if updated_at < cutoff:
            stale_repositories.append(
                {
                    "name": repo["full_name"],
                    "updated_at": updated_at,
                }
            )

    return stale_repositories


def print_stale_repositories(stale_repositories, stale_days):
    print(f"\nStale repositories (not updated in more than {stale_days} days)")

    if not stale_repositories:
        print("None")
        return

    for repo in stale_repositories:
        updated = repo["updated_at"].strftime("%Y-%m-%d")

        print(
            f"- {repo['name']} "
            f"(last updated {updated})"
        )


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

        get_rate_limit(headers)

        repositories = get_user_repositories(headers)
        print_repository_list(repositories)

        stale_days = 365

        stale_repositories = find_stale_repositories(
            repositories,
            stale_days,
        )

        print_stale_repositories(
            stale_repositories,
            stale_days,
        )

    except requests.exceptions.HTTPError as error:
        print("HTTP error:", error)

    except requests.exceptions.RequestException as error:
        print("Request failed:", error)


if __name__ == "__main__":
    main()

