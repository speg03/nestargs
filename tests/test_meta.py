from nestargs.meta import get_metadata, set_metadata


class TestMeta:
    def test_get_metadata(self):
        def some_function(param):
            pass

        assert get_metadata(some_function, "param", "arg_params") is None

        expected = {"nargs": 2, "help": "help for parameter"}
        set_metadata(some_function, "param", "arg_params", expected)

        assert get_metadata(some_function, "param", "arg_params") == expected
