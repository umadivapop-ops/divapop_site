import os, json, re
from pathlib import Path

# ✅ AJUSTE AQUI: a pasta onde estão as subpastas por data
ROOT = r"C:\Users\profe\Documents\divapop_api\sites\divapop_site\nossa_hitoria_em fotos"

IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

def natural_key(s: str):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", s)]

def extract_date_from_parts(parts):
    # procura um trecho tipo 2026-01-24 em qualquer parte do caminho
    for p in parts:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", p):
            return p
    return ""

def guess_tag(path_str: str):
    p = path_str.lower()
    if "ensaio" in p:
        return "ensaio"
    if "bastidor" in p:
        return "bastidores"
    if "palco" in p or "show" in p:
        return "palco"
    if "estudio" in p or "studio" in p or "grav" in p:
        return "estudio"
    if "carnaval" in p:
        return "carnaval"
    if "quanto" in p or "qtt" in p:
        return "qtt"
    return "foto"

root = Path(ROOT)
if not root.exists():
    raise SystemExit(f"Pasta não encontrada: {ROOT}")

items = []
for dirpath, _, filenames in os.walk(root):
    filenames = sorted(filenames, key=natural_key)
    for fn in filenames:
        ext = Path(fn).suffix.lower()
        if ext not in IMG_EXTS:
            continue

        full = Path(dirpath) / fn
        rel = full.relative_to(root).as_posix()  # caminho relativo com "/"

        parts = rel.split("/")
        date = extract_date_from_parts(parts[:-1])  # subpastas
        tag = guess_tag(rel)

        # título bonitinho (sem extensão)
        title = Path(fn).stem.replace("_", " ").strip()

        items.append({
            "src": rel,
            "date": date,
            "tag": tag,
            "title": title,
            "text": ""
        })

# Ordena por date (quando existir) e depois por src
items.sort(key=lambda x: ((x["date"] or "9999-99-99"), x["src"]))

out_path = root / "manifest.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"✅ manifest.json criado com {len(items)} fotos em: {out_path}")
