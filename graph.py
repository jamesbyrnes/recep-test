from queues import PriorityQueue

class StationGraph:
    """
    A class representing a graph of train stations and their connections.

    The private dictionary _nodes contains:
        keys - The names of each station (node) in the network.
        values - Another dict containing the name of each station (node) that
            station connects to (key), as well as the distance to that station
            (value).
    """
    def __init__(self, connection_list):
        """
        Initialize the _nodes dictionary with a user-provided list of station
            connections.

        Arguments:
            connection_list - A list of connection sets, each item consisting of
                two station names and the distance between the stations - e.g.
                'AB2'. The node names can only be one character each in this
                format. The distance number can be any length. Throws a ValueError
                if any item in the list has fewer than 3 characters.
        """
        self._nodes = {}
        for connection in connection_list:
            if len(connection) < 3:
                raise ValueError("Expected a connection list item with a " \
                        "length of 3 or more but got a length of {:d} "\
                        "instead.".format(len(connection)))
            self.add_connection(connection[0], connection[1], connection[2:])

    def get(self, key):
        """
        Returns the value of a given station key, else None if the key is not
            in the object.

        Arguments:
            key - The key to retrieve the value for.
        Returns:
            dict - The dict of connections associated with the key.
        """
        try:
            return self._nodes[key]
        except KeyError:
            return None

    def get_vertices(self):
        """
        Returns a list of the vertices in this graph. Returns an empty list
            if empty.

        Returns:
            list - all vertices in this graph. [] if empty.
        """
        if self._nodes == {}:
            return []
        return list(self._nodes.keys())

    def add_connection(self, node_from, node_to, distance):
        """
        Adds a single, unidirectional connection from any station to any other
            station. Stations that do not exist will be created and added to
            _nodes.

        Arguments:
            node_from - The origin of the connection between two stations.
            node_to - The destination of the connection between two stations. Will
                throw a ValueError if this has the same name as node_from.
            distance - The distance between the two stations being connected. Will
                throw a ValueError if the argument provided is not an int or
                the int is <=0.
        """
        if node_from == node_to:
            raise ValueError("Connection attempted between a node and " \
                    "itself: {:s} and {:s}".format(node_from, node_to))

        if self.get(node_from) is None:
            self._nodes[node_from] = {}
        if self.get(node_to) is None:
            self._nodes[node_to] = {}

        try:
            distance = int(distance)
        except ValueError:
            raise ValueError("Expected connection distance as an int but " \
                    "received {:s} instead".format(type(distance).__name__))
        else:
            if distance <= 0:
                raise ValueError("Distance of connection is zero or negative")
        self._nodes[node_from][node_to] = distance

    def are_adjacent(self, node_from, node_to):
        """
        Indicates whether or not two given nodes (specified by name) are
            connected.

        Arguments:
            node_from - The origin point of the connection being queried.
            node_to - The destination of the connection being queried.

        Returns:
            boolean - True if the two nodes named are directly connected
                to each other, False if they are not, or if one of the two
                nodes doesn't exist.
        """
        if self.get(node_from) is None or self.get(node_to) is None:
            return False
        return node_to in self.get(node_from).keys()

    def get_distance_by_route(self, route):
        """
        Provides the total distance between an arbitrary number of named
            nodes.

        Arguments:
            route - A list containing the individual node names, which is the
                route to be traversed.

        Returns:
            string - The total distance along the route provided, or
                'NO SUCH ROUTE' if the route cannot be followed as specified,
                or if any points along the specified route do not exist.
        """
        total_distance = 0
        # Iterate over all but last node in the route, check if current
        # and next point are adjacent
        for index, node in enumerate(route[:-1]):
            next_node = route[index + 1]
            if self.are_adjacent(node, next_node):
                total_distance += self.get(node)[next_node]
            else:
                return 'NO SUCH ROUTE'

        return str(total_distance)

    def num_trips_by_moves(self, node_from, node_to, min_moves, max_moves):
        """
        Determines the number of trips that can be made between two points
            within a certain number of moves. Calls on _num_trips().

        Arguments:
            node_from - The origin point of the connection being queried.
            node_to - The destination of the connection being queried.
            min_moves - The minimum number of moves required to be made before
                trips are counted.
            max_moves - The maximum number of moves until the number of trips
                stop being counted and the method exits.
        Returns:
            int - The number of possible trips given the move number
                restrictions.
        """
        return self._num_trips(node_from, node_to, min_moves, max_moves, False)

    def num_trips_by_distance(self, node_from, node_to, min_dist, max_dist):
        """
        Determines the number of trips that can be made between two points
            within a certain distance. Calls on _num_trips().

        Arguments:
            node_from - The origin point of the connection being queried.
            node_to - The destination of the connection being queried.
            min_dist - The minimum distance required to be made before
                trips are counted.
            max_dist - The maximum distance before which the number of trips
                stop being counted and the method exits.
        Returns:
            int - The number of possible trips given the move number
                restrictions.
        """
        return self._num_trips(node_from, node_to, min_dist, max_dist, True)

    def _num_trips(self, node_from, node_to, minimum, maximum, is_distance):
        """
        Determines the number of trips that can be made between two points
            within a certain number of moves, or less than a certain
            distance.

        Arguments:
            node_from - The origin point of the connection being queried.
                Method throws a ValueError if the node does not exist.
            node_to - The destination of the connection being queried.
                Method throws a ValueError if the node does not exist.
            minimum - The minimum moves/distance required to be made before
                trips are counted. Method will throw a ValueError if less
                than zero.
            maximum - The maximum moves/distance until the number of trips
                stop being counted and the method exits. Will throw a
                ValueError if less than minimum.
            is_distance - Whether or not we're calculating the number of trips
                possible based on distance (True) or number of moves (False).
        Returns:
            int - The number of possible trips given the restrictions.
        """
        if maximum < minimum:
            raise ValueError("maximum ({:d}) is less than " \
                    "minimum ({:d})".format(maximum, minimum))
        elif minimum <= 0:
            raise ValueError("minimum requires a value greater than zero")
        if self.get(node_from) is None or self.get(node_to) is None:
            raise ValueError("Non-existant origin or destination node was " \
                    "given")
        available_routes = 0

        # We start by building a priority queue made of tuples, which contains
        # origin node and the number of moves or distance needed to get there.
        # Then, we start populating the queue with the
        # name of connecting nodes and the number of connections traversed
        # or distance traversed to get from the origin to that point.
        trip_queue = PriorityQueue()
        trip_queue.add((0, node_from))
        while not trip_queue.is_empty():
            current_node = trip_queue.remove()
            # leave the loop now if we've reached the maximum.
            # in the current data set, our maximum move count limit is based
            # on being less than OR EQUAL TO the maximum, while the distance
            # limit is based on being LESS THAN to the maximum ONLY. That
            # conditional is reflected here.
            if is_distance and current_node[0] >= maximum:
                break
            elif not is_distance and current_node[0] > maximum:
                break
            # add to the count if we've reached the destination and
            # we're above our minimum
            if current_node[1] == node_to and current_node[0] >= minimum:
                available_routes += 1
            # continue adding to the queue - if we're measuring by distance,
            # add the distance to the next node. Else, just increment by one
            # and keep going.
            for connected_node, distance in self.get(current_node[1]).items():
                if is_distance:
                    increment = distance
                else:
                    increment = 1
                trip_queue.add((current_node[0]+increment, connected_node))

        return available_routes

    def min_route_distance(self, node_from, node_to):
        """
        Gets the shortest route between two points, using Dijkstra's
            algorithm. This version is modified to allow for a route that
            traverses back to the origin if such a route is possible.

        Arguments:
            node_from - The origin point of the connection being queried.
                Method throws a ValueError if the node does not exist.
            node_to - The destination of the connection being queried.
                Method throws a ValueError if the node does not exist.

        Returns:
            int/float - The minimum distance to traverse to complete the
                shortest possible route. If the route is origin to origin
                and no path can be made that traverses other routes to get
                back to the origin, 0 is returned. If it is impossible to get
                from the origin to the destination when the two are different,
                float("inf") (i.e. infinity) is returned.
        """
        if self.get(node_from) is None or self.get(node_to) is None:
            raise ValueError("Non-existant origin or destination node was " \
                    "given")

        min_distances = {}
        node_queue = PriorityQueue()

        # First, initialize min_distances with assumed min_distances for
        # the time being (i.e. 0 for origin, float("inf") for all possible
        # destinations
        for key in self._nodes.keys():
            if key == node_from:
                init_minimum = 0
            else:
                init_minimum = float("inf")
            min_distances[key] = init_minimum
            # Items in the priority queue are tuples, with the min_distance
            # listed first for sorting, then the key of the final point
            node_queue.add((init_minimum, key))

        while not node_queue.is_empty():
            minimum, current_node = node_queue.remove()
            for connected_node, connected_distance in self.get(current_node).items():
                new_distance = minimum + connected_distance
                # If the minimum distance from here plus the distance to the
                # next node is less than the current minimum distance to that
                # node from the origin, replace it
                # OR - if the distance is the origin (i.e. min_distance
                # from origin to connected_node is zero) - this allows us to
                # loop back to the origin!
                if new_distance < min_distances[connected_node] or \
                        min_distances[connected_node] == 0:
                    min_distances[connected_node] = new_distance
                    # Prevents the origin node from being added back into the
                    # queue, so we don't re-evaluate the whole graph again
                    if not connected_node == node_from:
                        node_queue.add((new_distance, connected_node))

        # Now we have a dict of all of the Dijkstra min distances to
        # those points from the origin -- we want to return the distance
        # to just one point (the destination)
        return min_distances[node_to]
