"""Build a tailored resume .docx from Brandon's base resume, preserving all formatting.

Usage: python3 tailor.py spec.json out.docx

spec.json keys (all optional):
  headline:      str  -> paragraph 1
  summary:       str  -> paragraph 4
  skills:        list of [label, items] in desired order (replaces paragraphs 6-12;
                 must be 1..7 entries; labels like "Security")
  communicai_bullets: list of str (replaces/reorders paragraphs 15-18; 1..4 entries)
  tracking_bullets:   list of str (paragraphs 20-21; 1..2 entries)
  coursework:    str  -> paragraph 33 full text
  section_order: ["PROJECTS","EXPERIENCE","EDUCATION"] order after skills (default as base)

RULE: every claim must come from ExperienceLibrary.json. This script does not check truth.
"""
import json, re, sys, zipfile, shutil, os
from xml.sax.saxutils import escape

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base")


def para_text_set(p, texts):
    """Replace the text of each <w:t> in paragraph p with texts (same count)."""
    ts = re.findall(r'<w:t[^>]*>[^<]*</w:t>', p)
    assert len(ts) == len(texts), (len(ts), texts)
    out = p
    for old, new in zip(ts, texts):
        out = out.replace(old, '<w:t xml:space="preserve">%s</w:t>' % escape(new), 1)
    return out


def main(spec_path, out_path):
    spec = json.load(open(spec_path))
    xml = open(os.path.join(BASE, "word/document.xml"), encoding="utf-8").read()
    ps = re.findall(r'<w:p[ >].*?</w:p>', xml, re.S)
    assert len(ps) == 37, len(ps)
    new = list(ps)

    if "headline" in spec:
        new[1] = para_text_set(ps[1], [spec["headline"]])
    if "summary" in spec:
        new[4] = para_text_set(ps[4], [spec["summary"]])
    skill_block = ps[6:13]
    if "skills" in spec:
        sk = spec["skills"]
        assert 1 <= len(sk) <= 7
        skill_block = [para_text_set(ps[6], [lab.rstrip(": ") + ": ", items]) for lab, items in sk]
    proj_bul = ps[15:19]
    if "communicai_bullets" in spec:
        b = spec["communicai_bullets"]; assert 1 <= len(b) <= 4
        proj_bul = [para_text_set(ps[15], [t]) for t in b]
    track_bul = ps[20:22]
    if "tracking_bullets" in spec:
        b = spec["tracking_bullets"]; assert 1 <= len(b) <= 2
        track_bul = [para_text_set(ps[20], [t]) for t in b]
    if "coursework" in spec:
        new[33] = para_text_set(ps[33], [spec["coursework"]])

    sections = {
        "PROJECTS": [ps[13], ps[14]] + proj_bul + [ps[19]] + track_bul,
        "EXPERIENCE": new[22:30],
        "EDUCATION": new[30:35],
    }
    order = spec.get("section_order", ["PROJECTS", "EXPERIENCE", "EDUCATION"])
    body = new[0:6] + skill_block
    for s in order:
        body += sections[s]
    body += new[35:37]

    # splice: replace the span from first to last paragraph
    start = xml.index(ps[0]); end = xml.index(ps[-1]) + len(ps[-1])
    out_xml = xml[:start] + "".join(body) + xml[end:]

    tmp = out_path + ".d"
    if os.path.exists(tmp): shutil.rmtree(tmp)
    shutil.copytree(BASE, tmp)
    open(os.path.join(tmp, "word/document.xml"), "w", encoding="utf-8").write(out_xml)
    if os.path.exists(out_path): os.remove(out_path)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        # [Content_Types].xml first
        z.write(os.path.join(tmp, "[Content_Types].xml"), "[Content_Types].xml")
        for root, _, files in os.walk(tmp):
            for f in files:
                full = os.path.join(root, f); arc = os.path.relpath(full, tmp)
                if arc != "[Content_Types].xml":
                    z.write(full, arc)
    shutil.rmtree(tmp)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
