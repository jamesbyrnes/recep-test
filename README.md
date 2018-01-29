# Coding Test - Directed graph route calculator

This is a set of tools used to calculate various aspects of a unidirectional directed graph.

The below discusses the contents of the repo and how to use the test files and CLI interface. The rest of the code is documented inside of the source code files themselves.

## Files
This repo consists of seven files:
* main.py - This file, intended to be used as a CLI frontend for the calculator.
* main_test.py - Unit test file for main.py
* graph.py - Class file for the directed graph data structure, including all of the calculation methods.
* graph_test.py - Unit test file for graph.py
* queues.py - Queue data structures for use with the directed graph.  Includes a simple queue data structure as well as a priority queue.  Currently only the priority queue is used, with the simple queue kept for posterity.
* queues_test.py - Unit test file for queues.py
* README.md - Recommended reading for more information

## Running tests
Tests can be run by calling the \*\_test.py file directly for the respective .py file.

The output tests as specified in the original text file (trains.txt) is available under graph_test.py, under the class StationGraphAdvCalcTestCases.

## Using the CLI
You can build a graph and run calculations through the CLI using main.py. 

The basic template for a CLI argument is formatted as follows:
```
./main.py -l CONN1,CONN2,CONN3... {function} FUNCTION_ARGS...
```
Where CONN1, etc. are graph connection arguments (represented by two letters and a number, e.g. AB1).

The four function args are as follows:

**route** - Gives the total distance of a specific route - i.e. all points of the route traversed must be specified -- if A>B>C is possible but A>C is not, asking for A>C will *not* give you A>B>C.

Arguments:
* (nodes) - A comma-separated list of node names.
```
./main.py -l AB1,BC1 route A,B,C
> output: 2
./main.py -l AB1,BC1 route A,C
> output: NO SUCH ROUTE
```

**movetrips** - Gives the total number of trips that can be made between two points within a certain number of moves. You can also provide a minimum number of moves.

Arguments:
* (nodes) - A comma-separated pair of node names.
* **--minimum**, **-m** - The minimum threshold of moves before we begin counting trips. Defaults to 1.
* **--maximum**, **-M** - The maximum threshold of moves where we stop counting trips. Stops counting where the total distance is **less than or equal to** this argument.
```
./main.py -l AB1,BC1,AC1 movetrips A,C --maximum 1
> output: 1
```

**disttrips** - Gives the total number of trips that can be made between two points within a certain distance. You can also provide a minimum distance.

Arguments:
* (nodes) - A comma-separated pair of node names.
* **--minimum**, **-m** - The minimum threshold of distance before we begin counting trips. Defaults to 1.
* **--maximum**, **-M** - The maximum threshold of distance where we stop counting trips. Stops counting where the total distance is **less than** this argument.
```
./main.py -l AB10,AC1,CB1 disttrips A,B --maximum 9
> output: 1
```

**mindist** - Gets the shortest total distance between two points using Dijkstra's algorithm. This version is modified to allow for a route that traverses back to the origin if such a route is possible.

Arguments:
* (nodes) - A comma-separated pair of node names.
```
./main.py -l AB10,AC1,CB1 mindist A,B
> output: 2
```
