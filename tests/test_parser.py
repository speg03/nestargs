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

    def test_parse_args_with_another_delimiter(self):
        parser = nestargs.NestedArgumentParser(delimiter="/")
        parser.add_argument("some/a")
        parser.add_argument("some/b")
        parser.add_argument("some/c/d")

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

    def test_add_arguments_from_dataclass(self):
        parser = nestargs.NestedArgumentParser()
        parser.add_arguments(
            [
                nestargs.ArgumentDefinition("user.name", type=str),
                nestargs.ArgumentDefinition("user.age", type=int, default=0),
                nestargs.ArgumentDefinition(
                    "--count", type=int, default=1, dest="limit"
                ),
            ]
        )

        args = parser.parse_args(["alice", "42", "--count", "7"])
        assert args.user.name == "alice"
        assert args.user.age == 42
        assert args.limit == 7

    def test_add_arguments_accepts_varargs(self):
        parser = nestargs.NestedArgumentParser()
        parser.add_arguments(
            nestargs.ArgumentDefinition("user.name", type=str),
            nestargs.ArgumentDefinition("user.tags", nargs="*", default=[]),
        )

        args = parser.parse_args(["alice", "red", "blue"])
        assert args.user.name == "alice"
        assert args.user.tags == ["red", "blue"]

    def test_add_arguments_preserves_explicit_none_default(self):
        parser = nestargs.NestedArgumentParser()
        parser.add_arguments(
            nestargs.ArgumentDefinition(
                "--mode", nargs="?", default=None, type=str, dest="mode"
            )
        )

        args = parser.parse_args([])
        assert args.mode is None

        args = parser.parse_args(["--mode", "fast"])
        assert args.mode == "fast"

    def test_create_argument_definitions_from_dict(self):
        definitions = nestargs.create_argument_definitions_from_dict(
            {
                "user": {
                    "name": "alice",
                    "profile": {"age": 42},
                },
                "enabled": True,
            },
            max_depth=1,
        )

        assert definitions[:2] == [
            nestargs.ArgumentDefinition(
                "--user.name",
                default="alice",
                type=str,
                dest="user.name",
            ),
            nestargs.ArgumentDefinition(
                "--user.profile",
                default="{'age': 42}",
                type=str,
                dest="user.profile",
            ),
        ]
        boolean_definition = definitions[2]
        assert boolean_definition.name == "--enabled"
        assert boolean_definition.default is True
        assert boolean_definition.dest == "enabled"
        assert boolean_definition.type("true") is True
        assert boolean_definition.type("false") is False

    def test_add_arguments_from_dict_parses_boolean_values(self):
        parser = nestargs.NestedArgumentParser()
        parser.add_arguments_from_dict({"enabled": True})

        assert parser.parse_args(["--enabled", "true"]).enabled is True
        assert parser.parse_args(["--enabled", "false"]).enabled is False

        with pytest.raises(SystemExit):
            parser.parse_args(["--enabled", "invalid"])

    def test_create_argument_definitions_from_dict_replaces_underscores(self):
        definitions = nestargs.create_argument_definitions_from_dict(
            {"_foo_bar_": "foobar"},
            max_depth=0,
        )

        assert definitions == [
            nestargs.ArgumentDefinition(
                "--foo-bar",
                default="foobar",
                type=str,
                dest="_foo_bar_",
            )
        ]

    def test_create_argument_definitions_from_nested_dict_with_underscores(self):
        definitions = nestargs.create_argument_definitions_from_dict(
            {"user_profile": {"_first_name_": "alice"}},
            max_depth=1,
            delimiter="/",
        )

        assert definitions == [
            nestargs.ArgumentDefinition(
                "--user-profile/first-name",
                default="alice",
                type=str,
                dest="user_profile/_first_name_",
            )
        ]

    def test_add_arguments_from_dict_uses_parser_delimiter(self):
        parser = nestargs.NestedArgumentParser(delimiter="/")
        parser.add_arguments_from_dict({"user": {"name": "alice"}}, max_depth=1)

        args = parser.parse_args(["--user/name", "alice"])
        assert args.user.name == "alice"

        definitions = nestargs.create_argument_definitions_from_dict(
            {"user": {"name": "alice"}},
            max_depth=1,
            delimiter="/",
        )
        assert definitions == [
            nestargs.ArgumentDefinition(
                "--user/name",
                default="alice",
                type=str,
                dest="user/name",
            )
        ]
