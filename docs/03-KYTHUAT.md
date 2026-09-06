# 03 — KỸ THUẬT (Reverse Engineering Findings)

Tổng hợp các phát hiện kỹ thuật khi nghịch đảo engine Yuzusoft (Kirikiri Z + KAG custom, archive biến thể **Hxv4**).

---

## 1. Archive & hook

- Archive `.xp3` biến thể **Hxv4**: magic `XP3\r\n \n\x1a\x8bg\x01`, index offset "giả" = 0x17, pointer thật (qword) ở offset 0x20, entry protected_flag riêng, filter mã hóa per-entry (đã recover qua `cxdec_static`, key trong `drip_program.json`).
- **Hook `version.dll`** (KirikiriUnencryptedArchive, từ KirikiriTools):
  - Nếu tồn tại `unencrypted\` trong game root → mọi file trùng tên được phục vụ từ đó (storage-level override).
  - Nếu tồn tại `extract-unencrypted.txt` → **chế độ dump**: ghi toàn bộ nội dung archive ra `unencrypted\` lúc boot (chỉ ghi file chưa tồn tại — override của ta không bị ghi đè).
  - Hỗ trợ **nhiều lớp patch archive**: `patch.xp3` (official) và `patch2.xp3` (unofficial) — engine mount theo domain, Auto Path Table quét lúc boot.
- **Độ ưu tiên thực nghiệm**: `unencrypted\` (hook) > `patch.xp3` (official overlay, entry hash-obfuscated) > base archive.

## 2. PSB scenario — cấu trúc dialogue

Mỗi `*.ks.scn` là **PSB v3**. JSON extract có dạng:

```
scenes[] → texts[] → dialogues[]
  text:     { name: "雪鷹"|null, dialogues: [...] }
  dialogue: { display_name: "…"|null, values: [...] }
```

**HAI dạng values:**

| Dạng | values | Ý nghĩa |
|---|---|---|
| v2 (17,823 câu) | `[%tag;text, int, text, text]` | [0] hiển thị (có tag điều khiển), [1] id/len?, [2] text gốc, [3] backlog |
| v0-only (51,788 câu) | `[text, int]` | [0] text hiển thị (có thể có tag prefix `%n;`), [1] id/len? |

⚠️ Chỉ dịch v2 mà bỏ v0 = mất 75% text. v0/v2 **xen kẽ nhau** trong cùng scene.

**Name fields**: `text.name` + `dialogue.display_name` là nguồn name plate — phải dịch riêng (tên ghép dùng dấu `・`). 95 `name` + 135 `display_name` distinct.

Thống kê nguồn: `tot=69,611 dialogues; ne0=69,611; ne2=17,823; ne0_only=51,788`.

## 3. Scramble format (`\xfe\xfe`)

File text hệ thống (.tjs/.toml/.ini/.ks) trong archive bị scramble:

```
header: FE FE <mode:u8> FF FE     (mode thường gặp = 1)
data:   UTF-16LE bytes, mỗi 16-bit word bị đảo bit:
        c' = ((c & 0xAAAA) >> 1) | ((c & 0x5555) << 1)
```

- Descramble: `KirikiriDescrambler.exe <file/folder>` (in-place).
- Scramble lại: `tools\scramble_mode1.py` (roundtrip-verified, header đúng `FE FE 01 FF FE`).
- Sau descramble, nội dung là **UTF-8** (có BOM). File override do mình sinh ra ở dạng UTF-16LE-scrambled — engine/TJS vẫn parse được (đã chứng minh bằng default.tjs crash-fix có hiệu lực).
- `.tjs` phần còn lại là **TJS2100 bytecode** (magic `TJS2100\0`) — KHÔNG descramble được bằng tool này, cần decompiler riêng (không có).
- `KBAD100` = format khác (ctxfontprefs.tjs), chưa xử lý.

## 4. Hệ thống font / multi-lang — **ĐÃ GIẢI MÃ (2026-09-06)**

- Chuỗi resolve của hộp thoại: `deffontmap.tjs → "MessageDefault".lang_jp = "スキップ"` → tra `embfontlist.tjs` entry `{ "name"=>"スキップ", "file"=>"font1_${size}.tft", "deffont"=>true }` = **TFT atlas prerender** (chỉ glyph JP). Ký tự lạ (VN) rơi xuống `FallbackFace` (prerenderfontex.tjs) → Source Han OTF → "đọc được nhưng xấu".
- Lần thử override `deffontmap.tjs` trước đó thất bại vì: message face KHÔNG đi qua deffontmap một mình — embfontlist entry vẫn ghim atlas `font1_*.tft`.
- **Giải pháp ROBOTO đã áp dụng** (trong gói hiện tại — đã hiệu chỉnh sau test thực tế):
  1. `embfontlist.tjs` — sửa trực tiếp entry message: `{ "name"=>"スキップ", "file"=>"font1_${size}.tft", "deffont"=>true }` → `{ "name"=>"スキップ", "file"=>"Roboto-Regular.ttf", "face"=>"Roboto", "deffont"=>true }` — text hội thoại resolve qua entry này nên TTF trực tiếp thay atlas (loader có nhánh **no-atlas** render TTF qua `AddTrueTypeFont`).
  2. `deffontmap.tjs` — **GIỮ NGUYÊN**. Bài học từ test 1: đổi `MessageDefault` sang "Roboto" chỉ đổi font của **một số label UI** (alias MessageFont), KHÔNG đụng vào text hội thoại (vẫn đi qua entry `スキップ`).
  3. Đóng gói `Roboto-Regular.ttf` (+Bold, LICENSE) vào `unencrypted.xp3` (loader đọc `file` qua storage → hook phục vụ từ override).
- **Format file override: plain UTF-16LE BOM** (`FF FE ...`) — KHÔNG cần scramble mode 1. Bằng chứng: CN patch ship `uitexts.toml`/`deffontmap.tjs`/`embfontlist.tjs` dạng plain UTF-16 BOM. Scramble vẫn hoạt động (syslangtext_jp.ini EN đang ship scramble), nhưng plain an toàn hơn khi tự sinh file.
- Lưu ý decode scramble: header `FE FE 01 FF FE` = **5 byte**, body bắt đầu offset 5 (không phải 6) — decode lệch 1 byte sinh mojibake Hangul giả.
- Multi-lang: `yuzu_default.tjs` có `multiLangLanguageTags=[jp,en,cn,tw]` + gate `_multilang.ini`, nhưng **CUSTOM_MULTILANG bị compile-out** — asset `uitexts_en.toml`/`syslangtext_en.ini` chỉ là template tàn dư (tên char Noa/Amane…) — chỉ dùng làm base tham khảo.

## 5. Root-cause crash nút ⚙ Settings

```
DialogManager: 初期化に失敗しました (Cannot convert (void) to Object): option
  tại movieaudiosample.tjs loadFilters, VM ip=107
```

Disassembly (từ krkr.console.log, UTF-16):
```
if (typeof kag.voiceEffectPlugin != "Object") {
    error "MovieAudioSampleFilterの使用にはvoiceeffectプラグインが必要です"
    kag.errorSound(...); return;      // ← trả VOID (bug của game)
}
%3 = kag.voiceEffectPlugin; %4 = %3.loadFilter(name, ...); … = %4.count  // crash nếu void
```

- Nguyên nhân: `kag.voiceEffectPlugin` chưa được load (plugin voice-effect khởi tạo lazy) → error-path của game trả void → caller đọc `.count` trên void → crash.
- **Fix an toàn**: `default.tjs` đặt `.MovieAudioSampleFilter = ""` — đầu hàm có early-return `if (name == "") return name;` → không chạm nhánh lỗi. Mất reverb preview trong config (tầm thường).
- Fix đúng hơn (chưa làm): force-load voiceeffect plugin lúc boot, hoặc vá bytecode movieaudiosample.tjs.
- Lỗi này **không liên quan** patch dịch; xảy ra cả trên game sạch v1.10/v1.22 trong môi trường có hook.

## 6. Title menu & UI texture

- Menu title (はじめから/つづきから/…) **KHÔNG phải text** — nằm trong texture `title_jp__pack.tlg` (+ `title_jp.pbd` layout). Tương tự label Options/Extra/backlog: `option_01..10_jp__pack.tlg`, `qconf_*`, `file_*`…
- Bằng chứng: không tìm thấy はじめから trong bất kỳ file text nào (uitexts/ks/tjs-text).
- CN patch v28 giải pháp = **vẽ lại ~25 file .tlg** (kèm `_pack` metadata). Làm tương tự cho EN/VN: decode TLG → sửa → encode.
- `uitexts.toml` có **nhiều section** (`[texts]` 421 key + `screen.*` với chuỗi single-quote lồng trong layout config) — parse bằng regex double-quote một mình sẽ sót; cần scan cả single-quote. Bắt buộc validate `tomllib` sau merge (toml11 của engine strict; value chứa newline thật làm crash khởi động với dialog `toml文法エラー`).

## 7. Official patch v1.22

- Ship dạng `patch.xp3` (635MB, 2,022 entry **hash-obfuscated tên**) + `.sig`. Engine tự map tên thật lúc mount.
- Cài xong xuất hiện `currev_patch.ini = "1406"` (base `currev.ini = "1267"`). `version.ks` vẫn ghi `software_version = "1.10"` — version theo `currev_patch`.
- Các bản patch cộng đồng (CN v28, EN asf, RU khms) đều yêu cầu/dính tới v1.22.

## 8. Bẫy môi trường (Windows/PowerShell)

- Path chứa `[250926]`: `-LiteralPath` bắt buộc; **glob `*` không hoạt động với -LiteralPath** (Copy-Item wildcard fail âm thầm); **glob() trong Python fail với `[...]`** (character class) → dùng os.listdir.
- `PYTHONIOENCODING=utf-8` bắt buộc; console in mojibake không có nghĩa file hỏng (kiểm tra bằng UTF-16/UTF-8 decode).
- `Start-Process` với path `[...]` fail → dùng `System.Diagnostics.ProcessStartInfo`.
- Stop game trước khi ghi file vào `unencrypted\` (file lock).
- Descrambler chạy **in-place** — luôn copy ra working dir trước khi descramble.
