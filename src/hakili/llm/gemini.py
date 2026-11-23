
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types, errors


# --------------------------------------------------
# 1. Configuration de l'environnement
# --------------------------------------------------

# Chemin vers le fichier .env à la racine de HAKILI
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL")


# --------------------------------------------------
# 2. Vérification de la configuration
# --------------------------------------------------

if not API_KEY:
    raise ValueError(
        "Configuration manquante : GEMINI_API_KEY "
        "est absente du fichier .env"
    )

if not MODEL:
    raise ValueError(
        "Configuration manquante : GEMINI_MODEL "
        "est absent du fichier .env"
    )


# --------------------------------------------------
# 3. Initialisation du client Gemini
# --------------------------------------------------

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        timeout=60_000
    )
)


# --------------------------------------------------
# 4. Fonction de génération
# --------------------------------------------------

def generate_response(prompt: str) -> str:
    """Envoie une demande à Gemini et retourne sa réponse."""

    if not prompt or not prompt.strip():
        raise ValueError("La demande ne peut pas être vide.")

    start = time.perf_counter()

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if not response.text:
            raise RuntimeError(
                "Gemini n'a retourné aucun texte exploitable."
            )

        return response.text

    except errors.APIError as exc:
        elapsed = time.perf_counter() - start

        print(f"\nErreur de l'API Gemini : {exc}")
        print(f"Temps avant échec : {elapsed:.2f} secondes")

        raise

    except Exception as exc:
        elapsed = time.perf_counter() - start

        print(
            f"\nErreur inattendue : "
            f"{type(exc).__name__}: {exc}"
        )
        print(f"Temps avant échec : {elapsed:.2f} secondes")

        raise


# --------------------------------------------------
# 5. Point d'entrée pour le test
# --------------------------------------------------

if __name__ == "__main__":
    test_prompt = "Réponds uniquement par : HAKILI OK"

    for i in range(1, 4):
        print(f"\n--- Appel {i} ---")

        response = generate_response(test_prompt)

        print("\nRéponse de Gemini :")
        print(response)
