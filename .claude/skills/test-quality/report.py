# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "mutmut>=2.4,<3",
#   "radon>=6.0",
#   "coverage>=7.0",
# ]
# ///
"""
Test Quality Report — mutation testing + CRAP score 통합 리포트 생성기.

Usage:
    uv run report.py [--src SRC] [--tests TESTS] [--output OUTPUT] [--changed-only]

Defaults:
    --src    src/
    --output quality-report.md
"""

import argparse
import datetime
import json
import sqlite3
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--src", default="src/", help="소스 디렉토리")
    p.add_argument("--tests", default="tests/", help="테스트 디렉토리")
    p.add_argument("--output", default="quality-report.md", help="출력 파일 경로")
    p.add_argument("--crap-threshold", type=float, default=5.0, help="CRAP 위험 기준 (기본: 5)")
    p.add_argument("--changed-only", action="store_true", help="git diff 기반으로 변경된 파일만 대상으로 실행")
    p.add_argument("--base-branch", default="main", help="--changed-only 기준 브랜치 (기본: main)")
    return p.parse_args()


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True)


def get_complexity(src: str) -> dict:
    result = run(["python", "-m", "radon", "cc", src, "-j"])
    if result.returncode != 0:
        print(f"radon 실행 실패: {result.stderr}", file=sys.stderr)
        return {}
    return json.loads(result.stdout)


def get_coverage() -> dict:
    cov_path = Path("coverage.json")
    if not cov_path.exists():
        result = run(["python", "-m", "pytest", "--cov", "--cov-report=json", "-q"])
        if result.returncode != 0:
            print("pytest --cov 실행 실패. coverage.json이 없습니다.", file=sys.stderr)
            return {}
    with open(cov_path) as f:
        return json.load(f)


def func_coverage(fname: str, lineno: int, endline: int, cov_data: dict) -> float:
    if fname not in cov_data.get("files", {}):
        return 0.0
    executed = set(cov_data["files"][fname]["executed_lines"])
    lines = list(range(lineno, endline + 1))
    if not lines:
        return 100.0
    return sum(1 for l in lines if l in executed) / len(lines) * 100


def crap_score(cc: int, cov_pct: float) -> float:
    cov = cov_pct / 100
    return cc**2 * (1 - cov) ** 3 + cc


def get_changed_files(src: str, base_branch: str) -> list[str]:
    """base_branch 대비 변경된 src 내 Python 파일 목록 반환."""
    result = run(["git", "diff", f"{base_branch}...HEAD", "--name-only"])
    if result.returncode != 0:
        return []
    src_prefix = src.rstrip("/")
    return [
        f for f in result.stdout.splitlines()
        if f.startswith(src_prefix) and f.endswith(".py")
    ]


def run_mutmut(src: str, tests: str, changed_only: bool, base_branch: str) -> bool:
    paths = src
    if changed_only:
        changed = get_changed_files(src, base_branch)
        if not changed:
            print("변경된 파일 없음 — mutmut 스킵", file=sys.stderr)
            return True
        paths = ",".join(changed)
        print(f"변경된 파일만 대상: {paths}", file=sys.stderr)
    else:
        print("mutmut 실행 중... (시간이 걸릴 수 있습니다)", file=sys.stderr)

    result = run([
        "python", "-m", "mutmut", "run",
        "--paths-to-mutate", paths,
        "--tests-dir", tests,
    ])
    # exit code 1 = survived mutants 있음 (정상), 2+ = 실제 에러
    return result.returncode <= 1


def get_survived_mutants() -> tuple[list[tuple], int, int]:
    cache = Path(".mutmut-cache")
    if not cache.exists():
        return [], 0, 0
    conn = sqlite3.connect(str(cache))
    survived = conn.execute("""
        SELECT m.id, sf.filename, l.line_number
        FROM Mutant m
        JOIN Line l ON m.line = l.id
        JOIN SourceFile sf ON l.sourcefile = sf.id
        WHERE m.status = 'bad_survived'
        ORDER BY sf.filename, l.line_number
    """).fetchall()
    total  = conn.execute("SELECT COUNT(*) FROM Mutant").fetchone()[0]
    killed = conn.execute("SELECT COUNT(*) FROM Mutant WHERE status='ok_killed'").fetchone()[0]
    conn.close()
    return survived, total, killed


def get_mutant_diff(mutant_id: int) -> list[str]:
    result = run(["python", "-m", "mutmut", "show", str(mutant_id)])
    return [
        l for l in result.stdout.splitlines()
        if (l.startswith("+") or l.startswith("-"))
        and not l.startswith("---") and not l.startswith("+++")
    ]


def build_func_list(cc_data: dict, cov_data: dict, survived_rows: list, threshold: float) -> list[dict]:
    survived_by_func: dict[tuple, list] = {}
    for mid, fname, lineno in survived_rows:
        for fn in cc_data.get(fname, []):
            if fn["lineno"] <= lineno <= fn["endline"]:
                key = (fname, fn["name"])
                survived_by_func.setdefault(key, []).append((mid, lineno))

    funcs = []
    for fname, fns in cc_data.items():
        for fn in fns:
            cc  = fn["complexity"]
            cov = func_coverage(fname, fn["lineno"], fn["endline"], cov_data)
            c   = crap_score(cc, cov)
            key = (fname, fn["name"])
            funcs.append({
                "fname": fname,
                "name": fn["name"],
                "lineno": fn["lineno"],
                "endline": fn["endline"],
                "cc": cc,
                "cov": cov,
                "crap": c,
                "survived": survived_by_func.get(key, []),
                "violation": c > threshold,
            })

    funcs.sort(key=lambda x: (-x["crap"], -len(x["survived"])))
    return funcs


def render_report(funcs: list[dict], total: int, killed: int, threshold: float, changed_only: bool = False, base_branch: str = "main") -> str:
    total_survived = sum(len(f["survived"]) for f in funcs)
    violations = [f for f in funcs if f["violation"]]
    mutation_score = killed / total * 100 if total else 0.0

    lines: list[str] = []

    scope = f"변경 파일만 (`{base_branch}...HEAD`)" if changed_only else "전체 소스"
    lines += [
        "# Test Quality Report",
        "",
        f"_생성: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} | 범위: {scope}_",
        "",
        "## 요약",
        "",
        "| 항목 | 값 |",
        "|------|----|",
        f"| Mutation Score | {mutation_score:.1f}% ({killed}/{total} killed) |",
        f"| Survived Mutants | {total_survived}개 |",
        f"| CRAP 위반 함수 | {len(violations)}개 (기준: > {threshold}) |",
        "",
        "## 함수별 분석",
        "",
        "| 함수 | 파일 | CC | Coverage | CRAP | 위험도 | Survived |",
        "|------|------|----|----------|------|--------|----------|",
    ]

    for f in funcs:
        flag = "🔥 위험" if f["violation"] else "✅ 양호"
        lines.append(
            f"| `{f['name']}` | `{f['fname']}:{f['lineno']}` "
            f"| {f['cc']} | {f['cov']:.1f}% | **{f['crap']:.1f}** "
            f"| {flag} | {len(f['survived'])}개 |"
        )

    lines += ["", "## Survived Mutants 상세", "", "> 테스트가 잡지 못한 변이들.", ""]

    for f in funcs:
        if not f["survived"]:
            continue
        lines.append(f"### `{f['name']}` (`{f['fname']}:{f['lineno']}–{f['endline']}`)")
        lines.append("")
        for mid, lineno in f["survived"]:
            diff = get_mutant_diff(mid)
            lines.append(f"**Mutant #{mid}** (line {lineno})")
            lines.append("```diff")
            lines.extend(diff[:2])
            lines.append("```")
            lines.append("")

    lines += ["## 액션 플랜", "", f"우선순위 순서 (CRAP > {threshold} 또는 survived > 0):", ""]

    i = 1
    for f in funcs:
        if not f["violation"] and not f["survived"]:
            continue
        actions = []
        if f["survived"]:
            actions.append(f"survived mutant {len(f['survived'])}개 → 경계값 테스트 추가")
        if f["violation"]:
            actions.append(f"CRAP {f['crap']:.1f} → 함수 분리 또는 테스트 보강")
        lines.append(f"{i}. **`{f['name']}`** — {', '.join(actions)}")
        i += 1

    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()

    cc_data  = get_complexity(args.src)
    cov_data = get_coverage()

    if not run_mutmut(args.src, args.tests, args.changed_only, args.base_branch):
        print("mutmut 실행 실패. report를 생성하지 않습니다.", file=sys.stderr)
        sys.exit(1)

    survived, total, killed = get_survived_mutants()
    funcs = build_func_list(cc_data, cov_data, survived, args.crap_threshold)
    report = render_report(funcs, total, killed, args.crap_threshold, args.changed_only, args.base_branch)

    Path(args.output).write_text(report)
    print(f"리포트 생성 완료: {args.output}", file=sys.stderr)
    print(report)


if __name__ == "__main__":
    main()
