# Student name: Xujie Yuan

import math
import sys
import copy

# input_file = sys.argv[1]
# output_file = sys.argv[2]
input_file = './INPUT/input4.txt'
output_file = './OUTPUT/output3.txt'
flag = 7


class Node:
    def __init__(self, parent=None, node_id=0):
        self.parent = parent
        self.id = node_id
        self.g = 0
        self.h = 0
        self.f = self.g + self.h
        self.path = None


def read_map():
    file_input = open(input_file)
    n = int(file_input.readline())
    map_list = []
    count = 0
    while count <= n:
        for node in file_input.readline():
            if node != '\n' and node != '\r':
                map_list.append(node)
        count += 1
    map1 = list_split(map_list, n)
    return [n, map1]


def list_split(nodes, j):
    return [nodes[i:i + j] for i in range(0, len(nodes), j)]


size = read_map()[0]

map_from_file = read_map()[1]


def get_id(x, y):
    return y * size + x


def find_child(node_id):
    child = []
    if find_down_child(node_id) is not None:
        child.append(find_down_child(node_id))
    if find_up_child(node_id) is not None:
        child.append(find_up_child(node_id))
    if find_left_child(node_id) is not None:
        child.append(find_left_child(node_id))
    if find_right_child(node_id) is not None:
        child.append(find_right_child(node_id))
    if find_left_up_child(node_id) is not None:
        child.append(find_left_up_child(node_id))
    if find_right_up_child(node_id) is not None:
        child.append(find_right_up_child(node_id))
    if find_left_down_child(node_id) is not None:
        child.append(find_left_down_child(node_id))
    if find_right_down_child(node_id) is not None:
        child.append(find_right_down_child(node_id))
    return child


def find_down_child(node_id):
    y = node_id // size
    x = node_id % size
    x_down = x
    y_down = y + 1
    if y_down < size:
        if map_from_file[y_down][x_down] != 'X':
            return get_id(x_down, y_down)


def find_up_child(node_id):
    y = node_id // size
    x = node_id % size
    x_up = x
    y_up = y - 1
    if y_up >= 0:
        if map_from_file[y_up][x_up] != 'X':
            return get_id(x_up, y_up)


def find_left_child(node_id):
    y = node_id // size
    x = node_id % size
    x_left = x - 1
    y_left = y
    if x_left >= 0:
        if map_from_file[y_left][x_left] != 'X':
            return get_id(x_left, y_left)


def find_right_child(node_id):
    y = node_id // size
    x = node_id % size
    x_right = x + 1
    y_right = y
    if x_right < size:
        if map_from_file[y_right][x_right] != 'X':
            return get_id(x_right, y_right)


def find_left_up_child(node_id):
    y = node_id // size
    x = node_id % size
    x_lu = x - 1
    y_lu = y - 1
    if x_lu >= 0 and y_lu >= 0:
        if map_from_file[y_lu][x_lu] != 'X':
            if map_from_file[y - 1][x] != 'X' and map_from_file[y][x - 1] != 'X':
                return get_id(x_lu, y_lu)


def find_right_up_child(node_id):
    y = node_id // size
    x = node_id % size
    x_ru = x + 1
    y_ru = y - 1
    if y_ru >= 0 and x_ru < size:
        if map_from_file[y_ru][x_ru] != 'X':
            if map_from_file[y - 1][x] != 'X' and map_from_file[y][x + 1] != 'X':
                return get_id(x_ru, y_ru)


def find_left_down_child(node_id):
    y = node_id // size
    x = node_id % size
    x_ld = x - 1
    y_ld = y + 1
    if x_ld >= 0 and y_ld < size:
        if map_from_file[y_ld][x_ld] != 'X':
            if map_from_file[y][x - 1] != 'X' and map_from_file[y + 1][x] != 'X':
                return get_id(x_ld, y_ld)


def find_right_down_child(node_id):
    y = node_id // size
    x = node_id % size
    x_rd = x + 1
    y_rd = y + 1
    if x_rd < size and y_rd < size:
        if map_from_file[y_rd][x_rd] != 'X':
            if map_from_file[y + 1][x] != 'X' and map_from_file[y][x + 1] != 'X':
                return get_id(x_rd, y_rd)


def find_xy(str_test):
    count = 0
    for lines in map_from_file:
        if str_test in lines:
            return count, lines.index(str_test)
        count += 1


def find_xy_by_id(node):
    return node // size, node % size


def find_min_f(nodes_list):
    min_f_node = nodes_list[0]
    for node in nodes_list:
        if node.f < min_f_node.f:
            min_f_node = node
    return min_f_node


def calculate_h(node1_id, node2_id):
    node1_id_xy = (node1_id // size, node1_id % size)
    node2_id_xy = (node2_id // size, node2_id % size)
    # p = 1 / size
    x = abs(node1_id_xy[0] - node2_id_xy[0])
    y = abs(node1_id_xy[1] - node2_id_xy[1])
    h = math.sqrt(x * x + y * y)
    # if x > y:
    # x, y = y, x
    return h


def console_output(node):
    console_g = get_path_list(st_id, node)[1]
    console_h = calculate_h(ed_id, node)
    console_f = console_g + console_h
    console_path_tmp = get_path_list(st_id, node)[0]
    console_path = ''
    for j in console_path_tmp:
        console_path += 'N' + str(j) + ' '
    return 'N' + str(node) + ':' + "%.2f" % float(console_g) + ' ' + "%.2f" % float(console_h) + ' ' + "%.2f" % float(
        console_f) + ' ' + str(calculate_route(node))


def normal_output(node):
    console_g = get_path_list(st_id, node)[1]
    console_path_tmp = get_path_list(st_id, node)[0]
    console_path = ''
    for j in console_path_tmp:
        console_path += 'N' + str(j) + ' '
    return 'N' + str(node) + ':' + str(console_g) + ' ' + 'S-' + str(calculate_route(node)) + '-G' + ' ' + str(
        console_path)


def get_path_list(start_node_id, goal_id):
    start_node = Node(None, start_node_id)
    start_node.f = 0
    start_node.g = 0
    start_node.h = 0

    goal_node = Node(None, goal_id)
    open_list = []
    close_list = []
    open_list_id = []
    close_list_id = []
    open_list.append(start_node)
    open_list_id.append(start_node.id)
    children_console = []
    open_list_console = []
    close_list_console = []
    temp_open_list = []
    temp_close_list = []
    current_visited = []
    while True:

        if not open_list:
            return "CAN NOT ARRIVE"

        current_node = find_min_f(open_list)
        open_list.remove(current_node)
        open_list_id.remove(current_node.id)
        close_list.append(current_node)
        if current_node.id not in close_list_id:
            close_list_id.append(current_node.id)
        # if goal found
        if current_node.id == goal_id:
            open_list_id = {}
            for i in open_list:
                open_list_id[i.id] = i.g
            close_list_id = {}
            for i in close_list:
                close_list_id[i.id] = i.g
            path = []
            final_g = current_node.g
            final_f = current_node.f
            final_h = current_node.h
            tem_node = current_node
            while tem_node is not None:
                path.append(tem_node.id)
                tem_node = tem_node.parent
            return path[
                   ::-1], final_g, final_h, final_f, children_console, open_list_console, close_list_console, current_visited

        neighbours = find_child(current_node.id)
        # print(neighbours)
        neighbours_node = []
        for neighbour_id in neighbours:
            neighbours_node.append(Node(None, neighbour_id))
        for neighbour in neighbours_node:
            if neighbour.id in close_list_id:
                continue
            for opened in open_list:
                if neighbour.id == opened.id:
                    if neighbour.g >= opened.g:
                        continue
            if abs(current_node.id - neighbour.id) == 1 or abs(current_node.id - neighbour.id) == size:
                neighbour.g = current_node.g + 2
                neighbour.h = calculate_h(neighbour.id, goal_id)
                neighbour.f = neighbour.g + neighbour.h
                neighbour.parent = current_node
            else:
                neighbour.g = current_node.g + 1
                neighbour.h = calculate_h(neighbour.id, goal_id)
                neighbour.f = neighbour.g + neighbour.h
                neighbour.parent = current_node
            open_list.append(neighbour)
            open_list_id.append(neighbour.id)
        children_console.append(neighbours)
        temp_open_list = copy.deepcopy(open_list_id)
        open_list_console.append(list(set(temp_open_list)))
        temp_close_list = copy.deepcopy(close_list_id)
        close_list_console.append(temp_close_list)
        current_visited.append(current_node.id)


def console_output_all():
    count = 0
    for k in static_console_output[-1]:  # range(int(flag)):
        print(console_output(int(k)))
        print('Children:{')
        for l in static_console_output[-4][count]:
            print(console_output(int(l)))
        print('}')
        print('Open_list:{')
        for l in static_console_output[-3][count]:
            print(console_output(int(l)))
        print('}')
        print('Close_list:{')
        for l in static_console_output[-2][count]:
            print(console_output(int(l)))
        print('}')
        print('')
        count += 1



def calculate_route(node):
    path1 = get_path_list(st_id, node)[0]
    global route1
    for n in path1:
        route1 = []
        index = 0
        while index <= (len(path1) - 2):
            if (path1[index + 1] - path1[index]) == 1:
                route1.append('R')
            elif (path1[index + 1] - path1[index]) == -1:
                route1.append('L')
            elif (path1[index + 1] - path1[index]) == size:
                route1.append('D')
            elif (path1[index + 1] - path1[index]) == -size:
                route1.append('U')
            elif (path1[index + 1] - path1[index]) == -size + 1:
                route1.append('RU')
            elif (path1[index + 1] - path1[index]) == -size - 1:
                route1.append('LU')
            elif (path1[index + 1] - path1[index]) == size + 1:
                route1.append('RD')
            elif (path1[index + 1] - path1[index]) == size - 1:
                route1.append('LD')
            index += 1
    return str('-'.join(route1))


if __name__ == '__main__':
    st_id = get_id(find_xy('S')[1], find_xy('S')[0])
    ed_id = get_id(find_xy('G')[1], find_xy('G')[0])
    path = get_path_list(st_id, ed_id)[0]
    cost = get_path_list(st_id, ed_id)[1]
    static_console_output = get_path_list(st_id, ed_id)
    f = open(output_file, "w")
    if get_path_list(st_id, ed_id) == "CAN NOT ARRIVE":
        print("NO-PATH")
        f.write("NO-PATH")
    else:
        console_output_all()
        route = []
        idx = 0
        while idx <= (len(path) - 2):
            if (path[idx + 1] - path[idx]) == 1:
                route.append('R')
            elif (path[idx + 1] - path[idx]) == -1:
                route.append('L')
            elif (path[idx + 1] - path[idx]) == size:
                route.append('D')
            elif (path[idx + 1] - path[idx]) == -size:
                route.append('U')
            elif (path[idx + 1] - path[idx]) == -size + 1:
                route.append('RU')
            elif (path[idx + 1] - path[idx]) == -size - 1:
                route.append('LU')
            elif (path[idx + 1] - path[idx]) == size + 1:
                route.append('RD')
            elif (path[idx + 1] - path[idx]) == size - 1:
                route.append('LD')
            idx += 1
        # print("Route:{S-", '-'.join(route), "-G}")
        if not route:
            output_route = "No path"
        else:
            output_route = str('-'.join(route))
        output_path = str(path)
        f.write("Route is ")
        f.write("S-")
        f.write(output_route)
        f.write("-G")
        f.write('\n')
        f.write("Path is ")
        f.write(output_path)
        f.write('\n')
        for steps in range(len(static_console_output[0])):
            f.write(normal_output(int(static_console_output[0][steps])))
            f.write('\n')
            temp_map = copy.deepcopy(read_map()[1])
            temp_map[find_xy_by_id(int(static_console_output[0][steps]))[0]][
                find_xy_by_id(int(static_console_output[0][steps]))[1]] = '*'
            for lines in temp_map:
                for element in lines:
                    f.write(str(element))
                f.write('\n')
            f.write('\n')
        f.close()
