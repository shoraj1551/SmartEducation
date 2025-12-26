import os, re, ast, json
from pathlib import Path

PROJECT_ROOT = Path(r"C:/Users/SHORAJ TOMER/SmartEducation")
REPORT_PATH = PROJECT_ROOT / "bugs_report.md"

def write_report(content):
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(content)

def find_hardcoded_patterns():
    patterns = {
        "urls": re.compile(r"https?://[\w./?=&%-]+"),
        "secrets": re.compile(r"(?i)(secret|key|token|password)[^\n]{0,30}"),
        "numeric_literals": re.compile(r"[^\w]([0-9]{2,})[^\w]")
    }
    findings = {k: [] for k in patterns}
    for py_file in PROJECT_ROOT.rglob("*.py"):
        if any(part.startswith(".") or part == "__pycache__" or part == "venv" or part == "env" for part in py_file.parts):
            continue
        try:
            text = py_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for name, regex in patterns.items():
            for m in regex.finditer(text):
                line_no = text[:m.start()].count("\n") + 1
                findings[name].append({"file": str(py_file), "line": line_no, "match": m.group(0).strip()})
    return findings

def build_import_graph():
    imports = {}
    used_names = {}
    for py_file in PROJECT_ROOT.rglob("*.py"):
        if any(part.startswith(".") or part == "__pycache__" or part == "venv" or part == "env" for part in py_file.parts):
            continue
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except Exception:
            continue
        file_key = str(py_file)
        imports[file_key] = []
        used_names[file_key] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports[file_key].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ""
                for alias in node.names:
                    full = f"{module}.{alias.name}" if module else alias.name
                    imports[file_key].append(full)
            elif isinstance(node, ast.Name):
                used_names[file_key].add(node.id)
    # Detect imported modules never used
    unused = []
    for file, imp_list in imports.items():
        for imp in imp_list:
            base = imp.split(".")[0]
            if base not in used_names[file]:
                unused.append({"file": file, "import": imp})
    return unused

def check_config_usage():
    config_path = PROJECT_ROOT / "app" / "config.py"
    if not config_path.exists():
        return []
    text = config_path.read_text(encoding="utf-8")
    hardcoded = []
    # simple heuristic: assignments with literal strings not using os.getenv
    for line_no, line in enumerate(text.splitlines(), start=1):
        if "=" in line and not "os.getenv" in line:
            if re.search(r"['\"]", line):
                hardcoded.append({"line": line_no, "code": line.strip()})
    return hardcoded

def main():
    report_lines = ["# Codebase Analysis Report\n"]
    # Hardcoded patterns
    patterns = find_hardcoded_patterns()
    for cat, items in patterns.items():
        report_lines.append(f"## {cat.replace('_', ' ').title()}\n")
        if not items:
            report_lines.append("- None found\n")
        else:
            for it in items:
                report_lines.append(f"- `{it['file']}`: line {it['line']}: `{it['match']}`\n")
    # Unused imports
    unused = build_import_graph()
    report_lines.append("## Unused Imports\n")
    if not unused:
        report_lines.append("- None found\n")
    else:
        for u in unused:
            report_lines.append(f"- `{u['file']}` imports `{u['import']}` but never uses it\n")
    # Config hardcoded
    cfg = check_config_usage()
    report_lines.append("## Config Hardcoded Values\n")
    if not cfg:
        report_lines.append("- None found\n")
    else:
        for c in cfg:
            report_lines.append(f"- config.py line {c['line']}: `{c['code']}`\n")
    write_report("\n".join(report_lines))
    print(f"Report written to {REPORT_PATH}")

if __name__ == "__main__":
    main()
