from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Any, Optional

from ..research_data import (
    NASA_HAZARDS,
    NASA_HEALTH_RISKS,
    NASA_EVIDENCE_REPORTS,
    NASA_CDSS_ARCHITECTURE,
    NASA_EIMO_CONOPS,
    NASA_EXPLORATION_CONDITIONS,
    NASA_SOURCE_REGISTRY,
    DATA_PROVENANCE_REGISTRY,
    RESEARCH_EVENT_CONTEXTS
)

router = APIRouter(prefix="/api/research", tags=["NASA Scientific Research & Knowledge Base"])

@router.get("/summary")
def get_research_summary():
    """
    Returns high-level statistics and metadata about the NASA Research Knowledge Layer.
    """
    return {
        "repository_name": "Dr D — Astronaut Health Intelligence Repository",
        "description": "Scientific evidence, spaceflight hazard framework, and clinical decision support architecture grounded in official NASA publications.",
        "hazards_count": len(NASA_HAZARDS),
        "health_risks_count": len(NASA_HEALTH_RISKS),
        "evidence_reports_count": len(NASA_EVIDENCE_REPORTS),
        "exploration_conditions_count": len(NASA_EXPLORATION_CONDITIONS),
        "official_sources_count": len(NASA_SOURCE_REGISTRY),
        "provenance_classifications_count": len(DATA_PROVENANCE_REGISTRY),
        "disclaimer": (
            "NASA publications and technical standards are used as scientific and technical research references. "
            "No direct live NASA biometric telemetry API is integrated into this prototype; all continuous vital streams "
            "are locally generated synthetic telemetry."
        )
    }

@router.get("/hazards")
def get_spaceflight_hazards():
    """
    Returns the 5 core spaceflight hazards defined by NASA Human Research Program (HRP).
    """
    return NASA_HAZARDS

@router.get("/risks")
def get_health_risks(
    hazard_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None) # MONITORED_IN_DR_D, RESEARCH_REFERENCE_ONLY, FUTURE_FLIGHT_SCOPE
):
    """
    Returns astronaut health risks taxonomy with Dr D monitoring status and physiological domain.
    """
    results = NASA_HEALTH_RISKS
    if hazard_id:
        results = [r for r in results if r.get("hazard_id") == hazard_id]
    if status:
        results = [r for r in results if r.get("status") == status.upper()]
    return results

@router.get("/evidence")
def get_evidence_reports(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """
    Returns NASA Human Research Roadmap evidence reports linked to Dr D telemetry features.
    """
    results = NASA_EVIDENCE_REPORTS
    if category:
        results = [r for r in results if category.lower() in r.get("category", "").lower()]
    if search:
        s = search.lower()
        results = [
            r for r in results 
            if s in r.get("title", "").lower() 
            or s in r.get("description", "").lower() 
            or s in r.get("physiological_system", "").lower()
            or s in r.get("dr_d_feature", "").lower()
        ]
    return results

@router.get("/architecture")
def get_cdss_architecture():
    """
    Returns comparative evaluation of Dr D against NASA ExMC CDSS Architecture Recommendation (HRP-48032 Rev. B).
    """
    return NASA_CDSS_ARCHITECTURE

@router.get("/eimo")
def get_eimo_conops():
    """
    Returns operational alignment with NASA ExMC Earth-Independent Medical Operations Concept of Operations (20240001402).
    """
    return NASA_EIMO_CONOPS

@router.get("/conditions")
def get_exploration_conditions(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """
    Returns structured Exploration Medical Condition List (IMPACT 1.0, HRP-48036 Rev. B).
    """
    results = NASA_EXPLORATION_CONDITIONS
    if category:
        results = [c for c in results if category.lower() in c.get("category", "").lower()]
    if search:
        s = search.lower()
        results = [
            c for c in results 
            if s in c.get("name", "").lower() 
            or s in c.get("system", "").lower() 
            or s in c.get("impact_relevance", "").lower()
            or s in c.get("telemetry_stream", "").lower()
        ]
    return results

@router.get("/sources")
def get_nasa_sources():
    """
    Returns the 5 official NASA publications and standards integrated into Dr D with URLs and document IDs.
    """
    return NASA_SOURCE_REGISTRY

@router.get("/provenance")
def get_data_provenance():
    """
    Returns full data provenance classification matrix distinguishing synthetic data from scientific references.
    """
    return DATA_PROVENANCE_REGISTRY

@router.get("/context/{event_type}")
def get_research_event_context(event_type: str):
    """
    Returns scientific research context, NASA hazard category, and evidence rationale for any scenario or alert.
    """
    context = RESEARCH_EVENT_CONTEXTS.get(event_type.lower())
    if not context:
        # Fallback generic context
        return {
            "event_id": event_type,
            "event_name": event_type.replace("_", " ").title(),
            "detected_condition": f"Simulated physiological or environmental anomaly: {event_type}",
            "nasa_hazard": "Spaceflight Physiological Stress",
            "hazard_id": "hazard_gravity",
            "potential_implications": "Requires clinical review by Flight Surgeon or autonomous stabilization.",
            "research_reference": "NASA Human Research Program (HRP) Evidence Library",
            "official_url": "https://humanresearchroadmap.nasa.gov/evidence/",
            "data_source": "Synthetic Telemetry Simulation",
            "suggested_countermeasure": "Review astronaut vitals against baseline and consult clinical protocols.",
            "clinical_evidence_summary": "Spaceflight environmental and physiological extremes require multi-parameter clinical oversight."
        }
    return context
