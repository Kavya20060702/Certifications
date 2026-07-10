import os, re

CERT_DIR = "certificates"
README = "README.md"

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

files = sorted(os.listdir(CERT_DIR))
lines = []
for f in files:
    if f.startswith("."):
        continue

    path = f"{CERT_DIR}/{f}"
    name = os.path.splitext(f)[0].replace("-", " ").replace("_", " ").title()
    ext = os.path.splitext(f)[1].lower()

    if ext in IMAGE_EXTS:
        # Thumbnail preview, clickable to open full size
        lines.append(
            f'<a href="{path}"><img src="{path}" width="200" alt="{name}"/></a><br/><sub>{name}</sub>'
        )
    else:
        # PDF or anything else -> plain link
        lines.append(f"- 📄 [{name}]({path})")

# Wrap image thumbnails in a flex row so they sit side by side
image_lines = [l for l in lines if l.startswith("<a")]
other_lines = [l for l in lines if not l.startswith("<a")]

block_parts = []
if image_lines:
    row = "\n".join(f'<span style="display:inline-block;margin:8px;text-align:center;">{l}</span>' for l in image_lines)
    block_parts.append(f'<div style="display:flex;flex-wrap:wrap;">{row}</div>')
if other_lines:
    block_parts.append("\n".join(other_lines))

block = "\n\n".join(block_parts) if block_parts else "_No certificates yet._"

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