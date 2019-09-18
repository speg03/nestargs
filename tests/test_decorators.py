import pytest

import nestargs
from nestargs.meta import get_metadata


class TestOption:
    def test_option(self):
        @nestargs.option("param", nargs=2, help="help for parameter")
        def some_function(param):
            pass

        expected = {"nargs": 2, "help": "help for parameter"}
        assert get_metadata(some_function, "param", "arg_params") == expected

    def test_option_with_invalid_parameter(self):
        with pytest.raises(ValueError):

            @nestargs.option("invalid", help="invalid parameter")
            def some_function(param):
                pass


class TestIgnores:
    def test_ignores(self):
        @nestargs.ignores("param2", "param3")
        def some_function(param1, param2, param3):
            pass

        assert get_metadata(some_function, "param1", "ignore") is None
        assert get_metadata(some_function, "param2", "ignore") is True
        assert get_metadata(some_function, "param3", "ignore") is True

    def test_ignores_with_invalid_parameter(self):
        with pytest.raises(ValueError):

            @nestargs.ignores("invalid")
            def some_function(param):
                pass
