from pydantic import BaseModel , ConfigDict, ValidationError
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


def normalize_response(response: str):
    result = re.search(r"```json\s*(.*?)```",response,re.DOTALL)

    if result:
        return result.group(1)
    else:
        return None


def parse_command_response(response: str):
    normalized = normalize_response(response)

    if normalized is None:
        return None

    return validate_command(normalized)