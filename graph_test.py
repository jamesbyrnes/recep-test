import unittest
from graph import StationGraph

class StationGraphSetupTestCases(unittest.TestCase):
    """
    Unit testing for the initialization of a StationGraph object.
    """
    def setUp(self):
        test_input = []
        self.stations = StationGraph(test_input)

    def test_connection_add_success(self):
        """
        Test that, when a conncetion is created, nodes for the origin and
            destination are added along with the distance to the destination.
        """
        self.stations.add_connection('A', 'B', 5)
        self.assertEqual(self.stations.get('A'), {'B': 5})
        self.assertEqual(self.stations.get('B'), {})

    def test_connection_distance_error(self):
        """
        Will an error be thrown when a distance that is not a number, or
            <= 0, is provided?
        """
        with self.assertRaises(ValueError):
            self.stations.add_connection('A', 'B', 'C')
        with self.assertRaises(ValueError):
            self.stations.add_connection('A', 'B', 0)
        with self.assertRaises(ValueError):
            self.stations.add_connection('A', 'B', -1)

    def test_connection_self_error(self):
        """
        Will an error be thrown when a connection is added between a station
            and itself?
        """
        with self.assertRaises(ValueError):
            self.stations.add_connection('A', 'A', 5)

    def test_get_vertices_empty(self):
        """
        Does the method get_vertices() return an empty list on an
            initialized graph?
        """
        self.assertEqual(self.stations.get_vertices(), [])

    def test_get_vertices_added(self):
        """
        Does the method get_vertices() return a list filled with the
            correct set of vertices when connections are added?
        """
        self.stations.add_connection('A', 'B', 5)
        self.assertEqual(self.stations.get_vertices(), ['A', 'B'])

    def test_min_distance_error_exist(self):
        """
        Does the method min_route_distance() throw an error when a nonexistant
            node is specified?
        """
        self.stations.add_connection('A', 'B', 5)
        with self.assertRaises(ValueError):
            self.stations.min_route_distance('A', '?')
        with self.assertRaises(ValueError):
            self.stations.min_route_distance('?', 'B')

    def test_min_distance_basic(self):
        """
        Does the method min_route_distance() choose the best route in a
            basic scenario? (i.e. shorter route is the one with more nodes)
        """
        self.stations.add_connection('A', 'B', 10)
        self.stations.add_connection('A', 'C', 1)
        self.stations.add_connection('C', 'B', 1)
        self.assertEqual(self.stations.min_route_distance('A', 'B'), 2)

class StationGraphSimpleCalcTestCases(unittest.TestCase):
    """
    Unit testing for simple distance calculation methods of a
        StationGraph object.
    """
    def setUp(self):
        test_input = ['AB5', 'BC4', 'CD6', 'AD7', 'ED5']
        self.stations = StationGraph(test_input)

    def test_adjacency(self):
        """
        Will adjacent nodes indicate they are adjacent, while non-
            adjacent nodes don't?
        """
        self.assertTrue(self.stations.are_adjacent('A', 'B'))
        self.assertFalse(self.stations.are_adjacent('A', 'C'))

    def test_distance_tracking(self):
        """
        Will the distance between points A and C show the correct
            total distance?
        """
        test_route_good = ['A', 'B', 'C']
        test_route_bad = ['A', 'C']
        self.assertEqual(self.stations.get_distance_by_route(test_route_good), '9')
        self.assertEqual(self.stations.get_distance_by_route(test_route_bad), 'NO SUCH ROUTE')

    def test_num_trips_by_moves_errors(self):
        """
        Will the method num_trips_by_moves() throw the
            correct errors?
        """
        with self.assertRaises(ValueError):
            # max_moves < min_moves
            self.stations.num_trips_by_moves('A', 'D', 5, 3)
            self.stations.num_trips_by_distance('A', 'D', 50, 3)
        with self.assertRaises(ValueError):
            # min_moves <= 0
            self.stations.num_trips_by_moves('A', 'D', 0, 5)
            self.stations.num_trips_by_distance('A', 'D', 0, 30)
        with self.assertRaises(ValueError):
            # non-existent node
            self.stations.num_trips_by_moves('A', 'X', 2, 5)
            self.stations.num_trips_by_distance('A', 'X', 2, 30)

    def test_num_trips_by_moves(self):
        """
        Will the method num_trips_by_moves() return the correct
            values?
        """
        self.assertEqual(self.stations.num_trips_by_moves('A', 'D', 1, 5), 2)
        self.assertEqual(self.stations.num_trips_by_moves('A', 'E', 1, 5), 0)

    def test_num_trips_by_distance(self):
        """
        Will the method num_trips_by_distance() return the correct
            values?
        """
        self.assertEqual(self.stations.num_trips_by_distance('A', 'D', 1, 8), 1)
        self.assertEqual(self.stations.num_trips_by_distance('A', 'E', 1, 5), 0)

class StationGraphAdvCalcTestCases(unittest.TestCase):
    """
    Unit testing for advanced distance calculation methods of a
        StationGraph object.
    """
    def setUp(self):
        test_input = ['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7']
        self.stations = StationGraph(test_input)

    def test_set_questions_1_through_5(self):
        """
        Runs the first five tests against the data set. (Tests 1-5)
        """
        # Listing tests separately so we can pinpoint which one fails the
        # unit test.
        self.assertEqual(self.stations.get_distance_by_route(['A', 'B', 'C']), '9')
        self.assertEqual(self.stations.get_distance_by_route(['A', 'D']), '5')
        self.assertEqual(self.stations.get_distance_by_route(['A', 'D', 'C']), '13')
        self.assertEqual(self.stations.get_distance_by_route(['A', 'E', 'B', 'C', 'D']), '22')
        self.assertEqual(self.stations.get_distance_by_route(['A', 'E', 'D']), 'NO SUCH ROUTE')

    def test_set_questions_6_through_7(self):
        """
        Runs the next two tests against the data set. (Tests 6-7)
        """
        self.assertEqual(self.stations.num_trips_by_moves('C', 'C', 1, 3), 2)
        self.assertEqual(self.stations.num_trips_by_moves('A', 'C', 4, 4), 3)

    def test_set_questions_8_through_9(self):
        """
        Runs the next two tests against the data set. (Tests 8-9)
        """
        self.assertEqual(self.stations.min_route_distance('A', 'C'), 9)
        self.assertEqual(self.stations.min_route_distance('B', 'B'), 9)

    def test_set_question_10(self):
        """
        Runs the final test against the data set. (Test 10)
        """
        self.assertEqual(self.stations.num_trips_by_distance('C', 'C', 1, 30), 7)

if __name__ == '__main__':
    unittest.main()
