
import pytest

from hakili.security.validator import (
    normalize_response,
    validate_command,
    parse_command_response,
    CommandProposal,
)


# ----------------------------------
# Tests de normalize_response()
# ----------------------------------

def test_normalize_response_valid_json():
    response = '''```json
{"program": "mkdir", "arguments": ["sauvegarde"]}
```'''

    result = normalize_response(response)

    assert result == '{"program": "mkdir", "arguments": ["sauvegarde"]}'


def test_normalize_response_without_json_block():
    response = '{"program": "mkdir", "arguments": ["sauvegarde"]}'

    assert normalize_response(response) is None


def test_normalize_response_unclosed_block():
    response = '```json\n{"program": "mkdir"}'

    assert normalize_response(response) is None


def test_normalize_response_empty():
    assert normalize_response("") is None


# ----------------------------------
# Tests de validate_command()
# ----------------------------------

def test_validate_command_valid():
    response = '{"program": "mkdir", "arguments": ["sauvegarde"]}'

    result = validate_command(response)

    assert isinstance(result, CommandProposal)
    assert result.program == "mkdir"
    assert result.arguments == ["sauvegarde"]


def test_validate_command_invalid_argument_type():
    response = '{"program": "mkdir", "arguments": [2026]}'

    result = validate_command(response)

    assert isinstance(result, str)
    assert "valid string" in result


def test_validate_command_missing_field():
    response = '{"program": "mkdir"}'

    result = validate_command(response)

    assert isinstance(result, str)


def test_validate_command_invalid_json():
    response = '{"program": "mkdir", "arguments": '

    result = validate_command(response)

    assert isinstance(result, str)


# ----------------------------------
# Tests de parse_command_response()
# ----------------------------------

def test_parse_command_response_valid():
    response = '''```json
{"program": "mkdir", "arguments": ["sauvegarde"]}
```'''

    result = parse_command_response(response)

    assert isinstance(result, CommandProposal)
    assert result.program == "mkdir"
    assert result.arguments == ["sauvegarde"]


def test_parse_command_response_invalid_proposal():
    response = '''```json
{"program": "mkdir", "arguments": [2026]}
```'''

    result = parse_command_response(response)

    assert isinstance(result, str)
    assert "valid string" in result


def test_parse_command_response_without_json():
    response = "Je ne peux pas proposer de commande."

    result = parse_command_response(response)

    assert result is None
