
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

def data(num_operations, precedence_list):
    in_degree = {i: 0 for i in range(num_operations)}
    out_degree = {i: 0 for i in range(num_operations)}
    neighbors = {i: [] for i in range(num_operations)}
    predecessors = {i: [] for i in range(num_operations)}

    for u, v in precedence_list:
        in_degree[v] += 1
        out_degree[u] += 1
        neighbors[u].append(v)
        predecessors[v].append(u)

    return in_degree, out_degree, neighbors, predecessors

def greedy_schedule(num_operations, num_machines, request_list, in_degree, neighbors, predecessors):
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
def create_var(num_operations, request_list, size_time):
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
    

    return s, x, m, counter    

def build_constraints(solver, num_operations, precedence_list, request_list, size_time, s, x, m, top_id):
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
        # print(f"Adding precedence constraint: Op {i} -> Op {j}")
        processing = request_list[i]
        for machine, process_time in processing.items():
            for t in range(size_time + 1):
                if t + process_time <= size_time:
                    solver.add_clause([-s[(i,t)], -m[(i,machine)], x[(j,t+process_time)]])
                else:
                    solver.add_clause([-s[(i,t)], -m[(i,machine)]])

    # (7) exactly one machine per operation
    for i in range(num_operations):
        machines= request_list[i].keys()
        enc = CardEnc.equals(lits=[m[(i,machine)] for machine in machines], bound=1, encoding=1, top_id=top_id)
        top_id = enc.nv
        solver.append_formula(enc.clauses)


    # #(11)
    for i in range(num_operations):
        for j in range(i+1, num_operations):
            common_machines = set(request_list[i].keys()).intersection(set(request_list[j].keys()))
            for machine in common_machines:
                p_i = request_list[i][machine]
                p_j = request_list[j][machine]

                for t_i in range(size_time + 1):

                    start = t_i - p_j # Biên time bên trái
                    end   = t_i + p_i # Biên time bên phải

                    clause = [
                        -m[(i, machine)],
                        -m[(j, machine)],
                        -s[(i, t_i)]
                    ]

                    # xử lý biên trái
                    if start > 0:
                        clause.append(-x[(j, start + 1)])
                    # nếu start <= 0 thì luôn thỏa → không cần thêm

                    # xử lý biên phải
                    if end <= size_time:
                        clause.append(x[(j, end)])
                    # nếu end >= size_time thì luôn thỏa

                    solver.add_clause(clause)

                    
        
def add_incremental_constraints(solver, num_operations, out_degree, request_list, ub, s, x, m):
    # (12) Giới hạn makespan cho toàn bộ thao tác, không chỉ các thao tác cuối.
    # Nếu một máy không thể hoàn thành thao tác trước hoặc tại ub, cấm gán máy đó.
    last_ops = [i for i in range(num_operations) if out_degree[i] == 0]
    # print(f"Adding incremental constraints for UB = {ub} on last operations: {last_ops}")
    for i in last_ops:
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
                if machine_assignment.get(i) is not None:
                    raise ValueError(f"Cảnh báo: Thao tác {i} đã được gán máy {machine_assignment[i]} trước đó, nhưng giờ lại được gán máy {machine}.")
                machine_assignment[i] = machine
                
        # 2. Trích xuất Thời điểm bắt đầu của mỗi thao tác
        for (i, t), lit in s.items():
            if lit in positive_lits:
                if start_times.get(i) is not None:
                    raise ValueError(f"Cảnh báo: Thao tác {i} đã có thời điểm bắt đầu {start_times[i]} trước đó, nhưng giờ lại có thời điểm bắt đầu {t}.")
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
    


def verify_schedule(num_operations, num_machines, precedence_list,
                    request_list, machine_assignment, start_times):

    """
    Verify schedule từ SAT model (KHÔNG dùng greedy queue)
    """

    # 1. Kiểm tra mỗi operation có đúng 1 machine
    for i in range(num_operations):
        if i not in machine_assignment:
            print(f"Op {i} chưa được gán máy")
            return False

        machine = machine_assignment[i]
        if machine not in request_list[i]:
            print(f"Op {i} gán máy {machine} không hợp lệ")
            return False

    # 2. Kiểm tra mỗi operation có đúng 1 start time
    for i in range(num_operations):
        if i not in start_times:
            print(f"Op {i} chưa có start time")
            return False

    # 3. Tính lại schedule thực tế (resolve conflict + precedence)
    machine_ready_time = {m: 0 for m in range(num_machines)}
    op_completion_time = {}

    # build predecessors
    predecessors = {i: [] for i in range(num_operations)}
    for u, v in precedence_list:
        predecessors[v].append(u)

    # sort theo start time từ SAT
    order = sorted(range(num_operations), key=lambda i: start_times[i])

    for i in order:
        machine = machine_assignment[i]
        proc_time = request_list[i][machine]

        # precedence constraint
        earliest_start = 0
        if predecessors[i]:
            for p in predecessors[i]:
                if p not in op_completion_time:
                    print(f"Op {i} có predecessor {p} chưa hoàn thành")
                    return False
            earliest_start = max(op_completion_time[p] for p in predecessors[i])

        # machine availability
        actual_start = max(start_times[i], machine_ready_time[machine], earliest_start)
        completion = actual_start + proc_time

        # cập nhật
        machine_ready_time[machine] = completion
        op_completion_time[i] = completion

    # 4. kiểm tra overlap trực tiếp (strong check)
    machine_usage = {m: [] for m in range(num_machines)}

    for i in range(num_operations):
        m = machine_assignment[i]
        st = start_times[i]
        pt = request_list[i][m]
        en = st + pt
        machine_usage[m].append((st, en, i))

    for m in machine_usage:
        intervals = sorted(machine_usage[m])
        for k in range(len(intervals) - 1):
            st1, en1, i1 = intervals[k]
            st2, en2, i2 = intervals[k+1]
            if en1 > st2:
                print(f"Machine {m} bị overlap giữa op {i1} (từ {st1} đến {en1}) và op {i2} (từ {st2} đến {en2})")
                return False

    # 5. kiểm tra precedence trực tiếp
    for u, v in precedence_list:
        mu = machine_assignment[u]
        mv = machine_assignment[v]

        end_u = start_times[u] + request_list[u][mu]
        start_v = start_times[v]

        if end_u > start_v:
            print(f"Vi phạm precedence: op {u} (kết thúc lúc {end_u}) phải trước op {v} (bắt đầu lúc {start_v})")
            return False

    # 6. makespan
    makespan = max(op_completion_time.values())

    return True



def main():
    start_time = perf_counter()
    file_path = sys.argv[1]
    num_operations, num_edges, num_machines, precedence_list, request_list = read_file(file_path)

    in_degree, out_degree, neighbors, predecessors = data(num_operations, precedence_list)
    size_time, assignment, queue = greedy_schedule(num_operations, num_machines, request_list, in_degree, neighbors, predecessors)
    ub = size_time - 1
    s, x, m, top_id = create_var(num_operations, request_list, ub)

    
    solver = Solver(name = 'cadical195')
    build_constraints(solver, num_operations, precedence_list, request_list, ub, s, x, m, top_id)
    print(f"Building constraints took {perf_counter() - start_time:.2f} seconds.")

    while True:
        add_incremental_constraints(solver, num_operations, out_degree, request_list, ub, s, x, m)
        machine_assignment, start_times, machine_queues, makespan = solve_and_print(solver, num_operations, s, m, request_list)
        if machine_assignment is None:
            break  # Không thể giảm UB nữa

        if not verify_schedule(num_operations, num_machines, precedence_list, request_list, machine_assignment, start_times):
            print("Schedule is not valid")
            return
        else:
            print("Schedule is valid")

        # Tìm nghiệm tốt hơn ở vòng lặp tiếp theo.
        ub = makespan - 1
        print(f" Time taken: {perf_counter() - start_time:.2f} seconds")
if __name__ == "__main__":
    main()