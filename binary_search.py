
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
                    raise ValueError(f"Warning: Operation {i} was already assigned to machine {machine_assignment[i]}, but now is assigned to machine {machine}.")
                machine_assignment[i] = machine
                
        # 2. Trích xuất Thời điểm bắt đầu của mỗi thao tác
        for (i, t), lit in s.items():
            if lit in positive_lits:
                if start_times.get(i) is not None:
                    raise ValueError(f"Warning: Operation {i} already has a start time {start_times[i]} assigned, but now has a new start time {t}.")
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
        #     print(f"Operation {i:2d}: Running on Machine {machine_assignment[i]}, From t = {start_times[i]} to t = {start_times[i] + request_list[i][machine_assignment[i]]}")
            
        # print("\n--- QUEUE ON EACH MACHINE ---")
        # for machine, queue in sorted(machine_queues.items()):
        #     # Format string for better readability: Op i [start -> end]
        #     queue_str = "  ->  ".join([f"Op {op} [{st}->{en}]" for st, en, op in queue])
        #     print(f"Machine {machine}: {queue_str}")
            
        print(f"\n=> TOTAL COMPLETION TIME (Makespan / UB): {makespan}")
            
        # Trả về thêm makespan (ub) ở vị trí thứ 4
        return machine_assignment, start_times, machine_queues, makespan
        
    else:
        print("UNSAT")
        # print(f"status: optimal")
        return None, None, None, None
    


def verify_schedule(num_operations, num_machines, precedence_list,
                    request_list, machine_assignment, start_times, expected_makespan=None):

    # 1. Kiểm tra mỗi operation có đúng 1 machine
    for i in range(num_operations):
        if i not in machine_assignment:
            print(f"Operation {i} is not assigned to any machine")
            return False

        machine = machine_assignment[i]
        if machine not in request_list[i]:
            print(f"Operation {i} is assigned to machine {machine} which is not valid")
            return False

    # 2. Kiểm tra mỗi operation có đúng 1 start time
    for i in range(num_operations):
        if i not in start_times:
            print(f"Operation {i} does not have a start time")
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
                    print(f"Operation {i} has predecessor {p} that is not completed")
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
                print(f"Machine {m} is overlapping between operation {i1} (from {st1} to {en1}) and operation {i2} (from {st2} to {en2})")
                return False

    # 5. kiểm tra precedence trực tiếp
    for u, v in precedence_list:
        mu = machine_assignment[u]
        mv = machine_assignment[v]

        end_u = start_times[u] + request_list[u][mu]
        start_v = start_times[v]

        if end_u > start_v:
            print(f"Violation of precedence: operation {u} (completed at {end_u}) must come before operation {v} (started at {start_v})")
            return False

    # 6. makespan
    makespan = max(op_completion_time.values())
    if expected_makespan is not None and makespan > expected_makespan:
        print(f"Schedule makespan {makespan} exceeds expected UB {expected_makespan}")
        return False

    return True



def main():
    start_time = perf_counter()
    file_path = sys.argv[1]
    num_operations, num_edges, num_machines, precedence_list, request_list = read_file(file_path)
    in_degree, out_degree, neighbors, predecessors = data(num_operations, precedence_list)
    size_time, assignment, queue = greedy_schedule(num_operations, num_machines, request_list, in_degree, neighbors, predecessors)
    lb = calculate_lower_bound(num_operations, num_machines, precedence_list, request_list)


    best_makespan = size_time
    ub = size_time - 1
    expected_makespan = (lb + ub) // 2
    last_expected_makespan = expected_makespan
    # while True:
    #     print(f"\nTrying to solve with expected makespan (UB) = {expected_makespan} (LB={lb}, UB={ub})")
    #     solver = Solver(name='cadical195')
    #     init_success, s, x, m, feasible_time = init_solver(solver, num_operations, precedence_list, request_list, out_degree, queue, neighbors, expected_makespan)
    #     if not init_success:
    #         print(f"Pre-processing determined no feasible solution with UB = {expected_makespan}. Adjusting bounds.")
    #         ub = expected_makespan - 1
    #         expected_makespan = (lb + ub) // 2
    #         continue

    #     machine_assignment, start_times, machine_queues, makespan = solve_and_print(solver, num_operations, s, m, request_list)
    #     solver.delete()

    #     if machine_assignment is not None:
    #         if verify_schedule(num_operations, num_machines, precedence_list,
    #                            request_list, machine_assignment, start_times, expected_makespan):
    #             print(f"Schedule verified successfully with makespan {makespan}. Updating UB.")
    #             print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
    #             best_makespan = makespan
    #             ub = makespan - 1
    #         else:
    #             print("Schedule verification failed. This should not happen if the SAT model is correct.")
    #             print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
    #             break
    #     else:
    #         print(f"No schedule found with UB = {expected_makespan}. Updating LB.")
    #         print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
    #         lb = expected_makespan + 1

    #     if lb > ub:
    #         print(f"Search complete. Optimal makespan is {best_makespan}.")
    #         print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
    #         break

    #     expected_makespan = (lb + ub) // 2

    while lb <= ub:
        print(f"\nTrying to solve with expected makespan (UB) = {expected_makespan} (LB={lb}, UB={ub})")
        
        # --- NHÁNH 1: INCREMENTAL SAT (Chỉ dùng khi giảm makespan và solver chưa bị xóa) ---
        if expected_makespan < last_expected_makespan :
            add_incremental_constraints(solver, num_operations, out_degree, request_list, expected_makespan, x, m, feasible_time)
            machine_assignment, start_times, machine_queues, makespan = solve_and_print(solver, num_operations, s, m, request_list)
            
        # --- NHÁNH 2: RE-INIT SOLVER (Dùng cho vòng đầu tiên, hoặc sau khi UNSAT) ---
        else:            
            solver = Solver(name='cadical195')
            init_success, s, x, m, feasible_time = init_solver(solver, num_operations, precedence_list, request_list, out_degree, queue, neighbors, expected_makespan)
            
            if not init_success:
                print(f"Pre-processing determined no feasible solution with UB = {expected_makespan}.")
                machine_assignment = None  # Ép nó hiểu là UNSAT
            else:
                machine_assignment, start_times, machine_queues, makespan = solve_and_print(solver, num_operations, s, m, request_list)

        if machine_assignment is not None:
            if verify_schedule(num_operations, num_machines, precedence_list, request_list, machine_assignment, start_times, expected_makespan):
                print(f"Schedule verified successfully with makespan {makespan}. Updating UB.")
                best_makespan = makespan
                ub = makespan - 1
            else:
                print("Schedule verification failed. This should not happen if the SAT model is correct.")
                break
        else:

            print(f"No schedule found with UB = {expected_makespan}. Updating LB.")
            lb = expected_makespan + 1
            if solver is not None:
                solver.delete()
                solver = None

        last_expected_makespan = expected_makespan
        expected_makespan = (lb + ub) // 2
        print(f"Time taken: {perf_counter() - start_time:.2f} seconds")

    # Kết thúc vòng lặp
    print(f"\nSearch complete. Optimal makespan is {best_makespan}.")
    
if __name__ == "__main__":
    main()