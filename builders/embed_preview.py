"""Produce a fully self-contained homepage snapshot (home-preview.html at the repo
root) by inlining every local asset referenced in design/home_preview.html as a
base64 data: URI. This is the file served on GitHub Pages, so it must never depend
on the design/assets folder. Run after build_preview (build_all does both)."""
import os, re, base64, mimetypes

ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC  = os.path.join(ROOT, "design", "home_preview.html")
OUT  = os.path.join(ROOT, "home-preview.html")
ASSETS_DIR = os.path.join(ROOT, "design")  # asset refs are relative: "assets/..."

def data_uri(rel_path):
    fpath = os.path.join(ASSETS_DIR, rel_path)
    if not os.path.isfile(fpath):
        return None
    mime = mimetypes.guess_type(fpath)[0] or "application/octet-stream"
    b64 = base64.b64encode(open(fpath, "rb").read()).decode("ascii")
    return f"data:{mime};base64,{b64}"

def main():
    html = open(SRC, encoding="utf-8").read()
    missing = []

    # Inline any assets/... reference, whether in src="...", href="..." or url(...).
    def repl(m):
        pre, rel, post = m.group("pre"), m.group("path"), m.group("post")
        uri = data_uri(rel)
        if uri is None:
            missing.append(rel)
            return m.group(0)
        return f"{pre}{uri}{post}"

    # src="assets/x"  /  href="assets/x"
    html = re.sub(r'(?P<pre>(?:src|href)=")(?P<path>assets/[^"]+)(?P<post>")', repl, html)
    # url(assets/x) with optional quotes
    html = re.sub(r"(?P<pre>url\(['\"]?)(?P<path>assets/[^'\")]+)(?P<post>['\"]?\))", repl, html)

    open(OUT, "w", encoding="utf-8").write(html)
    print("wrote", os.path.abspath(OUT), f"{len(html):,} bytes")
    if missing:
        print("WARNING: could not inline", len(set(missing)), "asset(s):",
              sorted(set(missing))[:10])

if __name__ == "__main__":
    main()
