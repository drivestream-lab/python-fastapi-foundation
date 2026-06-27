# Tests for {{cookiecutter.service_name}}

## Structure

```
tests/
  unit/        Pure unit tests — no real infra, no network calls.
               Run: make test
  verify/      Live verify tests — requires running docker-compose services.
               Run: make verify
  _helpers/    Shared fixtures and helpers.
```

## Running

```bash
# Unit only (CI gate)
make check && make test

# Live verify (integration)
docker-compose -f docker/docker-compose.yml up -d
make verify
```
