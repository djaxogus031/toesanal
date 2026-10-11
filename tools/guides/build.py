# -*- coding: utf-8 -*-
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from articles import ARTICLES, CALC

ROOT = sys.argv[1]  # repo/public
about = open(os.path.join(ROOT, "about.html"), encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", about, re.S).group(1)
fonts = re.search(r'<link rel="stylesheet"[^>]+>', about).group(0)
ads = ('<meta name="google-adsense-account" content="ca-pub-9077925235959210">\n'
       '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9077925235959210" crossorigin="anonymous"></script>')
DATE = "2026-10-11"
EXTRA = """
.crumb{font-size:12px;color:var(--ink-3);margin-bottom:10px}.crumb a{color:var(--ink-3)}
.doc h3{font-size:17px;margin:20px 0 6px}
.doc .meta{font-size:12px;color:var(--ink-3);margin:-6px 0 22px}
.doc .lede{font-size:16px;color:var(--ink)}
.formula{font-family:var(--f-mono);font-size:14px;background:var(--sheet);border:1px solid var(--rule);border-left:4px solid var(--seal);border-radius:var(--r);padding:14px 16px;margin:12px 0;overflow-x:auto}
table.t{min-width:0;margin:12px 0;background:var(--sheet)}
table.t td{font-family:var(--f-body)}
.cta{margin:32px 0 8px}.cta a{display:inline-block;background:var(--ink);color:var(--paper);text-decoration:none;font-weight:600;padding:12px 20px;border-radius:999px}
.rel{border-top:1px solid var(--rule);margin-top:32px;padding-top:16px}.rel ul{padding-left:18px}
.glist{display:grid;gap:12px;padding:0;list-style:none}
.glist a{display:grid;gap:4px;text-decoration:none;background:var(--sheet);border:1px solid var(--rule);border-radius:var(--r);padding:16px 18px}
.glist a:hover,.glist a:focus-visible{border-color:var(--ink)}
.glist small{font:600 11px var(--f-body);letter-spacing:.1em;color:var(--seal)}
.glist strong{font-family:var(--f-display);font-size:18px;line-height:1.4;color:var(--ink)}
.glist span{font-size:13px;color:var(--ink-2)}
.disc{font-size:12px;color:var(--ink-3);margin-top:28px}
"""
NAV = ('<header class="top"><div class="wrap"><a class="brand" href="/"><span class="sealmark" aria-hidden="true">날</span>퇴사날</a>'
       '<nav aria-label="사이트"><a href="/">계산기</a><a href="/guide/">가이드</a><a href="/about.html">소개</a><a href="/privacy.html">개인정보처리방침</a></nav></div></header>')
FOOT = ('<footer><div class="wrap"><div><b style="color:var(--ink)">퇴사날</b> · 퇴사일 정산 시뮬레이터</div>'
        '<div><a href="/guide/">가이드</a> · <a href="/about.html">소개</a> · <a href="/privacy.html">개인정보처리방침</a> · 문의 <a href="mailto:godaniday@gmail.com">godaniday@gmail.com</a></div></div></footer>')
DISC = '<p class="disc">이 글은 2026년 10월 기준 법령과 고시 금액을 바탕으로 작성한 일반 정보입니다. 개별 사안은 고용노동부 고객상담센터(1350)나 노무사와 확인하세요.</p>'

def page(title, desc, canon, body, ld=None):
    ldj = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{canon}"><meta property="og:type" content="article"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{canon}"><meta property="og:locale" content="ko_KR">
{fonts}
<style>{css}{EXTRA}</style>
{ads}
{ldj}
</head><body>
{NAV}
<main class="wrap doc">{body}</main>
{FOOT}
</body></html>
"""

os.makedirs(os.path.join(ROOT, "guide"), exist_ok=True)
by_cat = {}
for a in ARTICLES:
    by_cat.setdefault(a["cat"], []).append(a)
for a in ARTICLES:
    url = f"https://toesanal.com/guide/{a['slug']}.html"
    rel = [x for x in by_cat[a["cat"]] if x is not a][:3]
    if len(rel) < 3:
        rel += [x for x in ARTICLES if x is not a and x not in rel][: 3 - len(rel)]
    rel_html = '<div class="rel"><h2>함께 보면 좋은 글</h2><ul>' + "".join(
        f'<li><a href="/guide/{r["slug"]}.html">{r["title"]}</a></li>' for r in rel) + "</ul></div>"
    body = (f'<div class="crumb"><a href="/">퇴사날</a> › <a href="/guide/">가이드</a> › {a["cat"]}</div>'
            f'<h1>{a["title"]}</h1><p class="meta">{a["cat"]} · {DATE} 기준</p>'
            f'<p class="lede">{a["desc"]}</p>{a["body"]}{CALC}{rel_html}{DISC}')
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
          "datePublished": DATE, "dateModified": DATE, "inLanguage": "ko-KR", "mainEntityOfPage": url,
          "author": {"@type": "Organization", "name": "퇴사날"}, "publisher": {"@type": "Organization", "name": "퇴사날"}}
    open(os.path.join(ROOT, "guide", a["slug"] + ".html"), "w", encoding="utf-8").write(
        page(f'{a["title"]} | 퇴사날', a["desc"], url, body, ld))

# 목록 페이지
order = ["퇴직금", "연차", "실업급여", "퇴사 후", "퇴사 준비"]
lst = ""
for c in order:
    lst += f"<h2>{c}</h2><ul class=\"glist\">" + "".join(
        f'<li><a href="/guide/{a["slug"]}.html"><small>{c}</small><strong>{a["title"]}</strong><span>{a["desc"]}</span></a></li>'
        for a in by_cat[c]) + "</ul>"
idx = ('<div class="crumb"><a href="/">퇴사날</a> › 가이드</div><h1>퇴사 가이드</h1>'
       '<p class="lede">퇴직금, 연차수당, 실업급여, 퇴사 후 4대보험까지. 퇴사 전에 알아야 할 돈 이야기를 법 조문과 실제 계산 예시로 정리했습니다.</p>'
       + lst + CALC + DISC)
open(os.path.join(ROOT, "guide", "index.html"), "w", encoding="utf-8").write(
    page("퇴사 가이드: 퇴직금·연차수당·실업급여 총정리 | 퇴사날",
         "퇴직금 계산법, 연차수당, 실업급여 조건과 금액, 퇴사 후 건강보험·국민연금·연말정산까지 퇴사 전에 알아야 할 정보를 정리했습니다.",
         "https://toesanal.com/guide/", idx))

# sitemap
urls = ["https://toesanal.com/", "https://toesanal.com/guide/"] + \
       [f"https://toesanal.com/guide/{a['slug']}.html" for a in ARTICLES] + \
       ["https://toesanal.com/about.html", "https://toesanal.com/privacy.html"]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
     "".join(f"  <url><loc>{u}</loc><lastmod>{DATE}</lastmod></url>\n" for u in urls) + "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
print(len(ARTICLES), "articles")
for a in ARTICLES:
    txt = re.sub(r"<[^>]+>", "", a["body"])
    print(a["slug"], len(re.sub(r"\s", "", txt)))
