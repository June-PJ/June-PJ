#!/usr/bin/env python3
"""
直接调 GitHub GraphQL API 生成 stats / top-langs SVG，不依赖 vercel。

输入：环境变量 GITHUB_TOKEN（仓库默认 token 即可），USERNAME（GitHub 用户名）
输出：dist/ 下 4 个 SVG（stats / top-langs，浅深各一份）

配色对齐 junePortal：
- 浅色：强调 #E68282（珊瑚红），文字 #475569
- 深色：强调 #F2B94B（琥珀黄），文字 #C4C4D0
"""

import json
import os
import sys
import urllib.request

USERNAME = os.environ.get("USERNAME", "June-PJ")
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    name
    login
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges {
            size
            node { name color }
          }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
    }
  }
}
"""


def graphql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "june-pj-stats-generator",
        },
    )
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())
    if "errors" in body:
        raise RuntimeError(body["errors"])
    return body["data"]


def main():
    user = graphql(QUERY, {"login": USERNAME})["user"]
    repos = user["repositories"]["nodes"]
    total_stars = sum(r["stargazerCount"] for r in repos)
    contrib = user["contributionsCollection"]

    stats_rows = [
        ("Total Stars Earned",      total_stars,                                "★"),
        ("Total Commits (last yr)", contrib["totalCommitContributions"],        "❯"),
        ("Total PRs",               contrib["totalPullRequestContributions"],   "⤴"),
        ("Total Issues",            contrib["totalIssueContributions"],         "○"),
        ("Followers",               user["followers"]["totalCount"],            "♥"),
        ("Public Repos",            user["repositories"]["totalCount"],         "▣"),
    ]

    # 聚合各仓库语言字节数
    lang_size = {}
    lang_color = {}
    for r in repos:
        for edge in r["languages"]["edges"]:
            n = edge["node"]["name"]
            lang_size[n] = lang_size.get(n, 0) + edge["size"]
            lang_color[n] = edge["node"]["color"] or "#94A3B8"

    total = sum(lang_size.values()) or 1
    langs = sorted(lang_size.items(), key=lambda x: -x[1])[:6]

    display_name = user.get("name") or USERNAME

    files = {
        "dist/stats.svg":         render_stats("light", display_name, stats_rows),
        "dist/stats-dark.svg":    render_stats("dark",  display_name, stats_rows),
        "dist/top-langs.svg":     render_langs("light", langs, lang_color, total),
        "dist/top-langs-dark.svg": render_langs("dark",  langs, lang_color, total),
    }

    os.makedirs("dist", exist_ok=True)
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  wrote {path}  ({len(content)} bytes)")

    print()
    print(f"Stats: stars={total_stars}, "
          f"commits={contrib['totalCommitContributions']}, "
          f"prs={contrib['totalPullRequestContributions']}, "
          f"issues={contrib['totalIssueContributions']}, "
          f"followers={user['followers']['totalCount']}, "
          f"repos={user['repositories']['totalCount']}")
    print(f"Top langs: {[(n, f'{s/total*100:.1f}%') for n, s in langs]}")


def theme_colors(theme):
    if theme == "light":
        return {"accent": "#E68282", "text": "#475569", "muted": "#94A3B8"}
    return {"accent": "#F2B94B", "text": "#C4C4D0", "muted": "#94A3B8"}


def render_stats(theme, display_name, rows):
    c = theme_colors(theme)
    body = []
    y = 72
    for label, value, icon in rows:
        body.append(
            f'  <g transform="translate(28, {y})">'
            f'<text font-size="15" fill="{c["accent"]}" dominant-baseline="middle">{icon}</text>'
            f'<text x="26" font-size="13.5" fill="{c["text"]}" dominant-baseline="middle">{label}</text>'
            f'<text x="362" font-size="13.5" font-weight="600" fill="{c["accent"]}" text-anchor="end" dominant-baseline="middle">{value}</text>'
            f'</g>'
        )
        y += 24
    rows_svg = "\n".join(body)
    return f'''<svg width="380" height="220" viewBox="0 0 380 220" xmlns="http://www.w3.org/2000/svg" fill="none">
  <style>text {{ font-family: -apple-system, "Segoe UI", "Microsoft YaHei", Ubuntu, sans-serif; letter-spacing: 0.2px; }}</style>
  <text x="20" y="34" font-size="17" font-weight="700" fill="{c["accent"]}">{escape(display_name)}'s GitHub Stats</text>
  <line x1="20" y1="46" x2="360" y2="46" stroke="{c["muted"]}" stroke-opacity="0.25"/>
{rows_svg}
</svg>
'''


def render_langs(theme, langs, lang_color, total):
    c = theme_colors(theme)

    # 进度条
    bar_x, bar_y, bar_w, bar_h = 22, 60, 296, 8
    bar_segments = [
        f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="{bar_h/2}" fill="{c["muted"]}" fill-opacity="0.2"/>'
    ]
    accum = 0
    for name, size in langs:
        w = size / total * bar_w
        color = lang_color.get(name, c["accent"])
        # 头尾稍作圆角处理：用 mask 容易出错，简化为带 rx 的 rect 重叠
        bar_segments.append(
            f'<rect x="{bar_x + accum}" y="{bar_y}" width="{w:.2f}" height="{bar_h}" fill="{color}"/>'
        )
        accum += w

    # 两列图例
    legend = []
    for i, (name, size) in enumerate(langs):
        pct = size / total * 100
        color = lang_color.get(name, c["accent"])
        col, row = i % 2, i // 2
        x_pos = 22 + col * 150
        y_pos = 95 + row * 24
        legend.append(
            f'<circle cx="{x_pos+5}" cy="{y_pos}" r="5" fill="{color}"/>'
            f'<text x="{x_pos+18}" y="{y_pos+4}" font-size="12" fill="{c["text"]}">'
            f'{escape(name)} <tspan font-weight="600">{pct:.1f}%</tspan></text>'
        )

    return f'''<svg width="340" height="180" viewBox="0 0 340 180" xmlns="http://www.w3.org/2000/svg" fill="none">
  <style>text {{ font-family: -apple-system, "Segoe UI", "Microsoft YaHei", Ubuntu, sans-serif; letter-spacing: 0.2px; }}</style>
  <text x="20" y="34" font-size="16" font-weight="700" fill="{c["accent"]}">Most Used Languages</text>
  <line x1="20" y1="46" x2="320" y2="46" stroke="{c["muted"]}" stroke-opacity="0.25"/>
  {"".join(bar_segments)}
  {"".join(legend)}
</svg>
'''


def escape(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


if __name__ == "__main__":
    main()
