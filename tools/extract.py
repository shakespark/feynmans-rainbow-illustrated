#!/usr/bin/env python3
"""从本机的 epub 解压目录提取每章文本到 source/text/NN.txt（NN=00 序言，01–24 正文）。
每行一段，行首 [段号]；{F} 表示该段在纸质书里是斜体（费曼的原话，来自作者的笔记和录音）。"""
import html, os, re
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
s = open(os.path.join(ROOT, "source/epub/OEBPS/FeynmansRainbow-body.html"), encoding="utf-8", errors="replace").read()
ROM = "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI XXII XXIII XXIV".split()
parts = re.split(r'<h[12] class="(?:chp|part)"[^>]*>(.*?)</h[12]>', s, flags=re.S)
os.makedirs(os.path.join(ROOT, "source/text"), exist_ok=True)
for name, body in zip(parts[1::2], parts[2::2]):
    name = re.sub("<[^>]+>", "", name).strip()
    if name == "PREFACE": k = 0
    elif name in ROM: k = ROM.index(name) + 1
    else: continue
    out = []
    for cls, p in re.findall(r"<p\b([^>]*)>(.*?)</p>", body, flags=re.S):
        t = re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", "", p))).strip()
        if t: out.append(("{F} " if "sans-para" in cls else "") + t)
    open(os.path.join(ROOT, f"source/text/{k:02d}.txt"), "w", encoding="utf-8").write(
        "".join(f"[{i + 1}] {t}\n" for i, t in enumerate(out)))
    print(f"{k:02d} {len(out):3d} 段 {sum(len(x.split()) for x in out):5d} 词")
