"""KeyValues reader: the format rules that Valve data actually relies on."""
from Core.Code.keyvalues import KeyValues, loads


def test_simple_pairs():
    kv = loads('"Root" { "a" "1" "b" "two" }')
    assert kv.get_str("a") == "1"
    assert kv.get_str("b") == "two"
    assert kv.get_int("a") == 1
    assert kv.name == "Root"


def test_lookup_is_case_insensitive():
    kv = loads('"Root" { "Game" "tf" }')
    assert kv.get_str("game") == "tf"
    assert "GAME" in kv


def test_duplicate_keys_are_all_kept():
    # SearchPaths repeats "Game" once per mount; losing duplicates loses mounts
    kv = loads('"Paths" { "Game" "a" "Game" "b" "Game" "c" }')
    assert kv.all("Game") == ["a", "b", "c"]
    assert kv.get_str("Game") == "a"          # first wins
    assert kv.pairs() == [("Game", "a"), ("Game", "b"), ("Game", "c")]


def test_order_is_preserved():
    kv = loads('"Paths" { "z" "1" "a" "2" "m" "3" }')
    assert kv.keys() == ["z", "a", "m"]


def test_nested_blocks_and_path():
    kv = loads('''
    "GameInfo"
    {
        "FileSystem"
        {
            "SearchPaths" { "Game" "tf" }
        }
    }
    ''')
    assert kv.path("FileSystem", "SearchPaths").get_str("Game") == "tf"
    assert kv.path("FileSystem", "Nope") is None
    assert kv.path("Nope", "SearchPaths") is None


def test_comments_are_ignored():
    kv = loads('''
    "Root"
    {
        // a line comment
        "a" "1"     // trailing
        /* a block
           comment  "b" "ignored" */
        "c" "3"
    }
    ''')
    assert kv.get_str("a") == "1"
    assert kv.get_str("c") == "3"
    assert "b" not in kv


def test_unquoted_tokens():
    kv = loads("Root { game tf type multiplayer_only }")
    assert kv.get_str("game") == "tf"
    assert kv.get_str("type") == "multiplayer_only"


def test_backslash_is_a_path_separator_not_an_escape():
    # Valve writes Windows paths unescaped; treating \\t as a tab breaks them
    kv = loads(r'"Root" { "path" "models\tf\player.mdl" }')
    assert kv.get_str("path") == r"models\tf\player.mdl"


def test_escapes_are_off_by_default_like_valve():
    # \\n stays two characters unless escape handling is asked for
    kv = loads(r'"Root" { "text" "line\nnext" }')
    assert kv.get_str("text") == r"line\nnext"


def test_escapes_work_when_explicitly_enabled():
    kv = loads('"Root" { "text" "line\\nnext" }', escapes=True)
    assert kv.get_str("text") == "line\nnext"


def test_enabling_escapes_does_not_break_unknown_sequences():
    kv = loads(r'"Root" { "path" "models\zfile.mdl" }', escapes=True)
    assert kv.get_str("path") == r"models\zfile.mdl"


def test_missing_keys_return_defaults():
    kv = loads('"Root" { "a" "1" }')
    assert kv.get_str("nope") == ""
    assert kv.get_str("nope", "fallback") == "fallback"
    assert kv.get_int("nope", 7) == 7
    assert kv.get_int("a") == 1
    assert kv.block("nope") is None


def test_non_numeric_int_falls_back():
    kv = loads('"Root" { "a" "not a number" }')
    assert kv.get_int("a", 5) == 5


def test_unterminated_block_does_not_hang():
    kv = loads('"Root" { "a" "1"')
    assert kv.get_str("a") == "1"


def test_key_without_value_at_end_of_block():
    kv = loads('"Root" { "a" "1" "dangling" }')
    assert kv.get_str("a") == "1"
    assert kv.get_str("dangling") == ""


def test_empty_document():
    kv = loads("")
    assert len(kv) == 0
    assert kv.get_str("anything") == ""


def test_bom_is_stripped():
    kv = loads('﻿"Root" { "a" "1" }')
    assert kv.get_str("a") == "1"


def test_deep_nesting_is_refused_not_crashed():
    from Core.Code.keyvalues import KeyValuesError
    text = '"a" {' * 200 + "}" * 200
    try:
        loads(text)
        raise AssertionError("expected KeyValuesError for runaway nesting")
    except KeyValuesError:
        pass


def test_block_returns_only_blocks():
    kv = loads('"Root" { "x" "string" "x" { "inner" "1" } }')
    assert kv.get_str("x") == "string"
    block = kv.block("x")
    assert isinstance(block, KeyValues)
    assert block.get_str("inner") == "1"
