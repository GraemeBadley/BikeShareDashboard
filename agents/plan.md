# Plan for Real-Time Toronto Bike-Share Dashboard with Siting Model

This plan outlines phased work to build an end-to-end real-time dashboard, a Python data pipeline, a TypeScript/Express backend, Kafka pub/sub, a React frontend, and PostgreSQL storage, plus a siting model to recommend where the next bike station should go.

Each phase is a checklist. Check items as you complete them.

## Phase 0 — Prep and Governance
- [ ] Confirm production Kafka path: Strimzi on GKE
- [ ] Confirm backend: Express
- [ ] Confirm database: Cloud SQL PostgreSQL with PostGIS
- [ ] Confirm local development approach: Full Docker Compose (WSL2-friendly)
- [ ] Confirm real-time channel: REST + WebSocket
- [ ] Confirm siting model scope and MVP boundaries
- [ ] Establish repo structure and coding standards

## Phase 1 — MVP Local Stack (End-to-End Local Dev)
- [ ] Create local docker-compose.yml scaffolding
- [ ] Postgres container setup (with optional PostGIS)
- [ ] Zookeeper + Kafka container setup (single/burst broker for MVP)
- [ ] Python data-pipeline container (fetch Toronto API; publish to Kafka)
- [ ] Express backend container (REST endpoints; Kafka consumer; writes to Postgres)
- [ ] React frontend container (map UI with live updates via REST + WebSocket)
- [ ] Ensure all services expose ports accessible from Windows/WSL2
- [ ] Simple smoke tests for end-to-end data flow

## Phase 2 — Siting Model MVP (Planning and Core MVP)
- [ ] Define data contracts for siting_candidates and siting_recommendations
- [ ] Add DB tables for siting: siting_candidates, siting_recommendations, siting_scenarios
- [ ] Implement candidate generation prototype (grid/viability/demand signals)
- [ ] Implement optimization prototype (p-median or heuristic)
- [ ] Expose REST endpoints:
  - GET /sitings/candidates
  - POST /sitings/optimize (with P and optional constraints)
- [ ] Persist siting results in Postgres for UI review
- [ ] Build a simple admin UI view (map overlay + table) for siting outputs

## Phase 3 — Full Integration and Testing
- [ ] Integrate siting endpoints with existing data sources (demand, existing stations)
- [ ] Add scenario support (vary P; compare results)
- [ ] Implement end-to-end tests for siting flow (data in, candidate generation, optimization, results)
- [ ] Add basic caching to protect repeated expensive runs
- [ ] Document runtime/config flags for siting module

## Phase 4 — Production Readiness on GCP
- [ ] Confirm Kafka path in prod (Strimzi on GKE by default)
- [ ] Provision Cloud SQL PostgreSQL with PostGIS
- [ ] Deploy backend to Cloud Run or GKE; deploy frontend to Cloud Run or Cloud Storage + CDN
- [ ] Setup CI/CD (GitHub Actions) to build images and deploy
- [ ] Implement private networking for Cloud SQL; configure IAM roles
- [ ] Implement Secret Manager usage for credentials
- [ ] Add basic observability: Cloud Monitoring + Logging
- [ ] Instrument traces with OpenTelemetry

## Phase 5 — Observability, Security, Reliability
- [ ] Add metrics for Kafka lag, DB latency, endpoint latency
- [ ] Centralize logs and create dashboards
- [ ] Implement retries, backoffs, and idempotent consumers
- [ ] Harden security (TLS for Kafka; restricted network access; secret rotation)
- [ ] Define backup/recovery plan for Cloud SQL

## Phase 6 — Validation and Rollout
- [ ] Stakeholder walkthrough of siting model outputs
- [ ] Run staging tests with synthetic data
- [ ] Canary rollout plan for siting feature
- [ ] Prepare rollback/runbooks and incident response plan

## Phase 7 — Future Enhancements (Beyond MVP)
- [ ] Real-time siting recommendations stream (if needed)
- [ ] More sophisticated equity constraints and policy rules
- [ ] Enhanced demand forecasting (seasonality, events)
- [ ] Multi-region readiness and open data exports

## Data and API Contracts (High-Level Reference)
- Siting candidates: candidate_id, lat, lon, demand_score, viability_score, area_id, notes
- Siting recommendations: rec_id, candidate_id, p_value, objective_value, feasibility, install_cost_estimate
- Siting scenarios: scenario_id, p_value, date_generated, summary_metrics
- Endpoints (MVP):
  - GET /sitings/candidates
  - POST /sitings/optimize { p: int, constraints?: object }
  - GET /sitings/scenario/{id}
  - (Admin) GET/POST to review/export siting data

## Notes and Assumptions
- Local dev uses a plain Kafka cluster (for speed and simplicity). Production moves to Strimzi on GKE or a managed service.
- PostGIS is enabled in Cloud SQL for geospatial queries; locally you can use a PostGIS-enabled image.
- The siting model MVP is designed to be data-light and iteratively improved; start simple (grid + basic demand) and add constraints over time.

If you want any tweaks (different P defaults, specific signals for demand, or a stricter equity policy), tell me and I’ll adjust the plan.md content accordingly.
