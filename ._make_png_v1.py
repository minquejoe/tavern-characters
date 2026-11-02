import json, os, glob, base64, zlib, struct
BASE = r"E:\tavern characters"
OUT = os.path.join(BASE, "png_cards_v1")
os.makedirs(OUT, exist_ok=True)

def add_text_chunk(keyword, text_b64):
    keyword_b = keyword.encode("latin-1")
    data_b = text_b64.encode("latin-1")
    chunk_data = keyword_b + b"\x00" + data_b
    crc = zlib.crc32(b"tEXt" + chunk_data) & 0xffffffff
    return struct.pack(">I", len(chunk_data)) + b"tEXt" + chunk_data + struct.pack(">I", crc)

made = 0
for f in sorted(glob.glob(os.path.join(BASE, "anime_*.json"))):
    if "_cn" not in f:
        continue
    base = os.path.splitext(os.path.basename(f))[0]
    card = json.load(open(f, encoding="utf-8"))
    v2 = card["data"]
    # flat v1-style card: top-level fields, no spec wrapper
    v1 = {k: val for k, val in v2.items()}
    b64 = base64.b64encode(json.dumps(v1, ensure_ascii=False).encode("utf-8")).decode("latin-1")
    png_path = os.path.join(BASE, "avatars", base + ".png")
    raw = open(png_path, "rb").read()
    ihdr_end = 33
    out = raw[:ihdr_end] + add_text_chunk("chara", b64) + raw[ihdr_end:]
    open(os.path.join(OUT, base + ".png"), "wb").write(out)
    made += 1
print("v1 PNG cards written:", made)
