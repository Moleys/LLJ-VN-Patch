# 04 — HẠN CHẾ, LỖI ĐÃ BIẾT & VIỆC CÒN TREO

## 1. Title menu & label trên ảnh — vẫn tiếng Nhật

- Menu title (`はじめから / つづきから / 前回の続きから / フローチャート / エクストラモード / システム設定 / ゲームの終了`) nằm trong **texture** `title_jp__pack.tlg` (+ layout `title_jp.pbd`), không phải text.
- Tương tự: label Options (option_01..10), Backlog caption, Extra, quickmenu, file screen… đều là `*_jp__pack.tlg`.
- **Chưa làm.** Cần: decode TLG → PNG → sửa chữ → encode TLG (định dạng TLG6 có tài liệu). Tham khảo: CN patch v28 đã vẽ lại ~25 texture.

## 2. Title bar cửa sổ — vẫn tiếng Nhật

- `System.title` trong config.tjs (đã uncomment + set EN) **không ăn** — engine đặt caption từ exe FileDescription (`ライムライト・レモネードジャム`, UTF-16 trong version resource, offset ~0x3ff448) sau khi script chạy.
- Cách làm (chưa làm): hex-edit exe resource (chuỗi ≤15 ký tự + NUL để không tràn sang FileVersion) — chỉ personal use, không distribute exe đã sửa.

## 3. Font — hội thoại ĐÃ dùng Roboto; texture label còn JP

- **Đã giải quyết (2026-09-06):** message text resolve qua entry `スキップ` trong `embfontlist.tjs` — sửa entry này trỏ thẳng `Roboto-Regular.ttf` (TTF trực tiếp, nhánh no-atlas của `embfontloader.tjs`); kèm đăng ký group Roboto + file TTF trong `unencrypted.xp3`. Chi tiết cơ chế xem `03-KYTHUAT.md` §4.
- Bài học: override `deffontmap.tjs` (MessageDefault) chỉ đổi font label UI, KHÔNG đụng text hội thoại.
- Còn lại: label vẽ sẵn trên texture (mục 1) mặc định bitmap JP — xử lý khi vẽ lại texture.

## 4. Hỗ trợ tiếng Anh — mức hiện tại

- **EN xong + đã deploy**: uitexts.toml (toàn bộ section), syslangtext (system dialogs).
- **EN chưa**: title menu texture (mục 1), `help_*.txt` (màn Help trong Options), title bar (mục 2).

## 5. Lỗi engine đã biết (không do patch)

- **Crash ⚙ quick-config**: đã fix bằng `default.tjs` override (xem 03-KYTHUAT §5). Nếu revert file này, crash quay lại.
- `video.xp3` / `voice2.xp3` không mount được (`table not found`) — có sẵn từ bản phân phối, game chạy bình thường không cần chúng (mất OP movie / voice phần bổ sung).
- Cảnh báo `limelight_lj.cf not found` — bình thường (config engine tự tạo/không cần).

## 6. Ghi chú tương thích bản dịch

- Bản vá build trên dữ liệu scenario **v1.10** — **dùng cho game v1.10** (mục tiêu chính), tương thích v1.22 (patch.xp3 overlay). Đã test cả hai: 138 scene deploy + boot OK. Nếu Yuzusoft ra patch mới hơn thay đổi scenario, cần re-extract + re-merge.
- Ngắt dòng tiếng Việt: pipeline chèn `\n` tại dấu cách, ngưỡng 58 ký tự (hiệu chuẩn thực tế trên game — tràn thật ≈ 60). Script: `ui_work/wrap_vi.py` (workspace).
- Câu kết bằng từ "nhỉ" tự thêm "?" — script `ui_work/nhi_batch.py` (1,305 câu đã áp).
- Một số biệt danh thân mật giữ nguyên (Juju-chan, Ena-rin, Tsukky, Enarin…) — đúng cách nhân vật gọi nhau.
- Ký tự kéo dài `ー` và `「」` được giữ trong text VN (phong cách thống nhất của bản dịch).
- Name plate: 95 `name` + 135 `display_name` đã map; tên ghép `・` → `&`.

## 7. Việc có thể làm tiếp

1. Vẽ lại `title_jp__pack.tlg` + option textures (title menu EN/VN).
2. Dịch `help_opt.txt` + các help txt (màn Help trong Options).
3. Hex-edit exe FileDescription cho title bar (chỉ personal).
4. Vá bytecode `movieaudiosample.tjs` thay cho workaround hiện tại.
5. Chuẩn hóa danh sách school name (Rankyou/Rankei đang trộn).
