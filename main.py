#!/bin/python3
"""
CODING TEST FOR RECEPTIVITI.AI - DIRECTED GRAPH ROUTE CALCULATOR
Created by James Byrnes <mail@jamesbyrnes.ca>, January 2018

This repo consists of seven files:
    main.py - This file, intended to be used as a CLI frontend for the 
        calculator.
    main_test.py - Unit test file for main.py
    graph.py - Class file for the directed graph data structure, including
        all of the calculation methods.
    graph_test.py - Unit test file for graph.py
    queues.py - Queue data structures for use with the directed graph.
        Includes a simple queue data structure as well as a priority queue.
        Currently only the priority queue is used, with the simple queue
        kept for posterity.
    queues_test.py - Unit test file for queues.py
    README.md - Recommended reading for more information
"""

import argparse, sys
from graph import StationGraph

def get_arg_parser(args):
    """
    Returns the argument parser for the program.

    Arguments:
        args - The arguments to be parsed

    Returns:
        argparse.ArgumentParser - the argument parser as set up
            for this program.
    """
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')

    # argparse seems to be very touchy, so for our main argument
    # (i.e. the list of graph connections), we should specify the flag
    # -l or --list... this also opens up the opportunity to allow for
    # file inputs down the road...
    required_group = parser.add_argument_group("required arguments")
    required_group.add_argument('-l', '--list', type=str, nargs=None, 
            metavar='CONN1,CONN2,CONN3...', 
            help='A comma-separated listing of graph connections', 
            required=True)

    # POSITIONAL ARGUMENTS
    # 'route' takes an arbitrarily long comma-separated list of node
    # names and returns StationGraph method get_distance_by_route()
    sp_route = subparser.add_parser('route')
    sp_route.add_argument('nodes', metavar='NODE1,NODE2,NODE3...', type=str, 
            nargs=None)

    # 'movetrips' take a maximum of three arguments - a comma-separated pair
    # of node names (i.e. node_from and node_to), a --min number of moves 
    # before trips get counted, and a mandatory --max number of moves to be 
    # counting trips for. Returns StationGraph method num_trips_by_moves()
    sp_move_trips = subparser.add_parser('movetrips')
    sp_move_trips.add_argument('nodes', metavar='ORIGIN,DESTINATION', 
            type=str, nargs=None)
    sp_move_trips.add_argument('-m', '--minimum', metavar='STEPS', 
            type=int, nargs=None, default=1)
    sp_move_trips.add_argument('-M', '--maximum', metavar='STEPS',
            type=int, nargs=None, required=True)

    # 'disttrips' take a maximum of three arguments - a comma-separated pair
    # of node names (i.e. node_from and node_to), a --min distance
    # before trips get counted, and a mandatory --max distance to be 
    # counting trips for. Returns StationGraph method num_trips_by_distance()
    sp_dist_trips = subparser.add_parser('disttrips')
    sp_dist_trips.add_argument('nodes', metavar='ORIGIN,DESTINATION',
            type=str, nargs=None)
    sp_dist_trips.add_argument('-m', '--minimum', metavar='DISTANCE', 
            type=int, nargs=None, default=1)
    sp_dist_trips.add_argument('-M', '--maximum', metavar='DISTANCE',
            type=int, nargs=None, required=True)

    # 'route' takes a comma-separated pair of node names (i.e node_from and 
    # node_to) names and returns StationGraph method min_route_distance()
    sp_min_dist = subparser.add_parser('mindist')
    sp_min_dist.add_argument('nodes', metavar='ORIGIN,DESTINATION',
            type=str, nargs=None)

    return parser.parse_args(args)

def argument_handler(arguments):
    """
    Argument handler - takes the built argument set from argparse and builds
        what is necessary to make a StationGraph object and call the 
        appropriate method from it.

    Arguments:
        arguments - the argparse arguments set, passed from main()

    Returns:
        output - the output from the StationGraph object
    """
    # List of connections to construct the graph
    connection_list = arguments.list.split(',')
    # List of nodes to be traversed for the StationGraph methods
    node_name_list = arguments.nodes.split(',')

    station_graph = StationGraph(connection_list)
    
    output = ''

    # Method calls on the StationGraph object
    if arguments.command == 'route':
        output = station_graph.get_distance_by_route(node_name_list)
    elif arguments.command == 'movetrips':
        output = station_graph.num_trips_by_moves(node_name_list[0],
                node_name_list[1], arguments.minimum, 
                arguments.maximum)
    elif arguments.command == 'disttrips':
        output = station_graph.num_trips_by_distance(node_name_list[0],
                node_name_list[1], arguments.minimum, 
                arguments.maximum)
    elif arguments.command == 'mindist':
        output = station_graph.min_route_distance(node_name_list[0],
                node_name_list[1])

    return output

def main():
    """
    Main entry method for this file. Intended to be used as a CLI frontend.
    """
    parsed_args = get_arg_parser(sys.argv[1:])

    output = argument_handler(parsed_args)

    print(output)

if __name__ == '__main__':
    main()
