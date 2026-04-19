from collections import defaultdict, deque
import sys
import threading
from time import perf_counter
from pysat.solvers import Solver
from pysat.card import CardEnc

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

    in_degree_copy = in_degree.copy()

    queue = [i for i in range(num_operations) if in_degree_copy[i] == 0]
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
            in_degree_copy[neighbor] -= 1
            if in_degree_copy[neighbor] == 0:
                queue.append(neighbor)

    ub = max(machine_ready_time.values())
    print(f"Greedy Schedule UB: {ub}")

    return ub, machine_assignment, queue

def pre_processing_time(num_operations, precedence_list, out_degree, topo_queue, neighbors, request_list, ub):
    # Tính thời gian xử lý tối thiểu cho mỗi thao tác (dựa trên máy nhanh nhất)
    min_proc_time = {}
    for i in range(num_operations):
        min_proc_time[i] = min(request_list[i].values())
    # print(f"Minimum processing time for each operation: {min_proc_time}")
    
    # Tính thời gian sớm nhất thao tác có thể bắt đầu
    earliest_start = {i: 0 for i in range(num_operations)}
    for u in topo_queue:
        for v in neighbors[u]:
            earliest_start[v] = max(earliest_start[v], earliest_start[u] + min_proc_time[u])
    
    # Tính thời gian muộn nhất thao tác có thể bắt đầu
    latest_start = {i: ub - min_proc_time[i] if out_degree[i] == 0 else 0 for i in range(num_operations)}
    # print(f"lastest start 8 {latest_start[8]}")

    for u in reversed(topo_queue):
        for v in neighbors[u]:
            latest_start[u] = max(latest_start[u], latest_start[v] - min_proc_time[u])
    
    feasible_time = {}
    for i in range(num_operations):
        feasible_time[i] = (earliest_start[i], latest_start[i])
        if earliest_start[i] > latest_start[i]:
            print(f"Operation {i} cannot be scheduled (feasible time: {feasible_time[i]})")
            return None, False

    return feasible_time, True

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


def calculate_lower_bound(num_operations, num_machines, precedence_list, request_list):
    """
    Compute a valid makespan lower bound using three relaxations:
    1) precedence-only critical path with min processing times,
    2) average load over all machines,
    3) mandatory machine load from operations that have only one eligible machine.
    """
    min_proc_time = {i: min(request_list[i].values()) for i in range(num_operations)}

    # Build precedence graph.
    indegree = [0] * num_operations
    successors = [[] for _ in range(num_operations)]
    for u, v in precedence_list:
        successors[u].append(v)
        indegree[v] += 1

    # Topological order for longest path in DAG with node weights min_proc_time.
    queue = deque(i for i in range(num_operations) if indegree[i] == 0)
    topo = []
    while queue:
        u = queue.popleft()
        topo.append(u)
        for v in successors[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    if len(topo) != num_operations:
        raise ValueError("Precedence graph contains a cycle")

    longest_finish = [0] * num_operations
    for u in topo:
        if longest_finish[u] == 0:
            longest_finish[u] = min_proc_time[u]
        for v in successors[u]:
            cand = longest_finish[u] + min_proc_time[v]
            if cand > longest_finish[v]:
                longest_finish[v] = cand
    lb_precedence = max(longest_finish) if longest_finish else 0

    # Load-based lower bound from total minimum workload.
    total_min_work = sum(min_proc_time.values())
    lb_avg_load = (total_min_work + num_machines - 1) // num_machines

    # Mandatory load per machine (operations with exactly one eligible machine).
    mandatory_load = [0] * num_machines
    for i in range(num_operations):
        if len(request_list[i]) == 1:
            machine, p_time = next(iter(request_list[i].items()))
            mandatory_load[machine] += p_time
    lb_mandatory = max(mandatory_load) if mandatory_load else 0

    lb = max(lb_precedence, lb_avg_load, lb_mandatory)
    print(
        f"Lower Bound: {lb} "
        f"(precedence={lb_precedence}, avg_load={lb_avg_load}, mandatory={lb_mandatory})"
    )
    return lb

def create_var(num_operations, request_list, feasible_time):
    s={}
    x={}
    m={}
    counter = 0
    for i in range(num_operations):
        for t in range(feasible_time[i][0], feasible_time[i][1] + 1):
            counter += 1
            s[(i,t)] = counter
            counter += 1
            x[(i,t)] = counter
        for a, process_time in request_list[i].items():
            counter += 1
            m[(i, a)] = counter
    

    return s, x, m, counter    

def build_constraints(solver, num_operations, precedence_list, request_list, feasible_time, s, x, m, top_id):
    # (4) tạo dãy order
    for i in range(num_operations):

        # exactly one
        machines= request_list[i].keys()
        enc = CardEnc.equals(lits=[m[(i,machine)] for machine in machines], bound=1, encoding=1, top_id=top_id)
        top_id = enc.nv
        solver.append_formula(enc.clauses)

        # Create first bit of order
        solver.add_clause([x[(i,feasible_time[i][0])]])
        for t in range(feasible_time[i][0], feasible_time[i][1]):
            # (4) Tạo dãy order
            solver.add_clause([-x[(i,t+1)], x[(i,t)]]) 
            # (5) Link s và x
            solver.add_clause([-s[(i,t)], x[(i,t)]])
            solver.add_clause([-s[(i,t)], -x[(i,t+1)]])
            solver.add_clause([-x[(i,t)], x[(i,t+1)], s[(i,t)]])
        # t = feasible_time[i][1]
        solver.add_clause([-s[(i,feasible_time[i][1])], x[(i,feasible_time[i][1])]])
        solver.add_clause([s[(i,feasible_time[i][1])], -x[(i,feasible_time[i][1])]])

        # ràng buộc chống overlap
        for j in range(i+1, num_operations):
            if (i,j) in precedence_list or (j,i) in precedence_list:
                continue
            common_machines = set(request_list[i].keys()).intersection(set(request_list[j].keys()))
            for machine in common_machines:
                p_i = request_list[i][machine]
                p_j = request_list[j][machine]

                for t_i in range(feasible_time[i][0], feasible_time[i][1] + 1):

                    start = t_i - p_j # Biên time bên trái
                    end   = t_i + p_i # Biên time bên phải

                    clause = [
                        -m[(i, machine)],
                        -m[(j, machine)],
                        -s[(i, t_i)]
                    ]

                    # Nếu end < ES_j: j chắc chắn bắt đầu sau end -> Mệnh đề luôn ĐÚNG
                    if end <= feasible_time[j][0]:
                        continue

                    # Nếu start + 1 > LS_j: j chắc chắn bắt đầu trước start -> Mệnh đề luôn ĐÚNG
                    if start  >= feasible_time[j][1]:
                        continue

                    # xử lý biên trái
                    if start >= feasible_time[j][0]:
                        clause.append(-x[(j, start + 1)])

                    # xử lý biên phải
                    if end <= feasible_time[j][1]:
                        clause.append(x[(j, end)])

                    # nếu end >= feasible_time[j][1] thì luôn thỏa
                    solver.add_clause(clause)
    

            
        

    #(6) ràng buộc thứ tự ưu tiên
    for i,j in precedence_list:
        # print(f"Adding precedence constraint: Op {i} -> Op {j}")
        processing = request_list[i]
        for machine, process_time in processing.items():
            for t in range(feasible_time[i][0], feasible_time[i][1] + 1):
                finish_i = t + process_time
                
                if finish_i > feasible_time[j][1]:
                    # i kết thúc muộn hơn cả thời điểm muộn nhất j có thể bắt đầu -> Vô lý
                    solver.add_clause([-s[(i, t)], -m[(i, machine)]])
                elif finish_i > feasible_time[j][0]:
                    # i kết thúc trong khoảng [ES_j, LS_j] -> j phải bắt đầu >= finish_i
                    solver.add_clause([-s[(i, t)], -m[(i, machine)], x[(j, finish_i)]])
        

                    
        
def add_incremental_constraints(solver, num_operations, out_degree, request_list, expected_makespan, x, m, feasible_time):
    # (12) Giới hạn makespan cho toàn bộ thao tác, không chỉ các thao tác cuối.
    # Nếu một máy không thể hoàn thành thao tác trước hoặc tại expected_makespan, cấm gán máy đó.
    last_ops = [i for i in range(num_operations) if out_degree[i] == 0]
    # print(f"Adding incremental constraints for UB = {expected_makespan} on last operations: {last_ops}")
    for i in last_ops:
        for machine, process_time in request_list[i].items():
            limit_time = expected_makespan - process_time
            if limit_time < feasible_time[i][0] :
                solver.add_clause([-m[(i, machine)]]) 
            elif limit_time < feasible_time[i][1]:
                solver.add_clause([-m[(i, machine)], -x[(i, limit_time + 1)]])

def init_solver(solver, num_operations, precedence_list, request_list, out_degree, queue, neighbors, expected_makespan):
    feasible_time, is_feasible = pre_processing_time(num_operations, precedence_list, out_degree, queue, neighbors, request_list, expected_makespan)
    if not is_feasible:
        print(f"No feasible solution found with UB = {expected_makespan} during pre-processing.")
        return False, None, None, None, None
    s, x, m, top_id = create_var(num_operations, request_list, feasible_time)
    build_constraints(solver, num_operations, precedence_list, request_list, feasible_time, s, x, m, top_id)
    add_incremental_constraints(solver, num_operations, out_degree, request_list, expected_makespan, x, m, feasible_time)
    return True, s, x, m, feasible_time
# ==============================================================================
# KHU VỰC 2: CÁC LUỒNG TÌM KIẾM (WORKERS)
# ==============================================================================

# --- THREAD 1: BOTTOM-UP (RE-INIT, CÓ BỊ NGẮT) ---
def worker_bottom_up(shared_state, lock, stop_event, num_operations, precedence_list, request_list, out_degree, queue, neighbors, start_time):
    name = "BottomUp"
    while not stop_event.is_set():
        with lock: lb, ub = shared_state['lb'], shared_state['ub']
        if lb > ub: break
        if stop_event.is_set(): break
        print(f"[{name}] Trying with at most {lb}, LB = {lb}, UB = {ub}")
        solver = Solver(name='cadical195') 
        init_success, s, x, m, feasible_time = init_solver(solver, num_operations, precedence_list, request_list, out_degree, queue, neighbors, lb)

        if not init_success:
            with lock:
                if lb >= shared_state['lb']: shared_state['lb'] = lb + 1
            solver.delete(); continue
        if stop_event.is_set(): break
        with lock: shared_state['active_solvers'][name] = solver
        is_sat = solver.solve()
        with lock: shared_state['active_solvers'].pop(name, None)

        if stop_event.is_set(): solver.delete(); break
        if stop_event.is_set(): break
        if is_sat is True:
            # BOTTOM-UP TÌM THẤY NGHIỆM -> LÀ OPTIMAL
            with lock:
                if shared_state['status'] != 'Optimal':
                    print(f"[{name}] SAT in {lb}! FOUND OPTIMAL.")
                    print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
                    shared_state['ub'] = lb - 1
                    shared_state['best_makespan'] = lb
                    shared_state['status'] = 'Optimal'
                    shared_state['proved_by'] = name
                    stop_event.set() # Ngắt toàn cục
                    for n, s_obj in shared_state['active_solvers'].items(): s_obj.interrupt()
        elif is_sat is False:
            with lock:
                print(f"[{name}] UNSAT in {lb}. Incrementing LB.")
                print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
                if lb >= shared_state['lb']:
                    shared_state['lb'] = lb + 1
                    # Kiểm tra chéo nếu lb vượt ub
                    if shared_state['lb'] > shared_state['ub'] and shared_state['status'] != 'Optimal':
                        shared_state['status'] = 'Optimal'
                        shared_state['proved_by'] = name
                        stop_event.set()
                    for n, s_obj in shared_state['active_solvers'].items():
                        if n == "CoopBinary":
                            s_obj.interrupt()
                print(f"Current bounds: LB = {shared_state['lb']}, UB = {shared_state['ub']}")
        solver.delete()


# --- THREAD 2: TOP-DOWN ---
def worker_top_down(shared_state, lock, stop_event, num_operations, precedence_list, request_list, out_degree, queue, neighbors, start_time):
    name = "TopDown"
    with lock: ub = shared_state['ub']
    
    solver = Solver(name='cadical195')
    print(f"[{name}] Trying with at most {ub}, LB = {shared_state['lb']}, UB = {shared_state['ub']}")
    init_success, s, x, m, feasible_time = init_solver(solver, num_operations, precedence_list, request_list, out_degree, queue, neighbors, ub)

    while not stop_event.is_set():
        if stop_event.is_set(): break
        with lock: lb, ub = shared_state['lb'], shared_state['ub']
        if lb > ub: break
        add_incremental_constraints(solver, num_operations, out_degree, request_list, ub, x, m, feasible_time)
        if stop_event.is_set(): break
        with lock: shared_state['active_solvers'][name] = solver
        is_sat = solver.solve()
        with lock: shared_state['active_solvers'].pop(name, None)

        if stop_event.is_set(): break

        if is_sat is True:
            with lock:
                print(f"[{name}] SAT in {ub}! Updating UB.")
                print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
                if ub <= shared_state['ub']:
                    shared_state['ub'] = ub - 1
                    shared_state['best_makespan'] = ub
                    
                    # Kiểm tra chéo nếu ub tụt xuống dưới lb
                    if shared_state['lb'] > shared_state['ub'] and shared_state['status'] != 'Optimal':
                        shared_state['status'] = 'Optimal'
                        shared_state['proved_by'] = name
                        stop_event.set()
                    for n, s_obj in shared_state['active_solvers'].items():
                        if n == "CoopBinary":
                            s_obj.interrupt()
                print(f"Current bounds: LB = {shared_state['lb']}, UB = {shared_state['ub']}")
        elif is_sat is False:
            # TOP-DOWN ĐỤNG UNSAT -> LÀ OPTIMAL
            with lock:
                if shared_state['status'] != 'Optimal':
                    print(f"[{name}]  UNSAT in {ub}. FOUND OPTIMAL.")
                    print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
                    shared_state['status'] = 'Optimal'
                    shared_state['proved_by'] = name
                    stop_event.set() # Ngắt toàn cục
                    for n, s_obj in shared_state['active_solvers'].items(): s_obj.interrupt()
            break
    solver.delete()


# --- THREAD 3: INDEPENDENT BINARY SEARCH (INC/RE-INIT, KHÔNG BỊ NGẮT) ---
def worker_independent_binary(shared_state, lock, stop_event, num_operations, precedence_list, request_list, out_degree, queue, neighbors, start_time):
    name = "IndepBinary"
    solver = None
    last_target = float('inf')
    s, x, m, feasible_time = None, None, None, None

    while not stop_event.is_set():
        # Đọc bounds để tính target
        with lock: 
            lb, ub = shared_state['lb'], shared_state['ub']
        
        if lb > ub: 
            break
            
        target = (lb + ub) // 2
        print(f"[{name}] New iteration with LB = {lb}, UB = {ub}, Target = {target}")
        # QUYẾT ĐỊNH: RE-INIT HOẶC INCREMENTAL
        if solver is not None and target < last_target:
            # print(f"[{name}] ♻️ Incremental (Indep): Target {target}")
            add_incremental_constraints(solver, num_operations, out_degree, request_list, target, x, m, feasible_time)
        else:
            # print(f"[{name}] 🔄 Re-init (Indep): Target {target}")
            if solver: 
                solver.delete()
            solver = Solver(name='cadical195') # Sử dụng Cadical 1.9.5
            init_success, s, x, m, feasible_time = init_solver(solver, num_operations, precedence_list, request_list, out_degree, queue, neighbors, target)
            
            if not init_success:
                # Xử lý nhanh trường hợp vô nghiệm từ lúc khởi tạo
                with lock:
                    if target >= shared_state['lb']: 
                        shared_state['lb'] = target + 1
                        # Kiểm tra Optimal
                        if shared_state['lb'] > shared_state['ub'] and shared_state['status'] != 'Optimal':
                            print(f"[{name}] UB < LB when init. FOUND OPTIMAL.")
                            shared_state['status'] = 'Optimal'
                            shared_state['proved_by'] = name
                            stop_event.set()
                solver.delete()
                solver = None
                last_target = float('inf')
                continue
        if stop_event.is_set(): break
        # ĐỘC LẬP: Không đưa solver này vào shared_state['active_solvers'].
        # Nó sẽ lầm lũi giải cho đến khi xong, không ai ngắt được nó!
        is_sat = solver.solve()

        # Nếu có luồng khác đã báo dừng hệ thống trong lúc nó giải thì thoát
        if stop_event.is_set(): 
            break

        # XỬ LÝ KẾT QUẢ VÀ KIỂM TRA OPTIMAL
        if is_sat is True:
            with lock:
                if target < shared_state['ub']:
                    shared_state['ub'] = target - 1
                    shared_state['best_makespan'] = target
                    print(f"[{name}] SAT in {target}! Updating UB.")
                    print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
                    # Kiểm tra Optimal (UB < LB)
                    if shared_state['lb'] > shared_state['ub'] and shared_state['status'] != 'Optimal':
                        print(f"[{name}] UB < LB => OPTIMAL")
                        shared_state['status'] = 'Optimal'
                        shared_state['proved_by'] = name
                        stop_event.set()
                    print(f"Current bounds: LB = {shared_state['lb']}, UB = {shared_state['ub']}")    
                    # Dù nó độc lập, nó VẪN CÓ QUYỀN bắn ngắt các luồng khác
                    for n, s_obj in shared_state['active_solvers'].items(): 
                        s_obj.interrupt()
                        if stop_event.is_set(): break
            last_target = target # Lưu lại để vòng sau có thể Incremental

        elif is_sat is False:
            with lock:
                print(f"[{name}] UNSAT in {target}. Incrementing LB.")
                print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
                if target >= shared_state['lb']:
                    shared_state['lb'] = target + 1
                    
                    # Kiểm tra Optimal (UB < LB)
                    if shared_state['lb'] > shared_state['ub'] and shared_state['status'] != 'Optimal':
                        print(f"[{name}] UB < LB => OPTIMAL")
                        shared_state['status'] = 'Optimal'
                        shared_state['proved_by'] = name
                        stop_event.set()
                        
                    # Bắn ngắt các luồng khác vì LB đã thay đổi
                    for n, s_obj in shared_state['active_solvers'].items(): 
                        s_obj.interrupt()
                print(f"Current bounds: LB = {shared_state['lb']}, UB = {shared_state['ub']}")
                        
            # Bị UNSAT ở mốc này thì solver hiện tại vô dụng với mốc cao hơn -> Xóa, vòng sau Re-init
            solver.delete()
            solver = None
            last_target = float('inf')
        if stop_event.is_set(): break
    # Dọn dẹp trước khi thoát luồng
    if solver: 
        solver.delete()


# --- THREAD 4: COOPERATIVE BINARY (INC/RE-INIT, CÓ BỊ NGẮT) ---
def worker_cooperative_binary(shared_state, lock, stop_event, num_operations, precedence_list, request_list, out_degree, queue, neighbors, start_time):
    name = "CoopBinary"
    solver = None
    last_target = float('inf')
    s, x, m, feasible_time = None, None, None, None

    while not stop_event.is_set():
        with lock: lb, ub = shared_state['lb'], shared_state['ub']
        if lb > ub: break
        target = (lb + ub) // 2
        print(f"[{name}] New iteration with LB = {lb}, UB = {ub}, Target = {target}")
        if solver is not None and target < last_target:
            add_incremental_constraints(solver, num_operations, out_degree, request_list, target, x, m, feasible_time)
        else:
            if solver: solver.delete()
            solver = Solver(name='cadical195')
            init_success, s, x, m, feasible_time = init_solver(solver, num_operations, precedence_list, request_list, out_degree, queue, neighbors, target)
            if not init_success:
                with lock:
                    if target >= shared_state['lb']: shared_state['lb'] = target + 1
                solver.delete(); solver = None; last_target = float('inf'); continue
        if stop_event.is_set(): break
        with lock: shared_state['active_solvers'][name] = solver
        is_sat = solver.solve()
        with lock: shared_state['active_solvers'].pop(name, None)

        if stop_event.is_set(): break

        if is_sat is True:
            with lock:
                print(f"[{name}] SAT in {target}! Updating UB.")
                print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
                if target <= shared_state['ub']:
                    shared_state['ub'] = target - 1
                    shared_state['best_makespan'] = target
                    # BINARY SEARCH: NẾU UB < LB -> OPTIMAL
                    if shared_state['lb'] > shared_state['ub'] and shared_state['status'] != 'Optimal':
                        print(f"[{name}] UB < LB => OPTIMAL")
                        shared_state['status'] = 'Optimal'
                        shared_state['proved_by'] = name
                        stop_event.set()
                    for n, s_obj in shared_state['active_solvers'].items(): s_obj.interrupt()
                print(f"Current bounds: LB = {shared_state['lb']}, UB = {shared_state['ub']}")
            last_target = target

        elif is_sat is False:
            with lock:
                print(f"[{name}] UNSAT in {target}. Incrementing LB.")
                print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
                if target >= shared_state['lb']:
                    shared_state['lb'] = target + 1
                    # BINARY SEARCH: NẾU UB < LB -> OPTIMAL
                    if shared_state['lb'] > shared_state['ub'] and shared_state['status'] != 'Optimal':
                        print(f"[{name}] UB < LB => OPTIMAL")
                        shared_state['status'] = 'Optimal'
                        shared_state['proved_by'] = name
                        stop_event.set()
                    for n, s_obj in shared_state['active_solvers'].items(): s_obj.interrupt()
                print(f"Current bounds: LB = {shared_state['lb']}, UB = {shared_state['ub']}")
            solver.delete(); solver = None; last_target = float('inf')

    if solver: solver.delete()


# ==============================================================================
# KHU VỰC 3: HÀM MAIN (KHỞI TẠO TÀI NGUYÊN VÀ ĐIỀU PHỐI)
# ==============================================================================
def main():
    if len(sys.argv) < 2:
        print("Sử dụng: python3 script.py <file_path>")
        sys.exit(1)

    start_time = perf_counter()
    file_path = sys.argv[1]
    
    print(f"Loading data từ: {file_path}")
    num_operations, num_edges, num_machines, precedence_list, request_list = read_file(file_path)
    in_degree, out_degree, neighbors, predecessors = data(num_operations, precedence_list)
    
    # Lấy nghiệm tham lam làm Upper Bound
    size_time, assignment, queue = greedy_schedule(num_operations, num_machines, request_list, in_degree, neighbors, predecessors)
    
    # Tính toán Lower Bound
    lb_initial = calculate_lower_bound(num_operations, num_machines, precedence_list, request_list)
    ub = size_time - 1
    print(f"Complete preprocessing! Greedy UB = {size_time}")
    print(f"Initial UB = {ub}, LB = {lb_initial}")
    
    
    shared_state = {
        'lb': lb_initial,
        'ub': ub,
        'best_makespan': size_time,
        'active_solvers': {},
        'status': 'Solving',   # <--- Thêm dòng này
        'proved_by': None      # <--- Thêm dòng này
    }
    
    lock = threading.Lock()
    stop_event = threading.Event()

    # Nhóm các tham số truyền vào luồng
    args_chung = (
        shared_state, lock, stop_event, 
        num_operations, precedence_list, request_list, out_degree, queue, neighbors, start_time
    )

    t1 = threading.Thread(target=worker_bottom_up, args=args_chung)
    t2 = threading.Thread(target=worker_top_down, args=args_chung)
    t3 = threading.Thread(target=worker_independent_binary, args=args_chung)
    t4 = threading.Thread(target=worker_cooperative_binary, args=args_chung)

    print("-" * 50)
    print("Start multi-threaded search with 4 workers: Bottom-Up, Top-Down, Independent Binary, Cooperative Binary")
    t1.start(); t2.start(); t3.start(); t4.start()
    
    t1.join(); t2.join(); t3.join(); t4.join()

    print("-" * 50)
    print(f"Final result:")
    print(f"Status: {shared_state['status']}")
    print(f"Proved by: {shared_state['proved_by']}")
    print(f"Optimal Makespan: {shared_state['best_makespan']}")
    print(f"Total time: {perf_counter() - start_time:.2f} seconds")
if __name__ == "__main__":
    main()