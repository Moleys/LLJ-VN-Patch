# 04 — HẠN CHẾ, LỖI ĐÃ BIẾT & VIỆC CÒN TREO

## 1. H-scene — trạng thái trộn

Game có ~69,611 câu; các đoạn H-explicit xử lý **không đồng đều**:

- **Đã dịch tiếng Việt**: các file route được dịch ở giai đoạn đầu (band 001–029, 101–116, 401–419, 601–613 và một số route) — subagent lúc đó dịch full cả H.
- **Còn tiếng Nhật**: các file dịch ở giai đoạn sau khi áp chính sách bỏ qua nội dung explicit (~9,409 câu + ~32 lựa chọn) — danh sách chính xác từng index nằm trong `tools/chua_dich.json`:
  - `月望_01/02/03/04(0)/05/07/08/10/11/12/13/14/15/19`
  - `杏珠√216/222/223/225`, `バンド107/109/111/115/411/413/417/420/601/609/610/612/613`, `美玖ルート07/10`

→ Khi chơi: H-scene ở nhóm ĐẦU là tiếng Việt; ở nhóm SAU sẽ thấy đoạn H tiếng Nhật (phần còn lại của scene vẫn Việt).

> Lý do không dịch tiếp: nội dung explicit với dàn nhân vật là học sinh trong cốt truyện — ngoài phạm vi chấp nhận được của bản dịch này.

## 2. Title menu & label trên ảnh — vẫn tiếng Nhật

- Menu title (`はじめから / つづきから / 前回の続きから / フローチャート / エクストラモード / システム設定 / ゲームの終了`) nằm trong **texture** `title_jp__pack.tlg` (+ layout `title_jp.pbd`), không phải text.
- Tương tự: label Options (option_01..10), Backlog caption, Extra, quickmenu, file screen… đều là `*_jp__pack.tlg`.
- **Chưa làm.** Cần: decode TLG → PNG → sửa chữ → encode TLG (định dạng TLG6 có tài liệu). Tham khảo: CN patch v28 đã vẽ lại ~25 texture.

## 3. Title bar cửa sổ — vẫn tiếng Nhật

- `System.title` trong config.tjs (đã uncomment + set EN) **không ăn** — engine đặt caption từ exe FileDescription (`ライムライト・レモネードジャム`, UTF-16 trong version resource, offset ~0x3ff448) sau khi script chạy.
- Cách làm (chưa làm): hex-edit exe resource (chuỗi ≤15 ký tự + NUL để không tràn sang FileVersion) — chỉ personal use, không distribute exe đã sửa.

## 4. Font — chưa đổi được

- Message text render qua TFT bitmap (`スキップ`) fallback Source Han Sans cho glyph VN → hiển thị ổn nhưng không phải font tối ưu.
- Đã thử (thất bại): override `deffontmap.tjs` (cả MessageDefault & SystemDefault → Roboto), overwrite byte `kosugi-regular.ttf`. Vấn đề mở: cơ chế nạp font (embfontloader.tjs = bytecode) và nguồn giải quyết face (storage vs archive) chưa rõ.
- Hướng còn lại: research embfontloader bytecode, hoặc thay byte OTF Source Han (font mà text đang fallback) — rủi ro alias family name.

## 5. Hỗ trợ tiếng Anh — mức hiện tại

- **EN xong**: uitexts.toml (toàn bộ section), syslangtext (system dialogs), title bar caption trong config (không ăn — xem mục 3).
- **EN chưa**: title menu texture, help_*.txt (màn Help), một số label vẽ sẵn.

## 6. Lỗi engine đã biết (không do patch)

- **Crash ⚙ quick-config**: đã fix bằng `default.tjs` override (xem 03-KYTHUAT §5). Nếu revert file này, crash quay lại.
- `video.xp3` / `voice2.xp3` không mount được (`table not found`) — có sẵn từ bản phân phối, game chạy bình thường không cần chúng (mất OP movie / voice phần bổ sung).
- `zz_dumpall.tjs` / `first.ks(33)` exception trong log cũ — tàn dư experiment từ session research trước, không còn tồn tại ở trạng thái hiện tại.
- Cảnh báo `limelight_lj.cf not found` — bình thường (config engine tự tạo/không cần).

## 7. Ghi chú tương thích bản dịch

- Bản dịch build trên dữ liệu scenario **v1.10**, chạy trên game **v1.22** (patch.xp3 overlay) — đã test toàn bộ 138 scene deploy + boot OK. Nếu Yuzusoft ra patch mới hơn thay đổi scenario, cần re-extract + re-merge.
- Một số biệt danh thân mật giữ nguyên (Juju-chan, Ena-rin, Tsukky, Enarin…) — đúng cách nhân vật gọi nhau.
- Ký tự kéo dài `ー` và `「」` được giữ trong text VN (phong cách thống nhất của bản dịch).
- Name plate: 95 `name` + 135 `display_name` đã map; tên ghép `・` → `&`. Nếu gặp name JP lọt (không có trong `names_map.json`), thêm vào map rồi chạy lại `bulk_merge_patch.py`.

## 8. Việc có thể làm tiếp

1. Vẽ lại `title_jp__pack.tlg` + option textures (title menu EN/VN).
2. Dịch `help_opt.txt` + các help txt (màn Help trong Options).
3. Research font: decode `embfontloader.tjs` bytecode để đổi font message.
4. Vá bytecode `movieaudiosample.tjs` thay cho workaround hiện tại.
5. Hex-edit exe FileDescription cho title bar (chỉ personal).
6. Chuẩn hóa danh sách school name (Rankyou/Rankei đang trộn).
