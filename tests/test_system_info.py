
import pytest

from hakili.system_info import (
    get_distribution_info,
    parse_os_release,
)


class TestParseOsRelease:

    def test_parse_all_distribution_info(self):
        content = """
NAME="Ubuntu"
VERSION_ID="26.04"
ID=ubuntu
PRETTY_NAME="Ubuntu 26.04 LTS"
"""
        result = parse_os_release(content)

        assert result == {
            "NAME": "Ubuntu",
            "VERSION_ID": "26.04",
            "ID": "ubuntu",
            "PRETTY_NAME": "Ubuntu 26.04 LTS",
        }

    def test_parse_without_version_id(self):
        content = """
NAME="Ubuntu"
ID=ubuntu
PRETTY_NAME="Ubuntu"
"""
        result = parse_os_release(content)

        assert "NAME" in result
        assert "VERSION_ID" not in result
        assert result["ID"] == "ubuntu"

    def test_parse_empty_content(self):
        assert parse_os_release("") == {}

    def test_parse_content_without_target_keys(self):
        content = """
ID_LIKE=debian
HOME_URL=https://ubuntu.com
"""
        assert parse_os_release(content) == {}

    def test_parse_ignores_empty_and_malformed_lines(self):
        content = """
NAME="Ubuntu"

INVALID_LINE
VERSION_ID="26.04"
"""
        result = parse_os_release(content)

        assert result == {
            "NAME": "Ubuntu",
            "VERSION_ID": "26.04",
        }

    def test_parse_values_with_spaces(self):
        content = """
NAME="Ubuntu GNU/Linux"
VERSION_ID="26.04 LTS"
ID=ubuntu
PRETTY_NAME="Ubuntu GNU/Linux 26.04 LTS"
"""
        result = parse_os_release(content)

        assert result["NAME"] == "Ubuntu GNU/Linux"
        assert result["VERSION_ID"] == "26.04 LTS"
        assert result["PRETTY_NAME"] == "Ubuntu GNU/Linux 26.04 LTS"

    def test_parse_ignores_unrelated_keys(self):
        content = """
NAME="Ubuntu"
VERSION_ID="26.04"
ID=ubuntu
PRETTY_NAME="Ubuntu 26.04 LTS"
HOME_URL=https://ubuntu.com
"""
        result = parse_os_release(content)

        assert set(result.keys()) == {
            "NAME",
            "VERSION_ID",
            "ID",
            "PRETTY_NAME",
        }

    def test_parse_without_any_target_key(self):
        content = """
ID_LIKE=debian
VERSION_CODENAME=example
"""
        assert parse_os_release(content) == {}

    def test_parse_ignores_comments(self):
        content = """
# Distribution information
NAME="Ubuntu"
# Another comment
ID=ubuntu
"""
        result = parse_os_release(content)

        assert result == {
            "NAME": "Ubuntu",
            "ID": "ubuntu",
        }

    def test_parse_ignores_malformed_quotes(self):
        content = """
NAME="Ubuntu
ID=ubuntu
VERSION_ID="26.04"
"""
        result = parse_os_release(content)

        assert result == {
            "ID": "ubuntu",
            "VERSION_ID": "26.04",
        }


class TestGetDistributionInfo:

    def test_reads_os_release_file(self, monkeypatch):
        expected_content = 'NAME="Ubuntu"\nVERSION_ID="26.04"\n'

        class FakeFile:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                pass

            def read(self):
                return expected_content

        def fake_open(path, mode, encoding):
            assert path == "/etc/os-release"
            assert mode == "r"
            assert encoding == "utf-8"
            return FakeFile()

        monkeypatch.setattr("builtins.open", fake_open)

        assert get_distribution_info() == expected_content

    def test_raises_error_when_file_is_missing(self, monkeypatch):
        def fake_open(path, mode, encoding):
            raise FileNotFoundError("Fichier introuvable")

        monkeypatch.setattr("builtins.open", fake_open)

        with pytest.raises(FileNotFoundError):
            get_distribution_info()




    def test_raises_error_when_permission_is_denied(self, monkeypatch):
        def fake_open(path, mode, encoding):
            raise PermissionError("Accès refusé")

        monkeypatch.setattr("builtins.open", fake_open)

        with pytest.raises(PermissionError):
            get_distribution_info()

    def test_raises_error_when_an_os_error_occurs(self, monkeypatch):
        def fake_open(path, mode, encoding):
            raise OSError("Erreur système")

        monkeypatch.setattr("builtins.open", fake_open)

        with pytest.raises(OSError):
            get_distribution_info()
