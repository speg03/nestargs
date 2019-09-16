import nestargs
from nestargs.meta import get_metadata


class TestOption:
    def test_option(self):
        @nestargs.option("param", nargs=2, help="help for parameter")
        def some_function(param):
            pass

        expected = {"nargs": 2, "help": "help for parameter"}
        assert get_metadata(some_function, "param", "arg_params") == expected
