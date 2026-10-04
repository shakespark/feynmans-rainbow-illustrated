#!/usr/bin/env python3
"""从维基共享资源（Wikimedia Commons）找图、取图。国内打不开维基，所以图片必须下载到 assets/img/，不能外链。

  搜索： source/.venv/bin/python tools/fetch_img.py search "Caltech Millikan Library"
  下载： source/.venv/bin/python tools/fetch_img.py get 07 wolfram "File:Stephen Wolfram PR.jpg" [--width 900]
         → 保存为 assets/img/07-wolfram.jpg，在 assets/img/CREDITS.md 追加一行，并打印可直接粘贴的出处文字。

只用 Public domain / CC0 / CC BY / CC BY-SA 的图；其他授权（Fair use、NC、ND、无授权信息）脚本会拒绝。
"""
import io, json, os, re, sys, time, urllib.parse, urllib.request
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
UA = {"User-Agent": "feynman-reading-guide/0.1 (personal study site; shakespark)"}
OK = re.compile(r"^(public domain|pd\b|cc0|cc by(-sa)? \d|no restrictions|attribution$)", re.I)

def api(**kw):
    kw.update(format="json", action="query")
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(kw)
    for i in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40))
        except Exception as e:
            time.sleep(8 * (i + 1) + (os.getpid() % 7)); err = e
    sys.exit(f"API 失败：{err}")

def meta(ii):
    m = ii.get("extmetadata", {})
    g = lambda k, n=160: re.sub(r"\s+", " ", re.sub("<[^>]+>", "", m.get(k, {}).get("value", ""))).strip()[:n]
    return dict(lic=g("LicenseShortName"), artist=g("Artist", 80), desc=g("ImageDescription", 220), date=g("DateTimeOriginal", 40))

if len(sys.argv) >= 3 and sys.argv[1] == "search":
    r = api(generator="search", gsrsearch=" ".join(sys.argv[2:]) + " filetype:bitmap|drawing", gsrnamespace=6, gsrlimit=12,
            prop="imageinfo", iiprop="extmetadata|size")
    for p in sorted(r.get("query", {}).get("pages", {}).values(), key=lambda x: x.get("index", 0)):
        ii = p["imageinfo"][0]; m = meta(ii)
        flag = "✓" if OK.match(m["lic"]) else "✗"
        print(f'{flag} {p["title"]} | {m["lic"]} | {m["artist"]} | {ii["width"]}x{ii["height"]} | {m["date"]}\n    {m["desc"]}')
elif len(sys.argv) >= 5 and sys.argv[1] == "get":
    from PIL import Image
    ch, name, title = sys.argv[2], sys.argv[3], sys.argv[4]
    width = int(sys.argv[sys.argv.index("--width") + 1]) if "--width" in sys.argv else 900
    if not re.fullmatch(r"\d\d", ch) or not re.fullmatch(r"[a-z0-9-]+", name): sys.exit("用法：get <两位章号> <小写英文名> <File:标题>")
    r = api(titles=title, prop="imageinfo", iiprop="extmetadata|url", iiurlwidth=max(width, 1000))
    p = next(iter(r["query"]["pages"].values()))
    if "imageinfo" not in p: sys.exit(f"找不到 {title}")
    ii = p["imageinfo"][0]; m = meta(ii)
    if not OK.match(m["lic"]): sys.exit(f"授权不可用：{m['lic']!r}（只用公有领域 / CC0 / CC BY / CC BY-SA）")
    for i in range(5):
        try:
            data = urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=90).read(); break
        except Exception as e:
            time.sleep(10 * (i + 1) + (os.getpid() % 7)); data = None; err = e
    if not data: sys.exit(f"下载失败：{err}")
    im = Image.open(io.BytesIO(data)).convert("RGB"); im.thumbnail((width, width))
    out = f"assets/img/{ch}-{name}.jpg"
    im.save(os.path.join(ROOT, out), quality=82, optimize=True)
    page = "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(p["title"].replace(" ", "_"))
    with open(os.path.join(ROOT, "assets/img/CREDITS.md"), "a", encoding="utf-8") as f:
        f.write(f"- `{ch}-{name}.jpg` — {p['title']} — {m['artist'] or '作者不详'} — {m['lic']} — {page}\n")
    lic = "公有领域" if re.match(r"public domain|pd|cc0|no restr", m["lic"], re.I) else m["lic"]
    print(f"已保存 {out} {im.size}\n说明：{m['desc']}\n日期：{m['date']}\n出处（粘贴到 figcaption 的 .src 里）：{m['artist'] or '作者不详'}，{lic}，维基共享资源")
else:
    sys.exit(__doc__)
