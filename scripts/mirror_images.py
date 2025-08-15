import os, re, pathlib, hashlib, urllib.parse, shutil
import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "images"
ASSETS.mkdir(parents=True, exist_ok=True)

md_files = list(ROOT.rglob("*.md"))

remote_pat = re.compile(r'!\[[^\]]*\]\((https?://[^\s)]+)\)')
local_pat  = re.compile(r'!\[[^\]]*\]\((?!https?://)([^)\s]+)\)')

def hashed_name(src: str, ext_fallback=".png"):
    ext = os.path.splitext(src)[1] or ext_fallback
    h = hashlib.sha1(src.encode()).hexdigest()
    return f"{h}{ext}"

changed = 0

for md in md_files:
    text = md.read_text(encoding="utf-8")

    def repl_remote(m):
        url = m.group(1)
        name = hashed_name(url, ".png")
        dest = ASSETS / name
        if not dest.exists():
            try:
                r = requests.get(url, timeout=30)
                r.raise_for_status()
                dest.write_bytes(r.content)
                print(f"Downloaded: {url} -> {dest}")
            except Exception as e:
                print(f"Failed: {url} ({e})")
                return m.group(0)
        rel = os.path.relpath(dest, md.parent).replace("\\", "/")
        return m.group(0).replace(url, rel)

    new_text = remote_pat.sub(repl_remote, text)

    def repl_local(m):
        rel_link = m.group(1)
        if rel_link.replace("\\", "/").startswith("assets/images/"):
            return m.group(0)
        src_path = (md.parent / rel_link).resolve()
        if not src_path.exists():
            print(f"Skip missing local: {src_path}")
            return m.group(0)
        name = hashed_name(str(src_path))
        dest = ASSETS / name
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dest)
            print(f"Copied local: {src_path} -> {dest}")
        rel = os.path.relpath(dest, md.parent).replace("\\", "/")
        return m.group(0).replace(rel_link, rel)

    new_text2 = local_pat.sub(repl_local, new_text)

    if new_text2 != text:
        md.write_text(new_text2, encoding="utf-8")
        changed += 1
        print(f"Updated links in {md}")

print(f"Done. Updated {changed} markdown file(s).")
