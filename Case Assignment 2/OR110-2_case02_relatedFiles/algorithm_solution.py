from mailbox import MaildirMessage
import os
import csv

# sorting algorithms _ merge sort
def merge_sort_ATL(unsorted_list):
    if len(unsorted_list) <= 1:
        return unsorted_list
    # Find the middle point and devide it
    middle = len(unsorted_list) // 2
    left_list = unsorted_list[:middle]
    right_list = unsorted_list[middle:]

    left_list = merge_sort_ATL(left_list)
    right_list = merge_sort_ATL(right_list)
    return list(merge_ATL(left_list, right_list))

def merge_ATL(left_half,right_half):
    res = []
    while len(left_half) != 0 and len(right_half) != 0:
        if Processing_Time[left_half[0][0]][left_half[0][1]] > Processing_Time[right_half[0][0]][right_half[0][1]]:
            res.append(left_half[0])
            left_half.remove(left_half[0])
        elif Processing_Time[left_half[0][0]][left_half[0][1]] < Processing_Time[right_half[0][0]][right_half[0][1]]:
            res.append(right_half[0])
            right_half.remove(right_half[0])
        else:
            if len(Machine_List[left_half[0][0]][left_half[0][1]]) <= len(Machine_List[right_half[0][0]][right_half[0][1]]):
                res.append(left_half[0])
                left_half.remove(left_half[0])
            elif len(Machine_List[left_half[0][0]][left_half[0][1]]) > len(Machine_List[right_half[0][0]][right_half[0][1]]):
                res.append(right_half[0])
                right_half.remove(right_half[0])
    if len(left_half) == 0:
        res = res + right_half
    else:
        res = res + left_half
    return res

def merge_sort(unsorted_list):
    if len(unsorted_list) <= 1:
        return unsorted_list
    # Find the middle point and devide it
    middle = len(unsorted_list) // 2
    left_list = unsorted_list[:middle]
    right_list = unsorted_list[middle:]

    left_list = merge_sort(left_list)
    right_list = merge_sort(right_list)
    return list(merge(left_list, right_list))

# Merge the sorted halves
def merge(left_half,right_half):
    res = []
    while len(left_half) != 0 and len(right_half) != 0:
        if Due_Time[left_half[0][0]][left_half[0][1]] < Due_Time[right_half[0][0]][right_half[0][1]]:
            res.append(left_half[0])
            left_half.remove(left_half[0])
        elif Due_Time[left_half[0][0]][left_half[0][1]] > Due_Time[right_half[0][0]][right_half[0][1]]:
            res.append(right_half[0])
            right_half.remove(right_half[0])
        else:
            if Processing_Time[left_half[0][0]][left_half[0][1]] < Processing_Time[right_half[0][0]][right_half[0][1]]:
                res.append(left_half[0])
                left_half.remove(left_half[0])
            elif Processing_Time[left_half[0][0]][left_half[0][1]] > Processing_Time[right_half[0][0]][right_half[0][1]]:
                res.append(right_half[0])
                right_half.remove(right_half[0])
            else:
                if len(Machine_List[left_half[0][0]][left_half[0][1]]) <= len(Machine_List[right_half[0][0]][right_half[0][1]]):
                    res.append(left_half[0])
                    left_half.remove(left_half[0])
                elif len(Machine_List[left_half[0][0]][left_half[0][1]]) > len(Machine_List[right_half[0][0]][right_half[0][1]]):
                    res.append(right_half[0])
                    right_half.remove(right_half[0])
    if len(left_half) == 0:
        res = res + right_half
    else:
        res = res + left_half
    return res

# Read file
all_data_list = os.listdir('data')
for file_name in all_data_list:

    file_path = 'data/' + file_name

    # read data and store the information into your self-defined variables
    fp = open(file_path, 'r', newline = '')
    header = fp.readline() 
    reader = csv.reader(fp, delimiter = ',')

    LARGE_NUM = 0

    Processing_Time = []
    Machine_List = []
    Due_Time = []
    Job_n = 0
    for a_row in reader:
        Processing_Time.append([])
        Machine_List.append([])
        Due_Time.append([])

        job_id = int(a_row[0])
        Job_n += 1

        p_1 = float(a_row[1])
        p_2 = float(a_row[2])
        LARGE_NUM += p_1 + p_2
        
        Processing_Time[job_id-1].append(p_1)
        Processing_Time[job_id-1].append(p_2)

        m_1 = a_row[3].split(",")
        m_2 = a_row[4].split(",")
        m_int_1 = [int(i) for i in m_1]
        if m_2[0] == 'N/A':
            m_int_2 = []
        else:
            m_int_2 = [int(i) for i in m_2]
        Machine_List[job_id-1].append(m_int_1)
        Machine_List[job_id-1].append(m_int_2)

        d_2 = float(a_row[5])
        d_1 = d_2 - p_2
        Due_Time[job_id-1].append(d_1)
        Due_Time[job_id-1].append(d_2)

    Machine_n = max(max(max(j for j in i)) for i in Machine_List)

### start algorithm

# Step 1
    # Generate Already_tardy_Job_list
    Already_Tardy_Job_List = []
    for i in range(Job_n):
        if round(Processing_Time[i][0] + Processing_Time[i][1], 5) >= Due_Time[i][1]:
            Already_Tardy_Job_List.append(i)

# Step 2
    # Generate Job_list
    Job_List = []
    for i in range(Machine_n):
        Job_List.append([])
        for j in range(Job_n):
            if j in Already_Tardy_Job_List:
                continue
            job_machine_list = Machine_List[j]
            for k in job_machine_list[0]:
                if k == i + 1:
                    Job_List[i].append([j, 0]) # append the index in Machine_List
            for k in job_machine_list[1]:
                if k == i + 1:
                    Job_List[i].append([j, 1]) # append the index in Machine_List

    # Sorting Job_List
    for i in range(Machine_n):
        Job_List[i] = merge_sort(Job_List[i])

# Step 3
    # initialize
    machine = []
    completion_time = []
    for i in range(Job_n):
        machine.append([])
        machine[i].append(0)
        machine[i].append(0)
        completion_time.append([])
        completion_time[i].append(0)
        completion_time[i].append(0)


    machine_completed_jobs_stage = []
    accumulated_processing_time = []
    for i in range(Machine_n):
        machine_completed_jobs_stage.append([])
        accumulated_processing_time.append(0)

    # check for step 5
    all_job_list_empty = True
    for i in Job_List:
        if len(i) > 0:
            all_job_list_empty = False

    while not all_job_list_empty: # Step 5
        all_current_JS = []
        next_accumulated_PT = []
        for i in range(Machine_n):
            all_current_JS.append(0)
            next_accumulated_PT.append(LARGE_NUM)
        
        # check condition 1
        for i in range(Machine_n):
            if len(Job_List[i]) == 0:
                continue
            index = 0
            current_job_stage = Job_List[i][index]
            temp_accumulated_PT = accumulated_processing_time[i] + Processing_Time[current_job_stage[0]][current_job_stage[1]]
            finally_ok = False
            while not finally_ok:
                finally_ok = True
                # haven't start stage 1 
                while current_job_stage[1] == 1 and machine[current_job_stage[0]][0] == 0:
                    finally_ok = False
                    index += 1
                    if index >= len(Job_List[i]):
                        break
                    current_job_stage = Job_List[i][index]
                    temp_accumulated_PT = accumulated_processing_time[i] + Processing_Time[current_job_stage[0]][current_job_stage[1]]
                if index >= len(Job_List[i]):
                    break

                # started stage 1 but haven't finish yet
                while current_job_stage[1] == 1 and completion_time[current_job_stage[0]][0] > accumulated_processing_time[i]:
                    finally_ok = False
                    index += 1
                    if index >= len(Job_List[i]):
                        break
                    current_job_stage = Job_List[i][index]
                    temp_accumulated_PT = accumulated_processing_time[i] + Processing_Time[current_job_stage[0]][current_job_stage[1]]
                if index >= len(Job_List[i]):
                    break

            if index >= len(Job_List[i]):
                continue
            all_current_JS[i] = current_job_stage
            next_accumulated_PT[i] = temp_accumulated_PT


        # job and machine selection
        chosen_machine_index = 0
        reach_large_num_cnt = 0
        if next_accumulated_PT[0] == LARGE_NUM:
            reach_large_num_cnt += 1
        for i in range(1, Machine_n):
            if next_accumulated_PT[i] == LARGE_NUM:
                reach_large_num_cnt += 1
                continue
            if next_accumulated_PT[i] < next_accumulated_PT[chosen_machine_index]:
                chosen_machine_index = i
            elif next_accumulated_PT[i] == next_accumulated_PT[chosen_machine_index]:
                if Due_Time[all_current_JS[i][0]][all_current_JS[i][1]] < Due_Time[all_current_JS[chosen_machine_index][0]][all_current_JS[chosen_machine_index][1]]:
                    chosen_machine_index = i
                elif Due_Time[all_current_JS[i][0]][all_current_JS[i][1]] == Due_Time[all_current_JS[chosen_machine_index][0]][all_current_JS[chosen_machine_index][1]]:
                    if len(Job_List[i]) < len(Job_List[chosen_machine_index]):
                        chosen_machine_index = i
        # all reach large num (special case)
        if reach_large_num_cnt == Machine_n:
            break

# Step 4
        # (1) Job selected has a larger completion time than its due time.
        completed_job = all_current_JS[chosen_machine_index][0]
        completed_stage = all_current_JS[chosen_machine_index][1]
        
        if next_accumulated_PT[chosen_machine_index] > Due_Time[completed_job][completed_stage]:
            Already_Tardy_Job_List.append(completed_job)
            for j in range(Machine_n):
                if [completed_job, 0] in Job_List[j]:
                    Job_List[j].remove([completed_job, 0])
                if [completed_job, 1] in Job_List[j]:
                    Job_List[j].remove([completed_job, 1])
            if completed_stage == 1:
                deleted_machine_index = machine[completed_job][0] - 1
                reduction_PT = Processing_Time[completed_job][0]
                if [completed_job, 0] in machine_completed_jobs_stage[deleted_machine_index]:
                    deleted_index = machine_completed_jobs_stage[deleted_machine_index].index([completed_job, 0])
                    machine_completed_jobs_stage[deleted_machine_index].remove([completed_job, 0])
                    for j in range(deleted_index, len(machine_completed_jobs_stage[deleted_machine_index])):
                        to_adjust_job = machine_completed_jobs_stage[deleted_machine_index][j][0]
                        to_adjust_stage = machine_completed_jobs_stage[deleted_machine_index][j][1]
                        if to_adjust_stage == 1:
                            stage_1_completion_time = completion_time[to_adjust_job][0]
                            stage_2_processing_time = Processing_Time[to_adjust_job][1]
                            stage_2_completion_time = completion_time[to_adjust_job][1]
                            reduction_PT = min(reduction_PT, stage_2_completion_time - (stage_2_processing_time + stage_1_completion_time))
                        completion_time[to_adjust_job][to_adjust_stage] -= reduction_PT
                accumulated_processing_time[deleted_machine_index] -= reduction_PT
                machine[completed_job][0] = 0
                completion_time[completed_job][0] = 0
            continue

        # (2) Record the machine and CompleteTime of the selected job.
        machine[completed_job][completed_stage] = chosen_machine_index + 1
        completion_time[completed_job][completed_stage] = next_accumulated_PT[chosen_machine_index]
        machine_completed_jobs_stage[chosen_machine_index].append([completed_job, completed_stage])
        accumulated_processing_time[chosen_machine_index] += Processing_Time[completed_job][completed_stage]

        # (3) Remove the job in other machine’s job list.
        for i in range(Machine_n):
            if all_current_JS[chosen_machine_index] in Job_List[i]:
                Job_List[i].remove(all_current_JS[chosen_machine_index])

        # check for step 5
        all_job_list_empty = True
        for i in Job_List:
            if len(i) > 0:
                all_job_list_empty = False

# all reach large num (solve special case)
    all_job_list_empty = True
    for i in Job_List:
        if len(i) > 0:
            all_job_list_empty = False

    # continue the same process above
    while not all_job_list_empty:
        all_current_JS = []
        next_accumulated_PT = []
        for i in range(Machine_n):
            all_current_JS.append(0)
            next_accumulated_PT.append(LARGE_NUM)
        for i in range(Machine_n):
            if len(Job_List[i]) == 0:
                continue
            index = 0
            current_job_stage = Job_List[i][index]
            temp_accumulated_PT = accumulated_processing_time[i] + Processing_Time[current_job_stage[0]][current_job_stage[1]]

            # haven't start stage 1
            if current_job_stage[1] == 1 and machine[current_job_stage[0]][0] == 0:
                exit() # ???
            
            # started stage 1 but haven't finish yet
            elif current_job_stage[1] == 1 and completion_time[current_job_stage[0]][0] > accumulated_processing_time[i]: # Step 3 - 2
                temp_accumulated_PT = completion_time[current_job_stage[0]][0] + Processing_Time[current_job_stage[0]][current_job_stage[1]]

            # (1) job selected has a larger completion time than its due time
            while temp_accumulated_PT > Due_Time[current_job_stage[0]][current_job_stage[1]]:
                Already_Tardy_Job_List.append(current_job_stage[0])
                for j in range(Machine_n):
                    if [current_job_stage[0], 0] in Job_List[j]:
                        Job_List[j].remove([current_job_stage[0], 0])
                    if [current_job_stage[0], 1] in Job_List[j]:
                        Job_List[j].remove([current_job_stage[0], 1])
                if current_job_stage[1] == 1:
                    deleted_machine_index = machine[current_job_stage[0]][0] - 1
                    reduction_PT = Processing_Time[current_job_stage[0]][0]
                    if [current_job_stage[0], 0] in machine_completed_jobs_stage[deleted_machine_index]:
                        deleted_index = machine_completed_jobs_stage[deleted_machine_index].index([current_job_stage[0], 0])
                        machine_completed_jobs_stage[deleted_machine_index].remove([current_job_stage[0], 0])
                        for j in range(deleted_index, len(machine_completed_jobs_stage[deleted_machine_index])):
                            to_adjust_job = machine_completed_jobs_stage[deleted_machine_index][j][0]
                            to_adjust_stage = machine_completed_jobs_stage[deleted_machine_index][j][1]
                            if to_adjust_stage == 1:
                                stage_1_completion_time = completion_time[to_adjust_job][0]
                                stage_2_processing_time = Processing_Time[to_adjust_job][1]
                                stage_2_completion_time = completion_time[to_adjust_job][1]
                                reduction_PT = min(reduction_PT, stage_2_completion_time - (stage_2_processing_time + stage_1_completion_time))
                            completion_time[to_adjust_job][to_adjust_stage] -= reduction_PT
                        accumulated_processing_time[deleted_machine_index] -= reduction_PT
                    machine[current_job_stage[0]][0] = 0
                    completion_time[current_job_stage[0]][0] = 0
                
                index += 1
                if index >= len(Job_List[i]):
                    break
                current_job_stage = Job_List[i][index]
                temp_accumulated_PT = accumulated_processing_time[i] + Processing_Time[current_job_stage[0]][current_job_stage[1]]
            if index >= len(Job_List[i]):
                break
            all_current_JS[i] = current_job_stage
            next_accumulated_PT[i] = temp_accumulated_PT

        # job and machine selection
        chosen_machine_index = 0
        reach_large_num_cnt = 0
        if next_accumulated_PT[0] == LARGE_NUM:
            reach_large_num_cnt += 1
        for i in range(1, Machine_n):
            if next_accumulated_PT[i] == LARGE_NUM:
                reach_large_num_cnt += 1
                continue
            if next_accumulated_PT[i] < next_accumulated_PT[chosen_machine_index]:
                chosen_machine_index = i
            elif next_accumulated_PT[i] == next_accumulated_PT[chosen_machine_index]:
                if Due_Time[all_current_JS[i][0]][all_current_JS[i][1]] < Due_Time[all_current_JS[chosen_machine_index][0]][all_current_JS[chosen_machine_index][1]]:
                    chosen_machine_index = i
                elif Due_Time[all_current_JS[i][0]][all_current_JS[i][1]] == Due_Time[all_current_JS[chosen_machine_index][0]][all_current_JS[chosen_machine_index][1]]:
                    if len(Job_List[i]) < len(Job_List[chosen_machine_index]):
                        chosen_machine_index = i
        # all reach large num
        if reach_large_num_cnt == Machine_n:
            break
        
        # (2) Record the machine and CompleteTime of the selected job.
        completed_job = all_current_JS[chosen_machine_index][0]
        completed_stage = all_current_JS[chosen_machine_index][1]

        machine[completed_job][completed_stage] = chosen_machine_index + 1
        completion_time[completed_job][completed_stage] = next_accumulated_PT[chosen_machine_index]
        machine_completed_jobs_stage[chosen_machine_index].append([completed_job, completed_stage])
        accumulated_processing_time[chosen_machine_index] += Processing_Time[completed_job][completed_stage]

        # (3) Remove the job in other machine’s job list.
        for i in range(Machine_n):
            if all_current_JS[chosen_machine_index] in Job_List[i]:
                Job_List[i].remove(all_current_JS[chosen_machine_index])

        # check for step 5
        all_job_list_empty = True
        for i in Job_List:
            if len(i) > 0:
                all_job_list_empty = False

# Step 6 (similar to repeating the same process in step 2)
    # Step 2
        # Generate tardy jobs Job_List
    Job_List = []
    for i in range(Machine_n):
        Job_List.append([])
        for j in Already_Tardy_Job_List:
            job_machine_list = Machine_List[j]
            for k in job_machine_list[0]:
                if k == i + 1:
                    Job_List[i].append([j, 0]) # append the index in Machine_List
            for k in job_machine_list[1]:
                if k == i + 1:
                    Job_List[i].append([j, 1]) # append the index in Machine_List

        # Sorting Job_List
    for i in range(Machine_n):
        Job_List[i] = merge_sort_ATL(Job_List[i])

# Step 7 (similar to repeating the same process in step 3 ~ 5)
    # Step 3
        # check for step 5
    all_job_list_empty = True
    for i in Job_List:
        if len(i) > 0:
            all_job_list_empty = False

    while not all_job_list_empty: # Step 5

        # initialize
        all_current_JS = []
        next_accumulated_PT = []
        for i in range(Machine_n):
            all_current_JS.append(0)
            next_accumulated_PT.append(LARGE_NUM)
        
        # check condition 1
        for i in range(Machine_n):
            if len(Job_List[i]) == 0:
                continue
            index = 0
            current_job_stage = Job_List[i][index]
            temp_accumulated_PT = accumulated_processing_time[i] + Processing_Time[current_job_stage[0]][current_job_stage[1]]
            finally_ok = False
            while not finally_ok:
                finally_ok = True

                # haven't start stage 1 
                while current_job_stage[1] == 1 and machine[current_job_stage[0]][0] == 0:
                    finally_ok = False
                    index += 1
                    if index >= len(Job_List[i]):
                        break
                    current_job_stage = Job_List[i][index]
                    temp_accumulated_PT = accumulated_processing_time[i] + Processing_Time[current_job_stage[0]][current_job_stage[1]]
                if index >= len(Job_List[i]):
                    break

                # started stage 1 but haven't finish yet
                while current_job_stage[1] == 1 and completion_time[current_job_stage[0]][0] > accumulated_processing_time[i]:
                    finally_ok = False
                    index += 1
                    if index >= len(Job_List[i]):
                        break
                    current_job_stage = Job_List[i][index]
                    temp_accumulated_PT = accumulated_processing_time[i] + Processing_Time[current_job_stage[0]][current_job_stage[1]]
                if index >= len(Job_List[i]):
                    break

            if index >= len(Job_List[i]):
                continue
            all_current_JS[i] = current_job_stage
            next_accumulated_PT[i] = temp_accumulated_PT

        # job and machine selection
        chosen_machine_index = 0
        reach_large_num_cnt = 0
        if next_accumulated_PT[0] == LARGE_NUM:
            reach_large_num_cnt += 1
        for i in range(1, Machine_n):
            if next_accumulated_PT[i] == LARGE_NUM:
                reach_large_num_cnt += 1
                continue
            if next_accumulated_PT[i] < next_accumulated_PT[chosen_machine_index]:
                chosen_machine_index = i
            elif next_accumulated_PT[i] == next_accumulated_PT[chosen_machine_index]:
                if len(Job_List[i]) < len(Job_List[chosen_machine_index]):
                    chosen_machine_index = i
        # all reach large num (special case)
        if reach_large_num_cnt == Machine_n:
            break

        # (2) Record the m and CompleteTime of the selected job.
        completed_job = all_current_JS[chosen_machine_index][0]
        completed_stage = all_current_JS[chosen_machine_index][1]

        machine[completed_job][completed_stage] = chosen_machine_index + 1
        completion_time[completed_job][completed_stage] = next_accumulated_PT[chosen_machine_index]
        machine_completed_jobs_stage[chosen_machine_index].append([completed_job, completed_stage])
        accumulated_processing_time[chosen_machine_index] += Processing_Time[completed_job][completed_stage]

        # (3) Remove the job in other machine’s job list.
        for i in range(Machine_n):
            if all_current_JS[chosen_machine_index] in Job_List[i]:
                Job_List[i].remove(all_current_JS[chosen_machine_index])

        # check for step 5
        all_job_list_empty = True
        for i in Job_List:
            if len(i) > 0:
                all_job_list_empty = False

    # all reach large num (special case)
    all_job_list_empty = True
    for i in Job_List:
        if len(i) > 0:
            all_job_list_empty = False
    
    # continue the same process above
    while not all_job_list_empty:
        all_current_JS = []
        next_accumulated_PT = []
        for i in range(Machine_n):
            all_current_JS.append(0)
            next_accumulated_PT.append(LARGE_NUM)
        for i in range(Machine_n):
            if len(Job_List[i]) == 0:
                continue
            index = 0
            current_job_stage = Job_List[i][index]
            temp_accumulated_PT = accumulated_processing_time[i] + Processing_Time[current_job_stage[0]][current_job_stage[1]]
            if current_job_stage[1] == 1 and machine[current_job_stage[0]][0] == 0: # Step 3 - 2
                exit()
            elif current_job_stage[1] == 1 and completion_time[current_job_stage[0]][0] > accumulated_processing_time[i]: # Step 3 - 2
                temp_accumulated_PT = completion_time[current_job_stage[0]][0] + Processing_Time[current_job_stage[0]][current_job_stage[1]]
            all_current_JS[i] = current_job_stage
            next_accumulated_PT[i] = temp_accumulated_PT

        chosen_machine_index = 0
        reach_large_num_cnt = 0
        if next_accumulated_PT[0] == LARGE_NUM:
            reach_large_num_cnt += 1
        for i in range(1, Machine_n):
            if next_accumulated_PT[i] == LARGE_NUM:
                reach_large_num_cnt += 1
                continue
            if next_accumulated_PT[i] < next_accumulated_PT[chosen_machine_index]:
                chosen_machine_index = i
            elif next_accumulated_PT[i] == next_accumulated_PT[chosen_machine_index]:
                if len(Job_List[i]) < len(Job_List[chosen_machine_index]):
                    chosen_machine_index = i
        if reach_large_num_cnt == Machine_n: # all reach large num
            break

        completed_job = all_current_JS[chosen_machine_index][0]
        completed_stage = all_current_JS[chosen_machine_index][1]

        machine[completed_job][completed_stage] = chosen_machine_index + 1
        completion_time[completed_job][completed_stage] = next_accumulated_PT[chosen_machine_index]
        machine_completed_jobs_stage[chosen_machine_index].append([completed_job, completed_stage])
        accumulated_processing_time[chosen_machine_index] += Processing_Time[completed_job][completed_stage]

        for i in range(Machine_n):
            if all_current_JS[chosen_machine_index] in Job_List[i]:
                Job_List[i].remove(all_current_JS[chosen_machine_index])

        all_job_list_empty = True
        for i in Job_List:
            if len(i) > 0:
                all_job_list_empty = False
'''
# count tardy and makespan
    tardy_cnt = 0
    for i in range(Job_n):
        if completion_time[i][1] > Due_Time[i][1]:
            tardy_cnt += 1

    makespan = max(i for i in accumulated_processing_time)

    print("\n-------------\n")
    print("tardy =", tardy_cnt)
    print("makespan =", makespan)
    print("")
'''
# return machine, completion_time