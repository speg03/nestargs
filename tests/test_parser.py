import pytest

import nestargs


class TestNestedArgumentParser:
    def test_parse_args(self):
        parser = nestargs.NestedArgumentParser()
        parser.add_argument("some.a")
        parser.add_argument("some.b")
        parser.add_argument("some.c.d")

        args = parser.parse_args(["1", "2", "3"])
        assert args.some.a == "1"
        assert args.some.b == "2"
        assert args.some.c.d == "3"
        assert vars(args.some).keys() == {"a", "b", "c"}
        assert vars(args.some.c).keys() == {"d"}

    def test_parse_args_with_empty_parent(self):
        parser = nestargs.NestedArgumentParser()
        parser.add_argument(".empty")

        with pytest.raises(ValueError):
            parser.parse_args([""])

    def test_register_arguments(self):
        def some_function(param1, param2=True, param3=False, param4=1):
            pass

        parser = nestargs.NestedArgumentParser()

        actions = parser.register_arguments(some_function, prefix="some")
        assert actions.keys() == {"param1", "param2", "param3", "param4"}
        assert actions["param1"].required is True
        assert actions["param2"].default is True
        assert actions["param3"].default is False
        assert actions["param4"].type is int
        assert actions["param4"].default == 1

        args = parser.parse_args(
            [
                "--some.param1",
                "foo",
                "--some.no_param2",
                "--some.param3",
                "--some.param4",
                "2",
            ]
        )
        assert args.some.param1 == "foo"
        assert args.some.param2 is False
        assert args.some.param3 is True
        assert args.some.param4 == 2

    def test_register_arguments_with_no_prefixes(self):
        def some_function(param1, param2=True, param3=False, param4=1):
            pass

        parser = nestargs.NestedArgumentParser()

        actions = parser.register_arguments(some_function)
        assert actions.keys() == {"param1", "param2", "param3", "param4"}
        assert actions["param1"].required is True
        assert actions["param2"].default is True
        assert actions["param3"].default is False
        assert actions["param4"].type is int
        assert actions["param4"].default == 1

        args = parser.parse_args(
            ["--param1", "foo", "--no_param2", "--param3", "--param4", "2"]
        )
        assert args.param1 == "foo"
        assert args.param2 is False
        assert args.param3 is True
        assert args.param4 == 2

    def test_register_arguments_from_class(self):
        class SomeClass:
            def __init__(self, param, *args, **kwargs):
                pass

        parser = nestargs.NestedArgumentParser()

        actions = parser.register_arguments(SomeClass, prefix="some")
        assert actions.keys() == {"param"}
        assert actions["param"].required is True

        args = parser.parse_args(["--some.param", "foo"])
        assert args.some.param == "foo"

    def test_register_arguments_with_option_decorator(self):
        @nestargs.option("param", nargs=2, help="help for parameter")
        def some_function(param):
            pass

        parser = nestargs.NestedArgumentParser()

        actions = parser.register_arguments(some_function, prefix="some")
        assert actions.keys() == {"param"}
        assert actions["param"].nargs == 2
        assert actions["param"].help == "help for parameter"

        args = parser.parse_args(["--some.param", "foo", "bar"])
        assert args.some.param == ["foo", "bar"]
