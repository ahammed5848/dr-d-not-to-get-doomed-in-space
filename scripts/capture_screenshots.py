"""
Dr D — High-Resolution Automated Screenshot Capture Suite
Uses Playwright to capture high-definition (1920x1080 @ 2x DPR) screenshots of all platform capabilities.
"""
import os
import sys
import time
import json
import subprocess
import urllib.request
import urllib.error
from playwright.sync_api import sync_playwright

BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://127.0.0.1:5173"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "docs", "screenshots"))

PYTHON_EXE = sys.executable
NODE_DIR = r"C:\Users\AHAMMED\AppData\Local\Programs\nodejs"
NPM_CMD = os.path.join(NODE_DIR, "npm.cmd")
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

def is_url_ready(url, timeout=1.0):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DrD-Tester"})
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return res.status in (200, 304, 404)
    except Exception:
        return False

def post_json(endpoint, payload):
    try:
        req = urllib.request.Request(
            f"{BACKEND_URL}{endpoint}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "DrD-Tester"}
        )
        with urllib.request.urlopen(req, timeout=5.0) as res:
            return res.status
    except Exception as e:
        print(f"[Warning] POST {endpoint} failed: {e}")
        return None

def ensure_servers_running():
    spawned = []
    env = os.environ.copy()
    env["PATH"] = f"{NODE_DIR};{env.get('PATH', '')}"

    if not is_url_ready(f"{BACKEND_URL}/docs"):
        print("[Startup] Starting Dr D Backend (FastAPI + Simulation)...")
        backend_proc = subprocess.Popen(
            [PYTHON_EXE, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
            cwd=BACKEND_DIR,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        spawned.append(backend_proc)

    if not is_url_ready(FRONTEND_URL):
        print("[Startup] Starting Dr D Frontend (Vite)...")
        frontend_proc = subprocess.Popen(
            [NPM_CMD, "run", "dev", "--", "--host", "127.0.0.1"],
            cwd=FRONTEND_DIR,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        spawned.append(frontend_proc)

    print("[Startup] Waiting for servers to become ready...")
    for _ in range(40):
        b_ok = is_url_ready(f"{BACKEND_URL}/docs")
        f_ok = is_url_ready(FRONTEND_URL)
        if b_ok and f_ok:
            print("[Startup] Both Backend and Frontend are operational!")
            return spawned
        time.sleep(1)

    print("[Warning] Timed out waiting for servers. Proceeding with caution.")
    return spawned

def capture_all_screenshots():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    spawned_procs = ensure_servers_running()
    manifest = []

    try:
        with sync_playwright() as p:
            print("[Browser] Launching Chromium headless instance...")
            browser = p.chromium.launch(headless=True)

            def new_desktop_context():
                return browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    device_scale_factor=2,
                    color_scheme="dark"
                )

            # ----------------------------------------------------
            # 1. Login Page
            # ----------------------------------------------------
            print("[Capture 1/14] 01_login.png...")
            ctx = new_desktop_context()
            page = ctx.new_page()
            page.goto(f"{FRONTEND_URL}/login")
            page.wait_for_selector('text=1-Click Hackathon Demo Roles', timeout=15000)
            page.wait_for_timeout(1500)
            path_01 = os.path.join(OUTPUT_DIR, "01_login.png")
            page.screenshot(path=path_01)
            manifest.append(("01_login.png", "Dr D Secure Entry Portal with role-based quick authentication"))

            # ----------------------------------------------------
            # 2. Mission Control Dashboard (Nominal) - Flight Surgeon
            # ----------------------------------------------------
            print("[Capture 2/14] 02_dashboard_nominal.png...")
            page.click('button:has-text("Flight Surgeon")')
            page.wait_for_url("**/dashboard", timeout=15000)
            page.wait_for_selector('text=Commander Sarah Chen', timeout=15000)
            page.wait_for_timeout(4000)
            path_02 = os.path.join(OUTPUT_DIR, "02_dashboard_nominal.png")
            page.screenshot(path=path_02)
            manifest.append(("02_dashboard_nominal.png", "Mission Control Operations HUD with multi-crew biometric status and ECLSS status"))

            # ----------------------------------------------------
            # 3. Astronaut Detail Page with Live Telemetry Charts
            # ----------------------------------------------------
            print("[Capture 3/14] 03_astronaut_detail.png...")
            page.goto(f"{FRONTEND_URL}/astronauts/1")
            page.wait_for_selector('text=Commander Sarah Chen', timeout=15000)
            page.wait_for_timeout(3500)
            path_03 = os.path.join(OUTPUT_DIR, "03_astronaut_detail.png")
            page.screenshot(path=path_03)
            manifest.append(("03_astronaut_detail.png", "Astronaut Biometrics Telemetry Detail with anatomical silhouette and live charts"))

            # ----------------------------------------------------
            # 4. Risk Index Gauge & Explainability Breakdown
            # ----------------------------------------------------
            print("[Capture 4/14] 04_risk_index_gauge.png...")
            risk_header = page.locator('text=HEALTH RISK INDEX (HRI) & EXPLAINABILITY').first
            risk_header.scroll_into_view_if_needed()
            page.wait_for_timeout(1500)
            path_04 = os.path.join(OUTPUT_DIR, "04_risk_index_gauge.png")
            page.screenshot(path=path_04)
            manifest.append(("04_risk_index_gauge.png", "Composite Health Risk Index (0-100) gauge and multi-variable explainability breakdown"))

            # ----------------------------------------------------
            # 5. Predictive Forecast Overlay (Next 30 Minutes)
            # ----------------------------------------------------
            print("[Capture 5/14] 05_forecast_overlay.png...")
            forecast_sec = page.locator('text=30-Minute Predictive Forecast').first
            if forecast_sec.count() > 0:
                forecast_sec.scroll_into_view_if_needed()
                page.wait_for_timeout(1500)
            path_05 = os.path.join(OUTPUT_DIR, "05_forecast_overlay.png")
            page.screenshot(path=path_05)
            manifest.append(("05_forecast_overlay.png", "Predictive 30-minute vital horizon forecast with threshold breach detection"))

            # ----------------------------------------------------
            # 6. Alerts Center Page
            # ----------------------------------------------------
            print("[Capture 6/14] 06_alerts_center.png...")
            page.goto(f"{FRONTEND_URL}/alerts")
            page.wait_for_selector('text=MISSION ALERTS & INCIDENT MANAGEMENT CENTER', timeout=15000)
            page.wait_for_timeout(2500)
            path_06 = os.path.join(OUTPUT_DIR, "06_alerts_center.png")
            page.screenshot(path=path_06)
            manifest.append(("06_alerts_center.png", "Alerts Center with tri-level severity filters, crew filter, and triage action log"))

            # ----------------------------------------------------
            # 7. Cabin Environment & ECLSS Correlation
            # ----------------------------------------------------
            print("[Capture 7/14] 07_environment_eclss.png...")
            page.goto(f"{FRONTEND_URL}/environment")
            page.wait_for_selector('text=HABITATION MODULE ENVIRONMENTAL CONTROL & LIFE SUPPORT (ECLSS)', timeout=15000)
            page.wait_for_timeout(3000)
            path_07 = os.path.join(OUTPUT_DIR, "07_environment_eclss.png")
            page.screenshot(path=path_07)
            manifest.append(("07_environment_eclss.png", "Cabin ECLSS Atmospheric Telemetry and Physiological Correlation Matrix"))

            # ----------------------------------------------------
            # 8. Longitudinal Mission Trends
            # ----------------------------------------------------
            print("[Capture 8/14] 08_mission_trends.png...")
            page.goto(f"{FRONTEND_URL}/trends")
            page.wait_for_selector('text=LONG-DURATION SPACEFLIGHT PHYSIOLOGICAL TRENDS', timeout=15000)
            page.wait_for_timeout(3000)
            path_08 = os.path.join(OUTPUT_DIR, "08_mission_trends.png")
            page.screenshot(path=path_08)
            manifest.append(("08_mission_trends.png", "Longitudinal multi-sol physiological trends (Radiation dose, Bone mineral loss, Muscle mass)"))

            # ----------------------------------------------------
            # 9. Daily Wellbeing Check-in Page (Astronaut Role)
            # ----------------------------------------------------
            print("[Capture 9/14] 09_daily_checkin.png...")
            ctx.close()
            ctx_astro = new_desktop_context()
            page_astro = ctx_astro.new_page()
            page_astro.goto(f"{FRONTEND_URL}/login")
            page_astro.wait_for_selector('button:has-text("Cmdr. Sarah Chen")', timeout=15000)
            page_astro.click('button:has-text("Cmdr. Sarah Chen")')
            page_astro.wait_for_url("**/dashboard", timeout=15000)
            page_astro.goto(f"{FRONTEND_URL}/checkin")
            page_astro.wait_for_selector('text=ASTRONAUT DAILY SUBJECTIVE WELLBEING CHECK-IN', timeout=15000)
            page_astro.wait_for_timeout(2500)
            path_09 = os.path.join(OUTPUT_DIR, "09_daily_checkin.png")
            page_astro.screenshot(path=path_09)
            manifest.append(("09_daily_checkin.png", "Astronaut Daily Psychological & Somatic Wellbeing Check-In form with 1-10 Likert scales"))
            ctx_astro.close()

            # ----------------------------------------------------
            # 10. Demo Scenario Injection Modal Open
            # ----------------------------------------------------
            print("[Capture 10/14] 10_demo_matrix_modal.png...")
            ctx_demo = new_desktop_context()
            page_demo = ctx_demo.new_page()
            page_demo.goto(f"{FRONTEND_URL}/login")
            page_demo.wait_for_selector('button:has-text("Flight Surgeon")', timeout=15000)
            page_demo.click('button:has-text("Flight Surgeon")')
            page_demo.wait_for_url("**/dashboard", timeout=15000)
            page_demo.wait_for_timeout(2500)
            demo_btn = page_demo.locator('button:has-text("DEMO SCENARIOS")').first
            demo_btn.click()
            page_demo.wait_for_selector('text=CRISIS SCENARIOS (6 INJECTIONS)', timeout=15000)
            page_demo.wait_for_timeout(1500)
            path_10 = os.path.join(OUTPUT_DIR, "10_demo_matrix_modal.png")
            page_demo.screenshot(path=path_10)
            manifest.append(("10_demo_matrix_modal.png", "Mission Simulation Engine Modal displaying 6 physiological crisis injection scenarios"))
            ctx_demo.close()

            # ----------------------------------------------------
            # 11. Dashboard Under Critical Scenario Injection
            # ----------------------------------------------------
            print("[Capture 11/14] 11_dashboard_critical_scenario.png...")
            # Trigger CO2 spike and radiation storm directly via simulation API
            post_json("/api/simulation/scenario", {"scenario_type": "co2_spike", "severity": "severe"})
            post_json("/api/simulation/scenario", {"scenario_type": "radiation_storm", "severity": "severe"})
            
            ctx_crit = new_desktop_context()
            page_crit = ctx_crit.new_page()
            page_crit.goto(f"{FRONTEND_URL}/login")
            page_crit.wait_for_selector('button:has-text("Flight Surgeon")', timeout=15000)
            page_crit.click('button:has-text("Flight Surgeon")')
            page_crit.wait_for_url("**/dashboard", timeout=15000)
            page_crit.wait_for_timeout(4500)  # Wait for critical alerts and red alert banner to trigger
            path_11 = os.path.join(OUTPUT_DIR, "11_dashboard_critical_scenario.png")
            page_crit.screenshot(path=path_11)
            manifest.append(("11_dashboard_critical_scenario.png", "Mission Control Dashboard in CRITICAL alert state following cabin CO2 and radiation anomalies"))

            # ----------------------------------------------------
            # 12. Reports Dossier & Export Center
            # ----------------------------------------------------
            print("[Capture 12/14] 12_reports_dossier.png...")
            page_crit.goto(f"{FRONTEND_URL}/reports")
            page_crit.wait_for_selector('text=MISSION CLINICAL TELEMETRY REPORTS & ARCHIVAL EXPORT', timeout=15000)
            page_crit.wait_for_timeout(2500)
            path_12 = os.path.join(OUTPUT_DIR, "12_reports_dossier.png")
            page_crit.screenshot(path=path_12)
            manifest.append(("12_reports_dossier.png", "Comprehensive Biometric Report Dossier with date range filters and PDF/CSV export"))
            ctx_crit.close()

            # ----------------------------------------------------
            # 13. Admin Clinical Thresholds Configuration
            # ----------------------------------------------------
            print("[Capture 13/14] 13_admin_thresholds.png...")
            ctx_admin = new_desktop_context()
            page_admin = ctx_admin.new_page()
            page_admin.goto(f"{FRONTEND_URL}/login")
            page_admin.wait_for_selector('button:has-text("Mission Admin")', timeout=15000)
            page_admin.click('button:has-text("Mission Admin")')
            page_admin.wait_for_url("**/dashboard", timeout=15000)
            page_admin.goto(f"{FRONTEND_URL}/admin/thresholds")
            page_admin.wait_for_selector('text=ADMINISTRATION & THRESHOLD CALIBRATION MATRIX', timeout=15000)
            page_admin.wait_for_timeout(2500)
            path_13 = os.path.join(OUTPUT_DIR, "13_admin_thresholds.png")
            page_admin.screenshot(path=path_13)
            manifest.append(("13_admin_thresholds.png", "Flight Surgeon & Administrator Threshold Calibration Matrix with validation bounds"))
            ctx_admin.close()

            # ----------------------------------------------------
            # 14. Responsive Mobile Viewport (390x844)
            # ----------------------------------------------------
            print("[Capture 14/14] 14_dashboard_mobile.png...")
            ctx_mobile = browser.new_context(
                viewport={"width": 390, "height": 844},
                device_scale_factor=2,
                is_mobile=True,
                color_scheme="dark"
            )
            page_mobile = ctx_mobile.new_page()
            page_mobile.goto(f"{FRONTEND_URL}/login")
            page_mobile.wait_for_selector('button:has-text("Flight Surgeon")', timeout=15000)
            page_mobile.click('button:has-text("Flight Surgeon")')
            page_mobile.wait_for_url("**/dashboard", timeout=15000)
            page_mobile.wait_for_timeout(3500)
            path_14 = os.path.join(OUTPUT_DIR, "14_dashboard_mobile.png")
            page_mobile.screenshot(path=path_14)
            manifest.append(("14_dashboard_mobile.png", "Mobile handheld HUD (390x844) responsive layout for astronaut suit-side display"))
            ctx_mobile.close()

            browser.close()

    finally:
        for proc in spawned_procs:
            try:
                proc.terminate()
            except Exception:
                pass

    print("\n========================================================")
    print("  DR D AUTOMATED SCREENSHOT MANIFEST (14 CAPTURES)")
    print("========================================================")
    for filename, description in manifest:
        full_path = os.path.join(OUTPUT_DIR, filename)
        size_kb = os.path.getsize(full_path) / 1024 if os.path.exists(full_path) else 0
        print(f"[{filename}] ({size_kb:.1f} KB) -> {description}")
    print("========================================================\n")

if __name__ == "__main__":
    capture_all_screenshots()
