import os

ignore_dirs = {"node_modules", ".git", "dist", "build", "__pycache__", ".pytest_cache", "pdf_previews"}
ignore_exts = {".png", ".jpg", ".jpeg", ".ico", ".db", ".pdf", ".docx", ".log"}

matches = []
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

for root, dirs, files in os.walk(root_dir):
    # filter dirs in-place
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    for file in files:
        if file == "verify_rebrand.py" or any(file.endswith(ext) for ext in ignore_exts):
            continue
        full_path = os.path.join(root, file)
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "hermes" in content.lower():
                    # Check lines
                    for line_idx, line in enumerate(content.splitlines(), start=1):
                        if "hermes" in line.lower():
                            matches.append((os.path.relpath(full_path, root_dir), line_idx, line.strip()))
        except Exception:
            pass

print("========================================================")
print(f"  REPO-WIDE 'HERMES' AUDIT SEARCH: {len(matches)} MATCHES FOUND")
print("========================================================")
if matches:
    for rel_path, line_no, line in matches:
        print(f"{rel_path}:{line_no} -> {line}")
else:
    print("Zero case-insensitive occurrences of 'hermes' found in active codebase!")
print("========================================================\n")
