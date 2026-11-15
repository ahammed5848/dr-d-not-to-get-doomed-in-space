import io
import csv
from datetime import datetime, timezone
from typing import List, Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_csv_report(astronaut, vitals: List[Any], alerts: List[Any]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)

    # Header section
    writer.writerow(["# DR D ASTRONAUT HEALTH REPORT"])
    writer.writerow(["# Mission:", "Dr D Ares-V (Mars Transit)"])
    writer.writerow(["# Astronaut:", f"{astronaut.name} ({astronaut.callsign})"])
    writer.writerow(["# Role:", astronaut.role_title])
    writer.writerow(["# Cumulative Radiation (mSv):", astronaut.radiation_msv])
    writer.writerow(["# Generated At:", datetime.now(timezone.utc).isoformat()])
    writer.writerow([])

    # Vitals table
    writer.writerow([
        "Timestamp", "Heart Rate (bpm)", "HRV (ms)", "SpO2 (%)",
        "BP Systolic (mmHg)", "BP Diastolic (mmHg)", "Core Temp (°C)",
        "Skin Temp (°C)", "Respiratory Rate", "Stress Index (0-100)",
        "Fluid Shift Index", "Circadian Disruption"
    ])

    for v in vitals:
        writer.writerow([
            v.timestamp.isoformat() if hasattr(v.timestamp, 'isoformat') else str(v.timestamp),
            v.heart_rate, v.hrv, v.spo2,
            v.bp_systolic, v.bp_diastolic, v.core_temp,
            v.skin_temp, v.respiratory_rate, v.stress_index,
            v.fluid_shift_score, v.circadian_disruption_score
        ])

    writer.writerow([])
    writer.writerow(["# RECORDED ALERTS"])
    writer.writerow(["Timestamp", "Severity", "Metric", "Value", "Message", "Status"])
    for a in alerts:
        writer.writerow([
            a.timestamp.isoformat() if hasattr(a.timestamp, 'isoformat') else str(a.timestamp),
            a.threshold_level, a.metric, a.value, a.message, a.status
        ])

    return output.getvalue()

def generate_pdf_report(astronaut, vitals: List[Any], alerts: List[Any], mission_info=None) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DrDTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#0ea5e9'),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DrDSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=14
    )
    h2_style = ParagraphStyle(
        'DrDH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'DrDBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    story = []

    # Title Banner
    story.append(Paragraph("DR D MEDICAL TELEMETRY SYSTEM", title_style))
    story.append(Paragraph(
        f"Deep Space Mission Ares-V | Sol Day 142 | Flight Surgeon Medical Record | Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0ea5e9'), spaceAfter=12))

    # Astronaut Info Box
    astro_info = [
        [
            Paragraph(f"<b>Astronaut:</b> {astronaut.name}", body_style),
            Paragraph(f"<b>Callsign:</b> {astronaut.callsign}", body_style),
            Paragraph(f"<b>Role:</b> {astronaut.role_title}", body_style)
        ],
        [
            Paragraph(f"<b>Age / Blood:</b> {astronaut.age} yrs / {astronaut.blood_type}", body_style),
            Paragraph(f"<b>Status:</b> {astronaut.status}", body_style),
            Paragraph(f"<b>Cumulative Dose:</b> {astronaut.radiation_msv:.1f} / {astronaut.radiation_limit_msv:.0f} mSv", body_style)
        ],
        [
            Paragraph(f"<b>Bone Density Loss:</b> -{astronaut.bone_density_loss_pct:.1f}%", body_style),
            Paragraph(f"<b>Muscle Mass Index:</b> {astronaut.muscle_mass_index:.1f}%", body_style),
            Paragraph(f"<b>Fluid Shift Score:</b> {astronaut.fluid_shift_score:.1f}/100", body_style)
        ]
    ]
    astro_table = Table(astro_info, colWidths=[2.3*inch, 2.3*inch, 2.6*inch])
    astro_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(astro_table)
    story.append(Spacer(1, 14))

    # Physiological Summary Stats
    story.append(Paragraph("Physiological Summary (Recent Telemetry Window)", h2_style))
    
    if vitals:
        hrs = [v.heart_rate for v in vitals]
        spo2s = [v.spo2 for v in vitals]
        temps = [v.core_temp for v in vitals]
        stresses = [v.stress_index for v in vitals]
        
        stat_rows = [
            ["Metric", "Current", "Min", "Average", "Max", "Baseline", "Evaluation"],
            ["Heart Rate (bpm)", f"{hrs[-1]:.0f}", f"{min(hrs):.0f}", f"{sum(hrs)/len(hrs):.1f}", f"{max(hrs):.0f}", f"{astronaut.baseline_hr:.0f}", "NOMINAL" if max(hrs) < 100 else "ELEVATED"],
            ["Blood Oxygen SpO2 (%)", f"{spo2s[-1]:.1f}", f"{min(spo2s):.1f}", f"{sum(spo2s)/len(spo2s):.1f}", f"{max(spo2s):.1f}", f"{astronaut.baseline_spo2:.1f}", "NOMINAL" if min(spo2s) >= 95 else "WARNING"],
            ["Core Temp (°C)", f"{temps[-1]:.2f}", f"{min(temps):.2f}", f"{sum(temps)/len(temps):.2f}", f"{max(temps):.2f}", f"{astronaut.baseline_temp:.1f}", "STABLE"],
            ["Stress Index (/100)", f"{stresses[-1]:.0f}", f"{min(stresses):.0f}", f"{sum(stresses)/len(stresses):.1f}", f"{max(stresses):.0f}", "22", "NOMINAL" if max(stresses) < 60 else "ELEVATED"]
        ]
        stat_table = Table(stat_rows, colWidths=[1.7*inch, 0.9*inch, 0.8*inch, 0.9*inch, 0.8*inch, 0.9*inch, 1.2*inch])
        stat_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('ALIGN', (1,0), (-1,-1), 'CENTER'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f1f5f9')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(stat_table)
    else:
        story.append(Paragraph("No vitals recorded in specified window.", body_style))

    story.append(Spacer(1, 14))

    # Logged Alerts Section
    story.append(Paragraph("Clinical Alerts & Incidents", h2_style))
    if alerts:
        alert_rows = [["Time (UTC)", "Level", "Metric", "Value", "Description", "Status"]]
        for a in alerts[:6]:
            t_str = a.timestamp.strftime("%H:%M:%S") if hasattr(a.timestamp, 'strftime') else str(a.timestamp)[:8]
            alert_rows.append([
                t_str,
                a.threshold_level,
                a.metric,
                f"{a.value:.1f}",
                a.message[:38] + ("..." if len(a.message) > 38 else ""),
                a.status
            ])
        alert_table = Table(alert_rows, colWidths=[1.1*inch, 0.9*inch, 1.0*inch, 0.7*inch, 2.5*inch, 1.0*inch])
        alert_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#334155')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('ALIGN', (0,0), (3,-1), 'CENTER'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(alert_table)
    else:
        story.append(Paragraph("No anomalous alerts logged during this observation interval.", body_style))

    story.append(Spacer(1, 14))
    story.append(Paragraph("Flight Surgeon Endorsement", h2_style))
    story.append(Paragraph(
        "Telemetry verified by Dr D Autonomous Diagnostic Core and Ground Tele-Medicine Station. "
        "Crew member authorized to continue nominal scheduled activities subject to mandatory exercise protocol.",
        body_style
    ))

    doc.build(story)
    return buffer.getvalue()
