from pathlib import Path
import json
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream")

# gradle.properties
props_path = root / "gradle.properties"
props = props_path.read_text(encoding="utf-8")
replacements = {
    r"(?m)^mod_version=.*$": "mod_version=1.0.0",
    r"(?m)^maven_group=.*$": "maven_group=dev.fixpot47",
    r"(?m)^archives_base_name=.*$": "archives_base_name=see-your-trajectory",
}
for pattern, repl in replacements.items():
    props = re.sub(pattern, repl, props)
props_path.write_text(props, encoding="utf-8")

# Fabric metadata
fabric_path = root / "src/main/resources/fabric.mod.json"
data = json.loads(fabric_path.read_text(encoding="utf-8"))
data["id"] = "seeyourtrajectory"
data["name"] = "See your Trajectory!"
data["description"] = "Preview the trajectory of arrows, snowballs, eggs, tridents, ender pearls and other supported projectiles."
data["authors"] = [
    "fixpot47",
    "maDU59_ (original ProjectilesTrajectoryPreview author)"
]
data["contact"] = {
    "homepage": "https://github.com/fixpot47/see-your-projectory",
    "sources": "https://github.com/fixpot47/see-your-projectory",
    "issues": "https://github.com/fixpot47/see-your-projectory/issues"
}
data["license"] = "MIT"
fabric_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Internal mod namespace/config/networking ID.
ptp_path = root / "src/main/java/fr/madu59/ptp/Ptp.java"
text = ptp_path.read_text(encoding="utf-8")
text = text.replace('public static final String MOD_ID = "ptp";', 'public static final String MOD_ID = "seeyourtrajectory";')
text = text.replace('[PTP] Sending handshake to player...', '[See your Trajectory!] Sending handshake to player...')
text = text.replace('Hello Fabric world!', 'See your Trajectory! initialized.')
ptp_path.write_text(text, encoding="utf-8")

client_path = root / "src/client/java/fr/madu59/ptp/PtpClient.java"
text = client_path.read_text(encoding="utf-8")
text = text.replace('LogManager.getLogger("ptpClient")', 'LogManager.getLogger("SeeYourTrajectoryClient")')
text = text.replace('Identifier.fromNamespaceAndPath("ptp", "ptp")', 'Identifier.fromNamespaceAndPath(Ptp.MOD_ID, Ptp.MOD_ID)')
text = text.replace('[PTP]', '[See your Trajectory!]')
client_path.write_text(text, encoding="utf-8")

# Rebrand visible text while keeping existing translation keys for compatibility.
lang_dir = root / "src/main/resources/assets/ptp/lang"
if lang_dir.exists():
    for path in lang_dir.glob("*.json"):
        try:
            lang = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        changed = False
        for key, value in list(lang.items()):
            if not isinstance(value, str):
                continue
            new_value = value
            for old in (
                "Projectiles Trajectory Prediction",
                "Projectile Trajectory Prediction",
                "Projectiles Trajectory Preview",
                "Projectile Trajectory Preview",
            ):
                new_value = new_value.replace(old, "See your Trajectory!")
            if value.strip() == "PTP":
                new_value = "See your Trajectory!"
            if new_value != value:
                lang[key] = new_value
                changed = True
        if changed:
            path.write_text(json.dumps(lang, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Preserve attribution inside the built jar.
notice = root / "src/main/resources/NOTICE.md"
notice.write_text(
    "# Notice\n\n"
    "See your Trajectory! is based on ProjectilesTrajectoryPreview / Projectiles Trajectory Prediction by maDU59_.\n\n"
    "Original source: https://github.com/maDU59/ProjectilesTrajectoryPreview\n\n"
    "Licensed under the MIT License. Fork maintained by fixpot47.\n",
    encoding="utf-8",
)

print("Applied See your Trajectory! rebrand to", root)
