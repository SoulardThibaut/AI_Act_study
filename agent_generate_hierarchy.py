from pydantic import BaseModel, Field
from typing import Optional

class Hierarchy(BaseModel):
    """Schema for a single discovered relation (triple)."""
    
    subClass: str = Field(description="The more precise class")
    higherClass: str = Field(description="The more general class")
    justification: str = Field(description="A brief justification of why this link.")

class RelationCollection(BaseModel):
    """Container for a collection of discovered relations."""
    
    relations_ontology: list[Hierarchy]

def set_structured_output(model:BaseModel) -> BaseModel:
    """Configures an LLM to return data according to the ClassCollection schema."""
    
    return model.with_structured_output(RelationCollection)

def apply_prompt(model:BaseModel, prompt_skeleton:str, text_file:str) -> RelationCollection:
    """Executes the extraction process by invoking the model with a combined prompt and text."""

    prompt = prompt_skeleton+text_file

    structured_data = model.invoke(prompt)

    return structured_data