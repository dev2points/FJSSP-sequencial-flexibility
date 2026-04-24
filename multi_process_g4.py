from collections import defaultdict, deque
import sys
import multiprocessing as mp
import threading
from time import perf_counter, sleep
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

# def build_constraints(solver, num_operations, precedence_list, request_list, feasible_time, s, x, m, top_id):
#     # (4) tạo dãy order
#     for i in range(num_operations):

#         # exactly one
#         machines= request_list[i].keys()
#         enc = CardEnc.equals(lits=[m[(i,machine)] for machine in machines], bound=1, encoding=1, top_id=top_id)
#         top_id = enc.nv
#         solver.append_formula(enc.clauses)

#         # Create first bit of order
#         solver.add_clause([x[(i,feasible_time[i][0])]])
#         for t in range(feasible_time[i][0], feasible_time[i][1]):
#             # (4) Tạo dãy order
#             solver.add_clause([-x[(i,t+1)], x[(i,t)]]) 
#             # (5) Link s và x
#             solver.add_clause([-s[(i,t)], x[(i,t)]])
#             solver.add_clause([-s[(i,t)], -x[(i,t+1)]])
#             solver.add_clause([-x[(i,t)], x[(i,t+1)], s[(i,t)]])
#         # t = feasible_time[i][1]
#         solver.add_clause([-s[(i,feasible_time[i][1])], x[(i,feasible_time[i][1])]])
#         solver.add_clause([s[(i,feasible_time[i][1])], -x[(i,feasible_time[i][1])]])

#         # ràng buộc chống overlap
#         for j in range(i+1, num_operations):
#             if (i,j) in precedence_list or (j,i) in precedence_list:
#                 continue
#             common_machines = set(request_list[i].keys()).intersection(set(request_list[j].keys()))
#             for machine in common_machines:
#                 p_i = request_list[i][machine]
#                 p_j = request_list[j][machine]

#                 for t_i in range(feasible_time[i][0], feasible_time[i][1] + 1):

#                     start = t_i - p_j # Biên time bên trái
#                     end   = t_i + p_i # Biên time bên phải

#                     clause = [
#                         -m[(i, machine)],
#                         -m[(j, machine)],
#                         -s[(i, t_i)]
#                     ]

#                     # Nếu end < ES_j: j chắc chắn bắt đầu sau end -> Mệnh đề luôn ĐÚNG
#                     if end <= feasible_time[j][0]:
#                         continue

#                     # Nếu start + 1 > LS_j: j chắc chắn bắt đầu trước start -> Mệnh đề luôn ĐÚNG
#                     if start  >= feasible_time[j][1]:
#                         continue

#                     # xử lý biên trái
#                     if start >= feasible_time[j][0]:
#                         clause.append(-x[(j, start + 1)])

#                     # xử lý biên phải
#                     if end <= feasible_time[j][1]:
#                         clause.append(x[(j, end)])

#                     # nếu end >= feasible_time[j][1] thì luôn thỏa
#                     solver.add_clause(clause)
    

            
        

#     #(6) ràng buộc thứ tự ưu tiên
#     for i,j in precedence_list:
#         # print(f"Adding precedence constraint: Op {i} -> Op {j}")
#         processing = request_list[i]
#         for machine, process_time in processing.items():
#             for t in range(feasible_time[i][0], feasible_time[i][1] + 1):
#                 finish_i = t + process_time
                
#                 if finish_i > feasible_time[j][1]:
#                     # i kết thúc muộn hơn cả thời điểm muộn nhất j có thể bắt đầu -> Vô lý
#                     solver.add_clause([-s[(i, t)], -m[(i, machine)]])
#                 elif finish_i > feasible_time[j][0]:
#                     # i kết thúc trong khoảng [ES_j, LS_j] -> j phải bắt đầu >= finish_i
#                     solver.add_clause([-s[(i, t)], -m[(i, machine)], x[(j, finish_i)]])
        


def build_constraints(solver, num_operations, precedence_list, request_list, feasible_time, in_degree, s, x, m, top_id):
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

            sm={}              
            for machine in common_machines:
                # Khởi tạo same machine variable
                top_id += 1
                sm[(i,j,machine)] = top_id
                solver.add_clause([-m[(i, machine)], -m[(j, machine)], sm[(i,j,machine)]])
                solver.add_clause([-sm[(i,j,machine)], m[(i, machine)] ])
                solver.add_clause([-sm[(i,j,machine)], m[(j, machine)] ])

                p_i = request_list[i][machine]
                p_j = request_list[j][machine]

                for t_i in range(feasible_time[i][0], feasible_time[i][1] + 1):
                    start = t_i - p_j # Biên time bên trái
                    end   = t_i + p_i # Biên time bên phải
                    clause = [-sm[(i,j,machine)], -s[(i, t_i)]]

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
                    solver.add_clause(clause)

            
        

    #(6) ràng buộc thứ tự precedence
    for i,j in precedence_list:
        # print(f"Adding precedence constraint: Op {i} -> Op {j}")
        machines_i = sorted(request_list[i].items(), key=lambda x: x[1])
        first_flag = True
        for machine, process_time in machines_i:
            if first_flag:
                for t in range(feasible_time[i][0], feasible_time[i][1] + 1):
                    finish_i = t + process_time
                    
                    if finish_i > feasible_time[j][1]:
                        # i kết thúc muộn hơn cả thời điểm muộn nhất j có thể bắt đầu -> Vô lý
                        solver.add_clause([-s[(i, t)], -m[(i, machine)]])
                    elif finish_i > feasible_time[j][0]:
                        # i kết thúc trong khoảng [ES_j, LS_j] -> j phải bắt đầu >= finish_i
                        solver.add_clause([-s[(i, t)], x[(j, finish_i)]])
                first_flag = False
            else:
                for t in range(feasible_time[i][0], feasible_time[i][1] + 1):
                    finish_i = t + process_time
                    
                    if finish_i > feasible_time[j][1]:
                        # i kết thúc muộn hơn cả thời điểm muộn nhất j có thể bắt đầu -> Vô lý
                        solver.add_clause([-s[(i, t)], -m[(i, machine)]])
                    elif finish_i > feasible_time[j][0]:
                        # i kết thúc trong khoảng [ES_j, LS_j] -> j phải bắt đầu >= finish_i
                        solver.add_clause([-s[(i, t)], -m[(i, machine)], x[(j, finish_i)]])
    
    # # symmetry breaking: ít nhất 1 thao tác đầu tiên cua moi job phải bắt đầu tại thời điểm 0
    # first_ops = [i for i in range(num_operations) if in_degree[i] == 0]
    # # print(f"Adding symmetry breaking constraint for first operations: {first_ops}")
    # solver.add_clause([s[(i, 0)] for i in first_ops])

                    
        
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

def init_solver(solver, num_operations, precedence_list, request_list, in_degree, out_degree, queue, neighbors, expected_makespan):
    feasible_time, is_feasible = pre_processing_time(num_operations, precedence_list, out_degree, queue, neighbors, request_list, expected_makespan)
    if not is_feasible:
        print(f"No feasible solution found with UB = {expected_makespan} during pre-processing.")
        return False, None, None, None, None
    s, x, m, top_id = create_var(num_operations, request_list, feasible_time)
    build_constraints(solver, num_operations, precedence_list, request_list, feasible_time, in_degree, s, x, m, top_id)
    add_incremental_constraints(solver, num_operations, out_degree, request_list, expected_makespan, x, m, feasible_time)
    return True, s, x, m, feasible_time


def compute_ranked_targets(lb, ub, worker_count=4):
    if lb is None or ub is None or worker_count <= 0:
        return []

    if ub <= lb:
        return [lb] * worker_count

    span = ub - lb
    targets = []
    previous_target = lb - 1

    for rank in range(1, worker_count + 1):
        if rank == worker_count:
            target = ub
        else:
            target = lb + (span * rank) // worker_count

        if target <= previous_target:
            target = min(ub, previous_target + 1)

        targets.append(target)
        previous_target = target

    return targets


def get_rank_position(rank_queue, worker_index):
    for pos, idx in enumerate(rank_queue):
        if idx == worker_index:
            return pos
    return worker_index


def worker_ranked_binary(
    shared_state, lock, stop_event, interrupt_tickets, active_targets, rank_queue,
    num_operations, precedence_list, request_list, in_degree, out_degree, queue, neighbors, start_time, worker_index, worker_count=4
):
    name = f"Seeker-{worker_index + 1}"
    solver = None
    solver_bound = float('inf')
    s, x, m, feasible_time = None, None, None, None
    
    # 1. THÊM CỜ NÀY ĐỂ THEO DÕI TRẠNG THÁI
    just_found_sat = False 

    while not stop_event.is_set():
        with lock:
            lb, ub = shared_state.get('lb'), shared_state.get('ub')

        if lb is None or ub is None or lb > ub:
            break

        ranked_targets = compute_ranked_targets(lb, ub, worker_count)
        if worker_index >= len(ranked_targets):
            break

        # 2. LOGIC CHỌN TARGET THÔNG MINH HƠN
        if just_found_sat:
            # Nếu vừa SAT, lập tức chiếm đoạt mốc UB mới nhất để tiếp tục vắt kiệt Learned Clauses
            current_target = ub
            just_found_sat = False
        else:
            # Nếu không, ngoan ngoãn lấy target theo rank của mình
            current_target = ranked_targets[worker_index]
            
        print(f"[{name}] Interval: LB={lb}, UB={ub} => Target={current_target}")

        if solver is not None and current_target <= solver_bound:
            if current_target < solver_bound:
                add_incremental_constraints(solver, num_operations, out_degree, request_list, current_target, x, m, feasible_time)
                solver_bound = current_target
        else:
            if solver is not None:
                solver.delete()
                solver = None

            # 3. BẮT BUỘC ĐỔI SANG GLUCOSE ĐỂ HỖ TRỢ INTERRUPT()
            solver = Solver(name='glucose4')
            init_success, s, x, m, feasible_time = init_solver(solver, num_operations, precedence_list, request_list, in_degree, out_degree, queue, neighbors, current_target)

            if not init_success:
                with lock:
                    if current_target >= shared_state.get('lb'):
                        shared_state['lb'] = current_target + 1
                        if shared_state.get('lb') > shared_state.get('ub') and shared_state.get('status') != 'Optimal':
                            shared_state['status'] = 'Optimal'
                            shared_state['proved_by'] = name
                            stop_event.set()

                if solver:
                    solver.delete()
                    solver = None
                solver_bound = float('inf')
                continue

            solver_bound = current_target

        if stop_event.is_set():
            break

        # ... (Giữ nguyên phần check stale target và watchdog thread của bạn) ...
        current_lb, current_ub = shared_state.get('lb'), shared_state.get('ub')
        if current_lb > current_target or current_ub < current_target or current_lb > current_ub:
            print(f"[{name}] Target {current_target} became stale. Re-seeding.")
            continue

        watchdog_flag = [False]
        process_stop_event = threading.Event()
        local_ticket = interrupt_tickets.get(worker_index, 0)
        active_targets[worker_index] = current_target
        monitor_thread = threading.Thread(
            target=watchdog_both,
            args=(solver, shared_state, interrupt_tickets, worker_index, local_ticket, current_target, process_stop_event, name, watchdog_flag,)
        )
        monitor_thread.start()

        is_sat = None
        try:
            is_sat = solver.solve()
        except Exception as e:
            print(f"[{name}] Solver exception: {e}")
            is_sat = None

        process_stop_event.set()
        monitor_thread.join()
        active_targets.pop(worker_index, None)

        if stop_event.is_set():
            break

        was_interrupted = watchdog_flag[0]

        if is_sat is None or was_interrupted:
            print(f"[{name}] Interrupted. Keeping the solver for the next re-seed.")
            # 4. XÓA CỜ INTERRUPT NẾU DÙNG GLUCOSE, NẾU KHÔNG NÓ SẼ RA NGHIỆM GIẢ
            if hasattr(solver, 'clear_interrupt'):
                solver.clear_interrupt()
            continue

        if is_sat is True:
            with lock:
                print(f"[{name}] SAT in {current_target}! Updating UB.")
                
                # BẬT CỜ BÁO HIỆU VỪA TÌM THẤY SAT ĐỂ VÒNG TỚI GIỮ BOUND
                just_found_sat = True 

                if current_target <= shared_state.get('ub'):
                    shared_state['ub'] = current_target - 1
                    shared_state['best_makespan'] = current_target

                    if shared_state.get('lb') > shared_state.get('ub') and shared_state.get('status') != 'Optimal':
                        shared_state['status'] = 'Optimal'
                        shared_state['proved_by'] = name
                        stop_event.set()

                # ... (Giữ nguyên logic interrupt_tickets cho rank lớn hơn của bạn) ...
                my_pos = get_rank_position(rank_queue, worker_index)
                for other_pos in range(my_pos + 1, len(rank_queue)):
                    other_idx = rank_queue[other_pos]
                    other_target = active_targets.get(other_idx)
                    if other_target is not None and other_target > current_target:
                        interrupt_tickets[other_idx] = interrupt_tickets.get(other_idx, 0) + 1
            continue

        if is_sat is False:
            with lock:
                print(f"[{name}] UNSAT in {current_target}. Updating LB.")
                # Nếu dính UNSAT thì cờ SAT bị tắt (mặc định rồi nhưng viết rõ ra)
                just_found_sat = False 
                
                # ... (Giữ nguyên phần xử lý cập nhật LB và bắn vé ngắt rank nhỏ hơn) ...
            
            if solver:
                solver.delete()
                solver = None
            solver_bound = float('inf')

    if solver:
        solver.delete()




# 1. HÀM WATCHDOG ĐƯỢC TINH CHỈNH (Dành cho Top-Down)
def watchdog_ub(solver, shared_state, current_target, process_stop_event, worker_name, watchdog_flag):
    """Canh chừng biên UB (Dành cho Top-Down)"""
    while not process_stop_event.is_set():
        # Lấy UB mới nhất từ Share Memory một cách an toàn
        latest_ub = shared_state.get('ub')
        
        # Top-Down chỉ bị ngắt khi có process khác đè UB xuống THẤP HƠN target đang giải
        if latest_ub is not None and latest_ub < current_target:
            print(f"[{worker_name}-Watchdog] Phát hiện UB ({latest_ub}) < Target ({current_target}). INTERRUPT!")
            watchdog_flag[0] = True # Bật cờ ngắt
            if solver is not None:
                solver.interrupt()  # Bóp cò ngắt CaDiCaL
            break
            
        process_stop_event.wait(0.1)


# 1. HÀM WATCHDOG CHO BINARY SEARCH
def watchdog_both(
    solver,
    shared_state,
    interrupt_tickets,
    worker_index,
    local_ticket,
    current_target,
    process_stop_event,
    worker_name,
    watchdog_flag,
):
    """Canh chừng cả 2 biên LB và UB. Ngắt nếu target không còn giá trị."""
    while not process_stop_event.is_set():
        current_ticket = interrupt_tickets.get(worker_index, 0)
        if current_ticket != local_ticket:
            print(f"[{worker_name}-Watchdog] Received rank-queue interrupt signal.")
            watchdog_flag[0] = True
            if solver is not None:
                solver.interrupt()
            break

        # Dùng .get() để tránh lỗi khi đọc từ multiprocessing dict
        latest_lb = shared_state.get('lb')
        latest_ub = shared_state.get('ub')
        
        if latest_lb is not None and latest_ub is not None:
            # Bài toán đã Optimal bởi một process khác
            if latest_lb > latest_ub:
                watchdog_flag[0] = True
                if solver is not None: solver.interrupt()
                break
                
            # Cận dưới bị đẩy lên cao hơn Target đang giải
            if latest_lb > current_target:
                print(f"[{worker_name}-Watchdog] LB ({latest_lb}) over target {current_target}. Interrupt!")
                watchdog_flag[0] = True
                if solver is not None: solver.interrupt()
                break
                
            # Cận trên bị ép xuống thấp hơn Target đang giải
            if latest_ub < current_target:
                print(f"[{worker_name}-Watchdog] UB ({latest_ub}) under target {current_target}. Interrupt!")
                watchdog_flag[0] = True
                if solver is not None: solver.interrupt()
                break
            
        process_stop_event.wait(0.1)


def main():
    if len(sys.argv) < 2:
        print("Sử dụng: python3 script.py <file_path>")
        sys.exit(1)

    start_time = perf_counter()
    file_path = sys.argv[1]
    
    print(f"Loading data from: {file_path}")
    num_operations, num_edges, num_machines, precedence_list, request_list = read_file(file_path)
    in_degree, out_degree, neighbors, predecessors = data(num_operations, precedence_list)
    
    size_time, assignment, queue = greedy_schedule(num_operations, num_machines, request_list, in_degree, neighbors, predecessors)
    lb_initial = calculate_lower_bound(num_operations, num_machines, precedence_list, request_list)
    ub = size_time - 1
    initial_targets = compute_ranked_targets(lb_initial, ub, 4)
    
    print(f"Complete preprocessing! Greedy UB = {size_time}")
    print(f"Initial UB = {ub}, LB = {lb_initial}")
    print(f"Initial ranked targets = {initial_targets}")
    
    # ==============================================================
    # BẢN VÁ LỖI BROKEN PIPE
    # ==============================================================
    # 1. Khai báo Lock và Event NATIVE (Không thông qua Manager)
    # Tốc độ cực nhanh, không dùng Pipe, không bao giờ lỗi.
    lock = mp.Lock()
    stop_event = mp.Event()

    # 2. Dùng Manager bằng khối `with` để đảm bảo nó sống cho đến phút cuối cùng
    with mp.Manager() as manager:
        shared_state = manager.dict({
            'lb': lb_initial,
            'ub': ub,
            'best_makespan': size_time,
            'status': 'Solving',   
            'proved_by': None      
        })

        interrupt_tickets = manager.dict({i: 0 for i in range(4)})
        active_targets = manager.dict()
        rank_queue = manager.list([0, 1, 2, 3])
        
        args_chung = (
            shared_state, lock, stop_event, interrupt_tickets, active_targets, rank_queue,
            num_operations, precedence_list, request_list, in_degree, out_degree, queue, neighbors, start_time
        )

        processes = [
            mp.Process(target=worker_ranked_binary, args=args_chung + (0, 4)),
            mp.Process(target=worker_ranked_binary, args=args_chung + (1, 4)),
            mp.Process(target=worker_ranked_binary, args=args_chung + (2, 4)),
            mp.Process(target=worker_ranked_binary, args=args_chung + (3, 4))
        ]

        print("-" * 50)
        print(" Start MULTIPROCESSING search with 4 CPU Cores...")
        print("-" * 50)
        
        for p in processes:
            p.start()
        
        # Vòng lặp chờ an toàn
        try:
            while not stop_event.is_set() and any(p.is_alive() for p in processes):
                sleep(0.1) # Tăng tốc độ phản hồi lệnh dừng (0.5 -> 0.1)
                
        except KeyboardInterrupt:
            print("\n[Main] Found user interrupt (Ctrl+C)!")
            stop_event.set()

        print("\nFound optimal solution or received stop signal. Cleaning up processes...")
        
        # 3. Dọn dẹp an toàn thay vì bắn vỡ pipe
        for p in processes:
            if p.is_alive():
                p.terminate() 
                p.join() # Chờ tiến trình con trả lại tài nguyên
        
        # IN KẾT QUẢ CUỐI CÙNG NGAY TRONG KHỐI WITH (Khi Manager vẫn còn sống)
        print("-" * 50)
        print(f"   FINAL RESULT:")
        print(f"   Status: {shared_state['status']}")
        print(f"   Proved by: {shared_state['proved_by']}")
        print(f"   Optimal Makespan: {shared_state['best_makespan']}")
        print(f"   Total time: {perf_counter() - start_time:.2f} seconds")

if __name__ == '__main__':
    mp.freeze_support() 
    main()