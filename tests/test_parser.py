import pytest

from nestargs import ArgumentDefinition, ArgumentTypeError, NestedArgumentParser


class TestNestedArgumentParser:
    def test_parse_args(self):
        parser = NestedArgumentParser()
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
        parser = NestedArgumentParser(delimiter="/")
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
        parser = NestedArgumentParser()
        parser.add_argument(".empty")

        with pytest.raises(ValueError):
            parser.parse_args([""])

    def test_add_arguments_from_dataclass(self):
        parser = NestedArgumentParser()
        parser.add_arguments(
            [
                ArgumentDefinition("user.name", type=str),
                ArgumentDefinition("user.age", type=int, default=0),
                ArgumentDefinition("--count", type=int, default=1, dest="limit"),
            ]
        )

        args = parser.parse_args(["alice", "42", "--count", "7"])
        assert args.user.name == "alice"
        assert args.user.age == 42
        assert args.limit == 7

    def test_add_arguments_accepts_varargs(self):
        parser = NestedArgumentParser()
        parser.add_arguments(
            ArgumentDefinition("user.name", type=str),
            ArgumentDefinition("user.tags", nargs="*", default=[]),
        )

        args = parser.parse_args(["alice", "red", "blue"])
        assert args.user.name == "alice"
        assert args.user.tags == ["red", "blue"]

    def test_add_arguments_rejects_non_definitions(self):
        parser = NestedArgumentParser()

        with pytest.raises(TypeError, match="must be an ArgumentDefinition"):
            parser.add_arguments("user.name")

    def test_add_arguments_preserves_explicit_none_default(self):
        parser = NestedArgumentParser()
        parser.add_arguments(
            ArgumentDefinition("--mode", nargs="?", default=None, type=str, dest="mode")
        )

        args = parser.parse_args([])
        assert args.mode is None

        args = parser.parse_args(["--mode", "fast"])
        assert args.mode == "fast"

    def test_create_argument_definitions_from_dict(self):
        parser = NestedArgumentParser()
        definitions = parser.create_argument_definitions_from_dict(
            {
                "user": {
                    "name": "alice",
                    "profile": {"age": 42},
                },
                "enabled": True,
            },
            max_depth=1,
        )

        assert definitions[0] == ArgumentDefinition(
            "--user.name",
            default="alice",
            type=str,
            dest="user.name",
        )
        profile_definition = definitions[1]
        assert profile_definition.name == "--user.profile"
        assert profile_definition.default == {"age": 42}
        assert profile_definition.dest == "user.profile"
        assert profile_definition.type('{"age": 43}') == {"age": 43}
        with pytest.raises(ArgumentTypeError):
            profile_definition.type("age: 44")
        boolean_definition = definitions[2]
        assert boolean_definition.name == "--enabled"
        assert boolean_definition.default is True
        assert boolean_definition.dest == "enabled"
        assert boolean_definition.type("true") is True
        assert boolean_definition.type("false") is False

    def test_create_argument_definitions_from_dict_infers_scalar_types(self):
        parser = NestedArgumentParser()
        custom_value = object()

        definitions = parser.create_argument_definitions_from_dict(
            {
                "integer": 1,
                "floating": 1.5,
                "string": "value",
                "custom": custom_value,
                "optional": None,
            }
        )

        assert definitions[0].type is int
        assert definitions[1].type is float
        assert definitions[2].type is str
        assert definitions[3].type is str
        assert definitions[4].type is None

        parser.add_arguments(definitions)
        assert parser.parse_args(["--integer", "2"]).integer == 2
        assert parser.parse_args([]).optional is None

    def test_create_argument_definitions_from_dict_validates_input(self):
        parser = NestedArgumentParser()

        with pytest.raises(TypeError, match="values must be dict"):
            parser.create_argument_definitions_from_dict([])  # type: ignore[arg-type]

        with pytest.raises(ValueError, match="max_depth must be >= 0"):
            parser.create_argument_definitions_from_dict({}, max_depth=-1)

    def test_add_arguments_from_dict_parses_deep_dict_as_json(self):
        parser = NestedArgumentParser()
        parser.add_arguments_from_dict(
            {"user": {"profile": {"age": 42}}},
            max_depth=1,
        )

        args = parser.parse_args(["--user.profile", '{"age": 43}'])
        assert args.user.profile == {"age": 43}

        with pytest.raises(SystemExit):
            parser.parse_args(["--user.profile", "age: 44"])

    def test_add_arguments_from_dict_parses_list_values_as_json(self):
        parser = NestedArgumentParser()
        parser.add_arguments_from_dict({"values": [1, "default"]})

        definitions = parser.create_argument_definitions_from_dict(
            {"values": [1, "default"]}
        )
        assert definitions == [
            ArgumentDefinition(
                "--values",
                default=[1, "default"],
                type=definitions[0].type,
                dest="values",
            )
        ]

        assert parser.parse_args([]).values == [1, "default"]
        args = parser.parse_args(["--values", '[1, "text", true, null]'])
        assert args.values == [1, "text", True, None]

    def test_add_arguments_from_dict_parses_boolean_values(self):
        parser = NestedArgumentParser()
        parser.add_arguments_from_dict({"enabled": True})

        assert parser.parse_args(["--enabled", "true"]).enabled is True
        assert parser.parse_args(["--enabled", "false"]).enabled is False

        with pytest.raises(SystemExit):
            parser.parse_args(["--enabled", "invalid"])

    def test_create_argument_definitions_from_dict_replaces_underscores(self):
        parser = NestedArgumentParser()
        definitions = parser.create_argument_definitions_from_dict(
            {"_foo_bar_": "foobar"},
            max_depth=0,
        )

        assert definitions == [
            ArgumentDefinition(
                "--foo-bar",
                default="foobar",
                type=str,
                dest="_foo_bar_",
            )
        ]

    def test_create_argument_definitions_from_nested_dict_with_underscores(self):
        parser = NestedArgumentParser(delimiter="/")
        definitions = parser.create_argument_definitions_from_dict(
            {"user_profile": {"_first_name_": "alice"}},
            max_depth=1,
        )

        assert definitions == [
            ArgumentDefinition(
                "--user-profile/first-name",
                default="alice",
                type=str,
                dest="user_profile/_first_name_",
            )
        ]

    def test_add_arguments_from_dict_uses_parser_delimiter(self):
        parser = NestedArgumentParser(delimiter="/")
        parser.add_arguments_from_dict({"user": {"name": "alice"}}, max_depth=1)

        args = parser.parse_args(["--user/name", "alice"])
        assert args.user.name == "alice"

        definitions = parser.create_argument_definitions_from_dict(
            {"user": {"name": "alice"}},
            max_depth=1,
        )
        assert definitions == [
            ArgumentDefinition(
                "--user/name",
                default="alice",
                type=str,
                dest="user/name",
            )
        ]
