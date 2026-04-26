# Frontend-Backend Integration Test Report

> Status: historical integration report, not current project runtime documentation.

## What this file represents

This file captured one earlier integration test based on a specific temporary setup:

- frontend on `3000`
- backend on `8080`
- a simplified backend path rather than the current main project entry

That setup is no longer suitable as a default reference for the repository.

## Why it should not be treated as current truth

The old report hard-coded:

1. outdated frontend and backend ports
2. a temporary integration route
3. feature-completeness conclusions tied to that test setup

The current repository has multiple startup paths, and the main project should not be described through this single historical test run.

## What to use instead

For current startup and integration facts, prefer:

1. `README.md`
2. `docs/ONE_CLICK_STARTUP_GUIDE.md`
3. `services/main-app/`
4. current frontend configuration and API base settings

## Retained purpose

This file is kept only as a historical test artifact. It can still be useful when tracing earlier frontend/backend debugging work, but it should not be used as the current integration guide.
