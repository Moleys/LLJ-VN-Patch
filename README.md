# LimeLight ★ Lemonade Jam — Bản vá tiếng Việt (VN Patch)

Bản dịch tiếng Việt **không chính thức** cho game [ライムライト・レモネードジャム (LimeLight ★ Lemonade Jam)](https://www.yuzu-soft.com/products/lllj/) — Yuzusoft.

> **Trạng thái:** Story route hoàn thành ~99.6% · UI hệ thống tiếng Anh · H-scene một phần (xem [Hạn chế](docs/04-HANCHE.md))

---

## Cài đặt

### Yêu cầu
1. **Game bản gốc** (đã cài đầy đủ).
2. **Official Patch v1.22** của Yuzusoft — *bắt buộc*. Tải từ trang chủ Yuzusoft, chạy installer trỏ vào thư mục game (kết quả: file `patch.xp3` + `patch.xp3.sig` trong thư mục game).
3. **Hook `version.dll`** (KirikiriUnencryptedArchive, từ dự án KirikiriTools) — *đã kèm sẵn* trong `patch/version.dll`.

### Cài đặt — chỉ cần copy 2 file
1. Copy **2 file** sau vào **thư mục gốc của game** (thư mục chứa `limelight_lj.exe`):
   ```
   limelight_lj\
   ├── limelight_lj.exe
   ├── version.dll          ← từ patch/version.dll (nếu game chưa có sẵn hook)
   ├── unencrypted.xp3      ← từ patch/unencrypted.xp3 (toàn bộ bản vá trong 1 file)
   ├── data.xp3, scn.xp3, patch.xp3, ...
   ```
2. **Xóa file `extract-unencrypted.txt`** trong thư mục game nếu tồn tại (chế độ dump debug).
3. Chạy game bình thường.

> Gỡ bỏ: xóa `unencrypted.xp3` (và `version.dll` nếu game không cần hook nào khác) — game trở về nguyên bản.
> Nâng cấp bản vá: chỉ thay file `unencrypted.xp3`.

---

## Nội dung bản vá

| Thành phần | Ghi chú |
|---|---|
| **138/138 scene** (`*.ks.scn`, PSB) | 69,323/69,611 câu thoại tiếng Việt (99.6%) · 100/100 lựa chọn |
| **Name plate** | Toàn bộ ~230 tên nhân vật/vai diễn roman hóa chuẩn VNDB (Okinami Yukitaka, Futamihara Ririko, Nabari Anju, Misaka Hinami…) |
| **uitexts.toml** | Toàn bộ text UI hệ thống (menu, Options, Extra, Backlog, dialog…) → **tiếng Anh** |
| **syslangtext_jp.ini** | System dialogs (OK/Cancel, Search, GamePad, Shortcut…) → **tiếng Anh**; title bar caption |
| **default.tjs** | Fix crash nút ⚙ Settings (`MovieAudioSampleFilter=""`) |
| **config.tjs** | Config engine (giữ nguyên hành vi đã test) |

## Hạn chế chính (chi tiết tại `docs/04-HANCHE.md`)

- **H-scene**: các file route dịch ở giai đoạn sau để nguyên tiếng Nhật (~9,409 câu, danh sách trong `tools/chua_dich.json`). Các file route đầu thì H đã dịch → **trạng thái trộn**.
- **Title menu** (はじめから…) và label vẽ sẵn trên ảnh (`*_jp__pack.tlg`): vẫn tiếng Nhật — cần vẽ lại texture, chưa làm.
- **Title bar** cửa sổ: vẫn tiếng Nhật (lấy từ exe resource; `System.title` không ăn).
- **Font**: font gốc (Source Han fallback) — chưa đổi sang font khác được.

---

## Tài liệu

| File | Nội dung |
|---|---|
| [docs/01-QUYTRINH.md](docs/01-QUYTRINH.md) | Quy trình dịch hoàn chỉnh 6 bước (extract → slice → translate → merge → patch → deploy) |
| [docs/02-CONG-CU.md](docs/02-CONG-CU.md) | Công cụ + script, cách dùng, cách build lại từ đầu |
| [docs/03-KYTHUAT.md](docs/03-KYTHUAT.md) | Kỹ thuật ngược: PSB values v0/v2, scramble format, patch layers, root-cause crash Settings |
| [docs/04-HANCHE.md](docs/04-HANCHE.md) | Hạn chế, lỗi đã biết, việc còn treo |

## Phạm vi dữ liệu

- Dữ liệu nguồn: `scn.xp3` v1.10 (138 scene, 69,611 câu) — bản dịch build trên nền này, chạy trên game **v1.22** (đã test).
- UI tiếng Anh dựa trên asset EN có sẵn trong engine + dịch bổ sung.

## Ghi nhận

- [KirikiriTools](https://github.com/wamsoft/kirikiritools) — version.dll hook + Descrambler/Scrambler.
- Tool `scn-script-patch` / `scn-decompiler` — làm việc với PSB scenario.
- Patch Trung Quốc v28 (`unencrypted.xp3`) — tham khảo cấu trúc & phương pháp vẽ lại UI.
- Yuzusoft — game + official patch v1.22.

## Bản quyền / Miễn trừ

- Bản vá **KHÔNG kèm bất kỳ file game gốc nào**. Người dùng phải sở hữu game.
- KHÔNG bao gồm bất kỳ công cụ nào phục vụ việc phá bảo vệ game.
- Dành cho mục đích cá nhân, nghiên cứu. Vui lòng tôn trọng quyền của Yuzusoft.
