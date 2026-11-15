"""
Generate agency-grade architecture and data-flow diagrams for Dr D
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def setup_dirs():
    os.makedirs('docs/diagrams', exist_ok=True)
    os.makedirs('docs/screenshots', exist_ok=True)

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(16, 10), facecolor='#090d16')
    ax.set_facecolor('#090d16')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(8, 9.5, "Dr D — System Architecture & Component Topology", 
            ha='center', va='center', color='#38bdf8', fontsize=18, fontweight='bold', family='sans-serif')
    ax.text(8, 9.1, "Autonomous Deep Space Medical Operations Platform • Ares-V Architecture", 
            ha='center', va='center', color='#94a3b8', fontsize=11, family='sans-serif')

    layers = [
        {"y": 7.3, "h": 1.3, "title": "1. Telemetry & Simulation Layer", "color": "#0ea5e9",
         "boxes": [("Bio-Wearables Simulation\n(HR, SpO2, Temp, BP, Resp)", 0.6, 3.4),
                   ("ECLSS Atmospheric Sensors\n(CO2, O2, Pressure, Ambient)", 4.4, 3.4),
                   ("CSV Historical Batch Replay\n(Longitudinal Mission Telemetry)", 8.2, 3.4),
                   ("Crisis Scenario Injection\n(Solar Storm, CO2 Spike, EVA Stress)", 12.0, 3.4)]},
        {"y": 5.4, "h": 1.3, "title": "2. Ingestion & Communication Layer", "color": "#06b6d4",
         "boxes": [("FastAPI REST Engine\n(Endpoints /api/telemetry, /api/auth)", 0.6, 3.4),
                   ("JWT & Rate Limiting\n(Sliding Window Throttler)", 4.4, 3.4),
                   ("Starlette WebSocket Hub\n(1-2 Hz Real-Time Broadcast /ws/live)", 8.2, 3.4),
                   ("Pydantic V2 Validation\n(Strict Range & Type Enforcement)", 12.0, 3.4)]},
        {"y": 3.5, "h": 1.3, "title": "3. Intelligence, Analytics & Anomaly Detection Layer", "color": "#8b5cf6",
         "boxes": [("Isolation Forest Detector\n(Multi-variate Unsupervised Anomaly)", 0.6, 3.4),
                   ("Z-Score Baseline Monitor\n(Rolling 30-sol Microgravity Delta)", 4.4, 3.4),
                   ("Composite Health Risk Index\n(0-100 Weighted Risk Scoring Engine)", 8.2, 3.4),
                   ("Dr D Clinical Advisor\n(Actionable Countermeasure Rules)", 12.0, 3.4)]},
        {"y": 1.6, "h": 1.3, "title": "4. Persistence, Reporting & Presentation Layer", "color": "#10b981",
         "boxes": [("SQLAlchemy 2.0 ORM\n(dr_d.db SQLite / PostgreSQL)", 0.6, 3.4),
                   ("ReportLab / CSV Engine\n(Clinical Dossier & PDF Generation)", 4.4, 3.4),
                   ("Flight Surgeon Mission HUD\n(React 18, Vite, Tailwind CSS)", 8.2, 3.4),
                   ("Astronaut Wellbeing Tablet\n(Biometric Check-in & Personal View)", 12.0, 3.4)]}
    ]

    for layer in layers:
        # Layer Header Box
        rect_layer = patches.FancyBboxPatch((0.4, layer["y"]), 15.2, layer["h"], 
                                            boxstyle="round,pad=0.1,rounding_size=0.15", 
                                            linewidth=1.2, edgecolor=layer["color"], facecolor='#0f172a', alpha=0.9)
        ax.add_patch(rect_layer)
        ax.text(0.7, layer["y"] + layer["h"] - 0.22, layer["title"], 
                color=layer["color"], fontsize=11, fontweight='bold', family='sans-serif')

        # Sub-boxes
        for title, x, w in layer["boxes"]:
            sub_rect = patches.FancyBboxPatch((x, layer["y"] + 0.12), w, layer["h"] - 0.42, 
                                              boxstyle="round,pad=0.08,rounding_size=0.1", 
                                              linewidth=0.8, edgecolor='#334155', facecolor='#1e293b')
            ax.add_patch(sub_rect)
            ax.text(x + w/2, layer["y"] + 0.58, title, 
                    ha='center', va='center', color='#f8fafc', fontsize=8.5, family='sans-serif')

    # Flow arrows between layers
    arrow_props = dict(facecolor='#38bdf8', edgecolor='#38bdf8', width=2, headwidth=8, headlength=7, alpha=0.7)
    for x_arr in [2.3, 6.1, 9.9, 13.7]:
        ax.annotate('', xy=(x_arr, 6.7), xytext=(x_arr, 7.3), arrowprops=arrow_props)
        ax.annotate('', xy=(x_arr, 4.8), xytext=(x_arr, 5.4), arrowprops=arrow_props)
        ax.annotate('', xy=(x_arr, 2.9), xytext=(x_arr, 3.5), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig('docs/diagrams/architecture_diagram.png', dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.savefig('docs/diagrams/architecture_diagram.svg', bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Generated architecture_diagram.png & .svg")

def generate_data_flow_diagram():
    fig, ax = plt.subplots(figsize=(16, 7), facecolor='#090d16')
    ax.set_facecolor('#090d16')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 7)
    ax.axis('off')

    # Title
    ax.text(8, 6.5, "Dr D — Telemetry Data Pipeline & Clinical Inference Flow", 
            ha='center', va='center', color='#38bdf8', fontsize=17, fontweight='bold', family='sans-serif')
    ax.text(8, 6.1, "Autonomous Edge Pipeline from Physiological Sensor to Mission Control Alerting", 
            ha='center', va='center', color='#94a3b8', fontsize=10.5, family='sans-serif')

    steps = [
        {"x": 0.5, "w": 2.2, "title": "1. SENSORS", "desc": "Wearables (HR, SpO2)\nECLSS (CO2, O2, kPa)\nSimulator Engine", "color": "#0ea5e9"},
        {"x": 3.1, "w": 2.2, "title": "2. INGESTION", "desc": "FastAPI Validation\nPydantic V2 Schemas\nDB Commit (SQLite)", "color": "#06b6d4"},
        {"x": 5.7, "w": 2.2, "title": "3. BASELINES", "desc": "Rolling Mean / Std\nZ-Score Variance\nMicrogravity Drift", "color": "#6366f1"},
        {"x": 8.3, "w": 2.2, "title": "4. ML & ANOMALY", "desc": "Isolation Forest\nMulti-variate Clusters\nTrend Regression", "color": "#8b5cf6"},
        {"x": 10.9, "w": 2.2, "title": "5. RISK SCORING", "desc": "Composite Risk (0-100)\nThresholds (Warn/Crit)\nWeight Allocation", "color": "#ec4899"},
        {"x": 13.5, "w": 2.2, "title": "6. MISSION HUD", "desc": "WebSocket Broadcast\nLive Alert Banner\nAdvisor Suggestions", "color": "#10b981"}
    ]

    for step in steps:
        # Box
        rect = patches.FancyBboxPatch((step["x"], 1.8), step["w"], 3.5, 
                                      boxstyle="round,pad=0.1,rounding_size=0.15", 
                                      linewidth=1.2, edgecolor=step["color"], facecolor='#0f172a', alpha=0.9)
        ax.add_patch(rect)
        
        # Header bar
        header_rect = patches.FancyBboxPatch((step["x"], 4.7), step["w"], 0.6, 
                                            boxstyle="round,pad=0.05,rounding_size=0.1", 
                                            linewidth=0, facecolor=step["color"])
        ax.add_patch(header_rect)
        ax.text(step["x"] + step["w"]/2, 5.0, step["title"], 
                ha='center', va='center', color='#0f172a', fontsize=9.5, fontweight='bold', family='sans-serif')

        # Desc
        ax.text(step["x"] + step["w"]/2, 3.2, step["desc"], 
                ha='center', va='center', color='#f8fafc', fontsize=8.5, family='sans-serif', linespacing=1.6)

    # Connector arrows
    arrow_props = dict(facecolor='#38bdf8', edgecolor='#38bdf8', width=2.5, headwidth=9, headlength=8, alpha=0.8)
    for i in range(len(steps) - 1):
        x1 = steps[i]["x"] + steps[i]["w"] + 0.05
        x2 = steps[i+1]["x"] - 0.05
        ax.annotate('', xy=(x2, 3.5), xytext=(x1, 3.5), arrowprops=arrow_props)

    # Feedback / Countermeasure Loop below
    feedback_rect = patches.FancyBboxPatch((3.1, 0.4), 10.0, 0.9, 
                                           boxstyle="round,pad=0.08,rounding_size=0.1", 
                                           linewidth=1.0, edgecolor='#f59e0b', facecolor='#1e293b', linestyle='--')
    ax.add_patch(feedback_rect)
    ax.text(8.1, 0.85, "Closed-Loop Countermeasures: Dr D Clinical Advisor -> Ground Surgeon Intervention -> Astronaut Protocol Adjustment", 
            ha='center', va='center', color='#fbbf24', fontsize=8.5, fontweight='bold', family='sans-serif')

    plt.tight_layout()
    plt.savefig('docs/diagrams/data_flow_diagram.png', dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.savefig('docs/diagrams/data_flow_diagram.svg', bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Generated data_flow_diagram.png & .svg")

if __name__ == "__main__":
    setup_dirs()
    generate_architecture_diagram()
    generate_data_flow_diagram()
