# Dr D — NASA Executive Pitch & Technical Presentation Outline

**Document Reference:** NASA-HRP-ExMC-2026-DRD-SLIDES-REV2  
**Title:** Dr D: Autonomous Astronaut Health Monitoring and Early-Warning System  
**Audience:** NASA Flight Surgeons, Mission Directors, Exploration Medical Capability (ExMC) Working Group, Biomedical Engineers  
**Mission Architecture:** Ares-V Deep Space Transit (Mars Transit Sol 142 of 540)  
**Tagline:** *"Your health guardian beyond Earth."*  
**Research Attribution:** Grounded in NASA Human Research Program (HRP) & Exploration Medical Capability (ExMC) publications  

---

## Slide 1: Title & Operational Mission Context
- **Slide Title:** Dr D: Autonomous Health Intelligence System for Deep Space Exploration
- **Target Visual:** `docs/screenshots/01_login.png` & original Dr D mission badge
- **Key Talking Points:**
  - Introduce **Dr D — Not to Get Doomed in Space**: an intelligent astronaut health-monitoring, anomaly detection, risk assessment, and clinical decision support system.
  - Engineered specifically for long-duration interplanetary space missions (such as Mars transit, Sol 142 of 540, 78.4M km from Earth, 4.2s to 22m comm latency).
  - Role-based operational access: Flight Surgeon (fleet overview, alert triage, archival dossier export), Crew Commander (isolated personal telemetry), Flight Engineer (EVA recovery), Science Specialist, and Mission Administrator.
  - Transparent data provenance: Continuous biometric telemetry is synthetic/simulated; clinical evidence is derived from official NASA scientific technical publications.
- **Takeaway:** Dr D bridges the critical capability gap between Earth-dependent telemedicine and complete crew autonomy in deep space.

---

## Slide 2: The Deep Space Clinical Challenge & Latency Barrier
- **Slide Title:** The Reality of Interplanetary Medicine: Communication Delays & Deconditioning
- **Target Visual:** Split comparison graphic / `docs/diagrams/data_flow_diagram.png`
- **Key Talking Points:**
  - **Communication Blackout / Latency:** Electromagnetic signal delay ranges from 3.2 minutes to 22.0 minutes one-way (up to 44 minutes round-trip), precluding real-time ground surgical guidance or interactive telemedicine during acute emergencies.
  - **Multi-System Physiological Hazards (NASA HRP):** Microgravity-induced cephalic fluid shift (~15% plasma volume loss, optic disc edema / SANS risk), myocardial deconditioning, and 1.0–1.5% monthly bone mineral density loss.
  - **Unpredictable Closed-Cabin Contingencies:** Closed-loop ECLSS scrubber saturation (CO2 surges >2,000 ppm) and Solar Particle Events (SPE dose rates >0.45 mSv/min).
- **Takeaway:** When ground telemetry is delayed by 40 minutes, the spacecraft must host an autonomous, clinical-grade early-warning guardian.

---

## Slide 3: System Architecture & NASA ExMC Alignment
- **Slide Title:** Edge-First Flight Architecture Aligned with NASA ExMC Standards
- **Target Visual:** `docs/diagrams/architecture_diagram.png`
- **Key Talking Points:**
  - 4-Tier decoupled architecture aligned with NASA ExMC Clinical Decision Support Architecture Recommendation (HRP-48032 Rev. B) and Earth-Independent Medical Operations (EIMO TP-20240001402):
    1. **Simulation & Telemetry Layer:** High-fidelity 12+ channel vital synthesis, diurnal circadian oscillation, Gaussian sensor jitter, and 6 calibrated emergency scenario overrides.
    2. **Ingestion & Comms:** FastAPI REST engine, Pydantic V2 validation, sliding-window authentication rate limiter (5 attempts/min), and 1–2 Hz Starlette WebSocket streaming.
    3. **Intelligence & Analytics Core:** Unsupervised Scikit-learn Isolation Forest model, individualized rolling Z-scores, linear/exponential predictive forecaster, and rule-based Dr D Advisor.
    4. **Persistence & Operations HUD:** SQLAlchemy 2.0 ORM (`dr_d.db`), React 18, Tailwind CSS, Recharts, and automated PDF dossier export.
  - **Zero Cloud Reliance:** Lightweight, resilient computational footprint capable of running locally without cloud dependencies or paid APIs.
- **Takeaway:** Edge-first architecture designed from inception for deep-space autonomous avionics.

---

## Slide 4: Mission Control Operations HUD & Fleet Telemetry
- **Slide Title:** Fleet-Level Triage & Multi-Crew Physiological Surveillance
- **Target Visual:** `docs/screenshots/02_dashboard_nominal.png`
- **Key Talking Points:**
  - Instantaneous fleet overview of all 4 Ares-V astronauts: Commander Sarah Chen, Science Lead Marcus Vance, Flight Engineer Elena Rostova, and Medical Specialist Alex Rivera.
  - Live sparkline micro-charts displaying instantaneous cardiovascular and respiratory trajectories updated via sub-second WebSocket frames.
  - Concurrent spacecraft ECLSS telemetry display: cabin CO2 (ppm), O2 (%), cabin pressure (kPa), ambient temperature (°C), humidity, and acoustic noise (dB).
  - Explicit data provenance indicators: clear `SIMULATED DATA` labels ensure clinical evaluators distinguish simulated telemetry from real astronaut measurements.
- **Takeaway:** Flight Surgeons obtain instantaneous situational awareness across both human physiology and life-support systems on a single pane of glass.

---

## Slide 5: Explainable Health Risk Index (HRI) & Forecaster
- **Slide Title:** Explainable Composite Risk Scoring (0–100) & Predictive Forecasting
- **Target Visual:** `docs/screenshots/04_risk_index_gauge.png` & `docs/screenshots/05_forecast_overlay.png`
- **Key Talking Points:**
  - Composite Health Risk Index (HRI) formula combining weighted physiological domains with peak-factor amplification:
    $$\text{HRI} = 0.60 \sum (w_i s_i) + 0.35 \max(s_i) + 0.05 \, \text{Score}_{\text{IsolationForest}}$$
  - Five domain factors: Cardiovascular ($w=0.28$), Hypoxia ($w=0.28$), Thermoregulatory ($w=0.16$), Stress/Circadian ($w=0.14$), and Environmental Strain ($w=0.14$).
  - **No Black Boxes:** Plain-language explainability banner stating exact root causes (e.g., *"Risk elevated due to hypoxia risk (SpO2 91.2%) + cardiac strain (138 bpm) + elevated cabin CO2"*).
  - **30-Minute Predictive Horizon:** Combined linear regression and exponential smoothing projecting when vital parameters will cross warning or critical boundaries before clinical manifestation.
- **Takeaway:** Transparent, auditable algorithmic reasoning paired with proactive breach prevention.

---

## Slide 6: Emergency Simulation & Research-to-Alert Context
- **Slide Title:** Dynamic Crisis Injection & Scientific Research Mapping
- **Target Visual:** `docs/screenshots/10_demo_matrix_modal.png` & `docs/screenshots/11_dashboard_critical_scenario.png`
- **Key Talking Points:**
  - Interactive demonstration modal supporting 6 acute crisis scenarios:
    1. *Cabin CO2 Spike* (scrubber saturation past 2,100 ppm, compensatory tachycardia)
    2. *EVA Cardiac Stress* (metabolic workload tachycardia to 138 bpm, HRV collapse)
    3. *Solar Particle Event* (coronal mass ejection ionizing dose accumulation at 0.45 mSv/min)
    4. *Cumulative Sleep Deprivation* (circadian disruption, sympathetic stress index to 84)
    5. *Dehydration & Fluid Shift* (hypovolemic hypotension to 102/70 mmHg)
    6. *Biosensor Telemetry Dropout* (optical pulse-oximeter lead disconnect simulation)
  - **Research Context Panels (Part 6):** Every alert and scenario card features an expandable scientific panel explaining:
    - *Detected Condition:* What is happening in simulated telemetry.
    - *NASA Hazard:* Radiation, Isolation, Distance, Gravity, or Environment.
    - *Potential Health Implications:* Clinical risks based on NASA HRP evidence.
    - *Scientific Reference:* Official NASA HRP publication citation.
    - *Data Provenance:* Tagged unambiguously as Synthetic Telemetry.
- **Takeaway:** Telemetry tells the crew *what* is happening; NASA scientific research explains *why* it matters and *how* to respond.

---

## Slide 7: NASA Research Knowledge Base, Testing & Impact
- **Slide Title:** NASA Research & Evidence Knowledge Layer, Verification & Path to Flight
- **Target Visual:** NASA Research & Evidence Interface & `docs/DrD_Project_Report.pdf`
- **Key Talking Points:**
  - **Integrated Knowledge Repository:** Dedicated 7-section knowledge base in the application:
    1. Spaceflight Hazards (5 NASA HRP core categories)
    2. Astronaut Health Risks Taxonomy (12 mapped clinical domains)
    3. Scientific Evidence Reports (searchable and linked to telemetry)
    4. Medical Decision-Support Architecture (HRP-48032 Rev. B alignment)
    5. Earth-Independent Medical Operations (EIMO 20240001402 ConOps)
    6. Exploration Medical Conditions (IMPACT 1.0 119-condition taxonomy)
    7. Official NASA Source Library & 5-Category Data Provenance Matrix
  - **Verification & Rigor:** 35 passing backend pytest unit/integration tests; successful Vite production build; 0 external runtime dependencies.
  - **Impact & Ethics:** Empowers deep-space crews to self-triage during 40-minute communication blackouts, preserving life and mission success on the journey to Mars.
- **Takeaway:** Dr D is a scientifically grounded, technically verified, and transparent autonomous health guardian ready for exploration maturation.
