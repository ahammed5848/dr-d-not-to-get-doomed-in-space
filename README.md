# Dr D — Not to Get Doomed in Space
## Astronaut Health Intelligence System
> *"Your health guardian beyond Earth."*

**NASA Space Apps Challenge:** Create Health Monitoring Software for Astronauts on Space Missions  
**Mission Architecture:** Ares-V Deep Space Transit (Mars Transit Sol 142 of 540)  
**System Identity:** DR D • NOT TO GET DOOMED IN SPACE • ASTRONAUT HEALTH INTELLIGENCE SYSTEM  

![Dr D Mission Control](https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1200&auto=format&fit=crop&q=80)

---

## 1. Project Title & Identity
**Dr D – Not to Get Doomed in Space: Astronaut Health Intelligence System** is an intelligent, edge-first astronaut health-monitoring, anomaly detection, risk assessment, and clinical decision support platform designed to protect astronaut safety during long-duration deep space exploration missions beyond Low Earth Orbit.

## 2. Challenge Name
**NASA Space Apps Challenge** — *Create Health Monitoring Software for Astronauts on Space Missions*.

## 3. Project Overview
During an interplanetary voyage to Mars (such as the *Ares-V* transit), astronauts face unprecedented physical hazards: prolonged microgravity, high-energy cosmic ionizing radiation, cabin atmospheric fluctuations, and profound psychological isolation. Crucially, as the spacecraft moves tens of millions of kilometers from Earth, electromagnetic communication latency expands up to 22 minutes each way (up to 44 minutes round-trip). This latency window renders real-time terrestrial telemedicine or ground-directed surgical guidance impossible during acute emergencies.

**Dr D** bridges this critical operational gap. Operating entirely onboard without cloud dependencies, Dr D ingests multi-channel physiological vitals and cabin environmental life-support telemetry, computes rolling baseline Z-scores, executes unsupervised multi-variable anomaly detection via an Isolation Forest machine learning model, calculates an explainable composite 0–100 Health Risk Index (HRI), generates 30-minute predictive horizon forecasts, and provides automated, protocolized clinical countermeasures to guide astronauts and flight surgeons through high-stakes medical contingencies.

## 4. Problem Statement
Deep-space exploration crews operate under conditions where:
1. **Communication Latency:** Ground flight surgeons cannot interactively assist with acute medical decisions during emergencies when signal delays range from 4.2 seconds to 22 minutes.
2. **Multi-System Deconditioning:** Microgravity induces cephalad fluid shifts (~15% plasma volume loss, optic disc edema / SANS risk), myocardial deconditioning, and 1.0–1.5% monthly bone mineral loss.
3. **Closed-Cabin Contingencies:** Life-support scrubber saturation (CO2 spikes >2,000 ppm) and Solar Particle Events (ionizing radiation surges >0.45 mSv/min) can rapidly incapacitate crew members without instant early-warning indicators.
4. **Data Isolation & Operational Roles:** Flight surgeons require fleet-wide oversight and archival medical dossiers, while crew members require isolated personal telemetry without peer data exposure.

## 5. Objectives
- Deliver an autonomous, responsive astronaut health monitoring platform capable of operating onboard deep-space spacecraft.
- Implement explainable, multi-factor risk scoring (Health Risk Index 0–100) that decomposes overall risk into cardiovascular, hypoxia, thermal, circadian, and environmental domains.
- Detect subtle multi-variable physiological anomalies using an unsupervised Isolation Forest model and individualized baseline Z-scores.
- Enable proactive intervention through 30-minute predictive horizon forecasting with automated threshold breach alerts.
- Incorporate official NASA Human Research Program (HRP) and Exploration Medical Capability (ExMC) publications as an integrated scientific research and evidence layer.
- Maintain transparent data provenance, distinguishing simulated telemetry from verified NASA research references.

---

## 6. Key Features
- **Fleet-Wide Operations HUD:** Real-time physiological cards for all 4 crew members, live sparklines, and concurrent ECLSS cabin environmental telemetry.
- **Biometrics Console & Anatomical Silhouette:** Full time-series biometric graphs paired with localized organ hotspot illumination for clinical triage.
- **Composite Health Risk Index (HRI 0–100):** Explainable composite risk gauge decomposed into 5 physiological factors with plain-language clinical explanations.
- **30-Minute Predictive Horizon Forecast:** Linear regression and exponential dampening anticipating threshold breaches prior to clinical manifestation.
- **Mission Alerts & Incident Center:** Tri-level severity triage interface (`NORMAL`, `WARNING`, `CRITICAL`) with permanent flight surgeon audit logs and resolution notes.
- **Cabin ECLSS Environmental Monitoring:** Continuous tracking of cabin CO2 (ppm), O2 (%), cabin pressure (kPa), temperature (°C), humidity (%), and acoustic noise (dB).
- **Long-Duration Mission Trends:** Multi-sol tracking of cosmic radiation dose against NASA career limits, bone mineral density loss, and muscle mass retention.
- **Daily Astronaut Wellbeing Check-In:** Standardized 1.0–10.0 Likert self-reporting for sleep duration, fatigue, muscle soreness, headache, and space motion sickness.
- **Crisis Simulation Engine (Demo Mode):** Interactive injection panel for 6 acute spaceflight emergencies with automatic recovery and reset controls.
- **NASA Research & Evidence Knowledge Base:** Dedicated 7-section repository incorporating the 5 official NASA publications, hazard taxonomies, evidence reports, and IMPACT 1.0 condition catalogue.
- **Research-to-Alert Context Panels:** Every alert and contingency scenario features an expandable panel detailing the NASA hazard, clinical implications, official research reference, and synthetic provenance tag.
- **Archival Export Center:** Flight surgeon historical dossier review with one-click export to formatted PDF dossiers and CSV time-series logs.
- **Defensive Administrator Matrix:** Threshold calibration interface enforcing mathematical consistency (`critical_low <= warning_low <= warning_high <= critical_high`).
- **Responsive Mobile HUD:** Optimized touch-friendly layout for astronaut suit-side tablets and mobile viewport sizes.

---

## 7. System Architecture & Topology
Dr D is engineered as an edge-first, 4-tier decoupled architecture designed to run on spacecraft avionics without terrestrial cloud dependencies:

```
+-----------------------------------------------------------------------------------+
|                            TIER 1: PRESENTATION & HUD                             |
|  React 18 SPA • Tailwind CSS • Recharts • Lucide Icons • Native WebSocket Client  |
|  Views: Mission Control, Biometrics Silhouette, HRI Explainability, NASA Research |
+-----------------------------------------+-----------------------------------------+
                                          | JSON REST / WSS (Sub-second)
+-----------------------------------------v-----------------------------------------+
|                    TIER 2: INGESTION & COMMUNICATIONS HUB                         |
|  FastAPI • Uvicorn • Pydantic V2 • Starlette WebSockets • Sliding-Window Rate Limiter|
|  Endpoints: /api/auth, /api/astronauts, /api/alerts, /api/research, /api/reports   |
+-----------------------------------------+-----------------------------------------+
                                          |
+-----------------------------------------v-----------------------------------------+
|                  TIER 3: ANALYTICS & CLINICAL INTELLIGENCE CORE                   |
|  • Unsupervised Isolation Forest Anomaly Detection (Scikit-learn)                 |
|  • Individual Baseline Rolling Z-Score Normalization (NumPy / SciPy)              |
|  • Composite Health Risk Index (HRI 0-100) Explainable Engine                     |
|  • 30-Minute Predictive Horizon Forecaster (Linear + Exponential Dampening)       |
|  • Dr D Advisor Clinical Countermeasure Rule Engine                               |
+-----------------------------------------+-----------------------------------------+
                                          |
+-----------------------------------------v-----------------------------------------+
|                 TIER 4: SIMULATION, RESEARCH DATA & PERSISTENCE                   |
|  • Spacecraft Telemetry Simulator: Circadian sine waves, Gaussian sensor jitter   |
|  • 6 Dynamic Crisis Scenario Overrides (CO2 spike, solar storm, EVA strain, etc.) |
|  • NASA Research Knowledge Base: 5 HRP/ExMC publications, 119 IMPACT conditions   |
|  • SQLAlchemy 2.0 ORM with SQLite (`dr_d.db`) • ReportLab PDF Generator           |
+-----------------------------------------------------------------------------------+
```

---

## 8. Technology Stack
Derived directly from the verified codebase:

| Layer | Technologies & Libraries | License |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3.11+ / 3.13, FastAPI (v0.115+), Uvicorn, Starlette | MIT / BSD |
| **Data Validation & ORM** | Pydantic V2 (`ConfigDict`), SQLAlchemy 2.0 (`DeclarativeBase`), SQLite | MIT / Python |
| **Machine Learning & Math** | Scikit-learn (Isolation Forest), NumPy, Pandas, SciPy | BSD-3-Clause |
| **Security & Authentication** | PyJWT, Passlib, Bcrypt salt hashing, Sliding-window Rate Limiter | MIT / Apache 2.0 |
| **Reporting & Documents** | ReportLab (PDF Engine), python-docx | BSD / MIT |
| **Frontend Framework** | React 18, Vite, React Router v6 | MIT |
| **Styling & UI Components** | Tailwind CSS, Lucide React Icons, clsx, tailwind-merge | MIT |
| **Data Visualization** | Recharts (SVG Biometric Charts & Sparklines) | MIT |
| **HTTP & Networking** | Axios, Native HTML5 WebSocket API | MIT |
| **Testing & Quality** | Pytest (35 unit/integration test cases) | MIT |

---

## 9. Data Sources and Provenance
To ensure absolute scientific integrity and full transparency for NASA Space Apps evaluation, Dr D classifies every data stream into five explicit provenance categories:

```
+---------------------------------------------------------------------------------------------------+
|                                  DATA PROVENANCE CLASSIFICATION                                   |
+----------------------------+-----------------------+----------------------------------------------+
| Classification Category    | Visual UI Badge       | Nature & Implementation Description          |
+----------------------------+-----------------------+----------------------------------------------+
| 1. NASA Research Reference | NASA RESEARCH REF     | Static scientific publications & standards   |
| 2. Synthetic Telemetry     | SIMULATED DATA        | Locally simulated 12+ channel vital streams  |
| 3. User-Imported CSV       | USER-IMPORTED DATA    | User-uploaded external CSV telemetry records |
| 4. Model-Generated Output  | MODEL-GENERATED OUT   | Isolation Forest scores, HRI, 30m forecasts  |
| 5. Third-Party Library     | THIRD-PARTY DEPEND    | Open-source runtimes and frameworks          |
+----------------------------+-----------------------+----------------------------------------------+
```

> **MANDATORY DATA PROVENANCE DECLARATION:**  
> The current Dr D prototype uses **synthetic astronaut telemetry** and simulated spacecraft environmental data. Official NASA publications and standards are incorporated as **scientific and technical research references**. **No direct NASA live telemetry API or real human biometric dataset ingestion is currently implemented.**

---

## 10. NASA Research Resources Integrated
Dr D directly integrates findings and architectural principles from five official NASA scientific and technical publications into its knowledge layer:

1. **NASA Human Research Program — Risks of Human Spaceflight**  
   *Official URL:* https://www.nasa.gov/hrp/risks/  
   *Role in Dr D:* Establishes the core 5-hazard classification framework (Space Radiation, Isolation & Confinement, Distance from Earth, Altered Gravity Fields, Hostile and Closed Environments) and mapped physiological risk domains.

2. **NASA Human Research Roadmap — Evidence Reports**  
   *Official URL:* https://humanresearchroadmap.nasa.gov/evidence/  
   *Role in Dr D:* Provides empirical clinical evidence and physiological rationales for cardiovascular deconditioning, hypercapnia thresholds, hypoxia onset, circadian desynchronization, and cosmic radiation exposure.

3. **NASA ExMC — Clinical Decision Support System Architecture Recommendation (HRP-48032 Rev. B)**  
   *Official Citation:* NASA Johnson Space Center, 2022. https://ntrs.nasa.gov/citations/20220017869  
   *Role in Dr D:* Informs the 4-tier decoupled edge architecture, tiered anomaly detection, explainable risk decomposition, and edge-first autonomous execution.

4. **NASA ExMC — Earth-Independent Medical Operations (EIMO) Concept of Operations**  
   *Official Citation:* NASA Technical Publication TP-20240001402, 2024. https://ntrs.nasa.gov/citations/20240001402  
   *Role in Dr D:* Informs clinical autonomy workflows under high communication latency, autonomous emergency triage, pre-mission baseline profiling, and dual operational roles (onboard crew vs ground flight surgeon).

5. **NASA ExMC — Exploration Medical Capability Evidence Library Methods (HRP-48036 Rev. B)**  
   *Official Citation:* NASA Johnson Space Center, 2024. https://ntrs.nasa.gov/citations/20240004774  
   *Role in Dr D:* Provides the structured taxonomy for the Exploration Medical Condition List (IMPACT 1.0 119-condition catalogue) and symptom-to-telemetry mapping.

---

## 11. Super Intelligence (AI) and Machine Learning Disclosures
In accordance with NASA Space Apps Challenge transparency requirements:

### AI Tools Used to Assist Development
- **Google Gemini & Google Antigravity:** Utilized during software development for architectural co-pilot assistance, refactoring, test case synthesis, and documentation structuring.
- **Human Verification:** All generated code, database models, mathematical formulas, and scientific citations were manually reviewed, tested, and validated by the engineering team.

### AI/ML Algorithms Implemented Inside the Application
- **Isolation Forest Anomaly Detection:** An unsupervised machine learning algorithm implemented via Scikit-learn (`DrDAnalytics` in `backend/app/analytics.py`). Initialized with 100 decision trees (`n_estimators=100`, contamination $v=0.05$). Trained on 300 synthetic microgravity physiological samples. It evaluates multi-variable feature vectors to detect subtle anomalous correlations. **It is not an external generative AI API.**
- **Predictive Trend Forecaster:** Uses classical statistical regression (first-order polynomial fitting with exponential dampening) to project 30-minute vital horizons.
- **Dr D Advisor:** A deterministic rule-based clinical decision support expert system executing NASA clinical heuristics.
- **LLMAdvisorStub:** An interface placeholder stub in `backend/app/advisor.py` designed for future edge-quantized Small Language Model integration; currently functions as a mock demonstrating interface contracts.

### NASA Branding & Asset Restriction
- **Original Branding:** Dr D uses original branding, stylized CSS HUD graphics, and Lucide icons.
- **No Generative AI NASA Logos:** Generative AI was **never** used to create, redraw, alter, or fabricate NASA logos, insignia, flags, or mission patches.

---

## 12. Simulation Methodology
The spacecraft simulation engine (`backend/app/simulator.py`) generates realistic microgravity physiological dynamics:
1. **Individual Baselines:** Unique resting profiles per astronaut (Cmdr. Sarah Chen, Dr. Marcus Vance, Elena Rostova, Dr. Alex Rivera).
2. **Diurnal Circadian Oscillation:** A continuous sinusoidal wave ($24$-hour period) driving circadian variations in body temperature ($\pm 0.1^\circ\text{C}$) and heart rate ($\pm 3\text{ bpm}$).
3. **Gaussian Noise Modeling:** Natural biological jitter ($\text{HR } \pm 1.5\text{ bpm}$, $\text{SpO}_2 \pm 0.2\%$, $\text{Temp } \pm 0.04^\circ\text{C}$) mimicking sensor artifact.
4. **Time Multiplier:** Adjustable clock speed ($1\times$ real-time, $10\times$ accelerated, $60\times$ fast-forward) for rapid multi-sol trend observation.
5. **CSV Batch Replay:** External CSV upload endpoint allowing ingestion of recorded biometric logs.

---

## 13. Health Risk Index (HRI) Explanation
The Health Risk Index is an explainable composite score on a $0\text{--}100$ scale:

$$\text{HRI} = 0.60 \sum_{i=1}^5 (w_i s_i) + 0.35 \max(s_i) + 0.05 \, \text{Score}_{\text{IsolationForest}}$$

### Contributing Physiological Domains
- **Cardiovascular Autonomic Load ($w_1 = 0.28$):** Heart rate deviation from baseline, systolic/diastolic blood pressure, and RMSSD heart rate variability.
- **Oxygen Saturation & Ventilation ($w_2 = 0.28$):** Peripheral capillary oxygen saturation (SpO2) and minute respiratory rate.
- **Thermoregulatory Core Stability ($w_3 = 0.16$):** Internal deep-body temperature deviation from microgravity baseline ($36.8^\circ\text{C}$).
- **Stress & Circadian Rhythm Disruption ($w_4 = 0.14$):** Sympathetic stress index, circadian desynchronization score, and sleep quality.
- **Spacecraft Environmental Strain ($w_5 = 0.14$):** Cabin CO2 concentration, atmospheric oxygen fraction, and cabin pressure.

**Peak-Factor Amplifier:** The $0.35 \max(s_i)$ term prevents a single life-threatening metric (such as severe hypoxia) from being diluted by normal values in other channels.  
**Classification Bands:**
- `NOMINAL` ($0\text{--}24.9$): Physiological homeostasis maintained.
- `ELEVATED` ($25.0\text{--}49.9$): Mild compensatory physiological strain.
- `HIGH` ($50.0\text{--}74.9$): Substantial physiological deviation; telemetry watch commanded.
- `SEVERE` ($75.0\text{--}100.0$): Acute multi-system contingency; emergency countermeasure required.

> **MEDICAL DISCLAIMER:** The Health Risk Index is a computational engineering prototype developed for demonstration and research. It is **not** a clinically validated diagnostic device.

---

## 14. Emergency Simulation Scenarios
Dr D includes six calibrated emergency scenarios grounded in NASA HRP hazards:

1. **Cabin CO2 Spike:** Life-support scrubber failure elevates cabin CO2 past 2,100 ppm, driving compensatory tachycardia, respiratory acidosis, and hypoxia risk (*Hazard: Hostile & Closed Environments*).
2. **EVA Cardiac Stress:** High metabolic exertion during spacewalk pushes heart rate to 138 bpm and blood pressure to 154/96 mmHg with autonomic fatigue (*Hazard: Altered Gravity & Hostile Environments*).
3. **Solar Particle Event (SPE Radiation Storm):** Coronal mass ejection causes ionizing radiation dose accumulation (+0.45 mSv/min), triggering storm shelter protocols (*Hazard: Space Radiation*).
4. **Cumulative Sleep Deprivation:** Three consecutive fragmented sleep cycles collapse HRV and elevate sympathetic stress index to 82/100 (*Hazard: Isolation & Confinement*).
5. **Dehydration & Fluid Shift:** Negative fluid balance causes hypovolemic hypotension (102/70 mmHg) and cephalad fluid reduction (*Hazard: Altered Gravity Fields*).
6. **Biosensor Telemetry Dropout:** Optical pulse-oximeter lead disconnect simulation evaluating system robustness against sensor failure (*Hazard: Distance from Earth*).

---

## 15. Installation Instructions

### Prerequisites
- **Python 3.11+** (Tested on Python 3.13)
- **Node.js 18+** (Tested on Node v20 / v22)

```bash
# Clone or extract project repository
cd hermes
```

---

## 16. Backend Startup Instructions
```bash
cd backend

# Create & activate virtual environment (optional)
python -m venv venv
# Windows: venv\Scripts\activate | Linux/macOS: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch FastAPI server (auto-seeds database dr_d.db on initial startup)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **REST OpenAPI Documentation:** http://localhost:8000/docs
- **WebSocket Telemetry Stream:** ws://localhost:8000/ws/live

---

## 17. Frontend Startup Instructions
```bash
cd frontend

# Install dependencies
npm install

# Launch Vite development server
npm run dev

# Or build production bundle
npm run build
```
- **Mission Control Operations UI:** http://localhost:5173

---

## 18. Seeded Demo Credentials
Dr D comes pre-seeded with 7 days of historical vitals, cabin life-support data, active alerts, and medical notes:

| Role | Username | Password | Operational Access Scope |
| :--- | :--- | :--- | :--- |
| **Flight Surgeon** | `surgeon` | `Password123!` | Fleet-wide overview of all 4 crew members, acknowledge/resolve alerts, add clinical notes, export medical dossiers. |
| **Mission Commander** | `schen` | `Password123!` | Commander Sarah Chen's personal telemetry, daily check-in, personal alerts (isolated from peer data). |
| **Flight Engineer** | `erostova` | `Password123!` | Elena Rostova's biometrics, EVA cardiovascular recovery tracking. |
| **Science Specialist** | `mvance` | `Password123!` | Dr. Marcus Vance's personal telemetry, daily check-in. |
| **Medical Specialist** | `arivera` | `Password123!` | Dr. Alex Rivera's personal telemetry, daily check-in. |
| **Mission Administrator** | `admin` | `Password123!` | Physiological and ECLSS threshold calibration matrix, system reset controls. |

---

## 19. Testing Instructions
Run the complete backend test suite:
```bash
cd backend
python -m pytest -v
```
**Results:** All **35 unit and integration tests** execute and pass in ~6 seconds with 0 failures:
- `test_alerts.py` (2 tests: retrieval, acknowledge)
- `test_analytics.py` (3 tests: nominal risk, hypoxia elevation, forecast)
- `test_audit_fixes.py` (4 tests: rate limiting, threshold validation, RBAC isolation, check-in validation)
- `test_auth.py` (3 tests: login, password verification, profile)
- `test_nasa_research.py` (11 tests: summary, hazards, risks, evidence, architecture, EIMO, conditions, sources, provenance, event contexts, alert mapping)
- `test_reports.py` (3 tests: PDF export, CSV export, RBAC scoping)
- `test_simulator.py` (3 tests: trigger scenario, speed multiplier, simulation reset)
- `test_telemetry_csv.py` (2 tests: batch ingestion, CSV parser)
- `test_vitals.py` (4 tests: surgeon access, astronaut isolation, ingestion, environment)

---

## 20. Production Cloud Deployment (Render & GitHub)
Dr D is architected for zero-friction cloud deployment on **Render** via its declarative **Blueprint (`render.yaml`)**:

### Architecture Overview
```
[ User Browser / Evaluators ]
          |
          +---> https://dr-d-frontend.onrender.com (Render Static Site: React 18 + Vite)
          |        |
          |     (REST API / WebSocket: WSS)
          |        v
          +---> https://dr-d-backend.onrender.com (Render Web Service: FastAPI + Uvicorn)
                   |
                (SQLAlchemy ORM)
                   v
             [ SQLite / PostgreSQL Database ]
```

### 1. Render Web Service (FastAPI Backend)
- **Service Type:** Web Service (Python 3.11+)
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check Path:** `/` (returns JSON status `{ "status": "healthy" }`)
- **Required Environment Variables:**
  - `DR_D_SECRET_KEY`: High-entropy cryptographic JWT key (generated automatically by Render Blueprint)
  - `ENVIRONMENT`: `production`
  - `ALLOWED_ORIGINS`: Deployed frontend origin (e.g., `https://dr-d-frontend.onrender.com,http://localhost:5173`)
  - `DR_D_DB_URL`: SQLite (`sqlite:///./dr_d.db`) or managed PostgreSQL connection string (`postgresql://...`)

### 2. Render Static Site (React 18 Frontend)
- **Service Type:** Static Site
- **Root Directory:** `frontend`
- **Build Command:** `npm install && npm run build`
- **Publish Directory:** `dist`
- **Single Page Application (SPA) Rewrite:**
  - Configured via `frontend/public/_redirects` (`/*  /index.html  200`) and `render.yaml` `routes` rewrite rule.
- **Required Environment Variables:**
  - `VITE_API_BASE_URL`: Full URL of the deployed FastAPI backend (e.g. `https://dr-d-backend.onrender.com`).
  - `VITE_WS_URL`: (Optional) Automatically derived from `VITE_API_BASE_URL` converting `https://` to `wss://` on port 443.

### 3. One-Click Blueprint Deployment via `render.yaml`
1. Push this repository to GitHub: `https://github.com/<your-username>/dr-d-not-to-get-doomed-in-space`.
2. In the [Render Dashboard](https://dashboard.render.com), click **New +** -> **Blueprint**.
3. Connect your `dr-d-not-to-get-doomed-in-space` GitHub repository.
4. Render automatically parses `render.yaml`, provisions the backend Web Service and frontend Static Site, links environment variables, and launches both services.
5. Every future `git push origin main` triggers an automatic zero-downtime redeployment.

---

## 21. Limitations
1. **Synthetic Telemetry Prototype:** Telemetry is generated via mathematical simulation models rather than live human subject wearables.
2. **Non-Diagnostic System:** Designed for clinical decision support and aerospace evaluation; not FDA/CE-MDR cleared as a diagnostic medical device.
3. **No Direct Live NASA API:** NASA publications are scientific research references; no live classified NASA mission telemetry streams are connected.

---

## 22. Future Scope & Technology Maturation
1. **Wearable Biosensor BLE Drivers:** Integrating Bluetooth Low Energy drivers for flight-certified hardware (e.g., CSA Bio-Monitor smart shirt, AstroRad vest).
2. **Offline Quantized Biomedical SLMs:** Integrating quantized 8-bit Small Language Models (e.g., Med-Gemma) into `LLMAdvisorStub` for conversational offline diagnostic explanations.
3. **Autonomous Ultrasound & Medical Imaging:** Incorporating computer vision models for ultrasound organ imaging and SANS optic nerve sheath diameter (ONSD) measurement.
4. **Planetary Surface Descent Modes:** Extending physiological thresholds to model lunar (0.16g) and Martian (0.38g) surface gravity transitions.

---

## 23. Third-Party & Open-Source Acknowledgements
- **FastAPI / Starlette / Uvicorn:** Modern high-performance asynchronous Python web framework (MIT / BSD).
- **React / Vite / Tailwind CSS:** Frontend UI framework, build pipeline, and utility-first styling (MIT).
- **Scikit-learn / NumPy / Pandas / SciPy:** Scientific computing and unsupervised Isolation Forest machine learning (BSD-3-Clause).
- **Recharts:** Composable SVG charting library for React (MIT).
- **Lucide Icons:** Open-source icon library (ISC).
- **ReportLab / python-docx:** High-performance document compilation engines (BSD / MIT).
- **Unsplash:** Astronaut avatar photography used under the Unsplash License.

---

## 24. Licensing and Attribution
- **Software Codebase:** Copyright (c) 2026 Dr D Team. Released under the MIT License for NASA Space Apps Challenge demonstration.
- **NASA Scientific Works:** NASA Human Research Program and Exploration Medical Capability publications are public domain works of the United States Government (17 U.S.C. § 105).
