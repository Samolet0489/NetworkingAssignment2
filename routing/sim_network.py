#!/usr/bin/env python3
import sys
from multiprocessing import Process, Queue


def init_node(node_name, queue, neighbour_queues):
    """
    Initializes a node in the network
    :param node_name: The name of the node
    :param queue: The queue of the node
    :param neighbour_queues: The queues of the neighbours of the node
    :return:
    """
    print(f'[{node_name}]: Sending HELLO to all neighbours...')
    for neighbour in neighbour_queues:
        neighbour_queues[neighbour].put((node_name, 'HELLO'))

    print(f'[{node_name}]: Waiting for packets...')
    wait_for_packets(node_name, queue)


def wait_for_packets(node_name, queue):
    """
    Waits for incoming packets to arrive
    :param node_name: Name of the node
    :param queue The queue of the current node
    :return:
    """
    while True:
        node_from, packet = queue.get()
        print(f'[{node_name}]: received \'{packet}\' from {node_from}')


def start_network(adj_matrix):
    """
    Starts the simulated network
    :param adj_matrix: The adjacency matrix for each node
    :return:
    """
    queues = {}
    for node in adj_matrix:
        node_queue = Queue()
        queues[node] = node_queue

    node_processes = []
    for node in adj_matrix:
        neighbour_queues = {}
        for neighbour in adj_matrix[node]:
            neighbour_queues[neighbour] = queues[neighbour]
        node_process = Process(target=init_node, args=(node, queues[node], neighbour_queues))
        node_process.daemon = True
        node_process.start()
        node_processes.append(node_process)

    return node_processes


def read_adj_matrix(filename):
    """
    Reads the adjacency matrix of the network graph from a file
    :param filename: The file name
    :return:
    """
    adj_matrix = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        if len(lines) == 0:
            return None
        for line in lines[1:]:
            split_line = line.split()
            node_name = split_line[0]
            node_list = split_line[1:]
            adj_matrix[node_name] = node_list

    return adj_matrix


if __name__ == "__main__":
    file_name = sys.argv[1]
    adj_matrix = read_adj_matrix(file_name)
    print(adj_matrix)
    node_processes = start_network(adj_matrix)
    for process in node_processes:
        process.join()




