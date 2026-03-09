# Phase 1 — MVP Local Stack (End-to-End Local Dev)

- [ ] Task 1: Create local docker-compose.yml scaffolding
  - Objective: Define an end-to-end local stack with clear service boundaries and sane defaults.
  - Sub-tasks:
    - Decide service names and dependencies: postgres, postgres-postgis (optional), zookeeper, kafka, data-pipeline (python), backend (express), frontend (react), nginx (optional).
    - Create a single docker-compose.yml (Compose v2) with networks block and named volumes for persistence.
    - Add a .env file sample to centralize environment variables (DB credentials, Kafka broker addresses, API endpoints).
    - Configure healthchecks for each service to aid orchestration.
    - Add basic startup order hints (depends_on where appropriate) and restart policies.
    - Include a lightweight npm/script or make target to run docker-compose up quickly.
  - Acceptance criteria:
    - docker-compose config is valid (docker-compose config succeeds).
    - All services have accessible default endpoints/ports.
    - Logs show services starting without critical errors.
  - Notes:
    - If you prefer, consider a single-file compose with all services or split into multiple compose files for dev vs prod.

- [ ] Task 2: Postgres container setup (with optional PostGIS)
  - Objective: Stable relational store with optional geospatial features.
  - Sub-tasks:
    - Use a Postgres image (pin version); if PostGIS needed, choose a PostGIS-enabled image.
    - Initialize DB with credentials from .env.example; provide a seed/initial schema script for Phase 1 (stations, bikes, trips, users).
    - Mount a persistent volume for Postgres data.
    - If PostGIS: enable EXTENSION postgis in seed or migration.
    - Provide a connectivity check (e.g., psql from host/container).
  - Acceptance criteria:
    - DB is reachable (host:5432 or container host) and tables exist after startup.
  - Notes:
    - Keep schema stable for Phase 1; plan migrations for Phase 2 if needed.

- [ ] Task 3: Zookeeper + Kafka container setup (single/burst broker for MVP)
  - Objective: Reliable messaging backbone for MVP data flow.
  - Sub-tasks:
    - Choose a stack (Confluent or Bitnami) and set up Zookeeper and a Kafka broker in docker-compose.
    - Configure listeners and advertised.listeners to be accessible from host/WSL2.
    - Create initial topics (e.g., city.data, city.data.mpark or similar) or provide topic creation on startup.
    - Ensure a small startup script runs on boot to create topics.
  - Acceptance criteria:
    - Kafka broker starts and topics are creatable; a test producer/consumer can publish/consume.
  - Notes:
    - For MVP, a single broker suffices; plan to scale to multiple brokers if data volume grows.

- [ ] Task 4: Python data-pipeline container (fetch Toronto API; publish to Kafka)
  - Objective: Ingest data from the Toronto city API and publish to Kafka for downstream consumption.
  - Sub-tasks:
    - Implement a small Python app (requests + confluent_kafka or kafka-python).
    - Fetch data from the Toronto API (with rate limiting and backoff).
    - Normalize/shape payload to a defined schema (e.g., station_id, timestamp, coords, status).
    - Publish messages to the city.data topic on Kafka.
    - Add robust logging and basic retry logic; handle transient errors gracefully.
    - Containerize and wire environment variables: KAFKA_BROKER, TOPIC, API_URL, FETCH_INTERVAL.
  - Acceptance criteria:
    - Data-pipeline container runs and produces messages; a Kafka consumer can verify messages appear on city.data.
  - Notes:
    - Start with a simple polling loop (e.g., every 30–60 seconds) and iterate as needed.

- [ ] Task 5: Express backend container (REST endpoints; Kafka consumer; writes to Postgres)
  - Objective: Provide REST APIs and persist data consumed from Kafka into Postgres.
  - Sub-tasks:
    - Scaffold an Express server (prefer TypeScript) with endpoints: /stations, /bikes, /trips (GET/POST initial surface).
    - Implement a Kafka consumer that subscribes to city.data and writes relevant records to Postgres tables.
    - Implement a minimal ORM/DB client (e.g., Prisma, TypeORM, or pg with parameterized queries) to insert data.
    - Add middleware: error handling, simple request validation, CORS, and logging.
    - Expose a health check endpoint (e.g., /health).
    - Use environment variables to configure DB connection and Kafka broker.
  - Acceptance criteria:
    - REST endpoints respond; Kafka consumer writes messages to Postgres correctly.
  - Notes:
    - Keep schema and payload mapping explicit; document data contracts in plan.md.

- [ ] Task 6: React frontend container (map UI with live updates via REST + WebSocket)
  - Objective: Visualize data on a map with live updates from the backend.
  - Sub-tasks:
    - Scaffold a React app (TypeScript) with routes: Home, Stations, Map View.
    - Build a map UI (Leaflet or Mapbox) showing station markers and basic status (availability, capacity).
    - Implement data fetch from backend REST endpoints for initial data.
    - Implement a WebSocket client for live updates (how backend publishes updates via WebSocket or fallback to SSE/polling).
    - Create reusable UI components (MapCard, StationMarker) and a responsive layout.
  - Acceptance criteria:
    - Map renders with stations; initial data loads; live updates arrive via WebSocket.
  - Notes:
    - Ensure map is accessible and responsive; avoid blocking UI on data fetch.

- [ ] Task 7: Ensure all services expose ports accessible from Windows/WSL2
  - Objective: Accessibility from Windows hosts and WSL2 environment.
  - Sub-tasks:
    - Bind ports to 0.0.0.0 in docker-compose to allow host access.
    - Document host URLs, e.g., Postgres 5432, Kafka 9092, API 3000, Frontend 5173.
    - Verify network access from Windows and WSL2 (curl, psql, browser).
  - Acceptance criteria:
    - All services reachable without special networking tweaks.
  - Notes:
    - If you use Docker Desktop with WSL2, document any Windows/Docker Desktop settings that affect networking.

- [ ] Task 8: Simple smoke tests for end-to-end data flow
  - Objective: Validate end-to-end data flow from fetch to persistence and display.
  - Sub-tasks:
    - Define a lightweight smoke-test script that:
      - Starts/ensures all services are up.
      - Produces a test message via the data-pipeline and verifies it lands in Kafka.
      - Consumes from city.data and validates payload schema.
      - Confirms backend REST endpoints respond and that a sample write lands in Postgres.
      - Checks frontend loads a map and displays initial data; optionally verify WebSocket updates.
    - Include clear pass/fail criteria and a brief test log.
  - Acceptance criteria:
    - End-to-end flow completes within a defined time window and all checks pass.
  - Notes:
    - If CI is desired later, convert smoke tests into a dedicated workflow.

## Optional scaffolding references
- Docker Compose skeleton (adapt to your stack) in plan.md is a blueprint for the actual compose file.
- Service contracts: data payload schema, REST API surface, WebSocket/SSE contract.

## What I can do next
- Generate an initial docker-compose.yml and per-service Dockerfiles (starter templates) if you want me to commit them.
- Tailor this phase to your exact tech choices and repo structure and push a ready-to-paste Phase 1 block with DoD per task.
