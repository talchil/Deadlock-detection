import pulp

def check_deadlock_ILP_1safe_quick(places, transitions, incidence, reachable_markings, enable_cond):
    """
    Kiểm tra deadlock cho 1-safe Petri net dựa trên tập reachable markings.
    Dừng ngay khi phát hiện deadlock đầu tiên.
    """
    for M in reachable_markings:
        # 1. Khởi tạo ILP
        lp = pulp.LpProblem("DeadlockCheck", pulp.LpMinimize)

        # 2. Biến place (binary)
        x = {p: pulp.LpVariable(p, cat='Binary') for p in places}

        # 3. Biến transition (số lần fire, >=0)
        y = {t: pulp.LpVariable(t, lowBound=0, cat='Integer') for t in transitions}

        # 4. Ràng buộc reachable marking
        for p in places:
            lp += x[p] == M[p] + pulp.lpSum(incidence[p][t]*y[t] for t in transitions)

        # 5. Ràng buộc deadlock: tất cả pre-place của transitions = 0
        for t in transitions:
            for p in enable_cond.get(t, []):
                lp += x[p] == 0

        # 6. Giải ILP
        lp.solve(pulp.PULP_CBC_CMD(msg=False))

        # 7. Nếu tìm thấy deadlock → in và thoát
        if pulp.LpStatus[lp.status] == 'Optimal':
            deadlock_marking = {p: x[p].varValue for p in places}
            print(f"Deadlock detected at marking: {deadlock_marking}")
            return  # thoát ngay khi thấy deadlock

    # 8. Nếu duyệt hết mà không thấy deadlock
    print("No deadlock detected in all reachable markings")


# ==========================================
# NHẬP PETRI NET TỪ NGƯỜI DÙNG (simplified)
# ==========================================

num_places = int(input("Nhập số lượng place: "))
places = [input(f"Tên place {i+1}: ") for i in range(num_places)]

num_trans = int(input("\nNhập số lượng transition: "))
transitions = [input(f"Tên transition {i+1}: ") for i in range(num_trans)]

# ------- Nhập reachable markings -------
reachable_markings = []
num_markings = int(input("\nNhập số lượng reachable markings: "))
for k in range(num_markings):
    print(f"Marking {k+1}: nhập {num_places} giá trị 0/1 theo thứ tự {places}")
    values = list(map(int, input().split()))
    if len(values) != num_places:
        raise ValueError("Số phần tử không khớp số place")
    reachable_markings.append(dict(zip(places, values)))

# ------- Nhập pre-place và post-place để tạo incidence matrix -------
pre_places = {}
post_places = {}
incidence = {p: {} for p in places}

for t in transitions:
    raw_pre = input(f"Transition {t} enable khi có token ở place nào? ")
    pre_places[t] = raw_pre.split() if raw_pre.strip() else []

    raw_post = input(f"Transition {t} sau khi firing, token đi vào place nào? ")
    post_places[t] = raw_post.split() if raw_post.strip() else []

# Tạo incidence matrix tự động
for p in places:
    for t in transitions:
        pre = -1 if p in pre_places[t] else 0
        post = 1 if p in post_places[t] else 0
        incidence[p][t] = pre + post

# Dùng pre_places làm enable condition
enable_cond = pre_places

check_deadlock_ILP_1safe_quick(places, transitions, incidence, reachable_markings, enable_cond)
