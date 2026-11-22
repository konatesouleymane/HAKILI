import shlex


def get_distribution_info() -> str:
    """Lit et retourne le contenu de /etc/os-release."""
    with open("/etc/os-release", "r", encoding="utf-8") as file:
        return file.read()


def parse_os_release(content: str) -> dict[str, str]:
    """Extrait NAME, VERSION_ID, ID et PRETTY_NAME depuis le contenu de /etc/os-release."""
    targets = {"NAME", "VERSION_ID", "ID", "PRETTY_NAME"}
    result: dict[str, str] = {}

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        try:
            tokens = shlex.split(line, comments=True)
        except ValueError:
            continue

        for token in tokens:
            if "=" not in token:
                continue
            key, value = token.split("=", 1)
            key = key.strip()
            if key in targets:
                result[key] = value

    return result
