import unittest
import main
from graph import StationGraph

class MainTestCases(unittest.TestCase):
    """
    Unit testing for the CLI frontend.
    """
    def setUp(self):
        self.stations = StationGraph(['AB10', 'AC2', 'CB2', 'AD5'])
        # The initial set of arguments, to be added to later
        self.args = ['-l', 'AB10,AC2,CB2,AD5']

    def test_route_argument_functionality_exist(self):
        """
        Does the route function work in an equivalent way to the StationGraph
            object? (Existing route)
        """
        self.args.extend(['route','A,C,B'])
        parsed_args = main.get_arg_parser(self.args)
        output = main.argument_handler(parsed_args)
        self.assertEqual(output, self.stations.get_distance_by_route(['A','C','B']))

    def test_route_argument_functionality_nonexist(self):
        """
        Does the route function work in an equivalent way to the StationGraph
            object? (Non-existing route)
        """
        self.args.extend(['route','A,B,C'])
        parsed_args = main.get_arg_parser(self.args)
        output = main.argument_handler(parsed_args)
        self.assertEqual(output, self.stations.get_distance_by_route(['A','B','C']))

    def test_movetrips_argument_functionality(self):
        """
        Does the movetrips function work in an equivalent way to the StationGraph
            object?
        """
        self.args.extend(['movetrips', 'A,B', '-M', '4'])
        parsed_args = main.get_arg_parser(self.args)
        output = main.argument_handler(parsed_args)
        self.assertEqual(output, self.stations.num_trips_by_moves('A','B',1,4))

    def test_disttrips_argument_functionality(self):
        """
        Does the disttrips function work in an equivalent way to the StationGraph
            object?
        """
        self.args.extend(['disttrips', 'A,B', '-M', '10'])
        parsed_args = main.get_arg_parser(self.args)
        output = main.argument_handler(parsed_args)
        self.assertEqual(output, self.stations.num_trips_by_distance('A','B',1,10))

    def test_mindist_argument_functionality(self):
        """
        Does the mindist function work in an equivalent way to the StationGraph
            object?
        """
        self.args.extend(['mindist', 'A,B'])
        parsed_args = main.get_arg_parser(self.args)
        output = main.argument_handler(parsed_args)
        self.assertEqual(output, self.stations.min_route_distance('A','B'))

if __name__ == '__main__':
    unittest.main()
