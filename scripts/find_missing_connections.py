import os, ast
from pathlib import Path

PROJECT_ROOT = Path(r"C:/Users/SHORAJ TOMER/SmartEducation")
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

def build_import_graph():
    """Build a mapping of each Python file to the set of modules it imports."""
    imports = {}
    for py_file in PROJECT_ROOT.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except Exception:
            continue
        imports[str(py_file)] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports[str(py_file)].add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ""
                for alias in node.names:
                    full = f"{module}.{alias.name}" if module else alias.name
                    imports[str(py_file)].add(full)
    return imports

def find_missing_connections():
    imports = build_import_graph()
    reverse = {}
    for src, deps in imports.items():
        for dep in deps:
            possible = list(PROJECT_ROOT.rglob(f"{dep.split('.')[-1]}.py"))
            for p in possible:
                reverse.setdefault(str(p), set()).add(src)
    missing = []
    for script_file in SCRIPTS_DIR.rglob("*.py"):
        if not reverse.get(str(script_file)):
            missing.append(str(script_file))
    return missing

if __name__ == "__main__":
    try:
        missing = find_missing_connections()
        report_path = PROJECT_ROOT / "missing_connections_report.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Missing Connections Report\n\n")
            if missing:
                f.write("The following script files are not imported by any other module (potential dead code or missing entry points):\n\n")
                for m in missing:
                    f.write(f"- `{m}`\n")
            else:
                f.write("All script files are referenced somewhere in the codebase.\n")
        print(f"Report written to {report_path}")
        print(f"Missing scripts count: {len(missing)}")
    except Exception as e:
        print("Error during analysis:", e)
        raise
