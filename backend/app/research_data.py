"""
Dr D — NASA Scientific Research & Evidence Knowledge Base
Incorporates verified research citations, hazard classifications, evidence reports,
clinical decision support architecture recommendations, EIMO operational concepts,
and Exploration Medical Condition List (IMPACT 1.0) taxonomies.

Sources:
1. NASA Human Research Program – Risks of Human Spaceflight (https://www.nasa.gov/hrp/risks/)
2. NASA Human Research Roadmap – Evidence Reports (https://humanresearchroadmap.nasa.gov/evidence/)
3. NASA ExMC – Clinical Decision Support System Architecture Recommendation, HRP-48032 Rev. B (https://ntrs.nasa.gov/citations/20220017869)
4. NASA ExMC – Earth-Independent Medical Operations (EIMO) Concept of Operations (https://ntrs.nasa.gov/citations/20240001402)
5. NASA ExMC – Evidence Library Methods, HRP-48036 Rev. B (https://ntrs.nasa.gov/citations/20240004774)
"""

from typing import List, Dict, Any

# ==============================================================================
# 1. FIVE NASA SPACEFLIGHT HAZARDS (NASA HRP)
# ==============================================================================
NASA_HAZARDS: List[Dict[str, Any]] = [
    {
        "id": "hazard_radiation",
        "name": "Space Radiation",
        "acronym": "R",
        "description": "Galactic Cosmic Rays (GCR) and Solar Particle Events (SPE) penetrate spacecraft hull materials, delivering ionizing doses that damage DNA, elevate lifetime excess cancer risk, and induce acute degenerative cellular changes.",
        "dr_d_representation": "ACTIVE_MONITORING",
        "dr_d_features": ["Cumulative Radiation Dosimeter (mSv)", "Solar Particle Event (SPE) Crisis Scenario", "Mission Long-Duration Trends"],
        "hrp_reference": "NASA HRP Space Radiation Element; Human Research Roadmap Evidence Report on Degenerative Tissue Risks",
        "source_url": "https://www.nasa.gov/hrp/risks/",
        "physiological_systems": ["Hematopoietic", "Cardiovascular", "Central Nervous System"]
    },
    {
        "id": "hazard_isolation",
        "name": "Isolation and Confinement",
        "acronym": "I",
        "description": "Small crews living in constrained spacecraft volume during multi-year missions face sensory monotony, sleep architecture disruption, circadian desynchronization, and prolonged interpersonal psychosocial stress.",
        "dr_d_representation": "ACTIVE_MONITORING",
        "dr_d_features": ["Daily Astronaut Subjective Check-in", "Circadian Disruption Score (0-100)", "Sleep Quality Tracking", "Cumulative Sleep Deprivation Crisis Scenario"],
        "hrp_reference": "NASA HRP Behavioral Health and Performance (BHP) Element; Sleep & Circadian Evidence Report",
        "source_url": "https://www.nasa.gov/hrp/risks/",
        "physiological_systems": ["Neuro-Cognitive", "Autonomic Nervous System", "Circadian Pacemaker"]
    },
    {
        "id": "hazard_distance",
        "name": "Distance from Earth",
        "acronym": "D",
        "description": "As missions traverse toward Mars (up to 400M km), communication latency expands to 22 minutes one-way (44 minutes round-trip), completely precluding real-time telemedicine or Earth-guided emergency surgery and necessitating onboard autonomous decision support.",
        "dr_d_representation": "ACTIVE_MONITORING",
        "dr_d_features": ["Simulated Comm Delay Tracker (4.2s Sol 142 -> 22m Sol 400)", "Autonomous Dr D Advisor Recommendations", "Edge-First Local Analytics Core"],
        "hrp_reference": "NASA Exploration Medical Capability (ExMC) Element; EIMO Concept of Operations (20240001402)",
        "source_url": "https://ntrs.nasa.gov/citations/20240001402",
        "physiological_systems": ["Systemic / Autonomous Operations"]
    },
    {
        "id": "hazard_gravity",
        "name": "Altered Gravity Fields",
        "acronym": "G",
        "description": "Weightlessness eliminates hydrostatic blood pressure gradients, causing cephalad fluid redistribution (~1.5-2.0L shift toward upper torso and head), muscular atrophy (~1-2% monthly), skeletal osteopenia (~1.0% bone mineral loss monthly), and neuro-vestibular disorientation.",
        "dr_d_representation": "ACTIVE_MONITORING",
        "dr_d_features": ["Fluid Shift Score (0-100)", "Bone Mineral Density Trajectory", "Muscle Mass Index", "Dehydration & Fluid Shift Crisis Scenario", "Anatomical Silhouette Organ Hotspots"],
        "hrp_reference": "NASA HRP Human Factors and Behavioral Performance (HFBP); Cardiovascular & SANS Evidence Reports",
        "source_url": "https://humanresearchroadmap.nasa.gov/evidence/",
        "physiological_systems": ["Musculoskeletal", "Cardiovascular", "Neuro-Ocular (SANS)"]
    },
    {
        "id": "hazard_environment",
        "name": "Hostile and Closed Environments",
        "acronym": "E",
        "description": "Spacecraft life support systems (ECLSS) maintain a sealed artificial atmosphere where CO2 accumulation, particulate pocketing, trace contaminant buildup, microbial blooms, and acoustic noise pose acute and chronic health hazards.",
        "dr_d_representation": "ACTIVE_MONITORING",
        "dr_d_features": ["Spacecraft Cabin ECLSS Telemetry (CO2, O2, Pressure, Temp, Noise)", "Cabin CO2 Spike Crisis Scenario", "Environmental Risk Factor in HRI"],
        "hrp_reference": "NASA HRP Evidence Report on Hostile Spacecraft Cabin Atmosphere; NASA STD-3001 Vol 2",
        "source_url": "https://humanresearchroadmap.nasa.gov/evidence/",
        "physiological_systems": ["Respiratory", "Cardiopulmonary", "Acoustic / Vestibular"]
    }
]

# ==============================================================================
# 2. ASTRONAUT HEALTH RISKS TAXONOMY (NASA HRP)
# ==============================================================================
NASA_HEALTH_RISKS: List[Dict[str, Any]] = [
    {
        "id": "risk_cardiovascular",
        "name": "Cardiovascular Adaptations & Deconditioning",
        "hazard_id": "hazard_gravity",
        "status": "MONITORED_IN_DR_D",
        "summary": "Microgravity eliminates head-to-toe hydrostatic pressure gradient, inducing blood volume reduction, baroreceptor resetting, left ventricular mass decrement, and post-flight orthostatic intolerance.",
        "monitored_metrics": ["Heart Rate (bpm)", "HRV (RMSSD ms)", "Blood Pressure Systolic/Diastolic (mmHg)"],
        "dr_d_module": "Cardiovascular Autonomic Load (HRI factor $w=0.28$); EVA Cardiac Stress scenario",
        "citation": "NASA HRP Cardiovascular Evidence Report (Human Research Roadmap)"
    },
    {
        "id": "risk_hypoxia_respiratory",
        "name": "Spacecraft Atmosphere Hypoxia & Hypercapnia",
        "hazard_id": "hazard_environment",
        "status": "MONITORED_IN_DR_D",
        "summary": "Closed spacecraft cabin dynamics expose astronauts to elevated partial pressures of CO2 (often >2,000 ppm during scrubber maintenance) and reduced oxygen fraction, leading to headache, lethargy, cognitive decrements, and compensatory hyperventilation.",
        "monitored_metrics": ["Blood Oxygen Saturation (SpO2 %)", "Respiratory Rate (br/min)", "Cabin CO2 (ppm)", "Cabin O2 (%)"],
        "dr_d_module": "Oxygen Saturation & Ventilation (HRI factor $w=0.28$); Cabin CO2 Spike scenario",
        "citation": "NASA HRP Hostile Atmosphere Evidence Report; NASA STD-3001"
    },
    {
        "id": "risk_sleep_circadian",
        "name": "Sleep Loss & Circadian Rhythm Disruption",
        "hazard_id": "hazard_isolation",
        "status": "MONITORED_IN_DR_D",
        "summary": "Absence of natural 24-hour diurnal sunlight cycles, 90-minute orbital lighting variations, and mission task overload degrade slow-wave sleep and suppress melatonin rhythmicity, elevating neuro-cognitive error rates.",
        "monitored_metrics": ["Sleep Quality (0-100)", "Sleep Hours", "Cognitive Fatigue Score", "Stress Index (0-100)"],
        "dr_d_module": "Stress & Circadian Rhythm Disruption (HRI factor $w=0.14$); Daily Subjective Check-in",
        "citation": "NASA HRP Sleep and Circadian Evidence Report"
    },
    {
        "id": "risk_space_radiation",
        "name": "Cosmic Ionizing Radiation & Acute Solar Events",
        "hazard_id": "hazard_radiation",
        "status": "MONITORED_IN_DR_D",
        "summary": "Beyond Earth's magnetosphere, galactic cosmic rays and sudden solar proton events deliver ionizing dose without geomagnetic deflection. Acute exposure may induce nausea, prodromal sickness, and immunosuppression, while chronic accumulation elevates career cancer risk.",
        "monitored_metrics": ["Cumulative Dose (mSv)", "Radiation Limit Tracking (600 mSv career cap)"],
        "dr_d_module": "Solar Particle Event (SPE) crisis scenario (+0.45 mSv/min); Multi-Sol Mission Trend projection",
        "citation": "NASA HRP Space Radiation Health Risks Evidence Report"
    },
    {
        "id": "risk_musculoskeletal",
        "name": "Bone Mineral Loss & Skeletal Muscle Deconditioning",
        "hazard_id": "hazard_gravity",
        "status": "MONITORED_IN_DR_D",
        "summary": "Unloading of weight-bearing bones causes osteoclastic resorption outstripping osteoblastic synthesis, resulting in 1.0-1.5% cancellous bone density loss per month in trochanter and spine, accompanied by postural muscle fiber atrophy.",
        "monitored_metrics": ["Bone Density Loss %", "Muscle Mass Retention Index %"],
        "dr_d_module": "Mission Trends Dashboard; ARED exercise compliance tracker in medical notes",
        "citation": "NASA HRP Bone and Muscle Loss Evidence Reports"
    },
    {
        "id": "risk_fluid_shift_sans",
        "name": "Cephalad Fluid Shift & SANS (Neuro-Ocular Syndrome)",
        "hazard_id": "hazard_gravity",
        "status": "MONITORED_IN_DR_D",
        "summary": "Cephalad venous engorgement and elevated internal jugular pressure contribute to optic disc edema, globe flattening, choroidal folds, and hyperopic refractive shifts collectively termed SANS.",
        "monitored_metrics": ["Fluid Shift Index (0-100)", "Facial Edema Risk", "LBNP Countermeasure Protocol"],
        "dr_d_module": "Astronaut Detail Anatomical Silhouette; Dehydration & Fluid Shift crisis scenario",
        "citation": "NASA HRP SANS Evidence Report (2020 Revision)"
    },
    {
        "id": "risk_immune_dysfunction",
        "name": "Immune System Alterations & Viral Reactivation",
        "hazard_id": "hazard_isolation",
        "status": "RESEARCH_REFERENCE_ONLY",
        "summary": "Multi-factorial spaceflight stressors alter T-cell function, reduce delayed-type hypersensitivity responses, and trigger subclinical reactivation of latent herpesviruses (EBV, VZV, CMV).",
        "monitored_metrics": ["Documented via Clinical Notes & ExMC Reference"],
        "dr_d_module": "Research Library reference; Future Biomarker Ingestion Scope",
        "citation": "NASA HRP Immune System Changes Evidence Report"
    },
    {
        "id": "risk_microbiome_dysbiosis",
        "name": "Microbiome Alterations & Virulence Shift",
        "hazard_id": "hazard_environment",
        "status": "RESEARCH_REFERENCE_ONLY",
        "summary": "Enclosed environmental contact and sterile diets decrease microbial diversity of skin, gut, and nasal mucosa while altering bacterial antibiotic resistance profiles.",
        "monitored_metrics": ["Documented via Clinical Notes & ExMC Reference"],
        "dr_d_module": "Research Library reference; Future Sequencing Pipeline Scope",
        "citation": "NASA HRP Human Microbiome Evidence Report"
    },
    {
        "id": "risk_decompression_sickness",
        "name": "Decompression Sickness (DCS) during EVA",
        "hazard_id": "hazard_environment",
        "status": "MONITORED_IN_DR_D",
        "summary": "Transitions from spacecraft cabin pressure (101.3 kPa) to EMU spacesuit pressure (29.6 kPa) generate risk of nitrogen bubble formation in tissues without rigorous 100% O2 pre-breathe washouts.",
        "monitored_metrics": ["EVA Suit Pressure Telemetry", "Pre-breathe Status (STANDBY/ACTIVE)"],
        "dr_d_module": "Mission Control EVA Status; Cabin Environment widget",
        "citation": "NASA STD-3001; NASA HRP EVA Physiology Evidence Report"
    },
    {
        "id": "risk_nutrition_metabolism",
        "name": "Nutritional Depletion & Metabolic Alterations",
        "hazard_id": "hazard_distance",
        "status": "RESEARCH_REFERENCE_ONLY",
        "summary": "Nutrient degradation in packaged space food, altered folate metabolism, and elevated oxidative stress threaten crew caloric and micronutrient sufficiency across a 3-year Mars mission.",
        "monitored_metrics": ["Documented via Clinical Notes & ExMC Reference"],
        "dr_d_module": "Research Library reference; Future Metabolic Sensor Scope",
        "citation": "NASA HRP Food System & Nutrition Evidence Report"
    },
    {
        "id": "risk_landing_injury",
        "name": "Dynamic G-Transition & Landing Injuries",
        "hazard_id": "hazard_gravity",
        "status": "FUTURE_FLIGHT_SCOPE",
        "summary": "Deconditioned crew members returning to planetary gravity fields (0.38g on Mars, 1.0g on Earth) exhibit acute balance ataxia, high susceptibility to spinal loading injury, and syncopal risk.",
        "monitored_metrics": ["Documented via Clinical Notes & ExMC Reference"],
        "dr_d_module": "Research Library reference; Planetary Descent Operations Scope",
        "citation": "NASA HRP Injury and Recovery Following Planetary Landing"
    }
]

# ==============================================================================
# 3. NASA HUMAN RESEARCH ROADMAP EVIDENCE REPORTS (NASA RESOURCE 2)
# ==============================================================================
NASA_EVIDENCE_REPORTS: List[Dict[str, Any]] = [
    {
        "title": "Evidence Report: Risk of Adverse Health Effects Due to Hostile Spacecraft Cabin Atmosphere",
        "nasa_source": "NASA Human Research Program (HRP) Human Research Roadmap",
        "category": "Environmental & Life Support Systems",
        "description": "Examines hypercapnia thresholds, hypoxia onset, and trace contaminant toxicity in closed-loop ECLSS architecture. Demonstrates that ambient CO2 levels exceeding 0.5% (5,000 ppm) cause cognitive deficits and visual disturbances.",
        "physiological_system": "Cardiopulmonary & Neuro-Cognitive",
        "dr_d_feature": "Cabin CO2/O2 Telemetry, Anomaly Detection, Cabin CO2 Spike Scenario",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/"
    },
    {
        "title": "Evidence Report: Risk of Cardiovascular Disease and Orthostatic Intolerance From Spaceflight",
        "nasa_source": "NASA Human Research Program (HRP) Human Research Roadmap",
        "category": "Cardiovascular Autonomic Regulation",
        "description": "Documents cephalic blood shift, fluid loss (~15% plasma volume reduction), post-spaceflight orthostatic intolerance, and cardiac remodeling. Evaluates lower body negative pressure (LBNP) and ergometer countermeasures.",
        "physiological_system": "Cardiovascular & Hemodynamic",
        "dr_d_feature": "Heart Rate, HRV, Blood Pressure, Fluid Shift Score, EVA Cardiac Strain Scenario",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/"
    },
    {
        "title": "Evidence Report: Risk of Performance Decrements Resulting from Sleep Loss and Circadian Desynchronization",
        "nasa_source": "NASA Human Research Program (HRP) Human Research Roadmap",
        "category": "Behavioral Health & Performance (BHP)",
        "description": "Reviews operational sleep logs across Shuttle and ISS crews showing chronic average sleep durations of ~6.0 hours, leading to cognitive degradation, reaction-time slowing, and sympathetic tone hyperactivity.",
        "physiological_system": "Neuro-Psychiatric & Autonomic",
        "dr_d_feature": "Daily Astronaut Check-in, Stress Index, Cumulative Sleep Deprivation Scenario",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/"
    },
    {
        "title": "Evidence Report: Risk of Radiation Carcinogenesis and Acute Radiation Syndromes",
        "nasa_source": "NASA Human Research Program (HRP) Human Research Roadmap",
        "category": "Space Radiation Element",
        "description": "Details exposure limits for deep space exploration architectures, establishing Permissible Exposure Limits (PEL) to restrict career radiation-induced death risk to below 3% at a 95% confidence interval.",
        "physiological_system": "Hematopoietic & Systemic",
        "dr_d_feature": "Cumulative Radiation Meter, Solar Particle Event (SPE) Scenario, Mission Trends",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/"
    },
    {
        "title": "Evidence Report: Risk of Spaceflight Associated Neuro-ocular Syndrome (SANS)",
        "nasa_source": "NASA Human Research Program (HRP) Human Research Roadmap",
        "category": "Cross-Cutting Sensory Systems",
        "description": "Synthesizes clinical observations of papilledema, globe flattening, and hyperopic refractive shift resulting from microgravity cephalad venous congestion and altered trans-lamina cribrosa pressure gradients.",
        "physiological_system": "Neuro-Ophthalmic",
        "dr_d_feature": "Fluid Shift Score, Anatomical Silhouette Organ Hotspots",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/"
    },
    {
        "title": "Evidence Report: Risk of Adverse Health Outcomes and Decrements in Performance due to Inflight Medical Conditions",
        "nasa_source": "NASA Exploration Medical Capability (ExMC)",
        "category": "Exploration Clinical Decision Support",
        "description": "Analyzes medical event probabilities across exploration-class architectures, identifying high-risk clinical categories and justifying autonomous decision support systems.",
        "physiological_system": "Systemic Medical Operations",
        "dr_d_feature": "Health Risk Index (0-100), Isolation Forest Anomaly Detection, Dr D Advisor",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/"
    }
]

# ==============================================================================
# 4. NASA ExMC DECISION SUPPORT SYSTEM ARCHITECTURE (HRP-48032 REV. B)
# ==============================================================================
NASA_CDSS_ARCHITECTURE: Dict[str, Any] = {
    "document_title": "Clinical Decision Support System (CDSS) Architecture Recommendation",
    "document_id": "NASA HRP-48032 Rev. B",
    "publication_year": 2022,
    "official_url": "https://ntrs.nasa.gov/citations/20220017869",
    "core_principles": [
        {
            "layer": "Data Ingestion & Normalization",
            "nasa_recommendation": "Decoupled ingestion of disparate physiological telemetry streams with schema validation, time synchronization, and sensor health telemetry.",
            "dr_d_implementation": "FastAPI REST and Starlette WebSocket ingestion endpoints validating telemetry against Pydantic V2 schemas with microsecond UTC timestamps."
        },
        {
            "layer": "Clinical Inference & Anomaly Detection",
            "nasa_recommendation": "Tiered decision support executing both deterministic boundary rule screening and statistical/machine learning models to detect subtle multi-parameter drift.",
            "dr_d_implementation": "Dual analytical pipeline: Unsupervised Scikit-learn Isolation Forest for multi-parameter anomaly scoring combined with rolling Z-score baseline deviation checks."
        },
        {
            "layer": "Explainable Risk Scoring",
            "nasa_recommendation": "Decision support must be transparent, presenting clinicians with decomposed risk contributors, abnormal physiological parameters, and confidence bounds.",
            "dr_d_implementation": "Composite Health Risk Index (HRI 0-100) decomposed into 5 explainable factors (Cardiovascular, Hypoxia, Thermal, Stress, Environment) with plain-language clinical rationales."
        },
        {
            "layer": "Countermeasure & Recommendation Engine",
            "nasa_recommendation": "Rule-based and protocol-driven countermeasures providing actionable clinical guidance without presenting unverified automated diagnoses.",
            "dr_d_implementation": "Dr D Advisor generating categorized clinical protocols (Urgent Intervention, Physiological Countermeasures, Work-Rest Modification) with expected recovery timelines."
        },
        {
            "layer": "Edge-First Autonomous Operations",
            "nasa_recommendation": "Architecture must operate fully without active connection to terrestrial cloud servers, executing on spacecraft avionics with local persistence.",
            "dr_d_implementation": "Zero external cloud API dependencies; runs locally on standard compute hardware with SQLite persistence and local analytical processing."
        }
    ],
    "disclaimer": "Dr D's software architecture is inspired by and aligned with the architectural recommendations of NASA HRP-48032 Rev. B for exploration decision support, but is not certified or endorsed by NASA ExMC."
}

# ==============================================================================
# 5. NASA ExMC EARTH-INDEPENDENT MEDICAL OPERATIONS (EIMO, 20240001402)
# ==============================================================================
NASA_EIMO_CONOPS: Dict[str, Any] = {
    "document_title": "Earth-Independent Medical Operations (EIMO) Concept of Operations",
    "document_id": "NASA TP-20240001402",
    "publication_year": 2024,
    "official_url": "https://ntrs.nasa.gov/citations/20240001402",
    "operational_pillars": [
        {
            "pillar": "Pre-Mission Individualized Calibration",
            "eimo_concept": "Pre-flight physiological profiling to establish individualized baseline envelopes rather than relying on generic terrestrial population averages.",
            "dr_d_alignment": "Astronaut individual baselines stored in SQLite schema (`baseline_hr`, `baseline_temp`, `baseline_spo2`, `baseline_bp_sys`, `baseline_hrv`)."
        },
        {
            "pillar": "Autonomous Inflight Triage & Incident Response",
            "eimo_concept": "When communication latency exceeds several minutes, the onboard medical system must autonomously detect crises, alert the crew, and guide stabilization.",
            "dr_d_alignment": "Sub-second WebSocket alert generation with audio-visual banner triage (NORMAL, WARNING, CRITICAL) and direct suggested countermeasure instructions."
        },
        {
            "pillar": "Prolonged Medical Care & Trend Forecasting",
            "eimo_concept": "Long-term monitoring of deconditioning and predictive lookahead to anticipate threshold breaches prior to acute clinical deterioration.",
            "dr_d_alignment": "30-minute predictive horizon forecasting with linear regression and exponential dampening, tracking time-to-breach."
        },
        {
            "pillar": "Role-Based Distributed Medical Authority",
            "eimo_concept": "Support dual operational roles: crew medical officer conducting immediate bedside assessment vs ground flight surgeon reviewing historical dossiers.",
            "dr_d_alignment": "Strict Role-Based Access Control (RBAC): Flight Surgeon fleet oversight and dossier export vs Crew Member isolated personal telemetry and check-ins."
        }
    ]
}

# ==============================================================================
# 6. NASA ExMC EXPLORATION MEDICAL CONDITION LIST (IMPACT 1.0, HRP-48036 REV. B)
# ==============================================================================
NASA_EXPLORATION_CONDITIONS: List[Dict[str, Any]] = [
    {
        "condition_id": "EXMC-COND-001",
        "name": "Hypercapnia (Acute / Subacute)",
        "category": "Environmental & Toxicological",
        "system": "Respiratory / Neurological",
        "impact_relevance": "High probability in closed spacecraft environments due to ECLSS scrubber saturation or dead pocket ventilation failure.",
        "dr_d_monitoring": "MONITORED_DIRECTLY",
        "telemetry_stream": "Cabin CO2 concentration (ppm) + Respiratory Rate + SpO2",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue; HRP Evidence Report on Hostile Atmosphere"
    },
    {
        "condition_id": "EXMC-COND-002",
        "name": "Hypoxia / Acute Hypoxemia",
        "category": "Respiratory & Hypobaric",
        "system": "Cardiopulmonary",
        "impact_relevance": "Critical risk during suit operations (EMU/Orion suit depressurization) or cabin O2 scrubber malfunction.",
        "dr_d_monitoring": "MONITORED_DIRECTLY",
        "telemetry_stream": "SpO2 (%) + Respiratory Rate + Cabin Pressure (kPa)",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue"
    },
    {
        "condition_id": "EXMC-COND-003",
        "name": "Cardiovascular Deconditioning & Orthostatic Intolerance",
        "category": "Cardiovascular",
        "system": "Circulatory & Autonomic",
        "impact_relevance": "Universal physiological adaptation in microgravity resulting from cephalad fluid shift and baroreflex down-regulation.",
        "dr_d_monitoring": "MONITORED_DIRECTLY",
        "telemetry_stream": "Heart Rate + HRV (RMSSD) + Blood Pressure + Fluid Shift Score",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue; HRP Cardiovascular Evidence Report"
    },
    {
        "condition_id": "EXMC-COND-004",
        "name": "Supraventricular Tachycardia & Exertional Arrhythmia",
        "category": "Cardiovascular",
        "system": "Cardiac Electrophysiology",
        "impact_relevance": "Documented in spaceflight during vigorous EVA workloads and electrolyte shifts.",
        "dr_d_monitoring": "MONITORED_DIRECTLY",
        "telemetry_stream": "Heart Rate (>120 bpm at rest) + HRV collapse + EVA Cardiac Stress scenario",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue"
    },
    {
        "condition_id": "EXMC-COND-005",
        "name": "Circadian Rhythm Sleep Disorder",
        "category": "Neuro-Psychiatric",
        "system": "Central Nervous System",
        "impact_relevance": "Very high incidence; chronic sleep deprivation elevates mission error rates and immune dysfunction.",
        "dr_d_monitoring": "MONITORED_DIRECTLY",
        "telemetry_stream": "Daily Check-in Sleep Hours + Sleep Quality + Stress Index + HRV",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue; BHP Evidence Report"
    },
    {
        "condition_id": "EXMC-COND-006",
        "name": "Hypovolemia and Dehydration",
        "category": "Metabolic & Hemodynamic",
        "system": "Fluid & Renal",
        "impact_relevance": "Plasma volume drops 10-15% during early mission days; fluid intake deficits exacerbate hypotension.",
        "dr_d_monitoring": "MONITORED_DIRECTLY",
        "telemetry_stream": "Blood Pressure (hypotension) + Heart Rate (compensatory tachycardia) + Dehydration scenario",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue"
    },
    {
        "condition_id": "EXMC-COND-007",
        "name": "Acute Radiation Exposure / Prodromal Syndrome",
        "category": "Space Environmental",
        "system": "Hematopoietic & Systemic",
        "impact_relevance": "High consequence risk during Solar Particle Events (SPE) beyond Low Earth Orbit magnetospheric shielding.",
        "dr_d_monitoring": "MONITORED_DIRECTLY",
        "telemetry_stream": "Cumulative Dosimeter (mSv) + Solar Storm Crisis Scenario",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue; Space Radiation Evidence Report"
    },
    {
        "condition_id": "EXMC-COND-008",
        "name": "Core Hyperthermia / Exercise Thermal Stress",
        "category": "Thermoregulatory",
        "system": "Thermoregulation",
        "impact_relevance": "Microgravity impairs convective and evaporative heat loss; core body temp elevates during intensive exercise.",
        "dr_d_monitoring": "MONITORED_DIRECTLY",
        "telemetry_stream": "Core Body Temperature (°C) + Skin Temperature (°C)",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue"
    },
    {
        "condition_id": "EXMC-COND-009",
        "name": "Spaceflight Associated Neuro-ocular Syndrome (SANS)",
        "category": "Ophthalmic & Neurological",
        "system": "Neuro-Ocular",
        "impact_relevance": "Occurs in >50% of long-duration ISS crew members; optic disc edema, globe flattening, choroidal folds.",
        "dr_d_monitoring": "RESEARCH_REFERENCE_ONLY",
        "telemetry_stream": "Fluid Shift Index + Cephalad Venous Pressure proxy",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue; SANS Evidence Report"
    },
    {
        "condition_id": "EXMC-COND-010",
        "name": "Decompression Sickness (Bends / Paresthesia)",
        "category": "Hypobaric & Environmental",
        "system": "Musculoskeletal & Neurological",
        "impact_relevance": "Risk during extravehicular activity (EVA) suit depressurization without protocolized pre-breathe.",
        "dr_d_monitoring": "MONITORED_DIRECTLY",
        "telemetry_stream": "EVA Status Tracker + Cabin/Suit Pressure (kPa)",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue; NASA STD-3001"
    },
    {
        "condition_id": "EXMC-COND-011",
        "name": "Space Motion Sickness (SMS)",
        "category": "Neuro-Vestibular",
        "system": "Vestibular",
        "impact_relevance": "Affects 60-70% of crew members during initial 48-72 hours of microgravity exposure; nausea, malaise.",
        "dr_d_monitoring": "MONITORED_DIRECTLY",
        "telemetry_stream": "Daily Check-in Space Motion Sickness Score (1-10)",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue"
    },
    {
        "condition_id": "EXMC-COND-012",
        "name": "Musculoskeletal Lumbar Back Strain & Disc Herniation",
        "category": "Musculoskeletal & Trauma",
        "system": "Spine & Skeletal",
        "impact_relevance": "Spinal elongation (up to 5-7 cm) in microgravity increases disc intervertebral hydration and risk of herniation.",
        "dr_d_monitoring": "MONITORED_DIRECTLY",
        "telemetry_stream": "Daily Check-in Muscle Soreness Score (1-10) + Bone/Muscle Long-Duration Trends",
        "evidence_source": "NASA ExMC HRP-48036 Rev. B IMPACT 1.0 Catalogue"
    }
]

# ==============================================================================
# 7. OFFICIAL NASA PUBLICATION REGISTRY
# ==============================================================================
NASA_SOURCE_REGISTRY: List[Dict[str, Any]] = [
    {
        "resource_number": 1,
        "title": "NASA Human Research Program – Risks of Human Spaceflight",
        "category": "Hazards & Health Risks Framework",
        "authoring_organization": "NASA Human Research Program (HRP)",
        "official_url": "https://www.nasa.gov/hrp/risks/",
        "document_id": "NASA-HRP-RISKS",
        "role_in_dr_d": "Defines the core 5-hazard classification framework (Radiation, Isolation, Distance, Gravity, Environment) and mapped physiological risk domains.",
        "data_type": "Scientific Research Publication (Not a machine-readable telemetry dataset)",
        "provenance_tag": "NASA RESEARCH REFERENCE"
    },
    {
        "resource_number": 2,
        "title": "NASA Human Research Roadmap – Evidence Reports",
        "category": "Clinical & Physiological Evidence Base",
        "authoring_organization": "NASA Human Research Program (HRP)",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/",
        "document_id": "NASA-HRR-EVIDENCE",
        "role_in_dr_d": "Provides empirical clinical evidence and physiological rationales for cardiovascular, hypoxia, radiation, circadian, and environmental parameters.",
        "data_type": "Scientific Technical Reports & Peer-Reviewed Evidence",
        "provenance_tag": "NASA RESEARCH REFERENCE"
    },
    {
        "resource_number": 3,
        "title": "Clinical Decision Support System Architecture Recommendation",
        "category": "Decision Support Engineering",
        "authoring_organization": "NASA Exploration Medical Capability (ExMC)",
        "official_url": "https://ntrs.nasa.gov/citations/20220017869",
        "document_id": "NASA HRP-48032 Rev. B",
        "role_in_dr_d": "Informs the 4-tier decoupled edge architecture, tiered anomaly detection, explainable risk scoring, and local autonomous operations.",
        "data_type": "Technical Architecture Specification",
        "provenance_tag": "NASA RESEARCH REFERENCE"
    },
    {
        "resource_number": 4,
        "title": "Earth-Independent Medical Operations (EIMO) Concept of Operations",
        "category": "Deep-Space Clinical Operations",
        "authoring_organization": "NASA Exploration Medical Capability (ExMC)",
        "official_url": "https://ntrs.nasa.gov/citations/20240001402",
        "document_id": "NASA TP-20240001402",
        "role_in_dr_d": "Informs operational workflows during high communication latencies, autonomous alarm triage, and personalized baseline calibrations.",
        "data_type": "Operational Concept Document (ConOps)",
        "provenance_tag": "NASA RESEARCH REFERENCE"
    },
    {
        "resource_number": 5,
        "title": "Exploration Medical Capability Evidence Library Methods",
        "category": "Exploration Medical Condition List",
        "authoring_organization": "NASA Exploration Medical Capability (ExMC)",
        "official_url": "https://ntrs.nasa.gov/citations/20240004774",
        "document_id": "NASA HRP-48036 Rev. B",
        "role_in_dr_d": "Provides the structured taxonomy for the Exploration Medical Condition List (IMPACT 1.0) and guides symptom-to-telemetry mapping.",
        "data_type": "Methodological & Condition Taxonomy Standard",
        "provenance_tag": "NASA RESEARCH REFERENCE"
    }
]

# ==============================================================================
# 8. DATA PROVENANCE REGISTRY (PART 7)
# ==============================================================================
DATA_PROVENANCE_REGISTRY: List[Dict[str, Any]] = [
    {
        "classification": "NASA Research Reference",
        "badge_label": "NASA RESEARCH REFERENCE",
        "color": "cyan",
        "source_name": "NASA HRP & ExMC Publications (5 Official Citations)",
        "url": "https://www.nasa.gov/hrp/",
        "data_type": "Static scientific publications, technical standards, and evidence reports",
        "purpose": "Provides the scientific taxonomy, hazard definitions, and clinical decision support framework.",
        "integration_method": "Locally stored structured metadata in `backend/app/research_data.py`",
        "license_terms": "NASA Open Government Information (Public Domain USGov Works)",
        "provenance_nature": "Static Research Reference (NOT a live NASA telemetry dataset)"
    },
    {
        "classification": "Synthetic Telemetry",
        "badge_label": "SIMULATED DATA",
        "color": "amber",
        "source_name": "Dr D Spacecraft Simulation Engine (`backend/app/simulator.py`, `seed.py`)",
        "url": "Internal Codebase",
        "data_type": "12+ channel time-series physiological vitals and spacecraft cabin ECLSS readings",
        "purpose": "Generates continuous real-time astronaut vital signs, diurnal circadian waves, sensor noise, and emergency scenario dynamics.",
        "integration_method": "FastAPI background tick loop streaming via Starlette WebSockets and persisted to SQLite (`dr_d.db`)",
        "license_terms": "Proprietary Hackathon Project Code",
        "provenance_nature": "Synthetic Simulated Telemetry (NOT live astronaut data)"
    },
    {
        "classification": "User-Imported CSV",
        "badge_label": "USER-IMPORTED DATA",
        "color": "indigo",
        "source_name": "User-Uploaded Telemetry CSV / Equipment Logs",
        "url": "User Workspace / Preset CSV Samples",
        "data_type": "Recorded biometric logs from external wearables or clinical databases",
        "purpose": "Enables evaluation of real or external biometric series through Dr D's anomaly and risk pipeline.",
        "integration_method": "Multipart Form File Upload via `POST /api/simulation/import-csv`",
        "license_terms": "User-provided",
        "provenance_nature": "External User Upload"
    },
    {
        "classification": "Model-Generated Output",
        "badge_label": "MODEL-GENERATED OUTPUT",
        "color": "purple",
        "source_name": "Dr D Analytics Engine (`backend/app/analytics.py`)",
        "url": "Internal Codebase",
        "data_type": "Isolation Forest anomaly scores, rolling Z-score baselines, composite HRI (0-100), and 30-min predictive forecasts",
        "purpose": "Transforms raw biometric telemetry into actionable early-warning triage and explainable factor scores.",
        "integration_method": "Scikit-learn Isolation Forest, linear regression & exponential smoothing",
        "license_terms": "Open Source Algorithms (BSD / MIT)",
        "provenance_nature": "Locally Inferred Analytical Outputs"
    },
    {
        "classification": "Third-Party Library or Service",
        "badge_label": "THIRD-PARTY DEPENDENCY",
        "color": "slate",
        "source_name": "Open-Source Python & JavaScript Ecosystem",
        "url": "PyPI / npm registries",
        "data_type": "Runtime frameworks, mathematical libraries, chart rendering, UI components",
        "purpose": "Powering the client-server architecture (FastAPI, React 18, Recharts, Tailwind CSS, ReportLab, etc.)",
        "integration_method": "Package dependencies in `requirements.txt` and `package.json`",
        "license_terms": "Permissive Open-Source Licenses (MIT, BSD-3-Clause, Apache 2.0)",
        "provenance_nature": "Third-Party Dependencies"
    }
]

# ==============================================================================
# 9. RESEARCH-TO-FEATURE MAPPING (PART 6)
# ==============================================================================
RESEARCH_EVENT_CONTEXTS: Dict[str, Dict[str, Any]] = {
    "radiation_storm": {
        "event_id": "radiation_storm",
        "event_name": "Solar Particle Event (SPE Radiation Storm)",
        "detected_condition": "Elevated cosmic ionizing radiation dose intake (+0.45 mSv/min simulated accumulation rate).",
        "nasa_hazard": "Space Radiation",
        "hazard_id": "hazard_radiation",
        "potential_implications": "Acute prodromal sickness, lymphocyte depletion, cumulative DNA double-strand breaks, elevated career excess lifetime cancer risk.",
        "research_reference": "NASA Human Research Program – Space Radiation Element; Permissible Exposure Limits (PEL) Standards",
        "official_url": "https://www.nasa.gov/hrp/risks/",
        "data_source": "Synthetic Telemetry Simulation",
        "suggested_countermeasure": "Direct crew to heavily shielded storm shelter (e.g., water wall/polyethylene sleep module). Suspend all extravehicular activities immediately.",
        "clinical_evidence_summary": "SPEs produce high fluxes of solar protons capable of delivering hundreds of mSv within hours beyond Earth's protective geomagnetic shield."
    },
    "co2_spike": {
        "event_id": "co2_spike",
        "event_name": "Cabin CO2 Scrubber Saturation",
        "detected_condition": "Cabin atmospheric CO2 concentration elevated past 2,000 ppm (nominal baseline < 600 ppm).",
        "nasa_hazard": "Hostile and Closed Environments",
        "hazard_id": "hazard_environment",
        "potential_implications": "Respiratory acidosis, compensatory tachycardia, cerebral vasodilation with frontal headache, impaired cognitive task performance.",
        "research_reference": "NASA HRP Evidence Report on Hostile Spacecraft Cabin Atmosphere; NASA STD-3001 Vol 2",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/",
        "data_source": "Synthetic Telemetry Simulation",
        "suggested_countermeasure": "Command auxiliary Carbon Dioxide Removal Assembly (CDRA) bed to HIGH; inspect air duct diffusers; don emergency O2 masks if >2,500 ppm.",
        "clinical_evidence_summary": "NASA ISS medical data demonstrates that microgravity impairs atmospheric convection, creating localized CO2 pockets that exacerbate physiological hypercapnia."
    },
    "eva_cardiac_stress": {
        "event_id": "eva_cardiac_stress",
        "event_name": "Extravehicular Cardiac Exertion & Tachycardia",
        "detected_condition": "Sustained heart rate exceeding 135 bpm during EVA suit operations with HRV collapse (<18 ms).",
        "nasa_hazard": "Altered Gravity Fields & Hostile Environments",
        "hazard_id": "hazard_gravity",
        "potential_implications": "Metabolic overheating, acute cardiac fatigue, autonomic exhaustion, space suit metabolic CO2 production spike.",
        "research_reference": "NASA HRP Cardiovascular Evidence Report; NASA EVA Physiology Technical Specification",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/",
        "data_source": "Synthetic Telemetry Simulation",
        "suggested_countermeasure": "Enforce mandatory 15-minute tether rest pause; increase Liquid Cooling and Ventilation Garment (LCVG) coolant loop flow; monitor core body temperature.",
        "clinical_evidence_summary": "Pressurized suit gloves and joints impose high mechanical resistance, frequently driving astronaut metabolic expenditure past 300 kcal/hr."
    },
    "sleep_deprivation": {
        "event_id": "sleep_deprivation",
        "event_name": "Circadian Disruption & Cumulative Sleep Loss",
        "detected_condition": "Consecutive sleep cycles < 5.0 hours with subjective fatigue score >= 7/10 and autonomic stress index > 75/100.",
        "nasa_hazard": "Isolation and Confinement",
        "hazard_id": "hazard_isolation",
        "potential_implications": "Reaction-time degradation, high operational error vulnerability, impaired emotion regulation, suppressed immune function.",
        "research_reference": "NASA HRP Behavioral Health & Performance (BHP) Evidence Report on Sleep & Circadian Adaptation",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/",
        "data_source": "Synthetic Telemetry Simulation + Subjective Check-in",
        "suggested_countermeasure": "Engage blue-light-filtered 480nm warm lighting in crew quarters; schedule 45-minute tactical sleep window; review workload allocation.",
        "clinical_evidence_summary": "ISS operational monitoring reveals over 70% of crew members utilize sleep-promoting medications at least intermittently due to acoustic noise and circadian desynchrony."
    },
    "dehydration": {
        "event_id": "dehydration",
        "event_name": "Hypovolemic Dehydration & Orthostatic Shift",
        "detected_condition": "Blood pressure reduction (systolic < 105 mmHg) with compensatory heart rate elevation and reduced fluid shift index.",
        "nasa_hazard": "Altered Gravity Fields",
        "hazard_id": "hazard_gravity",
        "potential_implications": "Decreased cardiac preload, orthostatic pre-syncope, reduced physical performance, elevated renal stone risk from concentrated urine.",
        "research_reference": "NASA HRP Cardiovascular and Renal Stone Evidence Reports",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/",
        "data_source": "Synthetic Telemetry Simulation",
        "suggested_countermeasure": "Initiate oral electrolyte fluid replacement protocol (500 ml isotonic saline pouch); apply Lower Body Negative Pressure (LBNP) if symptomatic.",
        "clinical_evidence_summary": "Microgravity cephalad fluid redistribution stimulates atrial natriuretic peptide, causing rapid diuresis and a chronic 10-15% reduction in plasma volume."
    },
    "hypoxia": {
        "event_id": "hypoxia",
        "event_name": "Acute Hypoxemia & Ventilation Deficit",
        "detected_condition": "Peripheral capillary oxygen saturation drop (SpO2 < 93%) with compensatory tachypnea.",
        "nasa_hazard": "Hostile and Closed Environments",
        "hazard_id": "hazard_environment",
        "potential_implications": "Cellular hypoxia, cerebral hypoperfusion, visual tunnel effect, psychomotor coordination degradation.",
        "research_reference": "NASA HRP Evidence Report on Hostile Spacecraft Cabin Atmosphere; NASA STD-3001",
        "official_url": "https://humanresearchroadmap.nasa.gov/evidence/",
        "data_source": "Synthetic Telemetry Simulation",
        "suggested_countermeasure": "Inspect spacesuit/cabin O2 supply lines; don supplemental oxygen mask; verify ECLSS oxygen generation assembly.",
        "clinical_evidence_summary": "In microgravity, ventilation-perfusion mismatching occurs without gravity-dependent alveolar gradient, elevating hypoxia risk."
    },
    "sensor_failure": {
        "event_id": "sensor_failure",
        "event_name": "Biosensor Artifact & Telemetry Dropout",
        "detected_condition": "Sudden discontinuity or 0-value reading on optical SpO2 / pulse sensor channel.",
        "nasa_hazard": "Distance from Earth (Autonomous Diagnostics)",
        "hazard_id": "hazard_distance",
        "potential_implications": "Telemetry blindness for flight surgeons, false positive crisis alerts, inability to track vital trends.",
        "research_reference": "NASA ExMC HRP-48032 Rev. B Clinical Decision Support Architecture Recommendation",
        "official_url": "https://ntrs.nasa.gov/citations/20220017869",
        "data_source": "Synthetic Sensor Fault Injection",
        "suggested_countermeasure": "Re-seat pulse-oximeter probe; clean optical photodiode window; switch to redundant biosensor harness.",
        "clinical_evidence_summary": "ExMC medical architecture mandates sensor plausibility checks to discriminate true clinical collapse from hardware lead disconnects."
    }
}


def get_context_for_metric(metric: str) -> Dict[str, Any]:
    """Helper to return NASA research context for a specific vital or alert metric"""
    metric_lower = metric.lower()
    if "co2" in metric_lower:
        return RESEARCH_EVENT_CONTEXTS["co2_spike"]
    elif "spo2" in metric_lower or "o2" in metric_lower:
        return RESEARCH_EVENT_CONTEXTS["hypoxia"]
    elif "radiation" in metric_lower or "msv" in metric_lower:
        return RESEARCH_EVENT_CONTEXTS["radiation_storm"]
    elif "sleep" in metric_lower or "circadian" in metric_lower or "stress" in metric_lower:
        return RESEARCH_EVENT_CONTEXTS["sleep_deprivation"]
    elif "bp" in metric_lower or "blood_pressure" in metric_lower or "fluid" in metric_lower:
        return RESEARCH_EVENT_CONTEXTS["dehydration"]
    elif "sensor" in metric_lower:
        return RESEARCH_EVENT_CONTEXTS["sensor_failure"]
    else:
        return RESEARCH_EVENT_CONTEXTS["eva_cardiac_stress"]
