# 02 — CÔNG CỤ & SCRIPT

## Cấu trúc thư mục project

```
LLJ-VN-Patch\
├── README.md
├── docs\                      (tài liệu)
├── patch\                     (thành phẩm — copy vào game)
│   ├── version.dll            (hook KirikiriUnencryptedArchive)
│   └── unencrypted\           (138 scene + uitexts.toml + syslangtext_jp.ini + default.tjs + config.tjs)
├── tools\                     (script pipeline + names_map.json + chua_dich.json)
└── bin\                       (exe: scn-script-patch, scn-decompiler, scn-script-extractor, KirikiriDescrambler)
```

## Các exe

| Tool | Vai trò |
|---|---|
| `bin\scn-script-patch.exe` | `<patched.json> <gốc.psb> <ra>` — ghi JSON vào PSB scenario |
| `bin\scn-decompiler.exe` | `<psb> <out.txt>` — dump text PSB để soát |
| `bin\scn-script-extractor.exe` | `<psb> <out.json>` — extract PSB → JSON (cùng format với text_extract) |
| `bin\KirikiriDescrambler.exe` | `<file/folder>` — descramble/scramble file `\xfe\xfe` (in-place) |

Ngoài ra cần (không kèm, lấy từ research gốc):
- `xp3_inspect.py` + drip program (trong `cxdec_static\`) — decrypt/extract archive Hxv4.
- `HxNames-LLLJ.lst` — bảng hash→tên thật (61,335 dòng).

## Script pipeline (tools\)

### Story

| Script | Lệnh | Chức năng |
|---|---|---|
| `slice_any.py` | `<extract.json> <out.slice.json>` | Tách câu (v2 + v0-only) thành slice dịch |
| `merge_any.py` | `<extract.json> <slice.vi.json> <patched.json>` | Ghép dịch + **dịch name fields** qua `names_map.json` |
| `bulk_merge_patch.py` | `<_translation_work> <game>` | Hàng loạt: merge thiếu → patch thiếu → deploy tất cả |
| `verify_batch.py` | `<work>` | Đếm câu VN/JP từng file patched |
| `full_check.py` | `<work> <game>` | Kiểm tra toàn diện (coverage, name, skip, deploy) |
| `deep_check.py` | `<work>` | Phân biệt JP thật vs full-width/ー false-positive |
| `reslice_all.py` | `<base>` | Re-slice toàn bộ 138 file |

### Name fields

| Script/File | Chức năng |
|---|---|
| `names_map.json` | Map tên: component đơn (雪鷹→Yukitaka) + whole-name override (新・学生会長→New Student Council President) |
| `fix_names_text.py` | Đồng bộ tên trong vi-text theo official DB (Anzu→Anju…) word-boundary |

### UI system

| Script | Chức năng |
|---|---|
| `extract_uitexts.py` | Parse `[texts]` uitexts.toml → slice |
| `apply_uitexts2.py` | Merge EN vào uitexts + **sanitize TOML** (escape `\ "`, newline→space) + validate `tomllib` |
| `extract_jp_strings.py` | Trích mọi string literal chứa JP (double-quote) |
| `apply_literals.py` | Replace literal (single+double quote) chứa JP bằng EN từ map |
| `fix_syslang_en.py` | Sửa tàn dư template trong syslangtext EN (TitleCaption, copyright) |

### Scramble & workflow phụ

| Script | Chức năng |
|---|---|
| `scramble_mode1.py` | `<in> <out> [mode]` — scramble text → `\xfe\xfe<mode>\xff\xfe` (mặc định mode 1). **Roundtrip-verified** |
| `gen_todo2.py` | Tạo todo từ slice chưa dịch, bỏ qua mục đã đánh dấu trong `chua_dich.json` |
| `record_skips.py` | Ghi các index chưa dịch vào `chua_dich.json` |
| `merge_todo_vi.py` | Gộp `*.todo.vi.json` → `*.slice.vi.json` |
| `cleanup_vi.py` | Gỡ prefix "Tên:" trùng name plate + normalize full-width→ASCII trong vi-text |
| `fix_names_text.py` | Đồng bộ tên trong text theo VNDB |

## Build lại từ đầu (tóm tắt)

```powershell
$env:PYTHONIOENCODING = "utf-8"
# 0) extract scn.xp3 (dùng research gốc) + rename theo HxNames list
# 1) slice toàn bộ
Get-ChildItem text_extract\*.json | ForEach-Object {
    python tools\slice_any.py $_.FullName ("work\" + $_.BaseName + ".slice.json") }
# 2) dịch *.slice.json -> *.slice.vi.json (thủ công / LLM)
# 3) merge + patch + deploy
python tools\bulk_merge_patch.py <work> <game>
# 4) verify
python tools\full_check.py <work> <game>
```

UI: descramble (bin\KirikiriDescrambler.exe) → dịch → `apply_uitexts2.py` → `scramble_mode1.py` → copy `unencrypted\`.
