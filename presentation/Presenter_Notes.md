# Dr D – Not to Get Doomed in Space
## NASA Space Apps Challenge — 7-Slide Project Demonstration Script & Presenter Notes

**Challenge:** Create Health Monitoring Software for Astronauts on Space Missions  
**Target Presentation Time:** 3 to 4 minutes (~30–35 seconds per slide)  
**Tone:** Confident, professional, technically precise, and mission-oriented  

---

### Slide 1: Project Introduction
**Slide Title:** Dr D – Not to Get Doomed in Space  
**Subtitle:** Autonomous Astronaut Health Monitoring & Early-Warning Intelligence System  
**Visual Reference:** [`01_login.png`](../docs/screenshots/01_login.png) — Secure Mission Authentication & System Identity  
**Duration:** ~30 seconds  

#### Spoken Script:
> "Good day, judges and space medicine enthusiasts. This is **Dr D – Not to Get Doomed in Space**, an autonomous astronaut health monitoring and early-warning intelligence platform developed for the NASA Space Apps Challenge.
>
> On deep space missions—such as an Ares-V crew transit to Mars—radio communication latency can reach up to 22 minutes each way. When an astronaut experiences an acute medical emergency, waiting 44 minutes for mission control on Earth is not an option. Crew autonomy is vital.
>
> Dr D bridges this gap. It is an intelligent clinical decision support platform that combines multi-parameter physiological monitoring, spacecraft life-support telemetry, machine-learning anomaly detection, and NASA-grounded medical decision protocols into a unified command dashboard. Let's inspect the system in action."

---

### Slide 2: Mission Control Dashboard
**Slide Title:** One Dashboard. Complete Crew Health Awareness.  
**Subtitle:** Mission-wide biometric telemetry, cabin ECLSS monitoring, and fleet status indicators  
**Visual Reference:** [`02_dashboard_nominal.png`](../docs/screenshots/02_dashboard_nominal.png) — Real-Time Fleet Telemetry & ECLSS Panel  
**Duration:** ~30 seconds  

#### Spoken Script:
> "Here is our central Mission Control Dashboard. Designed for flight surgeons and crew medical officers, it provides complete physiological and environmental situational awareness at a single glance.
>
> Across the top, we see the four Ares-V crew members, each with real-time biometric feeds—including heart rate, heart rate variability, blood oxygen saturation, blood pressure, core temperature, respiratory rate, and stress index.
>
> Concurrently, the bottom panel monitors cabin life-support conditions directly from the Environmental Control and Life Support System (ECLSS)—tracking cabin CO₂, oxygen concentration, atmospheric pressure, temperature, humidity, and acoustics.
>
> Under nominal conditions, green status badges confirm that all crew metrics remain safely aligned with individual baseline profiles."

---

### Slide 3: Individual Astronaut Monitoring
**Slide Title:** Every Astronaut. Every Vital Sign.  
**Subtitle:** Deep-dive physiological telemetry, personalized statistical baselines, and anatomical mapping  
**Visual Reference:** [`03_astronaut_detail.png`](../docs/screenshots/03_astronaut_detail.png) — Anatomical Sensor Map & Individual Vitals  
**Duration:** ~30 seconds  

#### Spoken Script:
> "When an individual crew member requires detailed clinical evaluation, clicking their profile opens the Astronaut Detail view, shown here for Commander Chen.
>
> Rather than relying on rigid population averages, Dr D tracks personalized statistical baselines using Z-score deviation analysis. Microgravity induces profound physiological restructuring—such as cephalic fluid redistribution, baroreceptor resetting, and resting heart rate shifts. Evaluating an astronaut against their own baseline is vital for detecting early decompensation.
>
> The anatomical body map visualizes active sensor placement across cardiovascular, respiratory, and autonomic systems, paired with historical trend graphs, daily check-in logs, and customized crew self-care recommendations."

---

### Slide 4: Intelligent Health Risk Analysis
**Slide Title:** From Raw Telemetry to Early Warnings.  
**Subtitle:** Composite Health Risk Index (0–100 scale) and 30-minute predictive autoregressive forecasting  
**Visual Reference:** [`04_risk_index_gauge.png`](../docs/screenshots/04_risk_index_gauge.png) & [`05_forecast_overlay.png`](../docs/screenshots/05_forecast_overlay.png) — Split Screen  
**Duration:** ~35 seconds  

#### Spoken Script:
> "Streaming dozens of raw telemetry numbers can overwhelm a lone flight surgeon. Dr D transforms raw sensor data into explainable clinical intelligence through two analytical engines: the Health Risk Index and Predictive Forecasting.
>
> On the left, the Health Risk Index computes a continuous composite score from 0 to 100. It fuses five distinct hazard dimensions: cardiovascular strain, hypoxia risk, thermal stress, circadian fatigue, and cabin life-support toxicity. This provides instant risk stratification without presenting an unverified black-box diagnosis.
>
> On the right, predictive forecasting uses autoregressive trend projections to forecast vitals 30 minutes ahead, highlighting potential threshold violations before they occur. Simultaneously, an unsupervised Isolation Forest identifies multivariate anomalies—detecting subtle correlations between declining HRV, rising CO₂, and elevated core temperature that single-threshold monitors miss."

---

### Slide 5: Live Emergency Simulation
**Slide Title:** What Happens When an Emergency Occurs?  
**Subtitle:** Dynamic simulation engine: Six realistic spaceflight contingencies with research-grounded dynamics  
**Visual Reference:** [`10_demo_matrix_modal.png`](../docs/screenshots/10_demo_matrix_modal.png) — Emergency Scenario Injection Matrix  
**Duration:** ~35 seconds  

#### Spoken Script:
> "To rigorously evaluate system readiness, Dr D features an interactive spaceflight emergency simulation engine capable of triggering six realistic mission contingencies.
>
> These include life support failures like cabin CO₂ spikes, extravehicular cardiac over-exertion, solar particle radiation storms, chronic sleep deprivation, microgravity dehydration, and biometric lead disconnects. Each scenario drives mathematically modeled physiological and environmental changes in real time.
>
> *(Live Demo Transition)*: To demonstrate this live in the application: in the top navigation bar, click the 'Demo Matrix' button. In the modal that opens, select 'Cabin CO₂ Spike' and click 'Inject Scenario'.
>
> Instantly, the simulation engine elevates ambient CO₂ from nominal 0.4% up to 1.5%, triggering immediate respiratory rate elevation, cognitive fatigue indices, and autonomic stress responses across the crew. Let's see how the alert system responds."

---

### Slide 6: Alerts and Medical Decision Support
**Slide Title:** Detect. Alert. Respond.  
**Subtitle:** Closed-loop incident management: Severity triaging, clinical action checklists, and mission dossier export  
**Visual Reference:** [`11_dashboard_critical_scenario.png`](../docs/screenshots/11_dashboard_critical_scenario.png) & [`12_reports_dossier.png`](../docs/screenshots/12_reports_dossier.png) — Critical Alert & Report Generation  
**Duration:** ~35 seconds  

#### Spoken Script:
> "The moment the emergency is injected, Dr D executes a closed-loop incident management sequence.
>
> As seen on the left dashboard, the crew Health Risk Index surges into the CRITICAL band at 78 out of 100. High-priority red alert banners and audio cues immediately flag the severe hypercapnia event.
>
> Critically, Dr D is not just an alarm; it is an active clinical decision support system. Grounded in NASA Human Research Program evidence, the alert expands to deliver step-by-step countermeasure protocols: immediately donning emergency oxygen masks, activating secondary LiOH scrubbing beds, and venting cabin sectors.
>
> Once the emergency is controlled, as shown in the top right dossier view, the medical officer generates a comprehensive, timestamped clinical incident report with complete biometric telemetry graphs, ready to burst-transmit back to Houston once communication is re-established."

---

### Slide 7: How It Works & Project Takeaway
**Slide Title:** Your Health Guardian Beyond Earth.  
**Subtitle:** Autonomous architecture, modern technology stack, and core mission takeaways  
**Visual Reference:** Architecture Pipeline & Core Summary Cards  
**Duration:** ~35 seconds  

#### Spoken Script:
> "Under the hood, Dr D is built on a resilient, modular architecture. A high-performance FastAPI backend ingests simulated biometric and ECLSS telemetry, executes real-time Isolation Forest anomaly detection and composite Health Risk Index calculations, and streams updates via WebSockets directly into a reactive React 18 mission control interface.
>
> To summarize, Dr D delivers three pivotal innovations for human spaceflight:
> First, complete multi-parameter crew and environmental awareness.
> Second, early warning intelligence combining individual statistical baselines with machine learning.
> And third, autonomous clinical decision support that empowers astronaut crews when Earth is light-minutes away.
>
> Dr D: Not to Get Doomed in Space. Your health guardian beyond Earth. Thank you, and we welcome your questions!"

---

### Presenter Checklist Before Demonstration
- [ ] Backend running (`http://127.0.0.1:8000/docs` responding).
- [ ] Frontend running (`http://localhost:5173` loaded).
- [ ] User logged in as Flight Surgeon (`surgeon` / `Password123!`).
- [ ] Browser window set to full-screen (F11) on nominal dashboard.
- [ ] Demo Matrix tested once to ensure smooth scenario injection.
