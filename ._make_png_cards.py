import json, os, glob, base64, zlib, struct
BASE = r"E:\tavern characters"
OUT = os.path.join(BASE, "png_cards")
os.makedirs(OUT, exist_ok=True)

def add_text_chunk(png_bytes, keyword, text_b64):
    # PNG chunk: length + type(tEXt) + data(keyword\0 + base64) + crc(type+data)
    keyword_b = keyword.encode("latin-1")
    data_b = text_b64.encode("latin-1")
    chunk_data = keyword_b + b"\x00" + data_b
    crc = zlib.crc32(b"tEXt" + chunk_data) & 0xffffffff
    length = struct.pack(">I", len(chunk_data))
    return length + b"tEXt" + chunk_data + struct.pack(">I", crc)

made = 0
for f in sorted(glob.glob(os.path.join(BASE, "anime_*.json"))):
    if "_cn" not in f:
        continue
    base = os.path.splitext(os.path.basename(f))[0]
    card = json.load(open(f, encoding="utf-8"))
    # v2 card with chara (v1-ish spec) and ccv3; SillyTavern reads 'chara' base64 of full v2 json
    b64 = base64.b64encode(json.dumps(card, ensure_ascii=False).encode("utf-8")).decode("latin-1")
    png_path = os.path.join(BASE, "avatars", base + ".png")
    raw = open(png_path, "rb").read()
    # split at end of IHDR: signature 8 bytes + 4 len + 4 type + 13 data + 4 crc = 33
    ihdr_end = 8 + 4 + 4 + 13 + 4
    head, rest = raw[:ihdr_end], raw[ihdr_end:]
    # remove any existing chara chunks (we generated avatars fresh, none expected)
    out = head + add_text_chunk(head, "chara", b64) + rest
    open(os.path.join(OUT, base + ".png"), "wb").write(out)
    made += 1
print("PNG cards written:", made)
