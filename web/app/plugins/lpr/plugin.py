from web.app.plugins.models import Plugin


plugin = Plugin(
    plugin_id="lpr",
    name="License Plate Recognition",
    short_name="LPR",
    description=(
        "Live-Kamerabild, YOLO-Erkennung, Kennzeichenerkennung, "
        "OCR und Passage-Auswertung."
    ),
    route="/applications/lpr",
    status="available",
    enabled=True,
)
