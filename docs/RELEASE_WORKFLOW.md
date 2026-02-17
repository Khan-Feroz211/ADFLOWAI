# Release Workflow

## Branching Model
- `main`: demo-stable only. No direct experimental commits.
- `feature/<short-name>`: all new development work.
- `release/vX-demo`: frozen branch for client demo/review cycles.

## Required Flow
1. Create feature branch from `main`.
2. Implement and test changes.
3. Open PR into `main` with scope, risks, and test evidence.
4. Merge only after demo sanity checks pass.
5. Create/update release branch for client-facing stability snapshots.

## Version Tagging
- Use semantic tags for client-ready milestones.
- Example: `v1.0.0` (first stable demo), `v1.1.0` (next approved feature milestone).
- Tags must reference tested commits only.

## Client-Specific Configuration
- Keep client-specific values only in `.env`.
- Do not hardcode client names, domains, or keys in source code.
- Keep `.env.example` generic and environment-agnostic.

## Change Control
- Every scope request must have a ticket.
- Track estimate, acceptance criteria, and release target in the ticket.
