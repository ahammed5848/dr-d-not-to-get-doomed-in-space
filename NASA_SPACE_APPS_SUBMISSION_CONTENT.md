# NASA SPACE APPS CHALLENGE — SUBMISSION CONTENT
## Project: Dr D – Not to Get Doomed in Space
### Challenge: Create Health Monitoring Software for Astronauts on Space Missions

---

## A. SUMMARY

Dr D – Not to Get Doomed in Space is an autonomous astronaut health intelligence and early-warning platform designed for long-duration deep-space exploration, such as crewed transit to Mars. Beyond Low Earth Orbit, communication delays of up to 22 minutes one-way preclude real-time telemedicine from Earth. Dr D operates entirely onboard spacecraft edge avionics without external cloud dependencies.

The platform continuously monitors physiological vitals and spacecraft cabin life-support telemetry, executes unsupervised multi-variable anomaly detection via an Isolation Forest machine learning model, calculates an explainable composite 0–100 Health Risk Index (HRI), projects 30-minute predictive horizon forecasts to preempt threshold breaches, and delivers protocolized clinical countermeasures.

Dr D is scientifically grounded in five official publications from the NASA Human Research Program (HRP) and Exploration Medical Capability (ExMC), integrating NASA’s 5-hazard classification and the IMPACT 1.0 Exploration Medical Condition List. The current prototype utilizes synthetic astronaut telemetry and simulated spacecraft environmental data to demonstrate autonomous medical operations; official NASA publications are incorporated as scientific and technical research references. Dr D transforms space medicine from reactive ground triage into proactive onboard health guardianship.

*Word Count:* 179 words (Requirements: 50–200 words)  
*Character Count:* 1,397 characters (Requirements: Strictly < 1,500 characters)

---

## B. PROJECT DETAILS

### 1. What problem does Dr D solve?
On deep-space missions to the Moon or Mars, astronauts travel millions of kilometers beyond Earth's protective magnetosphere and immediate terrestrial support. Round-trip radio communication latency expands up to 44 minutes, eliminating the possibility of synchronous ground surgical guidance or interactive telemedicine during sudden acute crises. Crews must therefore manage medical contingencies autonomously. Dr D provides the spacecraft with an edge-first clinical intelligence system that ingests multi-channel telemetry, detects subtle multivariate physiological drift before clinical decompensation occurs, explains composite health risk, and provides immediate, protocolized countermeasures.

### 2. Why is astronaut health monitoring important?
Human spaceflight exposes crews to hostile stressors: microgravity deconditioning, muscle atrophy, cancellous bone mineral resorption, cephalad fluid redistribution (elevating intraocular pressure and SANS risk), high-energy cosmic ionizing radiation, closed-cabin atmospheric fluctuations (CO2 pocketing, hypoxia), and severe circadian desynchronization. Left unmitigated, these stressors degrade cognitive and psychomotor vigilance, precipitate acute medical crises, and jeopardize mission success. Continuous, autonomous health monitoring ensures early detection and defensive countermeasure administration.

### 3. How does the application work?
Dr D is built on a 4-tier edge architecture:
1. **Simulation & Telemetry Layer:** A continuous asynchronous engine generates 12+ channels of physiological vitals and ECLSS cabin readings with diurnal circadian waves, biological Gaussian jitter, and calibrated emergency scenario overrides.
2. **Ingestion & Comms:** FastAPI REST and Starlette WebSockets stream live 1–2 Hz frames with Pydantic V2 schema validation and sliding-window rate limiting.
3. **Analytics Core:** NumPy, SciPy, and Scikit-learn run individual baseline Z-score normalization, Isolation Forest multi-variable anomaly detection, composite Health Risk Index calculation, and predictive horizon forecasting.
4. **Operations HUD:** A React 18, Tailwind CSS, and Recharts single-page application displays multi-crew cards, anatomical organ silhouettes, explainable risk gauges, alert management, and dossier export.

### 4. What are its key features?
- **Fleet-Level Operations HUD:** Real-time multi-crew vitals cards and concurrent ECLSS environmental parameters.
- **Biometrics Console & Anatomical Silhouette:** Full time-series graphs paired with localized organ hotspot illumination.
- **Explainable Health Risk Index (HRI 0–100):** Decomposed into Cardiovascular, Hypoxia, Thermal, Circadian, and Environmental factors.
- **30-Minute Predictive Horizon Forecast:** Linear regression with exponential dampening to detect impending threshold breaches.
- **Mission Alerts & Incident Center:** Tri-level severity triage (`NORMAL`, `WARNING`, `CRITICAL`) with permanent audit logs.
- **Cabin ECLSS Monitoring:** Real-time tracking of CO2, O2, pressure, temperature, humidity, and acoustic noise.
- **Long-Duration Mission Trends:** Multi-sol tracking of cosmic radiation dose against career caps and musculoskeletal deconditioning.
- **Daily Astronaut Wellbeing Check-In:** Standardized Likert self-reporting for sleep, fatigue, mood, and space motion sickness.
- **Crisis Simulation Engine (Demo Mode):** Interactive injection panel for 6 acute spaceflight contingencies with auto-decay.
- **NASA Research & Evidence Knowledge Base:** 7-section repository housing official NASA publications, hazard taxonomies, and IMPACT 1.0 condition catalogue.
- **Research-to-Alert Context Panels:** Every alert details the associated NASA hazard, clinical implications, and research citation.
- **Archival Export Center:** One-click flight surgeon dossier export to formatted PDF reports and CSV time-series data.

### 5. How does its anomaly detection work?
Dr D implements a dual-tiered anomaly detection pipeline:
- **Individual Rolling Z-Scores:** Physiological values are compared against the astronaut's unique microgravity baseline ($z = (x - \mu)/\sigma$). Deviations exceeding $|z| > 2.0$ flag warnings, while $|z| > 3.0$ trigger critical clinical investigation.
- **Unsupervised Isolation Forest Model:** An ensemble of 100 decision trees (`n_estimators=100`, contamination $v=0.05$) evaluates 8-dimensional physiological vectors ([HR, HRV, SpO2, BP_sys, BP_dia, Temp, Resp, Stress]). It detects subtle non-linear multi-variable anomalies that individually stay within univariate thresholds but collectively signify acute clinical decompensation.

### 6. How is the Health Risk Index calculated?
The composite Health Risk Index (HRI) is expressed on an explainable 0–100 scale:
$$\text{HRI} = 0.60 \sum_{i=1}^5 (w_i s_i) + 0.35 \max(s_i) + 0.05 \, \text{Score}_{\text{IsolationForest}}$$
It synthesizes five domain sub-scores:
1. Cardiovascular Autonomic Load ($w_1 = 0.28$)
2. Oxygen Saturation & Ventilation ($w_2 = 0.28$)
3. Thermoregulatory Core Stability ($w_3 = 0.16$)
4. Stress & Circadian Rhythm Disruption ($w_4 = 0.14$)
5. Spacecraft Environmental Strain ($w_5 = 0.14$)

The peak-factor amplifier ($0.35 \max(s_i)$) guarantees that a single acute failure (such as severe hypoxia) cannot be obscured by nominal readings in other channels. The score maps to four clinical bands: `NOMINAL` (<25.0), `ELEVATED` (25.0–49.9), `HIGH` (50.0–74.9), and `SEVERE` (≥75.0), accompanied by plain-language clinical explanations.

### 7. How does forecasting work?
The forecasting engine evaluates historical physiological readings over rolling windows. It executes first-order polynomial regression combined with physiological dampening ($0.75\times$ slope damping) to project vital trajectories across a 30-minute lookahead horizon (+5m to +30m). An expanding uncertainty confidence cone ($\pm 3\%$ margin expanding over time) models physiological variability. The engine evaluates projected trajectories against warning and critical boundaries, computing exact time-to-breach ($T_{\text{breach}}$) to enable proactive, preemptive countermeasure administration.

### 8. How do emergency simulations work?
The built-in simulation engine features 6 calibrated crisis scenarios:
1. **Cabin CO2 Spike:** ECLSS scrubber failure elevates ambient CO2 past 2,100 ppm, inducing hypercapnia, compensatory tachycardia, and hypoxia risk.
2. **EVA Cardiac Stress:** Metabolic exertion during spacewalk pushes heart rate to 138 bpm and blood pressure to 154/96 mmHg with autonomic fatigue.
3. **Solar Particle Event (SPE):** Coronal mass ejection causes ionizing radiation dose intake (+0.45 mSv/min), triggering shelter protocols.
4. **Cumulative Sleep Deprivation:** Fragmented sleep collapses HRV and raises sympathetic stress index to 84/100.
5. **Dehydration & Fluid Shift:** Negative fluid balance causes hypovolemic hypotension (102/70 mmHg) and cephalad fluid reduction.
6. **Biosensor Telemetry Dropout:** Optical pulse-oximeter lead disconnect simulation evaluating system robustness.
All scenarios dynamically alter the backend database, recalculate the HRI, stream through WebSockets to update the UI in sub-second latency, and automatically decay over 60–120 seconds or upon manual reset.

### 9. How is NASA research incorporated?
Dr D incorporates five foundational NASA Human Research Program (HRP) and Exploration Medical Capability (ExMC) publications:
- The 5 hazards of human spaceflight framework (Space Radiation, Isolation & Confinement, Distance from Earth, Altered Gravity Fields, Hostile & Closed Environments).
- NASA Human Research Roadmap evidence reports justifying clinical limits for hypoxia, hypercapnia, cardiovascular deconditioning, and circadian disruption.
- ExMC Clinical Decision Support Architecture Recommendation (HRP-48032 Rev. B) guiding our 4-tier decoupled edge architecture.
- ExMC Earth-Independent Medical Operations (EIMO TP-20240001402) ConOps guiding delayed communication workflows and autonomous triage.
- ExMC Exploration Medical Condition List (IMPACT 1.0, HRP-48036 Rev. B) establishing a structured 119-condition taxonomy.
Every alert and scenario is directly linked to an expandable research context panel explaining *why* the condition matters scientifically.

### 10. What benefits does the application provide?
- **Crew Autonomy:** Allows astronauts to diagnose and stabilize emergencies during communication blackouts.
- **Clinical Explainability:** Eliminates black-box algorithms by decomposing risk into clear physiological factors.
- **Proactive Early Warning:** Identifies impending threshold breaches up to 30 minutes before clinical collapse.
- **Flight Surgeon Oversight:** Provides ground teams with centralized triage logs and one-click PDF medical dossiers.
- **Zero Cloud Footprint:** Runs locally on onboard spacecraft hardware without third-party internet dependencies.

### 11. Who are the intended users?
- **Astronaut Flight Crews:** Monitoring personal biometrics, completing daily wellbeing check-ins, and receiving guided countermeasures during EVAs or cabin emergencies.
- **Crew Medical Officers (CMO):** Onboard triage, localized anatomical assessment, and emergency stabilization.
- **Flight Surgeons (Mission Control):** Fleet-wide surveillance, threshold calibration, alert resolution audit trails, and archival dossier export.
- **Aerospace Human Factors Researchers:** Evaluating multi-variable physiological deconditioning models.

### 12. What is its potential impact?
Dr D fundamentally transforms human spaceflight medicine from reactive, Earth-dependent telemedicine to autonomous, predictive health guardianship. For future Artemis lunar base camps and crewed Mars exploration missions, this capability will drastically reduce mission abort risk, prevent preventable mortality, and protect crew cognitive and physical health.

### 13. What makes the project creative and innovative?
- **Explainable Multi-Domain Risk Formulation:** Rather than delivering an opaque neural network output, Dr D decomposes the HRI into transparent, clinical domains with peak-factor amplification.
- **Interactive Anatomical Hotspot Silhouette:** Visually maps real-time biometric anomalies directly to human organ systems.
- **Integrated NASA Research Knowledge Layer:** Merges live telemetry operations with an interactive scientific knowledge base grounded in official NASA publications.
- **Research-to-Alert Contextual Linking:** Provides instant clinical rationales explaining *why* an event matters directly on alert banners and crisis modals.
- **Dual-Tiered Anomaly Architecture:** Combines individualized baseline Z-scores with multivariate Isolation Forest machine learning.

### 14. What are the limitations?
- **Synthetic Telemetry Prototype:** Continuous vitals are generated via mathematical simulation models rather than human flight hardware.
- **Non-Diagnostic Prototype:** Built for research, hackathon evaluation, and operational decision support; not FDA or CE-MDR cleared.
- **Simulated ECLSS Integration:** Spacecraft life support readings are simulated based on NASA STD-3001 limits rather than live spacecraft sensor harnesses.

### 15. What are the future possibilities?
- **Hardware Sensor Integration:** Direct BLE/USB integration with spaceflight wearables (e.g., CSA Bio-Monitor, AstroRad vest).
- **Offline Quantized Biomedical SLMs:** Embedding quantized 8-bit Small Language Models (e.g., Med-Gemma) into `LLMAdvisorStub` for conversational offline diagnostic reasoning.
- **Autonomous Medical Ultrasound:** Integrating computer vision for automated SANS optic nerve sheath diameter (ONSD) measurement.
- **Planetary Surface Transition Modes:** Calibrating dynamic G-transition algorithms for lunar (0.16g) and Martian (0.38g) surface sorties.

---

## C. TOOLS, TECHNOLOGIES AND LANGUAGES

Derivation strictly from the final verified project codebase:

### Programming Languages
- **Python (3.11+ / 3.13):** Backend services, analytical modeling, simulation engine, PDF report generation, test suite.
- **JavaScript (ES2022+ / JSX):** Frontend single-page application, interactive UI components, state management.
- **SQL (SQLite dialect):** Relational persistence, indices, and querying.
- **HTML5 & CSS3:** HUD interface structure, styling, and animations.

### Backend Frameworks & Libraries
- **FastAPI (v0.115+):** High-performance asynchronous REST API framework.
- **Uvicorn (v0.30+):** Lightning-fast ASGI server implementation.
- **Starlette (v0.38+):** WebSocket broadcast hub and ASGI middleware.
- **SQLAlchemy (v2.0+):** Object-Relational Mapping (ORM) with `DeclarativeBase`.
- **Pydantic (v2.8+):** Robust data validation and schema serialization with `ConfigDict`.
- **SQLite:** Embedded zero-configuration ACID relational database (`dr_d.db`).
- **Scikit-learn (v1.4+):** Unsupervised Isolation Forest machine learning model.
- **NumPy (v1.26+) & SciPy (v1.12+):** Vector mathematics, polynomial regression, Gaussian noise modeling.
- **Pandas (v2.2+):** Tabular data structures and time-series manipulation.
- **PyJWT & Passlib / Bcrypt:** Cryptographic JSON Web Token generation and secure salt hashing.
- **ReportLab (v4.1+) & python-docx:** High-resolution PDF document compilation and DOCX report generation.
- **Pytest (v8.0+):** Automated unit and integration testing suite.

### Frontend Frameworks & Libraries
- **React (v18.3+):** Declarative component-based user interface library.
- **Vite (v5.4+):** Modern ES-module frontend build tool and development server.
- **React Router (v6.28+):** Client-side routing and protected view enforcement.
- **Tailwind CSS (v3.4+):** Utility-first styling with custom aerospace dark-mode design tokens.
- **Recharts (v2.13+):** Composable SVG biometric time-series charts and sparklines.
- **Lucide React (v0.460+):** Clean, consistent aerospace iconography.
- **Axios (v1.7+):** Promise-based HTTP client for REST communication.
- **Native HTML5 WebSocket API:** Sub-second bi-directional telemetry streaming.

### Development & Operational Tools
- **PowerShell & Windows Batch Scripts (`start.ps1`, `start.bat`):** Automated single-command startup.
- **Playwright:** Automated high-resolution interface screenshot capture suite.

---

## D. NASA DATA AND NASA RESOURCES

### 1. NASA Human Research Program – Risks of Human Spaceflight
- **Official URL:** https://www.nasa.gov/hrp/risks/
- **What it covers:** Comprehensive taxonomy of human spaceflight hazards (Space Radiation, Isolation and Confinement, Distance from Earth, Altered Gravity Fields, Hostile and Closed Environments) and mapped physiological risk areas.
- **Why it is relevant:** Establishes the authoritative aerospace health risk taxonomy for long-duration missions.
- **How it informs Dr D:** Directly structures Dr D's hazard categorization, health risk classifications, and research-to-alert mapping.
- **Data Nature:** Scientific research publication and risk framework (Not a live telemetry dataset).

### 2. NASA Human Research Roadmap – Evidence Reports
- **Official URL:** https://humanresearchroadmap.nasa.gov/evidence/
- **What it covers:** Peer-reviewed clinical evidence reports on cardiovascular deconditioning, hostile cabin atmospheres, sleep loss and circadian desynchronization, radiation carcinogenesis, and Spaceflight Associated Neuro-ocular Syndrome (SANS).
- **Why it is relevant:** Provides empirical biomedical foundations and clinical rationale for aerospace health monitoring.
- **How it informs Dr D:** Informs the physiological weighting of our Health Risk Index ($w_1\text{--}w_5$) and establishes clinical justification for our threshold boundaries.
- **Data Nature:** Scientific technical reports (Not a machine-readable telemetry dataset).

### 3. NASA ExMC – Clinical Decision Support System Architecture Recommendation (HRP-48032 Rev. B)
- **Official Citation:** NASA Johnson Space Center, 2022. https://ntrs.nasa.gov/citations/20220017869
- **What it covers:** Technical architecture specifications for exploration-class clinical decision support, covering data ingestion, inference engines, explainability, and edge-first autonomy.
- **Why it is relevant:** Outlines NASA's official engineering recommendations for deep-space medical decision support software.
- **How it informs Dr D:** Guided Dr D's 4-tier decoupled edge architecture, tiered anomaly detection, explainable risk scoring, and zero-cloud dependency.
- **Data Nature:** Technical architecture specification standard.

### 4. NASA ExMC – Earth-Independent Medical Operations (EIMO) Concept of Operations
- **Official Citation:** NASA Technical Publication TP-20240001402, 2024. https://ntrs.nasa.gov/citations/20240001402
- **What it covers:** Operational workflows for deep-space clinical autonomy when communication latency precludes Earth-based telemedicine.
- **Why it is relevant:** Defines the operational reality of crew autonomy during high-latency transit to Mars.
- **How it informs Dr D:** Directly informed Dr D's automated alarm triage, pre-mission baseline profiling, autonomous countermeasure delivery, and role-based access control.
- **Data Nature:** Operational concept standard (ConOps).

### 5. NASA ExMC – Exploration Medical Capability Evidence Library Methods (HRP-48036 Rev. B)
- **Official Citation:** NASA Johnson Space Center, 2024. https://ntrs.nasa.gov/citations/20240004774
- **What it covers:** Methodological framework for the Exploration Medical Condition List (IMPACT 1.0 catalogue of 119 conditions).
- **Why it is relevant:** Authoritative clinical condition list prioritized for long-duration exploration missions.
- **How it informs Dr D:** Integrated into Dr D's structured Exploration Medical Condition catalogue, mapping conditions to corresponding telemetry streams.
- **Data Nature:** Methodological standard and medical condition taxonomy.

> **MANDATORY DATA DISCLAIMER:**  
> "The current prototype uses synthetic astronaut telemetry and simulated spacecraft environmental data. NASA publications are used as scientific and technical research references. No direct NASA live telemetry API or NASA biometric dataset ingestion is currently implemented."

---

## E. OTHER DATA, RESOURCES AND TOOLS

### Software Libraries & Registries
- **Python Software Foundation (PyPI):** Host registry for FastAPI, Pydantic, SQLAlchemy, Scikit-learn, NumPy, Pandas, SciPy, ReportLab.
- **Node Package Manager (npm):** Host registry for React, Vite, Tailwind CSS, Recharts, Lucide Icons, Axios.

### Imagery & Iconography
- **Unsplash Photography:** High-resolution astronaut portrait photography and space background imagery used in compliance with the Unsplash License (photographers: Christina @ wocintechchat, Jurica Koletić).
- **Lucide Icon Library:** Open-source vector icon set (ISC License).

### Typography
- **Inter & JetBrains Mono:** Open-source font families (SIL Open Font License 1.1) providing modern legibility and high-density telemetry monospace display.

---

## F. SUPER INTELLIGENCE / AI DISCLOSURE

### Transparent Disclosure of AI Tools
In compliance with NASA Space Apps Challenge Super Intelligence & AI usage rules:
- **AI-Assisted Programming & Documentation:** The development team utilized **Google Gemini** and **Google Antigravity** as intelligent developer co-pilots for architectural ideation, code refactoring, test case generation, and technical documentation drafting.
- **Human Verification & Contribution:** Every line of code, algorithmic formula, database model, API endpoint, and technical claim was manually designed, implemented, reviewed, tested, and verified by human software engineers.
- **Embedded Machine Learning:** The application embeds an **unsupervised Isolation Forest** machine learning model (`Scikit-learn`) running locally in Python. It was fitted on 300 synthetic microgravity physiological samples. It functions as an anomaly detector, not a generative language model.
- **LLM Integration Status:** The codebase includes `LLMAdvisorStub` in `backend/app/advisor.py` as an architectural interface stub demonstrating how future edge-quantized language models (e.g., Med-Gemma) can be plugged in. **No external generative AI API or live LLM service is connected in the active prototype.**
- **NASA Branding & Insignia Integrity:** Generative AI was **never** used to create, redraw, alter, or fabricate NASA logos, insignia, flags, or mission patches. All visual branding consists of original Dr D graphics.

---

## G. DEMONSTRATION GUIDE

### Option 1 — 30-Second Screen-Recording Script

| Timestamp | Visual Action on Screen | Voiceover / Narration Script |
| :--- | :--- | :--- |
| **00:00–00:05** | Open `http://localhost:5173`. Quick-login as **Flight Surgeon**. Show dark futuristic Mission Control HUD with Sol 142 counter and 4-crew roster. | *"Meet Dr D — Not to Get Doomed in Space: an autonomous astronaut health intelligence system built for deep-space missions."* |
| **00:05–00:10** | Pan across the 4 crew cards showing real-time heart rate sparklines and concurrent ECLSS cabin environmental telemetry. | *"Operating on spacecraft edge avionics, Dr D continuously monitors crew vitals and cabin life support without cloud reliance."* |
| **00:10–00:15** | Click Commander Sarah Chen's card to open Astronaut Detail. Highlight the **Health Risk Index (HRI)** gauge and 30-minute predictive forecast. | *"Our explainable Health Risk Index decomposes multi-variable stress, while predictive forecasting flags threshold breaches in advance."* |
| **00:15–00:22** | Click glowing amber **DEMO SCENARIOS** button. Inject **Cabin CO2 Spike** (or **Solar Storm**). Dismiss modal and observe flashing crimson alert banner. | *"When an emergency strikes—like this cabin CO2 spike—Dr D triggers immediate sub-second audio-visual alerts and updates risk scores."* |
| **00:22–00:27** | Click **RESEARCH CONTEXT** on the alert banner to expand the NASA HRP hazard panel and clinical action countermeasure. | *"Every alert is mapped directly to NASA Human Research Program hazards, explaining the clinical impact and recommended countermeasure."* |
| **00:27–00:30** | Click **NASA Research** in the navbar to showcase the 7-section repository, and conclude. | *"Grounded in NASA evidence reports, Dr D ensures astronauts never get doomed in deep space."* |

---

### Option 2 — Seven-Slide Presentation Outline

#### Slide 1 — Title and Project Introduction
- **Slide Title:** Dr D: Not to Get Doomed in Space — Astronaut Health Intelligence System
- **Main Content:**
  - An intelligent, edge-first astronaut health-monitoring, anomaly detection, and clinical decision support system.
  - NASA Space Apps Challenge — *Create Health Monitoring Software for Astronauts on Space Missions*.
  - Mission Architecture: Ares-V 4-person crew transiting to Mars (Sol 142 of 540, 78.4M km from Earth).
- **Visual Elements:** Application login portal, mission badge, and high-level platform summary.
- **Presenter Explanation:** "Welcome to Dr D. When human crews venture to Mars, real-time medical help from Earth is impossible. Dr D acts as their autonomous health guardian beyond Earth."

#### Slide 2 — Problem Statement: The Reality of Interplanetary Medicine
- **Slide Title:** The Deep Space Clinical Challenge: Communication Latency & Multi-System Deconditioning
- **Main Content:**
  - Up to 22-minute one-way communication latency (44 minutes round-trip) precludes Earth-based telemedicine during acute emergencies.
  - Multi-system spaceflight hazards: cephalad fluid shifts (SANS risk), bone/muscle loss, cosmic ionizing radiation, and closed-cabin ECLSS atmospheric pocketing.
  - The critical need for onboard, autonomous clinical decision support that operates without terrestrial cloud servers.
- **Visual Elements:** Latency timeline graphic (Earth to Mars distance comparison) and NASA spaceflight hazard icons.
- **Presenter Explanation:** "At 80 million kilometers from Earth, ground control cannot guide acute surgical interventions. When a life-support failure occurs, the spacecraft itself must possess the intelligence to detect, predict, and guide response."

#### Slide 3 — Proposed Solution: Autonomous Health Intelligence Platform
- **Slide Title:** Dr D: Unified Biomedical Telemetry, Risk Modeling & Clinical Decision Support
- **Main Content:**
  - Edge-first architecture designed for onboard spacecraft avionics with zero cloud dependencies.
  - Continuous physiological telemetry ingestion (HR, HRV, SpO2, BP, Temp, Resp, Stress) paired with ECLSS cabin atmospheric telemetry.
  - Unsupervised machine learning anomaly detection paired with individualized baseline Z-score tracking.
  - Transparent data provenance distinguishing synthetic telemetry from NASA scientific research references.
- **Visual Elements:** 4-tier decoupled system architecture diagram and data pipeline flow.
- **Presenter Explanation:** "Dr D is a complete end-to-end platform combining real-time vital ingestion, machine learning anomaly detection, explainable risk scoring, and clinical decision support into a single pane of glass."

#### Slide 4 — System Architecture & Core Technology Stack
- **Slide Title:** Decoupled Edge Architecture Aligned with NASA ExMC Standards
- **Main Content:**
  - **Backend:** Python 3.13, FastAPI REST, Starlette WebSockets (1–2 Hz telemetry), SQLAlchemy 2.0 ORM, SQLite (`dr_d.db`).
  - **Analytics:** Scikit-learn (Isolation Forest), NumPy, Pandas, SciPy linear/exponential predictive forecaster.
  - **Frontend:** React 18 SPA, Vite, Tailwind CSS aerospace HUD styling, Recharts visualization, Lucide icons.
  - **Verification:** 35 passing Pytest unit/integration tests and production Vite build.
- **Visual Elements:** High-level component topology diagram and technology stack badges.
- **Presenter Explanation:** "Engineered in strict alignment with NASA ExMC Clinical Decision Support Architecture recommendations (HRP-48032 Rev. B), our software footprint is lightweight, robust, and fully functional offline."

#### Slide 5 — Live Application Demonstration: Operations HUD & Explainable Risk
- **Slide Title:** Mission Control Operations HUD, Biometrics Silhouette & Health Risk Index
- **Main Content:**
  - **Fleet Triage:** Instantaneous surveillance of all 4 astronauts with live sparklines and status badges.
  - **Interactive Anatomical Silhouette:** Highlights localized organ systems experiencing acute strain.
  - **Explainable Health Risk Index (HRI 0–100):** Decomposed into Cardiovascular, Hypoxia, Thermal, Circadian, and Environmental factors with plain-language clinical rationales.
  - **30-Minute Predictive Horizon Forecast:** Projects vital trends to preempt safety threshold breaches before decompensation occurs.
- **Visual Elements:** High-resolution screenshots of Mission Control HUD, Astronaut Biometrics Console, and HRI Gauge.
- **Presenter Explanation:** "Here is Dr D in action: flight surgeons and crew medical officers obtain instantaneous situational awareness. The HRI is explainable—no black boxes—showing exactly which physiological factors contribute to risk."

#### Slide 6 — Emergency Simulation & NASA Research Integration
- **Slide Title:** Dynamic Crisis Injection & Grounding in NASA Human Research Program
- **Main Content:**
  - **6 Spaceflight Emergency Scenarios:** Cabin CO2 Spike, EVA Cardiac Stress, Solar Particle Storm, Sleep Deprivation, Dehydration, and Biosensor Dropout.
  - **Research-to-Alert Context Panels:** Every alert links simulated conditions to NASA HRP hazards, potential clinical implications, and official publication references.
  - **Integrated Knowledge Repository:** Dedicated 7-section repository incorporating NASA's 5 hazards, evidence reports, EIMO ConOps (TP-20240001402), and the IMPACT 1.0 119-condition taxonomy.
- **Visual Elements:** Screenshots of the Crisis Injection Modal, Critical Red Alert State, and NASA Research & Evidence repository.
- **Presenter Explanation:** "With our simulation engine, evaluators can inject realistic spaceflight contingencies. Telemetry tells the crew what is happening; our integrated NASA research layer explains why it matters scientifically and guides the exact countermeasure."

#### Slide 7 — Impact, Limitations & Path to Flight
- **Slide Title:** Astronaut Safety, Operational Autonomy & Exploration Roadmap
- **Main Content:**
  - **Clinical Impact:** Preserves life, prevents mission-abort scenarios, and supports crew cognitive resilience during deep-space transit to Mars.
  - **Limitations & Transparency:** Prototype uses synthetic telemetry; not a certified clinical device; no live NASA hardware connected.
  - **Path to Flight Readiness:** Integration with flight-certified wearable biosensors (CSA Bio-Monitor), offline quantized Small Language Models (Med-Gemma), and planetary surface gravity transition protocols.
- **Visual Elements:** Mobile handheld viewport screenshot, technical report preview (`docs/DrD_Project_Report.pdf`), and summary roadmap.
- **Presenter Explanation:** "Dr D transforms deep space medicine from reactive ground triage to proactive onboard guardianship. Tested, verified, and scientifically grounded, Dr D is ready to protect the next generation of space explorers."
