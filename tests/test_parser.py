import nestargs
import pytest


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
