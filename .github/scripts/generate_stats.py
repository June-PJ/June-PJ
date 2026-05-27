#!/usr/bin/env python3
"""
直接调 GitHub GraphQL API 生成 stats / top-langs SVG，不依赖 vercel。

输入：环境变量 GITHUB_TOKEN（仓库默认 token 即可），USERNAME（GitHub 用户名）
输出：dist/ 下 4 个 SVG（stats / top-langs，浅深各一份）

设计要点：
- 不用 <style> 标签：GitHub camo 代理会剥掉某些 CSS，font-family 直接写在 <text> 属性上
- 坐标全部绝对定位，不嵌 <g transform>，避免坐标双层叠加溢出
- 配色对齐 junePortal：浅色 #E68282 珊瑚红，深色 #F2B94B 琥珀黄
"""

import json
import os
import urllib.request

USERNAME = os.environ.get("USERNAME", "June-PJ")
TOKEN = os.environ["GITHUB_TOKEN"]

FONT_STACK = "-apple-system,Segoe UI,Microsoft YaHei,Ubuntu,sans-serif"

QUERY = """
query($login: String!) {
  user(login: $login) {
    name
    login
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
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
        ("Total Stars Earned",      total_stars,                              "★"),
        ("Total Commits (last yr)", contrib["totalCommitContributions"],      "↗"),
        ("Total PRs",               contrib["totalPullRequestContributions"], "⤴"),
        ("Total Issues",            contrib["totalIssueContributions"],       "○"),
        ("Followers",               user["followers"]["totalCount"],          "♥"),
        ("Public Repos",            user["repositories"]["totalCount"],       "▣"),
    ]

    # 聚合各仓库语言字节数
    lang_size, lang_color = {}, {}
    for r in repos:
        for edge in r["languages"]["edges"]:
            n = edge["node"]["name"]
            lang_size[n] = lang_size.get(n, 0) + edge["size"]
            lang_color[n] = edge["node"]["color"] or "#94A3B8"

    total = sum(lang_size.values())
    langs = sorted(lang_size.items(), key=lambda x: -x[1])[:6]

    display_name = user.get("name") or USERNAME

    files = {
        "dist/stats.svg":          render_stats("light", display_name, stats_rows),
        "dist/stats-dark.svg":     render_stats("dark",  display_name, stats_rows),
        "dist/top-langs.svg":      render_langs("light", langs, lang_color, total),
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
    if langs:
        print(f"Top langs: {[(n, f'{s/total*100:.1f}%') for n, s in langs]}")
    else:
        print("Top langs: (none — no owned non-fork repos yet)")


def theme_colors(theme):
    if theme == "light":
        return {"accent": "#E68282", "text": "#475569", "muted": "#94A3B8"}
    return {"accent": "#F2B94B", "text": "#C4C4D0", "muted": "#94A3B8"}


def render_stats(theme, display_name, rows):
    c = theme_colors(theme)
    W, H = 420, 220
    parts = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" fill="none">',
        f'  <text x="20" y="32" font-family="{FONT_STACK}" font-size="16" font-weight="700" fill="{c["accent"]}">{escape(display_name)}\'s GitHub Stats</text>',
        f'  <line x1="20" y1="44" x2="{W-20}" y2="44" stroke="{c["muted"]}" stroke-opacity="0.25"/>',
    ]
    y = 74
    for label, value, icon in rows:
        parts.append(
            f'  <text x="22" y="{y}" font-family="{FONT_STACK}" font-size="14" fill="{c["accent"]}">{icon}</text>'
        )
        parts.append(
            f'  <text x="44" y="{y}" font-family="{FONT_STACK}" font-size="13" fill="{c["text"]}">{label}</text>'
        )
        parts.append(
            f'  <text x="{W-22}" y="{y}" font-family="{FONT_STACK}" font-size="13" font-weight="700" fill="{c["accent"]}" text-anchor="end">{value}</text>'
        )
        y += 22
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def render_langs(theme, langs, lang_color, total):
    c = theme_colors(theme)
    W, H = 380, 200

    parts = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" fill="none">',
        f'  <text x="20" y="32" font-family="{FONT_STACK}" font-size="16" font-weight="700" fill="{c["accent"]}">Most Used Languages</text>',
        f'  <line x1="20" y1="44" x2="{W-20}" y2="44" stroke="{c["muted"]}" stroke-opacity="0.25"/>',
    ]

    if not langs or total == 0:
        parts.append(
            f'  <text x="20" y="100" font-family="{FONT_STACK}" font-size="13" fill="{c["text"]}" fill-opacity="0.7">'
            f'No owned non-fork repos with code yet.</text>'
        )
        parts.append("</svg>")
        return "\n".join(parts) + "\n"

    # 进度条
    bar_x, bar_y, bar_w, bar_h = 22, 64, W - 44, 8
    parts.append(
        f'  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="{bar_h/2}" fill="{c["muted"]}" fill-opacity="0.2"/>'
    )
    accum = 0.0
    for name, size in langs:
        w = size / total * bar_w
        color = lang_color.get(name, c["accent"])
        parts.append(
            f'  <rect x="{bar_x + accum:.2f}" y="{bar_y}" width="{w:.2f}" height="{bar_h}" fill="{color}"/>'
        )
        accum += w

    # 两列图例
    col_w = (W - 44) // 2
    for i, (name, size) in enumerate(langs):
        pct = size / total * 100
        color = lang_color.get(name, c["accent"])
        col, row = i % 2, i // 2
        x_pos = 22 + col * col_w
        y_pos = 100 + row * 26
        parts.append(
            f'  <circle cx="{x_pos+5}" cy="{y_pos-3}" r="5" fill="{color}"/>'
        )
        parts.append(
            f'  <text x="{x_pos+18}" y="{y_pos}" font-family="{FONT_STACK}" font-size="12" fill="{c["text"]}">'
            f'{escape(name)} <tspan font-weight="700" fill="{c["accent"]}">{pct:.1f}%</tspan></text>'
        )

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def escape(s):
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


if __name__ == "__main__":
    main()
