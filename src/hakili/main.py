
from hakili.system_info import get_distribution_info, parse_os_release
from hakili.llm.gemini import generate_response
from hakili.security.validator import parse_command_response


def get_system_context() -> dict[str, str]:
    """Récupère les informations de la distribution Linux."""
    try:
        raw_info = get_distribution_info()
        return parse_os_release(raw_info)

    except OSError as error:
        print(f"Impossible de détecter le système : {error}")
        return {}


def build_prompt(
    user_request: str,
    system_context: dict[str, str],
) -> str:
    """Construit le prompt envoyé à Gemini."""

    if system_context:
        context_block = "\n".join(
            f"- {key}: {value}"
            for key, value in system_context.items()
        )
    else:
        context_block = "- Informations système indisponibles."

    return (
        "Tu es HAKILI, un assistant Linux spécialisé dans "
        "l'administration et la gestion du système.\n\n"
        "Utilise les informations système pour adapter ta proposition.\n"
        "Si les informations sont insuffisantes, reconnais ton incertitude.\n"
        "Ne suppose pas une distribution ou une version inconnue.\n"
        "Ne propose pas de commande destructive.\n"
        "Ne propose qu'une seule commande simple.\n\n"
        "Retourne exclusivement un bloc JSON au format suivant :\n"
        "```json\n"
        '{\n'
        '  "program": "nom_de_la_commande",\n'
        '  "arguments": ["argument1", "argument2"]\n'
        '}\n'
        "```\n\n"
        f"Contexte système :\n{context_block}\n\n"
        f"Demande utilisateur :\n{user_request}"
    )


def main() -> None:
    """Point d'entrée principal de HAKILI."""

    print("================================")
    print("       HAKILI - Assistant Linux")
    print("================================")

    user_request = input("\nQue souhaites-tu faire ? ").strip()

    if not user_request:
        print("La demande ne peut pas être vide.")
        return

    system_context = get_system_context()

    prompt = build_prompt(
        user_request=user_request,
        system_context=system_context,
    )

    print("\n HAKILI refléchit...\n")

    try:
        response = generate_response(prompt)

    except Exception as error:
        print(f"Impossible de contacter Gemini : {error}")
        return

    validation_result = parse_command_response(response)

    if not validation_result.success:
        print("\nLa réponse de Gemini n'a pas pu être validée.")
        print(validation_result.error)
        return

    proposal = validation_result.proposal

    print("\nCommande proposée :")
    print(proposal.program, *proposal.arguments)

    print("\nCette commande n'a pas été exécutée.")


if __name__ == "__main__":
    main()
