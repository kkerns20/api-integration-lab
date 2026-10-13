# API Integration Lab

A hands-on project for learning REST APIs, HTTP, JSON, Python, authentication, error handling, and system-to-system integration patterns through practical Solutions Engineering exercises.

## Current functionality

The first client queries the GitHub REST API for repository metadata.

It currently supports:

- command-line owner and repository input
- successful HTTP responses
- HTTP error handling
- request timeout handling
- JSON parsing
- selected repository metadata output

## Example

```bash
python github_repo.py kkerns20 api-integration-lab
```

Example output:

```text
Status: 200
Repository: kkerns20/api-integration-lab
Visibility: public
Default branch: main
Open issues: 0
```

## Current architecture

```text
User
  ↓
Python CLI
  ↓
HTTP GET request
  ↓
GitHub REST API
  ↓
JSON response
  ↓
Parsed repository summary
```

## Error handling

The client uses `requests.get(..., timeout=10)` and `raise_for_status()` so failed API responses are handled intentionally rather than causing downstream parsing errors.

A missing repository, for example, returns an HTTP `404` and is handled as an HTTP error instead of producing a Python traceback from missing JSON fields.

## Concepts practiced

- REST API requests
- HTTP methods and status codes
- JSON
- Python `requests`
- command-line arguments
- exceptions and error handling
- request timeouts
- Git/GitHub workflow
- SSH authentication for Git operations
- virtual environments and dependency isolation

## Project environment

This project uses a Python virtual environment so dependencies remain isolated from the system Python installation.

Create and activate it with:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Next steps

Planned additions include:

- authenticated GitHub API requests
- environment variables for secrets
- rate-limit inspection
- reusable functions
- logging
- pagination
- retries
- webhook or second-system integration

## Solutions Engineering focus

The purpose of this lab is not only to make API calls work. Each exercise is intended to practice the same workflow used in customer-facing technical work:

**understand the requirement → inspect the API → build the integration → handle failure cases → validate behavior → explain the design and tradeoffs**
