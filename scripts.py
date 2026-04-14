import os
import re
import glob
import csv

def parse_log_file(file_path):
    """Đọc và trích xuất thông tin từ một file log cụ thể."""
    benchmark_name = os.path.basename(file_path).replace('.log', '')
    
    num_ops = "N/A"
    num_machines = "N/A"
    num_edges = "N/A"
    greedy_ub = "N/A"
    build_time = "N/A"
    best_makespan = "N/A"
    status_opt = False
    runlim_status_raw = "N/A"
    run_time = "N/A"
    last_sample_time = "N/A"

    # Định nghĩa Regex
    regex_ops = re.compile(r"Operations:\s*(\d+)")
    regex_edges = re.compile(r"Edges:\s*(\d+)")
    regex_machines = re.compile(r"Machines:\s*(\d+)")
    
    regex_greedy = re.compile(r"Greedy Schedule UB:\s+(\d+)")
    regex_greedy_fallback = re.compile(r"Greedy UB (\d+) is valid!")
    regex_build = re.compile(r"Building constraints took ([\d.]+) seconds")
    regex_makespan = re.compile(r"THỜI GIAN HOÀN THÀNH TỔNG.*:\s+(\d+)")
    regex_status_opt = re.compile(r"status:\s+optimal")
    regex_runlim_status = re.compile(r"\[runlim\] status:\s+(\w+)")
    regex_runlim_real = re.compile(r"\[runlim\] real:\s+([\d.]+)")
    regex_runlim_time = re.compile(r"\[runlim\] time:\s+([\d.]+)")
    regex_runlim_sample = re.compile(r"\[runlim\] sample:.*,\s+([\d.]+)\s+real")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Trích xuất Operations, Edges, Machines
                m_ops = regex_ops.search(line)
                if m_ops: num_ops = m_ops.group(1)
                
                m_edges = regex_edges.search(line)
                if m_edges: num_edges = m_edges.group(1)
                
                m_machines = regex_machines.search(line)
                if m_machines: num_machines = m_machines.group(1)

                # Tìm nghiệm Greedy
                m_greedy = regex_greedy.search(line)
                if m_greedy: 
                    greedy_ub = m_greedy.group(1)
                else:
                    m_greedy_fb = regex_greedy_fallback.search(line)
                    if m_greedy_fb and greedy_ub == "N/A":
                        greedy_ub = m_greedy_fb.group(1)

                # Tìm thời gian build
                m_build = regex_build.search(line)
                if m_build: build_time = m_build.group(1)

                # Tìm Makespan tốt nhất (ghi đè liên tục để lấy số cuối cùng)
                m_makespan = regex_makespan.search(line)
                if m_makespan: best_makespan = m_makespan.group(1)

                # Kiểm tra xem solver có đạt đến trạng thái optimal không
                if regex_status_opt.search(line):
                    status_opt = True
                
                # Lấy status từ runlim
                m_rstatus = regex_runlim_status.search(line)
                if m_rstatus: runlim_status_raw = m_rstatus.group(1).lower()

                # Tìm thời gian chạy
                m_real = regex_runlim_real.search(line)
                if m_real: run_time = m_real.group(1)
                
                m_time = regex_runlim_time.search(line)
                if m_time and run_time == "N/A": run_time = m_time.group(1)
                
                m_sample = regex_runlim_sample.search(line)
                if m_sample: last_sample_time = m_sample.group(1)
                
    except Exception as e:
        print(f"Lỗi khi đọc file {file_path}: {e}")
        return None

    # Lấy thời gian từ sample cuối cùng nếu runlim bị ngắt đột ngột (TO/MO)
    if run_time == "N/A" and last_sample_time != "N/A":
        run_time = f"{last_sample_time}"

    # --- LOGIC XÁC ĐỊNH STATUS ---
    if status_opt:
        final_status = "OPT"
    elif runlim_status_raw in ["out", "timeout", "time"]:
        final_status = "TO"
    elif runlim_status_raw in ["mem", "memory", "oom"]:
        final_status = "MO"
    elif runlim_status_raw == "ok":
        final_status = "OK (Not Opt)" 
    else:
        final_status = "Unknown"

    return [benchmark_name, num_ops, num_machines, num_edges, greedy_ub, build_time, best_makespan, final_status, run_time]

def main():
    # Danh sách các thư mục cần quét
    directories = ['results/yfjs', 'results/dafjs']
    
    # Khởi tạo danh sách chứa kết quả với hàng Tiêu đề (Header)
    all_results = []
    headers = [
        "Benchmark", "Operations", "Machines", "Edges", 
        "Greedy UB", "Build Time (s)", "Best Makespan", 
        "Status", "Run Time (s)"
    ]
    all_results.append(headers)

    # Duyệt qua từng thư mục
    for directory in directories:
        if not os.path.exists(directory):
            print(f"Cảnh báo: Không tìm thấy thư mục '{directory}'. Bỏ qua...")
            continue
            
        # Tìm tất cả các file .log trong thư mục hiện tại
        log_files = glob.glob(os.path.join(directory, '*.log'))
        log_files.sort()
        
        for file_path in log_files:
            result = parse_log_file(file_path)
            if result:
                all_results.append(result)

    # --- IN KẾT QUẢ RA MÀN HÌNH DƯỚI DẠNG BẢNG ---
    if len(all_results) > 1:
        col_widths = [max(len(str(item)) for item in col) for col in zip(*all_results)]
        table_width = sum(col_widths) + 3 * len(headers) + 1
        
        print("\n" + "=" * table_width)
        for i, row in enumerate(all_results):
            row_str = " | ".join(str(item).ljust(width) for item, width in zip(row, col_widths))
            print(f"| {row_str} |")
            if i == 0:
                print("-" * table_width)
        print("=" * table_width + "\n")

        # --- LƯU RA FILE CSV ---
        csv_filename = "summary_results.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(all_results)
        print(f"✅ Đã lưu kết quả thành công vào file: {csv_filename}")
    else:
        print("Không tìm thấy file .log hợp lệ nào để phân tích.")

if __name__ == "__main__":
    main()