import random

''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''
'''
                For Search Algorithms 
'''
''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''

# Define Global variables used for search algorithms

bQueue = []
dQueue = []
uQueue = []
aQueue = []

'''
BFS add to queue 
'''
def add_to_queue_BFS(node_id, parent_node_id, cost, initialize=False):
     bQueue.append((node_id, parent_node_id)) 
     return

'''
BFS add to queue 
'''
def is_queue_empty_BFS():
    if not bQueue:
        return True
    else:
        return False

'''
BFS pop from queue
'''
def pop_front_BFS():
    (node_id, parent_node_id) = bQueue.pop(0)
    return (node_id, parent_node_id)

'''
DFS add to queue 
'''
def add_to_queue_DFS(node_id, parent_node_id, cost, initialize=False):
    dQueue.insert(0, (node_id,parent_node_id))
    return

'''
DFS add to queue 
'''
def is_queue_empty_DFS():
    if not dQueue:
        return True
    else:
        return False

'''
DFS pop from queue
'''
def pop_front_DFS():
    (node_id, parent_node_id) = dQueue.pop(0)
    return (node_id, parent_node_id)
    
'''
UC add to queue 
'''
def add_to_queue_UC(node_id, parent_node_id, cost, initialize=False):
    if initialize:
        uQueue.append((node_id, parent_node_id, cost))
    else:
        x = len(uQueue)
        for index in range(x):
            if cost < uQueue[index][2]:
                uQueue.insert(index, (node_id, parent_node_id, cost))
                break
    uQueue.append((node_id, parent_node_id, cost))
    return

'''
UC add to queue 
'''
def is_queue_empty_UC():
    if not uQueue:
        return True
    else:
        return False

'''
UC pop from queue
'''
def pop_front_UC():
    (node_id, parent_node_id, cost) = uQueue.pop(0)
    return (node_id, parent_node_id)

'''
A* add to queue 
'''
def add_to_queue_ASTAR(node_id, parent_node_id, cost, initialize=False):
    if initialize:
        del aQueue[:] #Assures that list is empty before start
        aQueue.append((node_id, parent_node_id, cost))
    else:
        x = len(aQueue)
        for i in range(x):
            if cost < aQueue[i][2]:
                aQueue.insert(i, (node_id, parent_node_id, cost))
                break
        aQueue.append((node_id, parent_node_id, cost))
    return

'''
A* add to queue 
'''
def is_queue_empty_ASTAR():
    if not aQueue:
        return True
    else:
        return False

'''
A* pop from queue
'''
def pop_front_ASTAR():
    (node_id, parent_node_id, cost) = aQueue.pop(0)
    return (node_id, parent_node_id)

''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''
'''
                For n-queens problem 
'''
''' ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ '''


'''
Compute a random state 
'''
def get_random_state(n):
    state = []

    if (n <= 0):
        print ("Entered 0x0 configuration. No result.")
        return state

    for i in range(n):
        r_num  = random.randint(1,n)
        state.append(r_num)
    return state

'''
Compute pairs of queens in conflict 
'''
def compute_attacking_pairs(state):
    number_attacking_pairs = 0

    state_len = len(state)

    #Declare empty table
    table = [[] for nothing in range(state_len)]

    row = 0
    #Initialize empty table
    while (row <= (state_len-1)):
        for i in range(state_len):
            table[row].append('')
        row+=1
    

    #Queen addition.
    for j in range(state_len):
        rowVal = state[j] - 1
        table[rowVal][j] = 'Q'



    #Compute Attacks: diagonal
    counter = 0
    diagonal_conflicts_upper = 0
    diagonal_conflicts_lower = 0
    for qCol_table in range (state_len-1):
        qRow_table = state[counter]-1


        subTable_r = qRow_table-1
        subTable_c = qCol_table+1
        while(subTable_r >=0 and subTable_c <= state_len-1):
            if (table[subTable_r][subTable_c] == table[qRow_table][qCol_table]):
                diagonal_conflicts_upper+=1
            subTable_r-=1
            subTable_c+=1


        subTable_r = qRow_table + 1
        subTable_c = qCol_table + 1
        while(subTable_r <= (state_len-1) and subTable_c <= (state_len-1)):
            if (table[subTable_r][subTable_c] == table[qRow_table][qCol_table]):
                diagonal_conflicts_lower+=1
            subTable_c+=1
            subTable_r+=1
        counter +=1

    totalDiagConflicts = diagonal_conflicts_lower + diagonal_conflicts_upper


    #Compute attacks: Horizontal

    horiConflicts = 0

    for index in range(state_len):
        current = state[index]

        newState = state[index+1:]

        for newRange in range(len(newState)):
            if newState[newRange] == current:
                horiConflicts+=1


    totalConflicts = horiConflicts + totalDiagConflicts


    number_attacking_pairs = totalConflicts


    return number_attacking_pairs

'''
The basic hill-climing algorithm for n queens
'''
def hill_desending_n_queens(state, comp_att_pairs):
    final_state = []
    new_state = []

    state_len = len(state)

    conflicts = comp_att_pairs(state)
    new_conflicts = conflicts
    smallest_conflict = conflicts - 1

    minCol = 0
    minRow = 0

    while(1):

        smallest_conflict = comp_att_pairs(state)
        column = 0

        for column in range(state_len-1):
            value = state[column] - 1
            #print "original_value:", original_value

            for new_row_position in range(state_len-1):
                state[column] = new_row_position+1
                testMin = comp_att_pairs(state)

                if (smallest_conflict>testMin):
                    smallest_conflict = testMin
                    minCol = column
                    minRow = new_row_position
            state[column] = value + 1

        state[minCol] = minRow + 1

        if (smallest_conflict==0):
            break
        elif (smallest_conflict==conflicts):
            break
        else:
            conflicts = smallest_conflict

    final_state = state
    return final_state

'''
Hill-climing algorithm for n queens with restart
'''
def n_queens(n, get_rand_st, comp_att_pairs, hill_descending):
    final_state = []
    conflicts = n

    if n==3:
        state = get_rand_st(n)
        final_state = hill_descending(state, comp_att_pairs)
        conflicts = comp_att_pairs(final_state)
    elif n>3:
        while(conflicts!=0):
            state = get_rand_st(n)
            final_state = hill_descending(state, comp_att_pairs)
            conflicts = comp_att_pairs(final_state)


    return final_state






