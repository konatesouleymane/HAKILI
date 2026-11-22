from pydantic import BaseModel , ConfigDict, ValidationError , model_validator
import re

class CommandProposal(BaseModel):
    model_config = ConfigDict (strict=True)
    program:str 
    arguments:list[str]


def validate_command(response:str) -> CommandProposal | None :
    try:
        return CommandProposal.model_validate_json(response)
    except ValidationError as e:
        return str(e)

class ValidationResult(BaseModel):
    success: bool
    proposal: CommandProposal | None = None
    error: str | None = None

    @model_validator(mode="after")
    def check_result(self):
        if self.success and self.proposal is None:
            raise ValueError("Une proposition est obligatoire")
    
        if self.success and self.error is not None:
            raise ValueError("Aucune erreur ne doit être présente lorsque success=True.")

        if not self.success and self.error is None:
            raise ValueError("Une erreur est obligatoire lorsque success=False.")
    
        if not self.success and self.proposal is not None:
            raise ValueError("Aucune proposition ne doit être présente lorsque success=False.")
        return self

def normalize_response(response: str):
    result = re.search(r"```json\s*(.*?)```",response,re.DOTALL)

    if result:
        return result.group(1).strip()
    else:
        return None


def parse_command_response(response: str) -> ValidationResult:
    normalized = normalize_response(response)

    if normalized is None:
        return ValidationResult(
            success=False,
            proposal=None,
            error="La réponse de Gemini ne contient aucun bloc JSON exploitable."
)
    result = validate_command(normalized)
    if isinstance(result, CommandProposal):
        success=True
        proposal=result
        error=None
    else:
        success=False
        proposal=None
        error=result      
    return ValidationResult(
        success=success,
        proposal=proposal,
        error=error
    )




