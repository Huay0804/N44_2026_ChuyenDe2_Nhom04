# So sánh RRT và RRT* trong lập kế hoạch đường đi 2D (Chuyên đề 2 – Nhóm 04)

Mô phỏng và thực nghiệm so sánh RRT với RRT* cho robot hình đĩa trên bản đồ 2D tĩnh
(kiểm tra va chạm liên tục trên toàn cạnh, cùng chuỗi mẫu theo seed).

## 1. Cài đặt

Yêu cầu Python ≥ 3.12.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate      Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Cấu trúc thư mục

| Đường dẫn | Nội dung |
|---|---|
| `src/` | Lõi thuật toán: `rrt.py`, `rrt_star.py`, `node.py` (cây + đổi cha), `collision.py`, `environment.py`, `visualization.py` |
| `configs/maps/` | Ba bản đồ: `simple`, `complex`, `narrow` (JSON) |
| `experiments/benchmark.py` | Chạy 3 bản đồ × 20 seed × 2 thuật toán, ghi CSV/JSON |
| `experiments/plots.py` | Tổng hợp thống kê (Wilson, Wilcoxon) và vẽ hình |
| `experiments/extra.py` | Thực nghiệm bổ sung: bán kính lân cận, độ phức tạp, bộ nhớ, baseline, độ nhạy, cùng thời gian |
| `tests/` | Kiểm thử bất biến cây, va chạm, tái lập, tính hợp lệ của đường |
| `results/` | Dữ liệu và hình của các đợt chạy |

## 3. Chạy mô phỏng một lần

```bash
python main.py --map simple --seed 0                 # in kết quả của RRT và RRT*
python main.py --map complex --seed 0 --save out.png  # lưu hình hai cây cạnh nhau
python main.py --map narrow --seed 1 --interactive   # giao diện tương tác
```

Tham số chính: `--iterations`, `--step-size`, `--goal-bias`, `--robot-radius`, `--gamma`, `--stop-on-first`.

## 4. Chạy benchmark

```bash
# Đợt chuẩn trong báo cáo (20 seed, 2500 vòng lặp); mỗi cấu hình đo 5 lần, lấy trung vị thời gian
python -m experiments.benchmark --output results/benchmark_v2 --seeds 20 --repeats 5

# Vẽ lại hình/thống kê từ dữ liệu đã có
python -m experiments.plots --input results/benchmark_v2
```

`--output` phải là thư mục chưa có kết quả. Thông tin máy, phiên bản thư viện và γ hiệu dụng được ghi vào `settings.json`.
Số đo thời gian phụ thuộc máy; chỉ so sánh các số được đo trong cùng một đợt chạy.

## 5. Thực nghiệm bổ sung

```bash
python -m experiments.extra radius                          # r_n thực tế, ngưỡng γ
python -m experiments.extra scaling --input results/benchmark_v2        # số mũ thời gian theo vòng lặp
python -m experiments.extra first-solution --input results/benchmark_v2 # RRT dừng ở lời giải đầu vs chạy hết ngân sách
python -m experiments.extra reference --input results/benchmark_v2      # optimality gap so với đồ thị tầm nhìn
python -m experiments.extra memory --seeds 5                # bộ nhớ đỉnh (tracemalloc)
python -m experiments.extra equal-time --budget 1.0 --seeds 20          # cùng ngân sách thời gian
python -m experiments.extra sensitivity --seeds 10          # độ nhạy η, p_g, γ
```

Kết quả ghi vào `results/extra/`.

## 6. Kiểm thử

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```
