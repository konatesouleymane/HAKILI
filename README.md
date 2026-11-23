# HAKILI 

### An AI-powered assistant designed to make Linux easier to use.

HAKILI is a Python-based Linux assistant that allows users to express their needs in natural language and receive relevant Linux command suggestions powered by Google's Gemini API.

The goal is to make Linux more accessible, especially for beginners, without requiring them to memorize terminal commands.

##  Features

- **Natural Language Interaction:** Describe what you want to do using simple language.
- **System Awareness:** Retrieves information about the Linux distribution to provide context to the AI.
- **AI-Powered Suggestions:** Uses Google Gemini to generate relevant Linux command proposals.
- **Response Validation:** Checks the structure of AI-generated responses using Pydantic.
- **User Control:** Commands are suggested but never executed automatically.

##  Architecture

```text
HAKILI/
├── src/
│   └── hakili/
│       ├── main.py
│       ├── llm/
│       │   └── gemini.py
│       ├── system/
│       │   └── system_info.py
│       └── security/
│           └── validator.py
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

*The structure above represents the main components; adapt the paths if your repository differs.*

##  Technologies

- Python 3.12+
- Google Gemini API
- Pydantic
- Pytest
- Git

##  Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/konatesouleymane/HAKILI.git
cd HAKILI
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file at the project root:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=your_model_name
```

Never commit your `.env` file or expose your API key.

### 5. Run HAKILI

```bash
PYTHONPATH=src python -m hakili.main
```

##  Tests

Run the automated tests with:

```bash
pytest -v
```

The current test suite includes 29 passing tests for the implemented components.

##  Security Approach

HAKILI is designed with user control in mind.

In its current version:
- AI responses are checked against an expected JSON structure.
- Invalid responses are handled.
- No command is executed automatically.

**Note:** Structural validation does not guarantee that a proposed command is safe. Command safety analysis and controlled execution are planned improvements.

##  Roadmap

- [x] Retrieve Linux distribution information.
- [x] Generate Linux command suggestions using Gemini.
- [x] Validate the structure of AI responses.
- [x] Add automated tests for implemented components.
- [ ] Improve command safety analysis.
- [ ] Add controlled execution with user confirmation.
- [ ] Support more advanced Linux requests.
- [ ] Expand distribution compatibility.

##  Project Status

HAKILI is currently under development. The project is an evolving experiment in combining Linux, Python and generative AI to create a more accessible command-line experience.

##  Author

**Souleymane Konaté**

- GitHub: [@konatesouleymane](https://github.com/konatesouleymane)

---

*Making Linux more accessible, one command at a time.*