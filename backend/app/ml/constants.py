FEATURE_NAMES = [
    "kills",
    "deaths",
    "assists",
    "headshots",
    "adr",
    "kast",
    "rating",
]

DEFAULT_N_CLUSTERS = 4
DEFAULT_PCA_COMPONENTS = 3

ARCHETYPE_TEMPLATES = [
    {
        "label": "Entry Fragger",
        "feedback": (
            "Perfil ofensivo con {kills:.1f} kills de media y ADR {adr:.1f}. "
            "Suele liderar la apertura de rounds y forzar duelos."
        ),
    },
    {
        "label": "Star Rifler",
        "feedback": (
            "Rifler de impacto con rating {rating:.2f} y {headshots:.1f} headshots por partida. "
            "Mantiene consistencia en intercambios decisivos."
        ),
    },
    {
        "label": "Support / Utility",
        "feedback": (
            "Contribución de equipo con {assists:.1f} asistencias y KAST {kast:.1f}%. "
            "Perfil orientado a habilitar y sostener al equipo."
        ),
    },
    {
        "label": "Anchor / Lurker",
        "feedback": (
            "Estilo de bajo riesgo con {deaths:.1f} muertes de media y KAST {kast:.1f}%. "
            "Eficaz en control de mapa y cierres de round."
        ),
    },
]

FALLBACK_CLUSTER_PROFILES: dict[int, dict[str, str]] = {
    index: {"label": template["label"], "feedback": template["feedback"].format(
        kills=0, deaths=0, assists=0, headshots=0, adr=0, kast=0, rating=1.0
    )}
    for index, template in enumerate(ARCHETYPE_TEMPLATES)
}
