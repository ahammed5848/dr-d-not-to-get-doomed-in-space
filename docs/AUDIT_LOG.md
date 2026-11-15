# Dr D — Security, Performance & Architecture Audit Log

**Project:** Dr D (Astronaut Health Monitoring and Early-Warning System)  
**Date:** November 2026  
**Auditor:** Flight Software & Mission Architecture Audit Team  
**Scope:** Backend (FastAPI, SQLAlchemy, Pydantic, Analytics, Security), Frontend (React/Vite, UI/UX, WebSocket), CI/Testing Harness.

---

## Executive Summary

A comprehensive architectural, clinical logic, security, and standards audit of the Dr D platform was conducted prior to operational qualification. The audit examined modern Python 3.11+ / 3.13 deprecations, Pydantic V2 compatibility, database ORM patterns, Role-Based Access Control (RBAC) boundaries, clinical threshold integrity, authentication rate limiting, and automated regression testing. 

All identified defects have been remediated, verified via 24 unit/integration tests, and confirmed with zero frontend build warnings or errors.

---

## Summary of Findings

| ID | Category | Severity | Description | Status |
|---|---|---|---|---|
| AUD-01 | Architecture / Pydantic V2 | **HIGH** | Deprecated `class Config` and `.from_orm()` invocations causing runtime deprecation warnings and potential V2 incompatibility. | **RESOLVED** |
| AUD-02 | Architecture / SQLAlchemy 2.0 | **MEDIUM** | Legacy `declarative_base()` usage replaced with modern `DeclarativeBase` subclassing. | **RESOLVED** |
| AUD-03 | Python 3.13 Runtime | **MEDIUM** | Deprecated `datetime.utcnow()` causing naive timestamp warnings; migrated to `datetime.now(timezone.utc)`. | **RESOLVED** |
| AUD-04 | Security / Auth | **HIGH** | Absence of rate limiting on `/api/auth/login` exposed endpoint to brute-force credential stuffing. | **RESOLVED** |
| AUD-05 | Clinical / Safety Logic | **HIGH** | Missing threshold boundary checks allowed inverted alert boundaries (e.g., warning_low > warning_high). | **RESOLVED** |
| AUD-06 | Security / RBAC | **HIGH** | Telemetry and clinical notes endpoints did not strictly enforce astronaut data isolation, risking HIPAA/crew privacy breach. | **RESOLVED** |
| AUD-07 | Input Validation | **MEDIUM** | Daily check-in submissions lacked strict physiological boundary validation (e.g., sleep > 24h, scores > 10). | **RESOLVED** |
| AUD-08 | Testing / CI Harness | **MEDIUM** | Test suite lacked coverage for authentication rate limiting, threshold validation, and RBAC isolation. | **RESOLVED** |

---

## Detailed Audit Records

### AUD-01: Pydantic V2 Migration (`ConfigDict` & `model_validate`)
- **Severity:** High
- **Files Modified:**
  - `backend/app/schemas.py`
  - `backend/app/routers/auth.py`
  - `backend/app/routers/alerts.py`
  - `backend/app/routers/astronauts.py`
- **Issue:** Pydantic V2 deprecated inner `class Config: from_attributes = True` in favor of `model_config = ConfigDict(from_attributes=True)`, and deprecated `.from_orm(obj)` in favor of `.model_validate(obj)`. Over 30 deprecation warnings were emitted during startup and test runs.
- **Resolution:** Replaced all schema configurations with `model_config = ConfigDict(from_attributes=True)` and updated all router serialization calls to use `.model_validate()`.

### AUD-02: SQLAlchemy 2.0 Modern Declarative Base
- **Severity:** Medium
- **Files Modified:**
  - `backend/app/database.py`
- **Issue:** Legacy `Base = declarative_base()` pattern was flagged for deprecation in SQLAlchemy 2.0+.
- **Resolution:** Refactored database declaration to inherit from `DeclarativeBase`:
  ```python
  from sqlalchemy.orm import DeclarativeBase

  class Base(DeclarativeBase):
      pass
  ```

### AUD-03: Python 3.13 Timezone-Aware UTC Datetimes
- **Severity:** Medium
- **Files Modified:**
  - `backend/app/models.py`
  - `backend/app/seed.py`
  - `backend/app/analytics.py`
  - `backend/app/simulator.py`
  - `backend/app/auth.py`
  - `backend/app/reports.py`
  - `backend/app/routers/*.py`
- **Issue:** `datetime.datetime.utcnow()` has been officially deprecated in Python 3.12+ because it produces naive datetime objects without UTC tzinfo, causing timezone mismatches and serialization ambiguities.
- **Resolution:** Systematically replaced all occurrences across models, database triggers, seed scripts, simulation loops, and API responses with `datetime.now(timezone.utc)`.

### AUD-04: In-Memory Authentication Rate Limiting
- **Severity:** High
- **Files Modified:**
  - `backend/app/routers/auth.py`
- **Issue:** The `/api/auth/login` endpoint had no throttling, permitting unlimited rapid authentication attempts per IP address.
- **Resolution:** Implemented a lightweight, memory-efficient sliding-window rate limiter on the login endpoint. Tracks failed login timestamps per client IP. If 5 failed attempts occur within a 60-second window, subsequent requests are rejected with `HTTP 429 Too Many Requests` with a clear countdown notice. Successful authentication clears the failure log.

### AUD-05: Threshold Boundary Validation & Clinical Edge Cases
- **Severity:** High
- **Files Modified:**
  - `backend/app/routers/thresholds.py`
- **Issue:** Flight surgeons or administrators updating clinical thresholds could accidentally set `warning_low` higher than `warning_high`, or `critical_low` higher than `warning_low`, which would disable alert triggering or cause conflicting alert states.
- **Resolution:** Added defensive boundary validation:
  - `critical_low <= warning_low <= warning_high <= critical_high`
  - Any boundary inversion immediately rejects the PUT request with `HTTP 422 Unprocessable Content` and an informative clinical error message.

### AUD-06: Strict Role-Based Access Control (RBAC) Isolation
- **Severity:** High
- **Files Modified:**
  - `backend/app/routers/astronauts.py`
- **Issue:** While top-level astronaut listing routes were scoped, secondary subroutes (`/api/astronauts/{id}/notes` and `/api/astronauts/{id}/advisor`) did not verify whether an authenticated astronaut was requesting their own record versus a crewmate's record.
- **Resolution:** Enforced strict RBAC checks: if `current_user.role == "astronaut"`, `current_user.astronaut_id` must match the path parameter `{astronaut_id}`. Unauthorized access is blocked with `HTTP 403 Forbidden`. Flight surgeons and administrators retain multi-crew visibility.

### AUD-07: Daily Wellbeing Check-in Range Constraints
- **Severity:** Medium
- **Files Modified:**
  - `backend/app/routers/checkins.py`
- **Issue:** The check-in submission endpoint accepted raw floats without range checks, allowing mathematically impossible values (e.g., negative sleep hours, >24 hours of sleep in a sol, or subjective scores outside the 1.0–10.0 Likert scale).
- **Resolution:** Added strict validation bounds (`0 <= sleep_hours <= 24`, `1.0 <= score <= 10.0`). Non-compliant payloads are rejected with `HTTP 422`.

### AUD-08: Dedicated Audit Regression Test Suite
- **Severity:** Medium
- **Files Added:**
  - `backend/tests/test_audit_fixes.py`
- **Resolution:** Authored an automated regression test suite covering:
  - `test_login_rate_limiting`: Verifies 5 failed attempts trigger HTTP 429.
  - `test_threshold_boundary_validation`: Confirms inverted thresholds return HTTP 422 while valid configurations return HTTP 200.
  - `test_astronaut_rbac_scoping`: Confirms an astronaut cannot access peer clinical notes or recommendations (HTTP 403) while their own data returns HTTP 200.
  - `test_checkin_validation`: Verifies out-of-bounds sleep hours or scores are rejected with HTTP 422.

---

## Verification & Status

- **Backend Pytest Suite:** 24 passed in 2.90s (0 failures, 0 errors).
- **Frontend Build:** Vite production build completed with 0 errors (`dist/index.html`, `dist/assets/index-*.js`).
- **Codebase Cleanliness:** Complete repo search confirms 0 residual instances of legacy naming.
