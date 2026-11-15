"""
Build Script for NASA Space Apps Challenge 7-Slide Presentation:
- Generates presentation/DrD_Project_Demo.pptx (16:9 widescreen, python-pptx)
- Generates presentation/DrD_Project_Demo.pdf (16:9 widescreen, ReportLab)
- Generates presentation/Presenter_Notes.md (Complete speaker script & live demo guide)
"""

import os
import shutil
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
SCREENSHOTS_DIR = DOCS_DIR / "screenshots"
PRESENTATION_DIR = PROJECT_ROOT / "presentation"
PRESENTATION_DIR.mkdir(parents=True, exist_ok=True)

FINAL_DIST_DIR = Path(r"C:\Users\AHAMMED\.gemini\antigravity\scratch\dr_d_space_apps_final\dr_d_astronaut_health\presentation")
FINAL_DIST_DIR.mkdir(parents=True, exist_ok=True)

PPTX_PATH = PRESENTATION_DIR / "DrD_Project_Demo.pptx"
PDF_PATH = PRESENTATION_DIR / "DrD_Project_Demo.pdf"
NOTES_PATH = PRESENTATION_DIR / "Presenter_Notes.md"

# Color Palette Constants
C_NAVY_BG = RGBColor(8, 12, 22)        # #080C16
C_CARD_BG = RGBColor(15, 23, 42)       # #0F172A
C_CARD_BORDER = RGBColor(30, 41, 59)   # #1E293B
C_CYAN_ACCENT = RGBColor(6, 182, 212)  # #06B6D4
C_CYAN_BRIGHT = RGBColor(34, 211, 238) # #22D3EE
C_WHITE = RGBColor(255, 255, 255)
C_SLATE_LIGHT = RGBColor(226, 232, 240)# #E2E8F0
C_SLATE_MUTED = RGBColor(148, 163, 184)# #94A3B8
C_AMBER = RGBColor(245, 158, 11)       # #F59E0B
C_RED = RGBColor(239, 68, 68)          # #EF4444
C_GREEN = RGBColor(16, 185, 129)       # #10B981

def add_header(slide, title_text, subtitle_text, slide_num_str):
    # Top badge
    badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.0), Inches(0.35))
    tf = badge_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NASA SPACE APPS CHALLENGE  •  DR D ASTRONAUT HEALTH INTELLIGENCE  •  ARES-V TRANSIT"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT

    # Slide Number / Status Badge
    num_box = slide.shapes.add_textbox(Inches(10.5), Inches(0.4), Inches(2.0), Inches(0.35))
    tf_num = num_box.text_frame
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"SLIDE {slide_num_str} / 07"
    p_num.font.name = "Arial"
    p_num.font.size = Pt(11)
    p_num.font.bold = True
    p_num.font.color.rgb = C_SLATE_MUTED

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.55))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Arial"
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE

    # Subtitle
    s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.7), Inches(0.4))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle_text
    p_s.font.name = "Arial"
    p_s.font.size = Pt(12)
    p_s.font.color.rgb = C_SLATE_LIGHT

def set_slide_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_NAVY_BG
    bg.line.fill.background()
    return bg

def add_card(slide, left, top, width, height, border_color=C_CARD_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_CARD_BG
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card

def add_image_with_border(slide, img_path, left, top, width, height, border_color=C_CYAN_ACCENT):
    # Border frame shape
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left - Inches(0.04), top - Inches(0.04), width + Inches(0.08), height + Inches(0.08))
    frame.fill.solid()
    frame.fill.fore_color.rgb = RGBColor(12, 18, 32)
    frame.line.color.rgb = border_color
    frame.line.width = Pt(1.5)
    # Picture
    slide.shapes.add_picture(str(img_path), left, top, width, height)

def build_pptx():
    print(f"Building PowerPoint presentation: {PPTX_PATH}")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # SLIDE 1: PROJECT INTRODUCTION
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)
    
    # Left Content Column
    left_x = Inches(0.8)
    # Header tag
    t_tag = slide1.shapes.add_textbox(left_x, Inches(0.9), Inches(5.8), Inches(0.4))
    p = t_tag.text_frame.paragraphs[0]
    p.text = "NASA SPACE APPS CHALLENGE 2026"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT

    # Main Project Title
    t_main = slide1.shapes.add_textbox(left_x, Inches(1.3), Inches(5.8), Inches(1.3))
    tf_m = t_main.text_frame
    tf_m.word_wrap = True
    p1 = tf_m.paragraphs[0]
    p1.text = "DR D – NOT TO GET DOOMED IN SPACE"
    p1.font.name = "Arial"
    p1.font.size = Pt(26)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    # Subtitle
    t_sub = slide1.shapes.add_textbox(left_x, Inches(2.7), Inches(5.8), Inches(0.7))
    tf_sub = t_sub.text_frame
    tf_sub.word_wrap = True
    p2 = tf_sub.paragraphs[0]
    p2.text = "Autonomous Astronaut Health Monitoring & Early-Warning Intelligence System"
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.color.rgb = C_CYAN_BRIGHT

    # Objective Card
    add_card(slide1, left_x, Inches(3.6), Inches(5.6), Inches(1.5))
    t_card = slide1.shapes.add_textbox(left_x + Inches(0.2), Inches(3.7), Inches(5.2), Inches(1.3))
    tf_c = t_card.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "CHALLENGE OBJECTIVE"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    
    p = tf_c.add_paragraph()
    p.text = "Create Health Monitoring Software for Astronauts on Space Missions. An intelligent, autonomous edge platform to monitor vitals, assess clinical risks, and guide medical response during deep-space transit under communication delays."
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.color.rgb = C_SLATE_LIGHT

    # Three Pillar Badges
    pillars = [
        ("Real-Time Telemetry", "7 vitals + 6 ECLSS cabin streams"),
        ("Predictive Risk (HRI)", "0–100 composite index & forecasting"),
        ("Emergency Simulation", "6 active contingency scenarios")
    ]
    for idx, (head, desc) in enumerate(pillars):
        bx = left_x + idx * Inches(1.9)
        add_card(slide1, bx, Inches(5.3), Inches(1.8), Inches(1.4), border_color=C_CYAN_ACCENT)
        t_b = slide1.shapes.add_textbox(bx + Inches(0.1), Inches(5.4), Inches(1.6), Inches(1.2))
        tf_b = t_b.text_frame
        tf_b.word_wrap = True
        p = tf_b.paragraphs[0]
        p.text = head
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p_sub = tf_b.add_paragraph()
        p_sub.text = desc
        p_sub.font.name = "Arial"
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = C_SLATE_MUTED

    # Right Image: 01_login.png
    add_image_with_border(slide1, SCREENSHOTS_DIR / "01_login.png", Inches(6.8), Inches(1.3), Inches(5.7), Inches(5.4), border_color=C_CYAN_ACCENT)

    # Speaker Notes
    slide1.notes_slide.notes_text_frame.text = (
        "SLIDE 1: PROJECT INTRODUCTION (Estimated time: ~30s)\n"
        "---------------------------------------------------\n"
        "SPEAKER SCRIPT:\n"
        "\"Good day, judges and space medicine enthusiasts. This is Dr D – Not to Get Doomed in Space, "
        "an autonomous astronaut health monitoring and early-warning intelligence platform developed for the NASA Space Apps Challenge.\n\n"
        "On long-duration deep space missions—such as an Ares-V crew transit to Mars—radio communication delays can reach up to 22 minutes each way. "
        "Waiting 44 minutes for mission control on Earth during an acute medical crisis is not an option. Astronauts require onboard medical autonomy.\n\n"
        "Dr D combines real-time physiological telemetry, spacecraft environmental life support monitoring, machine-learning anomaly detection, "
        "and NASA-grounded clinical decision protocols into a unified mission control interface. Let's inspect the system in action.\""
    )

    # ==========================================
    # SLIDE 2: MISSION CONTROL DASHBOARD
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "One Dashboard. Complete Crew Health Awareness.", "Mission-wide biometric telemetry, cabin ECLSS monitoring, and fleet status indicators", "02")

    # Left Callout Cards
    card_w = Inches(3.2)
    cards_data = [
        ("4-Astronaut Crew Roster", "Simultaneous monitoring of Commander, Flight Surgeon, Flight Engineer, and Science Specialist."),
        ("Multi-Parameter Telemetry", "HR, HRV, SpO2, Blood Pressure, Core Temperature, Respiratory Rate, and Stress Index."),
        ("Spacecraft ECLSS Monitoring", "Cabin CO2 concentration, O2 levels, atmospheric pressure, temperature, humidity, and acoustics."),
        ("Fleet Health Index & Status", "At-a-glance health status badges with color-coded risk stratification and anomaly warnings.")
    ]
    for idx, (title, desc) in enumerate(cards_data):
        cy = Inches(1.8) + idx * Inches(1.25)
        add_card(slide2, Inches(0.8), cy, card_w, Inches(1.15))
        tb = slide2.shapes.add_textbox(Inches(0.95), cy + Inches(0.1), card_w - Inches(0.3), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"0{idx+1} • {title}"
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_CYAN_BRIGHT
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Arial"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_SLATE_LIGHT

    # Dominant Screenshot: 02_dashboard_nominal.png
    add_image_with_border(slide2, SCREENSHOTS_DIR / "02_dashboard_nominal.png", Inches(4.3), Inches(1.8), Inches(8.2), Inches(4.9), border_color=C_CYAN_ACCENT)

    # Speaker Notes
    slide2.notes_slide.notes_text_frame.text = (
        "SLIDE 2: MISSION CONTROL DASHBOARD (Estimated time: ~30s)\n"
        "--------------------------------------------------------\n"
        "SPEAKER SCRIPT:\n"
        "\"Here is our central Mission Control Dashboard. Designed for flight surgeons and crew medical officers, it provides total physiological "
        "and environmental situational awareness in a single, high-density command view.\n\n"
        "Across the top, we see the four Ares-V crew members, each with real-time biometric telemetry—including heart rate, heart rate variability, "
        "blood oxygen saturation, blood pressure, core temperature, respiratory rate, and psychological stress.\n\n"
        "Concurrently, the bottom telemetry panel monitors life support conditions directly from the Environmental Control and Life Support System—"
        "tracking cabin carbon dioxide, oxygen levels, total pressure, temperature, humidity, and acoustic noise.\n\n"
        "Under nominal conditions, green status indicators confirm that all crew metrics remain safely aligned with individual baseline profiles.\""
    )

    # ==========================================
    # SLIDE 3: INDIVIDUAL ASTRONAUT MONITORING
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Every Astronaut. Every Vital Sign.", "Deep-dive physiological telemetry, personalized statistical baselines, and anatomical mapping", "03")

    # Dominant Visual Left: 03_astronaut_detail.png
    add_image_with_border(slide3, SCREENSHOTS_DIR / "03_astronaut_detail.png", Inches(0.8), Inches(1.8), Inches(8.2), Inches(4.9), border_color=C_CYAN_ACCENT)

    # Right Callout Cards
    rc_x = Inches(9.3)
    rc_w = Inches(3.2)
    vitals_features = [
        ("Anatomical Sensor Visualization", "Direct spatial mapping of physiological sensors across cardiac, pulmonary, autonomic, and thermal systems."),
        ("Personalized Baseline Tracking", "Calculates Z-score deviations against each astronaut's personal resting physiology, not generic population averages."),
        ("Microgravity Adaptation Trends", "Accounts for cephalic fluid shifts, orthostatic adjustments, and cardiovascular deconditioning over mission elapsed time."),
        ("Targeted Countermeasures", "Provides astronaut-specific guidance including fluid intake, sleep scheduling, and targeted aerobic exercise dosing.")
    ]
    for idx, (title, desc) in enumerate(vitals_features):
        cy = Inches(1.8) + idx * Inches(1.25)
        add_card(slide3, rc_x, cy, rc_w, Inches(1.15))
        tb = slide3.shapes.add_textbox(rc_x + Inches(0.15), cy + Inches(0.1), rc_w - Inches(0.3), Inches(0.95))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"• {title}"
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_CYAN_BRIGHT
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Arial"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_SLATE_LIGHT

    # Speaker Notes
    slide3.notes_slide.notes_text_frame.text = (
        "SLIDE 3: INDIVIDUAL ASTRONAUT MONITORING (Estimated time: ~30s)\n"
        "-------------------------------------------------------------\n"
        "SPEAKER SCRIPT:\n"
        "\"When an individual crew member requires detailed clinical evaluation, clicking their profile opens the Astronaut Detail view, shown here for Commander Chen.\n\n"
        "Rather than relying on rigid population averages, Dr D tracks personalized statistical baselines using Z-score deviation analysis. "
        "Microgravity induces profound physiological restructuring—including cephalic fluid redistribution, baroreceptor resetting, and resting heart rate shifts. "
        "Evaluating an astronaut against their own baseline is vital for detecting early decompensation.\n\n"
        "The anatomical body map visualizes active sensor placement across cardiovascular, respiratory, and autonomic systems, paired with "
        "historical trend graphs, daily check-in logs, and customized crew self-care recommendations.\""
    )

    # ==========================================
    # SLIDE 4: INTELLIGENT HEALTH RISK ANALYSIS
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "From Raw Telemetry to Early Warnings.", "Composite Health Risk Index (0–100 scale) and 30-minute predictive autoregressive forecasting", "04")

    # Split Screen: Left (04_risk_index_gauge.png), Right (05_forecast_overlay.png)
    split_w = Inches(5.6)
    split_h = Inches(3.6)
    
    # Left Column: Risk Index
    add_image_with_border(slide4, SCREENSHOTS_DIR / "04_risk_index_gauge.png", Inches(0.8), Inches(1.8), split_w, split_h, border_color=C_AMBER)
    add_card(slide4, Inches(0.8), Inches(5.55), split_w, Inches(1.35))
    tb_l = slide4.shapes.add_textbox(Inches(0.95), Inches(5.6), split_w - Inches(0.3), Inches(1.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "HEALTH RISK INDEX (HRI) MULTI-FACTOR MODEL"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p2 = tf_l.add_paragraph()
    p2.text = "Synthesizes 5 clinical risk vectors into an explainable 0–100 composite score: Cardiovascular strain, Hypoxia risk, Thermal stress, Stress/circadian disruption, and Environmental toxicity. Stratified into Nominal (0-29), Elevated (30-69), and Critical (70-100)."
    p2.font.name = "Arial"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_SLATE_LIGHT

    # Right Column: Forecasting & Isolation Forest
    add_image_with_border(slide4, SCREENSHOTS_DIR / "05_forecast_overlay.png", Inches(6.9), Inches(1.8), split_w, split_h, border_color=C_CYAN_ACCENT)
    add_card(slide4, Inches(6.9), Inches(5.55), split_w, Inches(1.35))
    tb_r = slide4.shapes.add_textbox(Inches(7.05), Inches(5.6), split_w - Inches(0.3), Inches(1.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "PREDICTIVE FORECASTING & ANOMALY DETECTION"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_BRIGHT
    p2 = tf_r.add_paragraph()
    p2.text = "Projects physiological trajectories 30 minutes forward using autoregressive modeling to detect impending threshold breaches. Complemented by Scikit-learn Isolation Forest detecting multivariate outlier states before clinical symptoms escalate."
    p2.font.name = "Arial"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_SLATE_LIGHT

    # Speaker Notes
    slide4.notes_slide.notes_text_frame.text = (
        "SLIDE 4: INTELLIGENT HEALTH RISK ANALYSIS (Estimated time: ~35s)\n"
        "--------------------------------------------------------------\n"
        "SPEAKER SCRIPT:\n"
        "\"Streaming dozens of raw telemetry numbers can overwhelm a lone flight surgeon. Dr D transforms raw sensor data into explainable clinical intelligence "
        "through two analytical engines: the Health Risk Index and Predictive Forecasting.\n\n"
        "On the left, the Health Risk Index computes a continuous composite score from 0 to 100. It fuses five distinct hazard dimensions: "
        "cardiovascular strain, hypoxia risk, thermal stress, circadian fatigue, and cabin life-support toxicity. This provides instant risk stratification "
        "without presenting a black-box diagnosis.\n\n"
        "On the right, predictive forecasting uses autoregressive trend projections to forecast vitals 30 minutes ahead, highlighting potential threshold "
        "violations before they occur. Simultaneously, an unsupervised Isolation Forest identifies multivariate anomalies—detecting subtle correlations "
        "between declining HRV, rising CO2, and elevated core temperature that single-threshold monitors miss.\""
    )

    # ==========================================
    # SLIDE 5: LIVE EMERGENCY SIMULATION
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "What Happens When an Emergency Occurs?", "Dynamic simulation engine: Six realistic spaceflight contingencies with research-grounded dynamics", "05")

    # Left Column: The 6 Scenarios Matrix
    sc_x = Inches(0.8)
    sc_w = Inches(4.3)
    add_card(slide5, sc_x, Inches(1.8), sc_w, Inches(4.9), border_color=C_AMBER)
    
    tb_sc = slide5.shapes.add_textbox(sc_x + Inches(0.2), Inches(1.9), sc_w - Inches(0.4), Inches(4.7))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True
    p = tf_sc.paragraphs[0]
    p.text = "SIX ACTIVE SIMULATION SCENARIOS"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    scenarios_list = [
        ("1. Cabin CO2 Spike", "ECLSS scrubber failure -> acute hypercapnia & respiratory acidosis."),
        ("2. EVA Cardiac Stress", "Excessive metabolic workload -> severe tachycardia & low HRV."),
        ("3. Solar Particle Event", "Radiation burst -> acute stress, shelter protocol, radiation exposure."),
        ("4. Cumulative Sleep Debt", "Circadian misalignment -> severe autonomic fatigue & micro-sleep risk."),
        ("5. Dehydration & Fluid Shift", "Volume depletion -> orthostatic instability & blood pressure collapse."),
        ("6. Sensor Disconnection", "Electrode loss / lead failure -> tests system sensor fault resilience.")
    ]
    for name, desc in scenarios_list:
        p_name = tf_sc.add_paragraph()
        p_name.text = f"\n{name}"
        p_name.font.name = "Arial"
        p_name.font.size = Pt(10)
        p_name.font.bold = True
        p_name.font.color.rgb = C_WHITE if "CO2" not in name else C_CYAN_BRIGHT
        p_d = tf_sc.add_paragraph()
        p_d.text = desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = C_SLATE_MUTED

    # Right Image: 10_demo_matrix_modal.png
    add_image_with_border(slide5, SCREENSHOTS_DIR / "10_demo_matrix_modal.png", Inches(5.3), Inches(1.8), Inches(7.2), Inches(4.9), border_color=C_CYAN_ACCENT)

    # Speaker Notes (With Live Demo Instructions)
    slide5.notes_slide.notes_text_frame.text = (
        "SLIDE 5: LIVE EMERGENCY SIMULATION (Estimated time: ~35s)\n"
        "--------------------------------------------------------\n"
        "SPEAKER SCRIPT:\n"
        "\"To rigorously evaluate system readiness, Dr D features an interactive spaceflight emergency simulation engine capable of triggering six realistic mission contingencies.\n\n"
        "These include life support failures like cabin CO2 spikes, extravehicular cardiac over-exertion, solar particle radiation storms, chronic sleep deprivation, "
        "microgravity dehydration, and biometric lead disconnects. Each scenario drives mathematically modeled physiological and environmental changes in real time.\n\n"
        "[LIVE DEMO INSTRUCTION]:\n"
        "\"To demonstrate this live in the application: in the top navigation bar, click the 'Demo Matrix' button. In the modal that opens, select "
        "'Cabin CO2 Spike' and click 'Inject Scenario'.\n"
        "Instantly, the simulation engine elevates ambient CO2 from nominal 0.4% up to 1.5%, triggering immediate respiratory rate elevation, cognitive fatigue indices, "
        "and autonomic stress responses across the crew. Let's see how the alert system responds.\""
    )

    # ==========================================
    # SLIDE 6: ALERTS AND MEDICAL DECISION SUPPORT
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Detect. Alert. Respond.", "Closed-loop incident management: Severity triaging, clinical action checklists, and mission dossier export", "06")

    # Left Dominant Image: 11_dashboard_critical_scenario.png
    add_image_with_border(slide6, SCREENSHOTS_DIR / "11_dashboard_critical_scenario.png", Inches(0.8), Inches(1.8), Inches(7.2), Inches(4.9), border_color=C_RED)

    # Right Column: Reports visual on top (12_reports_dossier.png), Workflow card on bottom
    add_image_with_border(slide6, SCREENSHOTS_DIR / "12_reports_dossier.png", Inches(8.2), Inches(1.8), Inches(4.3), Inches(2.35), border_color=C_CYAN_ACCENT)

    add_card(slide6, Inches(8.2), Inches(4.3), Inches(4.3), Inches(2.4), border_color=C_RED)
    tb_wf = slide6.shapes.add_textbox(Inches(8.35), Inches(4.4), Inches(4.0), Inches(2.2))
    tf_wf = tb_wf.text_frame
    tf_wf.word_wrap = True
    p = tf_wf.paragraphs[0]
    p.text = "CLOSED-LOOP MEDICAL INCIDENT RESPONSE"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_RED

    steps = [
        ("1. Immediate Threat Triage", "HRI surges to 78/100 (CRITICAL). Flashing red alert banners notify crew across all stations."),
        ("2. NASA Evidence Context", "Dynamic citation of NASA HRP Hostile & Closed Environments Evidence Report."),
        ("3. Countermeasure Checklist", "Step-by-step clinical protocol: Don O2 masks, deploy secondary LiOH scrubbers, ventilate cabin."),
        ("4. Audit Trail & PDF Dossier", "One-click generation of timestamped medical incident report for Earth burst transmission.")
    ]
    for st, sd in steps:
        p_st = tf_wf.add_paragraph()
        p_st.text = f"{st}: {sd}"
        p_st.font.name = "Arial"
        p_st.font.size = Pt(8.5)
        p_st.font.color.rgb = C_SLATE_LIGHT

    # Speaker Notes
    slide6.notes_slide.notes_text_frame.text = (
        "SLIDE 6: ALERTS AND MEDICAL DECISION SUPPORT (Estimated time: ~35s)\n"
        "-----------------------------------------------------------------\n"
        "SPEAKER SCRIPT:\n"
        "\"The moment the emergency is injected, Dr D executes a closed-loop incident management sequence.\n\n"
        "As seen on the left dashboard, the crew Health Risk Index surges into the CRITICAL band at 78 out of 100. High-priority red alert banners "
        "and audio cues immediately flag the severe hypercapnia event.\n\n"
        "Critically, Dr D is not just an alarm; it is an active clinical decision support system. Grounded in NASA Human Research Program evidence, "
        "the alert expands to deliver step-by-step countermeasure protocols: immediately donning emergency oxygen masks, activating secondary LiOH scrubbing beds, "
        "and venting cabin sectors.\n\n"
        "Once the emergency is controlled, as shown in the top right dossier view, the medical officer generates a comprehensive, timestamped clinical incident report "
        "with complete biometric telemetry graphs, ready to burst-transmit back to Houston once communication is re-established.\""
    )

    # ==========================================
    # SLIDE 7: HOW IT WORKS & PROJECT TAKEAWAY
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "Your Health Guardian Beyond Earth.", "Autonomous architecture, modern technology stack, and core mission takeaways", "07")

    # Top Architecture Flow Card
    add_card(slide7, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.35), border_color=C_CYAN_ACCENT)
    tb_arch = slide7.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.3), Inches(1.15))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True
    p = tf_arch.paragraphs[0]
    p.text = "END-TO-END AUTONOMOUS DATA FLOW ARCHITECTURE"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_BRIGHT
    
    p_flow = tf_arch.add_paragraph()
    p_flow.text = "SIMULATED TELEMETRY / ECLSS  ->  FASTAPI BACKEND  ->  HEALTH ANALYTICS & ISOLATION FOREST  ->  HEALTH RISK INDEX & ALERTS  ->  SQLITE / WEBSOCKETS  ->  REACT MISSION CONTROL DASHBOARD"
    p_flow.font.name = "Arial"
    p_flow.font.size = Pt(10)
    p_flow.font.bold = True
    p_flow.font.color.rgb = C_WHITE

    p_tech = tf_arch.add_paragraph()
    p_tech.text = "Built with: Python 3.13 • FastAPI • React 18 • Vite • SQLite / SQLAlchemy • Scikit-learn • NumPy • WebSockets • Recharts • Tailwind CSS"
    p_tech.font.name = "Arial"
    p_tech.font.size = Pt(9.5)
    p_tech.font.color.rgb = C_SLATE_MUTED

    # Bottom 3 Cards
    # Card 1: Three Core Capabilities
    add_card(slide7, Inches(0.8), Inches(3.35), Inches(3.7), Inches(3.4))
    tb_c1 = slide7.shapes.add_textbox(Inches(0.95), Inches(3.5), Inches(3.4), Inches(3.1))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "THREE CORE CAPABILITIES"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_ACCENT
    
    caps = [
        ("1. Total Fleet Visibility", "Real-time biometric and ECLSS monitoring across multi-member deep space crews."),
        ("2. Explainable Anomaly Detection", "Personalized Z-score baselines combined with unsupervised ML Isolation Forest."),
        ("3. Autonomous Medical CDSS", "Actionable clinical guidelines when Earth communication is delayed up to 22 minutes.")
    ]
    for c_t, c_d in caps:
        p = tf_c1.add_paragraph()
        p.text = f"\n• {c_t}:"
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p_sub = tf_c1.add_paragraph()
        p_sub.text = c_d
        p_sub.font.name = "Arial"
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = C_SLATE_LIGHT

    # Card 2: Scientific Grounding & Data Provenance
    add_card(slide7, Inches(4.8), Inches(3.35), Inches(3.7), Inches(3.4))
    tb_c2 = slide7.shapes.add_textbox(Inches(4.95), Inches(3.5), Inches(3.4), Inches(3.1))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "NASA SCIENTIFIC GROUNDING"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    scis = [
        ("NASA HRP 5 Hazards (RIDGE)", "Radiation, Isolation, Distance, Altered Gravity, Closed Environments."),
        ("Human Research Roadmap", "Evidence reports for SANS, Cardiovascular, Sleep debt, Immune dysregulation."),
        ("ExMC CDSS Architecture", "Aligned with NASA HRP-48032 autonomous clinical decision support standards."),
        ("ExMC IMPACT 1.0 Library", "12 spaceflight exploration medical conditions and countermeasure methods.")
    ]
    for s_t, s_d in scis:
        p = tf_c2.add_paragraph()
        p.text = f"\n• {s_t}:"
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE
        p_sub = tf_c2.add_paragraph()
        p_sub.text = s_d
        p_sub.font.name = "Arial"
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = C_SLATE_LIGHT

    # Card 3: Project Sign-off & Data Note
    add_card(slide7, Inches(8.8), Inches(3.35), Inches(3.7), Inches(3.4), border_color=C_CYAN_ACCENT)
    tb_c3 = slide7.shapes.add_textbox(Inches(8.95), Inches(3.5), Inches(3.4), Inches(3.1))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "DATA PROVENANCE & SUMMARY"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_CYAN_BRIGHT

    p = tf_c3.add_paragraph()
    p.text = "\nHonest Data Provenance:"
    p.font.name = "Arial"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p_dp = tf_c3.add_paragraph()
    p_dp.text = "Current demonstration uses synthetic astronaut telemetry and simulated environmental data. NASA research publications provide scientific and technical context; no direct NASA live telemetry or biometric dataset integration is implemented."
    p_dp.font.name = "Arial"
    p_dp.font.size = Pt(8.5)
    p_dp.font.color.rgb = C_SLATE_MUTED

    p = tf_c3.add_paragraph()
    p.text = "\nDR D – NOT TO GET DOOMED IN SPACE"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p = tf_c3.add_paragraph()
    p.text = "\"Your health guardian beyond Earth.\""
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.italic = True
    p.font.color.rgb = C_CYAN_BRIGHT

    # Speaker Notes
    slide7.notes_slide.notes_text_frame.text = (
        "SLIDE 7: HOW IT WORKS & PROJECT TAKEAWAY (Estimated time: ~35s)\n"
        "--------------------------------------------------------------\n"
        "SPEAKER SCRIPT:\n"
        "\"Under the hood, Dr D is built on a resilient, modular architecture. A high-performance FastAPI backend ingests simulated biometric and ECLSS telemetry, "
        "executes real-time Isolation Forest anomaly detection and composite Health Risk Index calculations, and streams updates via WebSockets directly into "
        "a reactive React 18 mission control interface.\n\n"
        "To summarize, Dr D delivers three pivotal innovations for human spaceflight:\n"
        "First, complete multi-parameter crew and environmental awareness.\n"
        "Second, early warning intelligence combining individual statistical baselines with machine learning.\n"
        "And third, autonomous clinical decision support that empowers astronaut crews when Earth is light-minutes away.\n\n"
        "Dr D: Not to Get Doomed in Space. Your health guardian beyond Earth. Thank you, and we welcome your questions!\""
    )

    prs.save(str(PPTX_PATH))
    print(f"PowerPoint presentation created successfully at: {PPTX_PATH}")

def build_pdf():
    print(f"Building PDF presentation: {PDF_PATH}")
    # 16:9 widescreen in points: 960 x 540 (13.333 x 7.5 inches at 72 dpi)
    page_w = 13.333 * 72
    page_h = 7.5 * 72
    c = canvas.Canvas(str(PDF_PATH), pagesize=(page_w, page_h))

    slides_info = [
        {
            "num": "01",
            "title": "DR D – NOT TO GET DOOMED IN SPACE",
            "sub": "Autonomous Astronaut Health Monitoring & Early-Warning Intelligence System",
            "img": SCREENSHOTS_DIR / "01_login.png",
            "bullet_title": "CHALLENGE OBJECTIVE",
            "bullets": [
                "NASA Space Apps Challenge: Create Health Monitoring Software for Astronauts on Space Missions.",
                "An intelligent, autonomous edge platform to monitor vitals and assess clinical risks during deep-space transit.",
                "Core Pillars: Multi-parameter Telemetry • Health Risk Index (HRI) • Emergency Simulation Engine."
            ]
        },
        {
            "num": "02",
            "title": "One Dashboard. Complete Crew Health Awareness.",
            "sub": "Mission-wide biometric telemetry, cabin ECLSS monitoring, and fleet status indicators",
            "img": SCREENSHOTS_DIR / "02_dashboard_nominal.png",
            "bullet_title": "MISSION CONTROL OVERVIEW",
            "bullets": [
                "4-Astronaut Crew Roster: Commander, Flight Surgeon, Flight Engineer, Science Specialist.",
                "Multi-Parameter Telemetry: Heart Rate, HRV, SpO2, Blood Pressure, Core Temp, Resp Rate, Stress.",
                "Cabin ECLSS Environmental Telemetry: CO2, Oxygen, Pressure, Temperature, Humidity, Noise.",
                "Unified Fleet Health Status: Instant color-coded risk stratification and anomaly indicators."
            ]
        },
        {
            "num": "03",
            "title": "Every Astronaut. Every Vital Sign.",
            "sub": "Deep-dive physiological telemetry, personalized statistical baselines, and anatomical mapping",
            "img": SCREENSHOTS_DIR / "03_astronaut_detail.png",
            "bullet_title": "INDIVIDUAL ASTRONAUT DEEP DIVE",
            "bullets": [
                "Anatomical Sensor Visualization: Spatial localization across cardiac, respiratory, autonomic, and thermal systems.",
                "Personalized Baseline Tracking: Z-score deviation against personal resting vitals, not generic population averages.",
                "Microgravity Adaptation: Accounts for microgravity cephalic fluid shifts and mission elapsed time.",
                "Targeted Crew Countermeasures: Personalized sleep schedules, fluid balance, and aerobic exercise protocols."
            ]
        },
        {
            "num": "04",
            "title": "From Raw Telemetry to Early Warnings.",
            "sub": "Composite Health Risk Index (0–100 scale) and 30-minute predictive autoregressive forecasting",
            "img": SCREENSHOTS_DIR / "04_risk_index_gauge.png",
            "img2": SCREENSHOTS_DIR / "05_forecast_overlay.png",
            "bullet_title": "INTELLIGENT RISK ASSESSMENT",
            "bullets": [
                "Health Risk Index (HRI): 0-100 composite synthesizing Cardiovascular, Hypoxia, Thermal, Stress, and ECLSS factors.",
                "Stratified Risk Bands: Nominal (0-29), Elevated (30-69), and Critical (70-100) with full factor transparency.",
                "Predictive Telemetry Forecasting: 30-minute forward autoregressive projection of impending threshold breaches.",
                "Isolation Forest ML: Unsupervised outlier detection uncovering multi-parameter deviations before symptom onset."
            ]
        },
        {
            "num": "05",
            "title": "What Happens When an Emergency Occurs?",
            "sub": "Dynamic simulation engine: Six realistic spaceflight contingencies with research-grounded dynamics",
            "img": SCREENSHOTS_DIR / "10_demo_matrix_modal.png",
            "bullet_title": "SIX EMERGENCY SCENARIOS",
            "bullets": [
                "1. Cabin CO2 Spike: ECLSS scrubber failure -> acute hypercapnia and respiratory acidosis (LIVE DEMO).",
                "2. EVA Cardiac Stress: Heavy physical exertion -> extreme tachycardia and decreased HRV.",
                "3. Solar Particle Event: Radiation burst -> radiation shelter protocols and acute stress response.",
                "4. Cumulative Sleep Deprivation: Circadian disruption -> cognitive fatigue and autonomic imbalance.",
                "5. Dehydration & Fluid Shift: Volume depletion -> blood pressure volatility and orthostatic intolerance.",
                "6. Sensor Disconnection / Lead Failure: Tests sensor fault resilience without system failure."
            ]
        },
        {
            "num": "06",
            "title": "Detect. Alert. Respond.",
            "sub": "Closed-loop incident management: Severity triaging, clinical action checklists, and mission dossier export",
            "img": SCREENSHOTS_DIR / "11_dashboard_critical_scenario.png",
            "img2": SCREENSHOTS_DIR / "12_reports_dossier.png",
            "bullet_title": "CLOSED-LOOP MEDICAL RESPONSE",
            "bullets": [
                "Immediate Threat Triage: HRI surges to 78/100 (CRITICAL). Flashing red alert banners notify crew.",
                "NASA Research Grounding: Dynamic link to NASA HRP Hostile & Closed Environments Evidence Report.",
                "Actionable Countermeasure Checklist: Don O2 masks, deploy secondary LiOH scrubbers, ventilate cabin.",
                "Mission Dossier Generation: One-click export of timestamped medical report for Earth burst transmission."
            ]
        },
        {
            "num": "07",
            "title": "Your Health Guardian Beyond Earth.",
            "sub": "Autonomous architecture, modern technology stack, and core mission takeaways",
            "bullet_title": "DATA FLOW & KEY TAKEAWAYS",
            "bullets": [
                "End-to-End Pipeline: Simulated Telemetry -> FastAPI Backend -> Isolation Forest & HRI -> WebSockets -> React UI.",
                "Core Stack: Python 3.13 • FastAPI • React 18 • Vite • SQLite • Scikit-learn • WebSockets • Recharts • Tailwind CSS.",
                "Three Core Values: Complete crew visibility • Explainable early anomaly detection • Deep-space medical autonomy.",
                "Data Provenance: Current demo uses synthetic telemetry; NASA publications provide scientific context.",
                "Closing Motto: DR D – NOT TO GET DOOMED IN SPACE • Your health guardian beyond Earth."
            ]
        }
    ]

    for s_idx, s in enumerate(slides_info):
        # Background
        c.setFillColor(colors.HexColor("#080C16"))
        c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

        # Header Badge
        c.setFillColor(colors.HexColor("#06B6D4"))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(45, page_h - 35, "NASA SPACE APPS CHALLENGE  •  DR D ASTRONAUT HEALTH INTELLIGENCE  •  ARES-V TRANSIT")

        c.setFillColor(colors.HexColor("#94A3B8"))
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(page_w - 45, page_h - 35, f"SLIDE {s['num']} / 07")

        # Title
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.setFont("Helvetica-Bold", 18)
        c.drawString(45, page_h - 60, s["title"])

        # Subtitle
        c.setFillColor(colors.HexColor("#E2E8F0"))
        c.setFont("Helvetica", 10.5)
        c.drawString(45, page_h - 78, s["sub"])

        # Card / Content Layout
        if s_idx in [0, 1, 2, 4]:
            # Left text, right image or vice-versa
            if s_idx in [1, 2]:
                # Image on left/center, text card on right
                img_x = 45
                img_y = 45
                img_w = 560
                img_h = 360
                c.setStrokeColor(colors.HexColor("#06B6D4"))
                c.setLineWidth(1)
                c.rect(img_x, img_y, img_w, img_h, fill=0, stroke=1)
                c.drawImage(str(s["img"]), img_x, img_y, width=img_w, height=img_h)

                # Right card
                rc_x = 620
                rc_y = 45
                rc_w = 295
                rc_h = 360
                c.setFillColor(colors.HexColor("#0F172A"))
                c.setStrokeColor(colors.HexColor("#1E293B"))
                c.roundRect(rc_x, rc_y, rc_w, rc_h, 6, fill=1, stroke=1)

                c.setFillColor(colors.HexColor("#22D3EE"))
                c.setFont("Helvetica-Bold", 11)
                c.drawString(rc_x + 15, rc_y + rc_h - 25, s["bullet_title"])

                cur_y = rc_y + rc_h - 55
                for b in s["bullets"]:
                    c.setFillColor(colors.HexColor("#E2E8F0"))
                    c.setFont("Helvetica", 9)
                    # Wrap simple bullet
                    words = b.split()
                    line1 = ""
                    for w in words:
                        if len(line1 + " " + w) < 42:
                            line1 += " " + w
                        else:
                            c.drawString(rc_x + 15, cur_y, "• " + line1.strip() if line1 == words[0] else "  " + line1.strip())
                            cur_y -= 14
                            line1 = w
                    if line1:
                        c.drawString(rc_x + 15, cur_y, ("• " if not b.startswith(line1) else "") + line1.strip())
                        cur_y -= 22
            else:
                # Text on left, image on right (Slide 1 and Slide 5)
                lc_x = 45
                lc_y = 45
                lc_w = 330
                lc_h = 360
                c.setFillColor(colors.HexColor("#0F172A"))
                c.setStrokeColor(colors.HexColor("#1E293B"))
                c.roundRect(lc_x, lc_y, lc_w, lc_h, 6, fill=1, stroke=1)

                c.setFillColor(colors.HexColor("#22D3EE"))
                c.setFont("Helvetica-Bold", 11)
                c.drawString(lc_x + 15, lc_y + lc_h - 25, s["bullet_title"])

                cur_y = lc_y + lc_h - 55
                for b in s["bullets"]:
                    c.setFillColor(colors.HexColor("#E2E8F0"))
                    c.setFont("Helvetica", 9)
                    words = b.split()
                    line1 = ""
                    for w in words:
                        if len(line1 + " " + w) < 46:
                            line1 += " " + w
                        else:
                            c.drawString(lc_x + 15, cur_y, line1.strip())
                            cur_y -= 13
                            line1 = w
                    if line1:
                        c.drawString(lc_x + 15, cur_y, line1.strip())
                        cur_y -= 18

                img_x = 390
                img_y = 45
                img_w = 525
                img_h = 360
                c.setStrokeColor(colors.HexColor("#06B6D4"))
                c.setLineWidth(1)
                c.rect(img_x, img_y, img_w, img_h, fill=0, stroke=1)
                c.drawImage(str(s["img"]), img_x, img_y, width=img_w, height=img_h)

        elif s_idx in [3, 5]:
            # Split screen with 2 images
            img1_x = 45
            img1_y = 110
            img1_w = 425
            img1_h = 290
            c.drawImage(str(s["img"]), img1_x, img1_y, width=img1_w, height=img1_h)
            c.setStrokeColor(colors.HexColor("#F59E0B" if s_idx == 3 else "#EF4444"))
            c.rect(img1_x, img1_y, img1_w, img1_h, fill=0, stroke=1)

            img2_x = 490
            img2_y = 110
            img2_w = 425
            img2_h = 290
            c.drawImage(str(s["img2"]), img2_x, img2_y, width=img2_w, height=img2_h)
            c.setStrokeColor(colors.HexColor("#06B6D4"))
            c.rect(img2_x, img2_y, img2_w, img2_h, fill=0, stroke=1)

            # Bottom caption cards
            c.setFillColor(colors.HexColor("#0F172A"))
            c.setStrokeColor(colors.HexColor("#1E293B"))
            c.roundRect(45, 40, 870, 60, 4, fill=1, stroke=1)
            c.setFillColor(colors.HexColor("#E2E8F0"))
            c.setFont("Helvetica", 8.5)
            c.drawString(55, 80, s["bullets"][0])
            c.drawString(55, 65, s["bullets"][1])
            c.drawString(55, 50, s["bullets"][2] + (" • " + s["bullets"][3] if len(s["bullets"]) > 3 else ""))

        elif s_idx == 6:
            # Slide 7 architecture & cards
            c.setFillColor(colors.HexColor("#0F172A"))
            c.setStrokeColor(colors.HexColor("#06B6D4"))
            c.roundRect(45, 310, 870, 85, 6, fill=1, stroke=1)

            c.setFillColor(colors.HexColor("#22D3EE"))
            c.setFont("Helvetica-Bold", 10)
            c.drawString(60, 375, "DATA FLOW & SYSTEM ARCHITECTURE")
            c.setFillColor(colors.HexColor("#FFFFFF"))
            c.setFont("Helvetica-Bold", 9.5)
            c.drawString(60, 355, "SIMULATED TELEMETRY / ECLSS  ->  FASTAPI BACKEND  ->  HEALTH ANALYTICS & ISOLATION FOREST  ->  HRI & ALERTS  ->  WEBSOCKETS  ->  REACT UI")
            c.setFillColor(colors.HexColor("#94A3B8"))
            c.setFont("Helvetica", 9)
            c.drawString(60, 335, "Built with: Python 3.13 • FastAPI • React 18 • Vite • SQLite • Scikit-learn • NumPy • WebSockets • Recharts • Tailwind CSS")

            # 3 bottom cards
            c1_w = 275
            c1_h = 245
            for c_i, (c_title, c_color, c_text) in enumerate([
                ("THREE CORE CAPABILITIES", "#06B6D4", [
                    "• Total Fleet Visibility: Real-time telemetry.",
                    "• Explainable AI: Personalized Z-score & ML.",
                    "• Medical CDSS: 22-min delay autonomy."
                ]),
                ("NASA SCIENTIFIC GROUNDING", "#F59E0B", [
                    "• NASA HRP 5 Hazards (RIDGE framework).",
                    "• Human Research Roadmap Evidence Reports.",
                    "• NASA ExMC CDSS Architecture (HRP-48032).",
                    "• ExMC IMPACT 1.0 Medical Library."
                ]),
                ("PROVENANCE & CLOSING", "#22D3EE", [
                    "• Data Provenance: Synthetic telemetry.",
                    "• Publications provide clinical context.",
                    "• DR D – NOT TO GET DOOMED IN SPACE",
                    "• \"Your health guardian beyond Earth.\""
                ])
            ]):
                bx = 45 + c_i * (c1_w + 22)
                c.setFillColor(colors.HexColor("#0F172A"))
                c.setStrokeColor(colors.HexColor(c_color))
                c.roundRect(bx, 45, c1_w, c1_h, 6, fill=1, stroke=1)
                c.setFillColor(colors.HexColor(c_color))
                c.setFont("Helvetica-Bold", 10)
                c.drawString(bx + 15, 45 + c1_h - 25, c_title)
                c.setFillColor(colors.HexColor("#E2E8F0"))
                c.setFont("Helvetica", 8.5)
                cy = 45 + c1_h - 55
                for t in c_text:
                    c.drawString(bx + 15, cy, t)
                    cy -= 20

        c.showPage()

    c.save()
    print(f"PDF presentation created successfully at: {PDF_PATH}")

def build_notes_md():
    print(f"Building speaker notes markdown: {NOTES_PATH}")
    content = """# Dr D – Not to Get Doomed in Space
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
"""
    with open(NOTES_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Presenter notes written successfully to: {NOTES_PATH}")

def copy_to_distribution():
    for f in [PPTX_PATH, PDF_PATH, NOTES_PATH]:
        dest = FINAL_DIST_DIR / f.name
        shutil.copy2(f, dest)
        print(f"Mirrored {f.name} to {dest}")

if __name__ == "__main__":
    build_pptx()
    build_pdf()
    build_notes_md()
    copy_to_distribution()
    print("ALL PRESENTATION ARTIFACTS SUCCESSFULLY GENERATED!")
