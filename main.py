
import sys
from time import perf_counter, time
from pysat.solvers import Solver
from pysat.formula import CNF
from pysat.card import CardEnc
from collections import deque, defaultdict


def read_file(file_path):
    with open(file_path, 'r') as file:
        if 'mk' in file_path.lower():
            for _ in range(1):
                next(file, None)
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
                map = dict(sorted(map.items(), key=lambda item: item[1]))
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
    # print(f"in_degree: {in_degree}")
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
    latest_start = {}
    # print(f"lastest start 8 {latest_start[8]}")

    for u in reversed(topo_queue):
        latest_start[u] = min(latest_start[v] - min_proc_time[u] for v in neighbors[u]) if neighbors[u] else ub - min_proc_time[u]
    
    feasible_time = {}
    for i in range(num_operations):
        feasible_time[i] = (earliest_start[i], latest_start[i])
        if earliest_start[i] > latest_start[i]:
            print(f"Operation {i} cannot be scheduled (feasible time: {feasible_time[i]})")
            return None, False

    return feasible_time, True


def create_var(num_operations, request_list, feasible_time):
    s={}
    x={}
    m={}
    xm={}
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
            counter += 1
            xm[(i, a)] = counter

    return s, x, m, xm, counter   

def transitive_closure_weighted(num_operations, precedence_list,request_list, neighbors, in_degree):
   
    # processing time nhỏ nhất của mỗi operation
    min_proc = {
        i: min(request_list[i].values())
        for i in range(num_operations)
    }

    # Khởi tạo khoảng cách giữa các thao tác
    graph = {(u,v): min_proc[u] for u, v in precedence_list}

    neighbors = neighbors.copy()
    in_degree = in_degree.copy()

    # Sử dụng thuật toán Floyd-Warshall để tính transitive closure có trọng số
    for k in range(num_operations):
        for i in range(num_operations):
            for j in range(num_operations):
                if (i, k) in graph and (k, j) in graph:
                    new_dist = graph[(i, k)] + graph[(k, j)]
                    if (i, j) not in graph or new_dist > graph[(i, j)]:
                        graph[(i, j)] = new_dist
                        if j not in neighbors[i]:
                            neighbors[i].append(j)
                            in_degree[j] += 1
    
    # Trả về danh sách các cạnh closure dưới dạng (u, v, w) với w là thời gian tối thiểu từ u đến v
    return [(u, v, w) for (u, v), w in graph.items()] 

def build_constraints(solver, num_operations, precedence_list, request_list, feasible_time, in_degree, s, x, m, xm, top_id, graph):
    # (4) tạo dãy order
    for i in range(num_operations):    
        

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

        # Exactly one machine
        request_list_i = list(request_list[i].items())

        last_machine = request_list_i[-1][0]
        solver.add_clause([xm[(i, last_machine)]])

        for idx in range(len(request_list_i) - 1):
            machine1 = request_list_i[idx][0]
            machine2 = request_list_i[idx + 1][0]
            solver.add_clause([-xm[(i, machine1)], xm[(i, machine2)]])

        first_machine = request_list_i[0][0]
        solver.add_clause([-m[(i, first_machine)], xm[(i, first_machine)]])
        solver.add_clause([-xm[(i, first_machine)],m[(i, first_machine)]])

        for idx in range(1, len(request_list_i)):

            prev_machine = request_list_i[idx - 1][0]
            curr_machine = request_list_i[idx][0]

            solver.add_clause([-m[(i, curr_machine)],-xm[(i, prev_machine)]])
            solver.add_clause([-m[(i, curr_machine)],xm[(i, curr_machine)]])

            solver.add_clause([xm[(i, prev_machine)],-xm[(i, curr_machine)],m[(i, curr_machine)]])


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
                # Constraint 1 way to decrease the number of clauses
                solver.add_clause([-m[(i, machine)], -m[(j, machine)], sm[(i,j,machine)]])
                # solver.add_clause([-sm[(i,j,machine)], m[(i, machine)] ])
                # solver.add_clause([-sm[(i,j,machine)], m[(j, machine)] ])

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

            # # (options) 
            # diff_machines_i = set(request_list[i].keys()).difference(set(request_list[j].keys()))
            # diff_machines_j = set(request_list[j].keys()).difference(set(request_list[i].keys()))
            # for machine_i in diff_machines_i:
            #     for machine_j in diff_machines_j:
            #         for machine in common_machines:
            #         # Nếu i và j không có máy nào chung, thì i và j chắc chắn không thể chạy cùng lúc trên cùng 1 máy -> Thêm mệnh đề cứng: -m[i, machine_i] OR -m[j, machine_j]
            #             solver.add_clause([-m[(i, machine_i)], -m[(j, machine_j)], -sm[(i,j,machine)]])
            
        

    
    for (i, j) in precedence_list:
        # Chuyển đổi thành list để lấy được chỉ số idx của máy trong danh sách đã sắp xếp
        request_list_i = list(request_list[i].items())

        for t in range(feasible_time[i][0], feasible_time[i][1] + 1):
            for idx in range(len(request_list_i)):
                machine, processing_time = request_list_i[idx]
                finish_i = t + processing_time
                
                if finish_i > feasible_time[j][0]:
                    if finish_i <= feasible_time[j][1]:
                        if idx == 0:
                            # Nếu là máy nhanh nhất (idx=0) mà j vẫn bắt đầu trước khi i xong, 
                            # thì không còn máy nào nhanh hơn nữa -> Clause ép j phải đợi đến finish_i
                            solver.add_clause([-s[(i, t)], x[(j, finish_i)]])
                            # print(f"at operation {i} at time {t}, finish_i={finish_i} is within [ES_j, LS_j]=[{feasible_time[j][0]}, {feasible_time[j][1]}] of operation {j}. Clause added: [-s[({i}, {t})], x[({j}, {finish_i})]]")
                        else:
                            # SỬA TẠI ĐÂY: Nếu j bắt đầu trước finish_i, ép buộc phải chọn các máy nhanh hơn phía trước
                            prev_machine = request_list_i[idx - 1][0]
                            solver.add_clause([-s[(i, t)], x[(j, finish_i)], xm[(i, prev_machine)]])
                    else:
                        # Trường hợp finish_i vượt quá cả thời gian muộn nhất của j (LS_j)
                        if idx == 0:
                            # Ngay cả máy nhanh nhất cũng không kịp -> thời điểm t này bất khả thi
                            # Don't need because pre processing build on first machine, but keep it for safety
                            solver.add_clause([-s[(i, t)]])
                            print(f"at operation {i} at time {t}, finish_i={finish_i} is beyond LS_j={feasible_time[j][1]} of operation {j}. Clause added: [-s[({i}, {t})]]")
                        else:
                            # Bắt buộc phải chọn các máy nhanh hơn phía trước thì mới kịp giờ của j
                            prev_machine = request_list_i[idx - 1][0]
                            solver.add_clause([-s[(i, t)], xm[(i, prev_machine)]])
                            # print(f"at operation {i} at time {t}, finish_i={finish_i} is beyond LS_j={feasible_time[j][1]} of operation {j}. Clause added: [-s[({i}, {t})], xm[({i}, {prev_machine})]]")
                        
                        # Vì các máy phía sau còn chậm hơn nữa, chắc chắn cũng sẽ vượt quá LS_j,
                        # nên ta có thể break luôn để giảm số lượng clause thừa.
                        break
                else:
                    print(f"at operation {i} at time {t}, finish_i={finish_i} is before ES_j={feasible_time[j][0]} of operation {j}. No clause needed.")


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
                        # i kết thúc muộn hơn cả thời ddiểm muộn nhất j có thể bắt đầu macwj duf masy nhanh nhaats -> Vô lý
                        solver.add_clause([-s[(i, t)]])
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

    for u, v, w in graph:
        if (u, v) in precedence_list:
            continue
        # Chỉ thêm ràng buộc thứ tự cho các thao tác không có phụ thuộc trực tiếp, và chỉ khi u là thao tác đầu tiên (in_degree[u] == 0) để tránh trùng lặp với các ràng buộc precedence đã có.
        if in_degree[u] != 0:
            continue
        # print(f"Adding transitive precedence constraint: Op {u} -> Op {v} with min gap {w}")
        for t in range(feasible_time[u][0], feasible_time[u][1] + 1):
            finish_u = t + w
            
            if finish_u > feasible_time[v][1]:
                # u kết thúc muộn hơn cả thời điểm muộn nhất v có thể bắt đầu -> Vô lý
                solver.add_clause([-s[(u, t)]])
            elif finish_u > feasible_time[v][0]:
                # u kết thúc trong khoảng [ES_v, LS_v] -> v phải bắt đầu >= finish_u
                solver.add_clause([-s[(u, t)], x[(v, finish_u)]])


    # symmetry breaking: ít nhất 1 thao tác đầu tiên cua moi job phải bắt đầu tại thời điểm 0
    # first_ops = [i for i in range(num_operations) if in_degree[i] == 0]
    # # print(f"Adding symmetry breaking constraint for first operations: {first_ops}")
    # solver.set_phases([s[(i, 0)] for i in first_ops])  # ưu tiên các thao tác đầu tiên bắt đầu sớm nhất
    

                    
        
def add_incremental_constraints(solver, num_operations, out_degree, request_list, ub, s, x, m, xm, feasible_time, k):
    # (12) Giới hạn makespan cho toàn bộ thao tác, không chỉ các thao tác cuối.
    # Nếu một máy không thể hoàn thành thao tác trước hoặc tại ub, cấm gán máy đó.
    last_ops = [i for i in range(num_operations) if out_degree[i] == 0]
    # print(f"Adding incremental constraints for UB = {ub} on last operations: {last_ops}")
    for i in last_ops:
        for machine, process_time in request_list[i].items():
            limit_time = ub - process_time
            if limit_time < feasible_time[i][0] :
                solver.add_clause([-m[(i, machine)]]) 
            elif limit_time < feasible_time[i][1]:
                solver.add_clause([-m[(i, machine)], -x[(i, limit_time + 1)]])
    for i in range(num_operations):
        for t in range(k):
            solver.add_clause([-s[(i, feasible_time[i][1] - t)]])

        # request_list_i = list(request_list[i].items())  
        # for idx in range(len(request_list_i)):
        #     machine, process_time = request_list_i[idx]
        #     limit_time = ub - process_time
            
        #     # TRƯỜNG HỢP 1: Máy thứ k quá chậm, ngay cả bắt đầu từ mốc sớm nhất cũng không kịp UB
        #     if limit_time < feasible_time[i][0]:
        #         if idx == 0:
        #             # Máy nhanh nhất cũng không kịp -> Bài toán vô nghiệm (UNSAT) tại mốc UB này
        #             solver.add_clause([]) 
        #         else:
        #             # Bắt buộc phải chọn máy từ (idx-1) trở về trước
        #             prev_machine = request_list_i[idx-1][0]
        #             solver.add_clause([xm[(i, prev_machine)]])
        #         break # Nhờ Order Encoding, toàn bộ các máy chậm hơn phía sau tự động bị khóa
                
        #     # TRƯỜNG HỢP 2: Thời gian giới hạn nằm trong khoảng khả thi (Ý tưởng của bạn)
        #     elif limit_time < feasible_time[i][1]:
        #         if idx == 0:
        #             # Nếu là máy nhanh nhất (idx=0), không có máy nào nhanh hơn nó nữa.
        #             # Theo ý tưởng của bạn: Nếu start >= limit_time + 1, không thể chọn máy nào cả (Vô nghiệm).
        #             # Vì vậy, Solver không bao giờ được phép cho start vượt quá mốc này:
        #             solver.add_clause([-x[(i, limit_time + 1)]])
        #         else:
        #             prev_machine = request_list_i[idx-1][0]
        #             # ĐÚNG THEO Ý TƯỞNG CỦA BẠN: Start muộn -> Buộc phải chọn máy nhanh hơn (<= idx-1)
        #             solver.add_clause([
        #                 -x[(i, limit_time + 1)], 
        #                 xm[(i, prev_machine)]
        #             ])
                    
        #     else:
        #         # Máy này hoàn toàn an toàn dưới mốc UB, không cần thêm ràng buộc
        #         continue


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
        print(f"status: optimal")
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
    size_time, assignment, queue = greedy_schedule(num_operations, num_machines, request_list, in_degree.copy(), neighbors, predecessors)
    ub = size_time - 1
    feasible_time, is_feasible = pre_processing_time(num_operations, precedence_list, out_degree, queue, neighbors, request_list, ub)
    if not is_feasible:
        print("No feasible solution found")
        print("status: optimal")
        print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
        return
    # print(f"Feasible time windows: {feasible_time}  ")
    s, x, m, xm, top_id = create_var(num_operations, request_list, feasible_time)

    
    solver = Solver(name = 'cadical195')

    graph = transitive_closure_weighted(num_operations, precedence_list, request_list, neighbors.copy(), in_degree.copy())
    build_constraints(solver, num_operations, precedence_list, request_list, feasible_time, in_degree, s, x, m, xm, top_id, graph)
    print(f"Building constraints took {perf_counter() - start_time:.2f} seconds.")
    k = 0
    while True:
        add_incremental_constraints(solver, num_operations, out_degree, request_list, ub, s, x, m, xm, feasible_time, k)
        machine_assignment, start_times, machine_queues, makespan = solve_and_print(solver, num_operations, s, m, request_list)
        if machine_assignment is None:
            print(f"Time taken: {perf_counter() - start_time:.2f} seconds")
            break  # Không thể giảm UB nữa

        if not verify_schedule(num_operations, num_machines, precedence_list, request_list, machine_assignment, start_times, makespan):
            print("Schedule is not valid")
            return
        else:
            print("Schedule is valid")

        # Tìm nghiệm tốt hơn ở vòng lặp tiếp theo.
        k = ub - makespan
        ub = makespan - 1
        print(f" Time taken: {perf_counter() - start_time:.2f} seconds")
if __name__ == "__main__":
    main()