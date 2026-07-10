import os, re

CERT_DIR = "certificates"
README = "README.md"
COLS = 3  # certificates per row

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

files = sorted(os.listdir(CERT_DIR))
cells = []

for f in files:
    if f.startswith("."):
        continue

    path = f"{CERT_DIR}/{f}"
    name = os.path.splitext(f)[0].replace("-", " ").replace("_", " ").title()
    ext = os.path.splitext(f)[1].lower()

    if ext in IMAGE_EXTS:
        cell = f'<a href="{path}"><img src="{path}" width="180"/></a><br/><sub><b>{name}</b></sub>'
    else:
        cell = f'📄<br/><a href="{path}">{name}</a>'

    cells.append(cell)

# Build an HTML table, COLS cells per row
rows = []
for i in range(0, len(cells), COLS):
    row_cells = cells[i:i + COLS]
    # pad the last row so the table stays aligned
    while len(row_cells) < COLS:
        row_cells.append("")
    row_html = "".join(f'<td align="center">{c}</td>' for c in row_cells)
    rows.append(f"<tr>{row_html}</tr>")

if rows:
    block = "<table>\n" + "\n".join(rows) + "\n</table>"
else:
    block = "_No certificates yet._"

with open(README, "r") as f:
    content = f.read()

new_content = re.sub(
    r"<!-- CERTS-START -->.*<!-- CERTS-END -->",
    f"<!-- CERTS-START -->\n{block}\n<!-- CERTS-END -->",
    content,
    flags=re.DOTALL,
)

with open(README, "w") as f:
    f.write(new_content)