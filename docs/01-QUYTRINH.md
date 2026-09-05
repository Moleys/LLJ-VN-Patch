# 01 — QUY TRÌNH DỊCH (WORKFLOW)

Tài liệu này mô tả toàn bộ quy trình tạo bản vá tiếng Việt cho LimeLight ★ Lemonade Jam (Yuzusoft / Kirikiri Z + KAG custom engine), từ archive mã hóa đến file patch hoàn chỉnh.

> Toàn bộ lệnh PowerShell. **Bắt buộc** set `$env:PYTHONIOENCODING = "utf-8"` trước mọi lệnh python (mặc định cp1252 sẽ crash với tên file Nhật). Path có `[250926]` phải dùng `-LiteralPath`.

---

## Tổng quan pipeline

```
[scn.xp3] --extract--> [text_extract\*.json]  (138 file, cấu trúc scenes/texts/dialogues)
        |
        v  slice_any.py
[work\*.slice.json]               (danh sách câu cần dịch: v2 + v0-only)
        |
        v  DỊCH (subagent/LLM đọc file → ghi *.slice.vi.json)
[work\*.slice.vi.json]
        |
        v  merge_any.py           (ghép vi vào extract, xử lý name fields)
[work\*.patched.json]
        |
        v  scn-script-patch.exe   (PSB patch)
[work\*.ks.scn]                   (PSB đã dịch, tên entry thật)
        |
        v  copy                   (Stop game trước!)
[game\unencrypted\*.ks.scn]       ← ENGINE TỰ ƯU TIÊN FILE NÀY
```

UI system tương tự nhưng đổi format: descramble → dịch → **re-scramble mode 1** → copy vào `unencrypted\`.

---

## Bước 0 — Chuẩn bị dữ liệu nguồn

Extract `scn.xp3` (Hxv4) bằng tool tĩnh (`xp3_inspect.py extract-all` + drip program đã recover) rồi rename entry hash → tên thật bằng `HxNames-LLLJ.lst`. Kết quả: `scn_named\*.psb` (138 file) và `text_extract\*.json` (JSON cấu trúc scenes → texts → dialogues).

> Chi tiết decrypt Hxv4 xem `docs/03-KYTHUAT.md`.

## Bước 1 — Slice (tách câu cần dịch)

```powershell
python tools\slice_any.py <text_extract\X.ks.scn.json> <work\X.slice.json>
```

Logic slice (`slice_any.py`):
- **v2-line** `values=[%tag;text, int, text, text]` → lấy `values[2]` làm `jp`, đánh dấu `src=v2`.
- **v0-only** `values=[text, int]` → lấy `values[0]`, **strip control-tag prefix** (`%n;`…), đánh dấu `src=v0`.
- Bỏ qua câu rỗng. Ghi kèm `i` (global dialogue index), `si/ti/di`, `name`.
- Selects (lựa chọn) thêm dạng `{kind:"s", si, sel, jp}`.

⚠️ **Bài học lớn**: pipeline đầu chỉ slice `values[2]≠empty` → sót **51,788 câu v0-only** (75% lượng text!). Phải đối chiếu với patch CN để phát hiện. Luôn đối chiesto tổng: `tot=69611, ne2=17823, ne0_only=51788`.

## Bước 2 — Dịch

Giao từng file (hoặc nhóm file nhỏ) cho translator (LLM subagent) với prompt quy ước:

- Đọc slice JSON → dịch `jp` → ghi `*.slice.vi.json` **1-1 giữ key** + thêm `vi`.
- Giữ control-tag (`%n; %f %r %i`, pattern `%[a-zA-Z]+;?`) đúng vị trí đầu chuỗi.
- Tên nhân vật roman hóa theo VNDB: Okinami **Yukitaka**, Futamihara **Ririko**, Harumi **Ena**, Nabari **Anju**, Shimakoshi **Tsukimi**, Saen **Nayuka**, Koishikawa **Miku/Suguru/Yuuma**, Nakahara **Hiromu**, Misaka **Hinami**, Okinami **Ruiko**…
- Self-check: số phần tử output == input, không còn ký tự JP.

## Bước 3 — Merge

```powershell
python tools\merge_any.py <extract.json> <slice.vi.json> <patched.json>
```

`merge_any.py` xử lý:
- **v2-line**: `values[0]` = tag + vi (replace jp nếu có trong v0), `values[2]=vi`, `values[3]=vi`.
- **v0-only (len==2)**: `values[0]` = tag + vi (giữ nguyên `values[1]` int).
- **Name fields**: `text.name` + `dialogue.display_name` dịch qua `names_map.json` (hỗ trợ tên ghép `恵凪・杏珠・月望` → `Ena & Anzu & Tsukimi`).
- Selects: `scenes[si].selects[sel] = vi`.
- In `index_mismatch` — **phải = 0**.

Chạy hàng loạt cả 138 file: `bulk_merge_patch.py` (merge + patch + deploy một lượt, skip file đã làm).

## Bước 4 — Patch PSB

```powershell
bin\scn-script-patch.exe <patched.json> <scn_named\X.ks.scn.psb> <work\X.ks.scn>
```

- File ra **KHÔNG có đuôi `.psb`** (tên entry gốc đã gồm `.ks.scn`).
- Patcher ghi lại toàn bộ nội dung JSON vào PSB (values, name, display_name).

## Bước 5 — Deploy

```powershell
Stop-Process -Name limelight_lj -Force   # BẮT BUỘC: file bị lock khi game chạy
Copy-Item work\X.ks.scn <game>\unencrypted\X.ks.scn
```

## Bước 6 — Verify

- `verify_batch.py` — đếm câu áp dụng / JP sót từng file.
- `full_check.py` — toàn diện: coverage, name, skip-list reconcile, deploy integrity, double-name prefix.
- `deep_check.py` — phân biệt JP thật vs full-width/ー (false positive).
- `scn-decompiler.exe <psb> <out.txt>` — dump text để soát.

---

## UI system (tiếng Anh)

### uitexts.toml
- Scramble `\xfe\xfe` mode 1. Descramble bằng `KirikiriDescrambler.exe` (in-place).
- Section `[texts]` (421 key) + `screen.*` (layout + text lồng nhau, dùng chuỗi single-quote).
- Dịch: `extract_uitexts.py` → translate → `apply_uitexts2.py` (merge, **sanitize: escape `\` `"` + newline→space** — engine dùng toml11 strict, string gãy dòng là crash) → validate bằng `tomllib` → scramble lại (`scramble_mode1.py`) → deploy.

### syslangtext_jp.ini
- INI dạng `Key<TAB>value`, có key chứa ký tự JP (là **lookup key — giữ nguyên**), value dịch.
- Dùng bản `syslangtext_en.ini` có sẵn làm base, sửa tàn dư template (`TitleCaption`, `ConfigPreviewText2`).
- Deploy đè lên tên `syslangtext_jp.ini` (game đọc theo `CurrentLanguageTag=jp`).

### Fix crash Settings
`default.tjs`: `.MovieAudioSampleFilter = "wf_reverb"` → `""`. Root-cause xem `docs/03-KYTHUAT.md`.

### Re-scramble
`scramble_mode1.py <in> <out> 1` — header `\xfe\xfe\x01\xff\xfe` + bit-swap mode 1 từng word UTF-16LE. Đã roundtrip-verify.
