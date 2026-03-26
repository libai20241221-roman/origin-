#!/usr/bin/env python3
"""修复 GitHub Desktop 在 Windows 下出现的“can't find 7-Zip ...”配置错误。

该错误通常由 Git 配置中的 editor/difftool/mergetool 指向了无效路径导致。
本脚本会扫描 local/global/system 配置中包含 `7-Zip` 的条目，并尝试清理。
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from typing import Iterable

SCOPES = ("--local", "--global", "--system")
PATTERN = "7-Zip"


@dataclass
class ConfigEntry:
    scope: str
    key: str
    value: str


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def list_entries(scope: str) -> list[ConfigEntry]:
    proc = run_git(["config", scope, "--list"])
    if proc.returncode != 0:
        return []

    out: list[ConfigEntry] = []
    for line in proc.stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if PATTERN.lower() in value.lower():
            out.append(ConfigEntry(scope=scope, key=key.strip(), value=value.strip()))
    return out


def unset_key(scope: str, key: str) -> bool:
    proc = run_git(["config", scope, "--unset-all", key])
    return proc.returncode == 0


def summarize(entries: Iterable[ConfigEntry]) -> str:
    lines = ["检测到以下疑似异常配置："]
    for entry in entries:
        lines.append(f"- {entry.scope} {entry.key} = {entry.value}")
    return "\n".join(lines)


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    found: list[ConfigEntry] = []

    for scope in SCOPES:
        found.extend(list_entries(scope))

    if not found:
        print("未发现包含 '7-Zip' 的 Git 配置项。")
        return 0

    print(summarize(found))

    if dry_run:
        print("\n当前为 --dry-run，仅显示，不做修改。")
        return 0

    failed: list[ConfigEntry] = []
    for entry in found:
        if unset_key(entry.scope, entry.key):
            print(f"已清理: {entry.scope} {entry.key}")
        else:
            failed.append(entry)
            print(f"清理失败: {entry.scope} {entry.key}")

    if failed:
        print("\n仍有未清理项，请使用管理员权限重试（尤其是 --system）。")
        return 1

    print("\n清理完成。请重启 GitHub Desktop 再试。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
