# API Integration Lab

A hands-on Solutions Engineering project for learning REST APIs, HTTP, JSON, Python, authentication, pagination, input validation, error handling, and system-to-system integration patterns through practical exercises.

## Project goal

This lab is designed to move beyond simply making API calls. The objective is to build a small but realistic integration client that can:

- authenticate securely
- call multiple API endpoints
- inspect HTTP responses and headers
- parse and transform JSON data
- follow paginated responses
- validate user input
- apply business rules to returned data
- fail cleanly when requests or inputs are invalid

The current implementation uses the GitHub REST API as the external system.

## Current functionality

The Python client can:

- authenticate to GitHub using a `GITHUB_TOKEN` environment variable
- query a specific repository by owner and repository name
- display repository metadata
- inspect API rate-limit headers
- query GitHub's `/rate_limit` endpoint
- convert Unix reset timestamps into human-readable local time
- retrieve the authenticated user's repositories
- follow GitHub pagination links automatically
- combine paginated results into a single repository list
- identify repositories that have not been updated within a configurable number of days
- validate command-line input with `argparse`
- handle HTTP errors and request failures
- enforce request timeouts

## Example usage

Query a repository and use the default stale threshold of 365 days:

```bash
python github_repo.py kkerns20 api-integration-lab
```

Use a custom stale threshold:

```bash
python github_repo.py kkerns20 api-integration-lab --stale-days 90
```

Display built-in CLI help:

```bash
python github_repo.py --help
```

Invalid values are rejected before any API request is made:

```bash
python github_repo.py kkerns20 api-integration-lab --stale-days -20
```

Example validation response:

```text
error: argument --stale-days: stale-days must be greater than 0
```

## Current architecture

```text
User
  |
  v
Python CLI / argparse
  |
  +--> Validate input
  |
  +--> Read GITHUB_TOKEN from environment
  |
  v
GitHub REST API
  |
  +--> GET /repos/{owner}/{repo}
  |
  +--> GET /rate_limit
  |
  +--> GET /user/repos
          |
          +--> follow Link headers when another page exists
  |
  v
JSON responses + HTTP headers
  |
  v
Parse / transform / analyze
  |
  +--> repository summary
  +--> rate-limit information
  +--> repository inventory
  +--> stale repository analysis
```

## Authentication and secrets

The GitHub token is not stored in the source code. The client reads it from an environment variable:

```bash
export GITHUB_TOKEN='your-token-value'
```

The token should never be committed to Git or stored in the public repository.

The authenticated request includes GitHub's recommended REST API headers:

```text
Authorization: Bearer <token>
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
```

## Pagination

GitHub may split large result sets across multiple pages. The client requests up to 100 repositories per page and checks the parsed `Link` response header for a `next` URL.

Conceptually:

```text
page 1
  |
  +--> next page exists
          |
          v
        page 2
          |
          +--> repeat until no next link remains
```

Each page is added to one combined Python list before analysis.

## Business logic

The client now does more than display raw API output. It applies a configurable rule to determine whether a repository should be considered stale.

For example:

```bash
python github_repo.py kkerns20 api-integration-lab --stale-days 90
```

The program converts each repository's ISO 8601 `updated_at` value into a Python `datetime`, calculates the cutoff date, and returns repositories older than the requested threshold.

This demonstrates a common integration workflow:

```text
external data
    |
    v
parse and normalize
    |
    v
apply business rule
    |
    v
produce useful output
```

## Error handling and validation

The client uses:

- `requests.get(..., timeout=10)` to prevent indefinite waits
- `raise_for_status()` to surface HTTP failures
- `HTTPError` handling for unsuccessful HTTP responses
- `RequestException` handling for network-level failures
- `argparse` validation to reject invalid CLI values before network activity begins

A missing repository returns an HTTP `404` and is handled intentionally instead of causing a downstream JSON parsing failure.

## Concepts practiced

- REST API requests
- HTTP methods and status codes
- HTTP response headers
- JSON parsing
- authenticated API requests
- environment variables for secrets
- Python `requests`
- functions and separation of responsibilities
- CLI design with `argparse`
- input validation
- exception handling
- request timeouts
- pagination
- datetime parsing and timezone-aware comparisons
- data transformation
- business-rule implementation
- Git/GitHub workflow
- SSH authentication for Git operations
- Python virtual environments and dependency isolation

## Project environment

Create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

The local virtual environment is excluded from version control through `.gitignore`.

## Development progression

The project has progressed through these stages:

1. Test the GitHub API manually with `curl`.
2. Inspect HTTP status codes and response headers.
3. Parse repository JSON in Python.
4. Handle `404` and request failures cleanly.
5. Add reusable functions.
6. Authenticate with a GitHub token stored outside the code.
7. Inspect API rate limits.
8. Convert raw timestamps into readable values.
9. Retrieve repository collections.
10. Implement pagination.
11. Add stale-repository analysis.
12. Replace manual argument handling with `argparse`.
13. Validate CLI input before making API requests.

## Next steps

Planned additions include:

- reusable `requests.Session()` configuration
- retry handling for transient failures such as `500`, `502`, and `503`
- backoff behavior and rate-limit-aware failure handling
- structured logging
- cleaner separation between API access, analysis, and presentation
- tests for validation and analysis logic
- a second-system integration or webhook workflow

## Solutions Engineering focus

The purpose of this lab is not only to make API calls work. Each exercise is intended to practice a customer-facing technical workflow:

**understand the requirement → inspect the API → authenticate securely → build the integration → handle failure cases → transform data → apply business logic → validate behavior → explain the design and tradeoffs**

That progression turns a simple script into a small integration client that can be discussed in terms of architecture, reliability, security, and business value.
