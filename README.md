# RRT và RRT* – Chuyên đề 2, Nhóm 04

Mô phỏng và so sánh hai thuật toán tìm đường cho robot hình đĩa trong môi trường 2D có vật cản.

## Cài đặt

Dùng Python 3.12 trở lên. Chạy các lệnh từ thư mục chứa `main.py`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Nếu không kích hoạt được môi trường ảo, thay `python` bằng `.\.venv\Scripts\python.exe` trong các lệnh dưới.

## Chạy mô phỏng

```powershell
# Giao diện tương tác: chạy/dừng, từng bước, đổi seed, lưu PNG
python main.py --map simple --seed 0 --interactive

# Chạy và lưu ảnh hai thuật toán
python main.py --map complex --seed 0 --save results/demo.png
```

Bản đồ: `simple`, `complex`, `narrow`. Mặc định chạy cả RRT và RRT* với 2500 vòng lặp. Có thể chỉnh `--iterations`, `--step-size`, `--goal-bias`, `--robot-radius`.

## Chạy thực nghiệm

```powershell
python -m experiments.benchmark --output results/benchmark_new --seeds 20 --repeats 5
```

Chạy 3 bản đồ × 20 seed × 2 thuật toán, mỗi cấu hình đo 5 lần và lấy trung vị thời gian. Tự lưu dữ liệu, thống kê, Wilcoxon và hình tiếng Việt. Dùng thư mục đầu ra mới để tránh ghi đè kết quả cũ.

## Tạo lại hình từ kết quả đã lưu

```powershell
python -m experiments.plots --input results/benchmark_v2
```

Thay đường dẫn bằng thư mục kết quả muốn dùng. Thêm `--charts-only` nếu chỉ cần biểu đồ và thống kê, không dựng lại cây. Lệnh không cập nhật báo cáo Word/PDF.

Giữ `runs.csv`, `convergence.csv`, `paths.jsonl` và `settings.json` để tạo lại hình. Thời gian đo có thể thay đổi giữa các đợt chạy.

## Thư mục chính

- `src/`: thuật toán, kiểm tra va chạm và giao diện.
- `configs/maps/`: bản đồ JSON.
- `experiments/`: benchmark, biểu đồ và thực nghiệm bổ sung.
- `results/`: dữ liệu và hình kết quả.
- `tests/`: chạy bằng `python -m pytest -q`.

Đây là lập kế hoạch đường đi hình học 2D, chưa bao gồm điều khiển robot thực tế.