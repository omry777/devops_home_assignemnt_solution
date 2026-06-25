# Platform Engineer Home Assignment

This repository contains two services wired together in a small monorepo:

- `epoch-service`: Python/FastAPI service exposing `POST /epoch`.
- `now-time-service`: imported Spring Boot service exposing `GET /now` and calling `epoch-service`.

## Repository Structure

```text
.
├── .github/
│   ├── CODEOWNERS
│   └── workflows/ci.yml
├── services/
│   ├── epoch-service/
│   │   ├── app/main.py
│   │   ├── tests/
│   │   └── Dockerfile
│   └── now-time-service/
│       ├── src/
│       ├── build.gradle
│       └── Dockerfile
├── tests/integration/
├── docker-compose.yml
└── Makefile
```

## Run Locally

Start both services with one command:

```bash
docker compose up --build
```

The services are exposed on:

- `epoch-service`: `http://localhost:8081`
- `now-time-service`: `http://localhost:8080`

Example requests:

```bash
curl -X POST http://localhost:8081/epoch \
  -H 'Content-Type: application/json' \
  -d '{"date":"2026-06-15T10:00:00Z"}'
```

```json
{"epoch":1781517600}
```

```bash
curl http://localhost:8080/now
```

```json
{"message":"now is 1781517600"}
```

Stop the environment:

```bash
docker compose down --remove-orphans
```

## Run Tests

Install Python test tooling:

```bash
make install
```

Run the Python service checks:

```bash
make lint
make test-epoch
```

Run the Java service unit test:

```bash
make test-now
```

`make test-now` expects `gradle` on your `PATH`. If you do not have Gradle installed,
the CI workflow and Dockerfile still build the service using the official Gradle image.

Run the integration test against both services:

```bash
make integration
```

The integration test starts Docker Compose, waits for the HTTP endpoints, calls
`GET /now`, and verifies that the response contains a current epoch value. That
validates the `now-time-service` to `epoch-service` call path.

## CI Pipeline

GitHub Actions workflow: `.github/workflows/ci.yml`.

For pull requests, the workflow:

- Detects affected services with path filters.
- Verifies Python formatting with Ruff.
- Runs Python and Java tests for affected services.
- Builds Docker images for affected services.
- Runs the Compose-based integration test when service or integration files change.

For pushes to `main`, the workflow:

- Builds Docker images for affected services.
- Tags images as `ghcr.io/<owner>/<repo>/<service>:<commit-sha>`.
- Simulates publishing by printing the image tag instead of pushing to a real registry.

To approximate CI locally:

```bash
make ci
```

You can also run the GitHub Actions workflow locally with `act` if it is installed:

```bash
act pull_request
```

## Design Decisions

- Python backend uses FastAPI with Pydantic validation so malformed requests are rejected at the API boundary.
- `POST /epoch` requires a timezone-aware ISO-8601 timestamp. Naive timestamps are rejected instead of guessing a timezone.
- Docker Compose provides the local integration environment and uses service DNS (`http://epoch-service:8081`) for service-to-service communication.
- Containers run as non-root users.
- The now-time service is kept close to the provided upstream code and placed under `services/now-time-service`.
- Image publishing is intentionally simulated because the assignment does not require real registry credentials.
