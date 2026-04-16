
import sys
from time import perf_counter, time
from pysat.solvers import Solver
from pysat.formula import CNF
from pysat.card import CardEnc
from collections import deque, defaultdict


def read_file(file_path):
    with open(file_path, 'r') as file:
        if 'yfjs' in file_path.lower():
            for _ in range(4):
                next(file, None)
        line = file.readline()
        line = line.strip().split()
        if line:
            num_operations = int(line[0])
            num_edges = int(line[1])
            num_machines = int(line[2])
            print(f"Operations: {num_operations}, Edges: {num_edges}, Machines: {num_machines}")
        precedence_list = []
        for _ in range(num_edges):
            line = file.readline()
            line = line.strip().split()
            if line:
                precedence_list.append((int(line[0]), int(line[1])))
        request_list = []
        for _ in range(num_operations):
            line = file.readline()
            line = line.strip().split()
            if line:
                num_resources = int(line[0])
                map = {}
                for i in range(num_resources):
                    machine = int(line[1 + 2 * i])
                    process_time = int(line[2 + 2 * i])
                    map[machine] = process_time
                request_list.append(map)

    return num_operations, num_edges, num_machines, precedence_list, request_list

def data(num_operations, num_edges, num_machines, precedence_list, request_list):
    in_degree = {i: 0 for i in range(num_operations)}
    out_degree = {i: 0 for i in range(num_operations)}
    for u, v in precedence_list:
        in_degree[v] += 1
        out_degree[u] += 1

    neighbors = {i: [] for i in range(num_operations)}
    predecessors = {i: [] for i in range(num_operations)}
    for u, v in precedence_list:
        neighbors[u].append(v)
        predecessors[v].append(u)

    return in_degree, out_degree, neighbors, predecessors


def greedy_schedule(num_operations, num_machines, precedence_list, request_list, in_degree, neighbors, predecessors):
    machine_ready_time = {m: 0 for m in range(num_machines)}
    op_completion_time = {i: 0 for i in range(num_operations)} 
    machine_assignment = {i: None for i in range(num_operations)}

    queue = [i for i in range(num_operations) if in_degree[i] == 0]
    index = 0
    
    while index < num_operations:
        curr = queue[index]
        index += 1
        min_completion = float('inf')

        earliest_start = 0
        if predecessors[curr]:
            earliest_start = max(op_completion_time[p] for p in predecessors[curr])

        for machine, proc_time in request_list[curr].items():
            actual_start = max(machine_ready_time[machine], earliest_start)
            completion = proc_time + actual_start

            if completion < min_completion:
                min_completion = completion
                machine_assignment[curr] = machine

        if machine_assignment[curr] is not None:
            machine_ready_time[machine_assignment[curr]] = min_completion
            op_completion_time[curr] = min_completion

        for neighbor in neighbors[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    ub = max(machine_ready_time.values())
    print(f"Greedy Schedule UB: {ub}")

    return ub, machine_assignment, queue

def generate_size_time(num_operations, num_machines, request_list):
    size_time = 0
    for request in request_list:
        size_time += max(request.values())
    print(f"Size Time: {size_time}")
    return size_time

def calculate_greedy_ub(num_operations, num_machines, precedence_list, request_list):
    """
    Tính Cận trên (Upper Bound - UB) bằng thuật toán Heuristic Tham Lam.
    """
    # Bước 1: Xây dựng đồ thị và tính bán bậc vào (in-degree) cho Sắp xếp Topo
    adj_list = defaultdict(list)
    in_degree = {i: 0 for i in range(num_operations)}
    predecessors = defaultdict(list)
    
    for u, v in precedence_list:
        adj_list[u].append(v)
        in_degree[v] += 1
        predecessors[v].append(u)
        
    # Bước 2: Sắp xếp Topo (Kahn's Algorithm)
    queue = deque([i for i in range(num_operations) if in_degree[i] == 0])
    topo_order = []
    
    while queue:
        curr = queue.popleft()
        topo_order.append(curr)
        for neighbor in adj_list[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # Kiểm tra an toàn: Đảm bảo đồ thị không có chu trình
    if len(topo_order) != num_operations:
        raise ValueError("Đồ thị chứa chu trình, không thể giải quyết!")

    # Bước 3: Lập lịch tham lam (Greedy Scheduling)
    machine_ready_time = {m: 0 for m in range(num_machines)}
    op_completion_time = {i: 0 for i in range(num_operations)}
    
    for op in topo_order:
        # Thời điểm sớm nhất thao tác này có thể bắt đầu (sau khi các thao tác trước đã xong)
        earliest_start = 0
        if predecessors[op]:
            earliest_start = max(op_completion_time[p] for p in predecessors[op])
            
        best_completion = float('inf')
        best_machine = -1
        
        # Duyệt qua các máy có thể xử lý thao tác này
        for machine, proc_time in request_list[op].items():
            # Thời điểm thực tế có thể bắt đầu trên máy này
            actual_start = max(earliest_start, machine_ready_time[machine])
            completion = actual_start + proc_time
            
            # Tham lam: Chọn máy giúp thao tác hoàn thành sớm nhất
            if completion < best_completion:
                best_completion = completion
                best_machine = machine
                
        # Cập nhật thời gian rảnh của máy và thời gian hoàn thành của thao tác
        machine_ready_time[best_machine] = best_completion
        op_completion_time[op] = best_completion

    # Bước 4: UB chính là thời điểm hoàn thành của thao tác muộn nhất
    ub = max(op_completion_time.values())
    return ub
def create_var(num_operations, num_machines, request_list, size_time):
    s={}
    counter = 0
    for i in range(num_operations):
        for t in range(size_time + 1):
            counter += 1
            s[(i,t)] = counter

    x = {}
    for i in range(num_operations):
        for t in range(size_time + 1):
            counter += 1
            x[(i,t)] = counter
    
    m = {}
    for i in range(num_operations):
        for a, process_time in request_list[i].items():
            counter += 1
            m[(i, a)] = counter
    
    a = {}
    for i in range(num_operations):
        for t in range(size_time + 1):
            counter += 1
            a[(i,t)] = counter

    return s, x, m, a, counter    

def build_constraints(solver, num_operations, num_machines, precedence_list, request_list, size_time, s, x, m, a, top_id):
    # (4) tạo dãy order
    for i in range(num_operations):
        for t in range(size_time):
            solver.add_clause([-x[(i,t+1)], x[(i,t)]])
    
    #(5) link s và x
    for i in range(num_operations):
        solver.add_clause([x[(i,0)]])
        for t in range(size_time):
            solver.add_clause([-s[(i,t)], x[(i,t)]])
            solver.add_clause([-s[(i,t)], -x[(i,t+1)]])
            solver.add_clause([-x[(i,t)], x[(i,t+1)], s[(i,t)]])
        # t = size_time
        solver.add_clause([-s[(i,size_time)], x[(i,size_time)]])
        solver.add_clause([s[(i,size_time)], -x[(i,size_time)]])

    #(6) ràng buộc thứ tự ưu tiên
    for i,j in precedence_list:
        processing = request_list[i]
        for machine, process_time in processing.items():
            for t in range(size_time + 1):
                if t + process_time <= size_time:
                    solver.add_clause([-s[(i,t)], -m[(i,machine)], x[(j,t+process_time)]])
                else:
                    break

    # (7) exactly one machine per operation
    for i in range(num_operations):
        machines= request_list[i].keys()
        enc = CardEnc.equals(lits=[m[(i,machine)] for machine in machines], bound=1, encoding=1, top_id=top_id)
        top_id = enc.nv
        solver.append_formula(enc.clauses)

    # liên kết trạng thái active 
    for i in range(num_operations):
        processing = dict(sorted(request_list[i].items(), key=lambda x: x[1]))
        first = 1
        for machine, process_time in processing.items():
            if first == 1:
                first_process_time = process_time
                first = 0
                for t in range(size_time + 1):
                    for delta in range(first_process_time):
                        if t + delta <= size_time:
                            solver.add_clause([-s[(i,t)], a[(i,t+delta)]]) #(8)
                        else:
                            break
            else:
                for t in range(size_time + 1):
                    for delta in range(first_process_time, process_time):
                        if t + delta <= size_time:
                            solver.add_clause([-s[(i,t)], -m[(i,machine)], a[(i,t+delta)]]) #(9)
                        else:
                            break
    
    # (10) 
    for i in range(num_operations):
        for t in range(size_time):
            solver.add_clause([-a[(i,t)], -x[(i,t+1)]])

    #(11)
    for i in range(num_operations):
        processing_i = request_list[i]
        for j in range(i+1, num_operations):
            processing_j = request_list[j]
            for machine_i in processing_i.keys():
                for machine_j in processing_j.keys():
                    if machine_i == machine_j:
                        for t in range(size_time + 1):
                            solver.add_clause([-m[(i,machine_i)], -m[(j,machine_j)], -a[(i,t)], -a[(j,t)]]) #(11)                    
            
        
def add_incremental_constraints(solver, num_operations, out_degree, request_list, ub, s, x, m, a):
    # (12) Giới hạn makespan cho toàn bộ thao tác, không chỉ các thao tác cuối.
    # Nếu một máy không thể hoàn thành thao tác trước hoặc tại ub, cấm gán máy đó.
    last_ops = [i for i in range(num_operations) if out_degree[i] == 0]
    for i in last_ops:
    # for i in range(num_operations):
        for machine, process_time in request_list[i].items():
            limit_time = ub - process_time
            if limit_time >= 0:
                solver.add_clause([-m[(i, machine)], -x[(i, limit_time + 1)]])
            else:
                solver.add_clause([-m[(i, machine)]])

def solve_and_print(solver, num_operations, s, m, request_list):
    if solver.solve():
        print("SAT")
        model = solver.get_model()
        
        # Chuyển model thành set chứa các biến (literals) có giá trị True (số dương)
        positive_lits = set(model)
        
        machine_assignment = {}
        start_times = {}
        
        # 1. Trích xuất Máy được gán cho mỗi thao tác
        for (i, machine), lit in m.items():
            if lit in positive_lits:
                machine_assignment[i] = machine
                
        # 2. Trích xuất Thời điểm bắt đầu của mỗi thao tác
        for (i, t), lit in s.items():
            if lit in positive_lits:
                start_times[i] = t
                
        # 3. Tạo hàng đợi và tính Makespan (UB)
        machine_queues = {}
        makespan = 0  # Biến lưu thời gian hoàn thành cuối cùng
        
        for i in range(num_operations):
            assigned_machine = machine_assignment[i]
            start_t = start_times[i]
            process_time = request_list[i][assigned_machine]
            end_t = start_t + process_time
            
            # Cập nhật makespan nếu end_t của thao tác hiện tại lớn hơn
            if end_t > makespan:
                makespan = end_t
            
            if assigned_machine not in machine_queues:
                machine_queues[assigned_machine] = []
                
            # Lưu trữ theo tuple: (Thời điểm bắt đầu, Thời điểm kết thúc, ID thao tác)
            machine_queues[assigned_machine].append((start_t, end_t, i))
            
        # Sắp xếp hàng đợi trên mỗi máy theo thời gian bắt đầu
        for machine in machine_queues:
            machine_queues[machine].sort()
            
        # --- IN KẾT QUẢ ---
        # print("\n--- CHI TIẾT GÁN MÁY ---")
        # for i in range(num_operations):
        #     print(f"Thao tác {i:2d}: Chạy trên Máy {machine_assignment[i]}, Từ t = {start_times[i]} đến t = {start_times[i] + request_list[i][machine_assignment[i]]}")
            
        # print("\n--- HÀNG ĐỢI TRÊN TỪNG MÁY ---")
        # for machine, queue in sorted(machine_queues.items()):
        #     # Định dạng chuỗi cho đẹp: Op i [start -> end]
        #     queue_str = "  ->  ".join([f"Op {op} [{st}->{en}]" for st, en, op in queue])
        #     print(f"Máy {machine}: {queue_str}")
            
        print(f"\n=> THỜI GIAN HOÀN THÀNH TỔNG (Makespan / UB): {makespan}")
            
        # Trả về thêm makespan (ub) ở vị trí thứ 4
        return machine_assignment, start_times, machine_queues, makespan
        
    else:
        print("UNSAT")
        print(f"status: optimal")
        return None, None, None, None
    


def verify_schedule(num_operations, num_machines, precedence_list, request_list, machine_assignment, queue, expected_ub):
    """
    Hàm kiểm tra tính hợp lệ của lịch trình sinh ra từ thuật toán Greedy.
    """
    # 1. Kiểm tra tính hợp lệ của việc gán máy
    for i in range(num_operations):
        assigned_machine = machine_assignment.get(i)
        if assigned_machine is None:
            return False, f"LỖI: Thao tác {i} chưa được gán máy!"
        if assigned_machine not in request_list[i]:
            return False, f"LỖI: Thao tác {i} được gán cho máy {assigned_machine} không có trong request_list!"

    # 2. Kiểm tra tính hợp lệ của chuỗi Topological (Queue)
    if len(queue) != num_operations:
        return False, f"LỖI: Số lượng thao tác trong queue ({len(queue)}) không khớp với tổng số thao tác ({num_operations})!"
        
    pos = {op: idx for idx, op in enumerate(queue)}
    for u, v in precedence_list:
        if pos[u] >= pos[v]:
            return False, f"LỖI RÀNG BUỘC: Thao tác {u} phải xong trước {v} nhưng lại xếp sau trong queue!"

    # 3. Mô phỏng lại lịch trình để kiểm tra thời gian
    machine_ready_time = {m: 0 for m in range(num_machines)}
    op_completion_time = {i: 0 for i in range(num_operations)}
    
    predecessors = {i: [] for i in range(num_operations)}
    for u, v in precedence_list:
        predecessors[v].append(u)

    for curr in queue:
        machine = machine_assignment[curr]
        proc_time = request_list[curr][machine]

        # Thời gian nguyên liệu đến từ các công đoạn trước
        earliest_start = 0
        if predecessors[curr]:
            earliest_start = max(op_completion_time[p] for p in predecessors[curr])

        # Máy rảnh VÀ nguyên liệu đã đến
        actual_start = max(machine_ready_time[machine], earliest_start)
        completion = actual_start + proc_time

        # Cập nhật thời gian
        machine_ready_time[machine] = completion
        op_completion_time[curr] = completion

    # 4. Đối chiếu Makespan (UB)
    actual_ub = max(machine_ready_time.values())
    if actual_ub > expected_ub:
        return False, f"LỖI MAKESPAN: UB dự kiến là {expected_ub}, nhưng tính toán lại ra {actual_ub}!"

    return True



def main():
    file_path = sys.argv[1]
    num_operations, num_edges, num_machines, precedence_list, request_list = read_file(file_path)

    # size_time = calculate_greedy_ub(num_operations, num_machines, precedence_list, request_list)
    # print(f"Greedy Upper Bound (UB): {size_time}")

    in_degree, out_degree, neighbors, predecessors = data(num_operations, num_edges, num_machines, precedence_list, request_list)
    ub, assignment, queue = greedy_schedule(num_operations, num_machines, precedence_list, request_list, in_degree, neighbors, predecessors)
    if verify_schedule(num_operations, num_machines, precedence_list, request_list, assignment, queue, ub):
        print(f"Greedy UB {ub} is valid!")
    else:
        print(f"Greedy UB {ub} is NOT valid!")
        return
    s, x, m, a, top_id = create_var(num_operations, num_machines, request_list, ub)

    start_time = perf_counter()
    solver = Solver(name = 'cadical195')
    build_constraints(solver, num_operations, num_machines, precedence_list, request_list, ub, s, x, m, a, top_id)
    print(f"Building constraints took {perf_counter() - start_time:.2f} seconds.")

    while True:
        add_incremental_constraints(solver, num_operations, out_degree, request_list, ub, s, x, m, a)
        machine_assignment, start_times, machine_queues, makespan = solve_and_print(solver, num_operations, s, m, request_list)
        if machine_assignment is None:
            break  # Không thể giảm UB nữa

        if verify_schedule(num_operations, num_machines, precedence_list, request_list, machine_assignment, queue, ub):
            print(f"UB {ub} is valid!")
            print(f"Time taken for UB {ub}: {perf_counter() - start_time:.2f} seconds.")
        else:
            print(f"UB {ub} is NOT valid!")
            break

        # Tìm nghiệm tốt hơn ở vòng lặp tiếp theo.
        ub = makespan - 1
if __name__ == "__main__":
    main()