"""Build the public repository handbook using only the Python standard library."""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs"
DATA = ROOT / "data" / "repositories"


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def listing(items: list, *, code: bool = False) -> str:
    if not items:
        return '<p class="muted">不适用；请参见仓库原始说明。</p>'
    if code:
        return "<pre><code>" + escape("\n".join(str(i) for i in items)) + "</code></pre>"
    return "<ul>" + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul>"


def page(title: str, body: str, prefix: str = "") -> str:
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="xiaoshecode 公开仓库的使用、结构、维护与验证记录。">
<title>{escape(title)} · 开源仓库手册</title>
<link rel="stylesheet" href="{prefix}assets/style.css"></head>
<body><a class="skip" href="#content">跳到正文</a>
<header><div class="wrap"><a class="brand" href="{prefix}index.html">xiaoshecode <span>/ 开源仓库手册</span></a><a href="https://github.com/xiaoshecode">GitHub ↗</a></div></header>
<main id="content" class="wrap">{body}</main>
<footer class="wrap">检查快照：2026-10-30 · 文档由版本控制中的结构化记录生成。通过某项检查不等于项目不存在其他错误。<br><a href="https://github.com/xiaoshecode/xiaoshecode/tree/codex/repository-maintenance-20261030/data/repositories">查看记录与修订历史</a></footer>
</body></html>'''


def build() -> None:
    records = [json.loads(p.read_text(encoding="utf-8-sig")) for p in sorted(DATA.glob("*.json"))]
    if not records:
        raise SystemExit("No repository records found")
    names = [r["name"] for r in records]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate repository record")
    (OUTPUT / "assets").mkdir(parents=True, exist_ok=True)
    for record in records:
        name = record["name"]
        if Path(name).name != name or name in {".", ".."}:
            raise ValueError(f"Invalid repository name: {name}")
        source = "https://github.com/xiaoshecode/" + quote(name, safe="")
        upstream = record.get("upstream")
        checks = "".join(
            f'<tr><td>{escape(c["name"])}</td><td>{escape(c["status"])}</td><td>{escape(c["detail"])}</td></tr>'
            for c in record.get("checks", [])
        )
        review = record.get("review_url")
        current_source = source + "/tree/codex/repository-maintenance-20261030" if review else source
        body = f'''<p class="eyebrow">{'FORK / 上游项目' if upstream else 'ORIGINAL / 原创仓库'}</p>
<h1>{escape(name)}</h1><p class="lead">{escape(record.get('purpose') or record.get('summary', ''))}</p>
<div class="links"><a href="{current_source}">本轮源码与 README ↗</a><a href="{source}/commits">默认分支提交 ↗</a><a href="../../index.html">全部仓库</a></div>'''
        if review:
            if not str(review).startswith("https://github.com/xiaoshecode/"):
                raise ValueError(f"Unexpected review URL: {review}")
            body += f'<p class="notice">本页记录维护分支的改动和验证结果。默认分支是否已更新，请查看 <a href="{escape(review)}">Pull Request 的合并状态 ↗</a>。</p>'
        if upstream:
            if not str(upstream).startswith("https://github.com/"):
                raise ValueError(f"Unexpected upstream URL: {upstream}")
            body += f'<p class="notice">这是 Fork 仓库。保留上游目录、许可与贡献说明；安装和兼容性以上游对应版本为准。<a href="{escape(upstream)}">查看上游 ↗</a></p>'
        body += f'''<nav class="toc" aria-label="本页目录"><a href="#setup">准备环境</a><a href="#usage">使用入口</a><a href="#structure">目录结构</a><a href="#checks">检查结果</a></nav>
<section id="setup"><h2>准备环境</h2>{listing(record.get('setup', []))}</section>
<section id="usage"><h2>使用入口</h2>{listing(record.get('usage', []))}</section>
<section id="structure"><h2>目录结构与职责</h2>{listing(record.get('structure', []))}</section>
<section><h2>本次整理</h2>{listing(record.get('changes', []))}</section>
<section id="checks"><h2>检查结果</h2><div class="table-wrap"><table><thead><tr><th>检查项</th><th>状态</th><th>证据 / 范围</th></tr></thead><tbody>{checks}</tbody></table></div></section>
<section><h2>已知限制与后续工作</h2>{listing(record.get('limitations', []))}</section>'''
        destination = OUTPUT / "repos" / name
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "index.html").write_text(page(name, body, "../../"), encoding="utf-8")

    originals = sum(not r.get("upstream") for r in records)
    cards = "".join(
        f'''<article class="card" data-kind="{'fork' if r.get('upstream') else 'original'}" data-search="{escape((r['name'] + ' ' + r.get('summary', '')).lower())}"><div class="card-meta">{'FORK' if r.get('upstream') else '原创'}</div><h2><a href="repos/{quote(r['name'], safe='')}/index.html">{escape(r['name'])}<span aria-hidden="true"> ↗</span></a></h2><p>{escape(r.get('summary') or r.get('purpose', ''))}</p><span class="card-bottom">使用说明 · 结构 · 检查记录</span></article>'''
        for r in records
    )
    body = f'''<p class="eyebrow">REPOSITORY HANDBOOK / 2026.10</p><h1>让每个项目<br>都有清晰的入口。</h1><p class="lead">查找仓库用途、环境准备、代码结构与检查记录。原创项目和上游 Fork 分别维护，已有项目网站保留原入口。</p>
<div class="links"><a href="reviews.html">查看全部修改与 Pull Request →</a></div>
<div class="stats"><div><strong>{len(records)}</strong><span>公开仓库</span></div><div><strong>{originals}</strong><span>原创项目</span></div><div><strong>{len(records)-originals}</strong><span>上游 Fork</span></div></div>
<div class="filters"><label for="search">查找仓库<input id="search" type="search" placeholder="名称或用途，例如 quantum" autocomplete="off"></label><label for="kind">项目类型<select id="kind"><option value="all">全部仓库</option><option value="original">原创项目</option><option value="fork">上游 Fork</option></select></label></div><p id="count" aria-live="polite">显示 {len(records)} 个仓库</p>
<div class="grid">{cards}</div><p class="notice">验证分为实际运行的测试、构建、静态检查和未执行项。GPU、FPGA、商业 SDK、实验设备与历史依赖的限制在各项目页面单独说明。</p>
<script src="assets/search.js" defer></script>'''
    (OUTPUT / "index.html").write_text(page("项目索引", body), encoding="utf-8")
    rows = []
    for record in records:
        name = record["name"]
        review = record.get("review_url")
        destination = review or f"https://github.com/xiaoshecode/{quote(name, safe='')}/commits"
        label = "Pull Request" if review else "默认分支提交"
        rows.append(f'<tr><td><a href="repos/{quote(name, safe="")}/index.html">{escape(name)}</a></td><td>{escape(record["summary"])}</td><td><a href="{escape(destination)}">{label} ↗</a></td></tr>')
    review_body = '<p class="eyebrow">CHANGE REVIEW</p><h1>逐仓库修改入口</h1><p class="lead">查看具体差异、验证结果与合并状态。29 个仓库通过维护分支和 Pull Request 提交；RTMQ 已更新默认分支。GitHub 页面显示实时合并状态。</p><p><a href="index.html">返回项目索引</a></p><div class="table-wrap"><table><thead><tr><th>仓库</th><th>整理内容</th><th>修改入口</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
    (OUTPUT / "reviews.html").write_text(page("修改与审阅", review_body), encoding="utf-8")
    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built {len(records)} repository pages and index in {OUTPUT}")


if __name__ == "__main__":
    build()
