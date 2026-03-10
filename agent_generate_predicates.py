from pydantic import BaseModel, Field
from typing import Optional

class RelationOntology(BaseModel):
    """Schema for a single discovered relation (triple)."""
    
    name: str = Field(description="The name of the relation in camelCase.")
    definition: str = Field(description="The legal context of this relation.")
    domain: Optional[str] = Field(description="The source class name.")
    range: Optional[str] = Field(description="The target class name.")

class RelationCollection(BaseModel):
    """Container for a collection of discovered relations."""
    
    relations_ontology: list[RelationOntology]
def set_structured_output(model:BaseModel) -> BaseModel:
    """Configures an LLM to return data according to the ClassCollection schema."""
    
    return model.with_structured_output(RelationCollection)

def apply_prompt(model:BaseModel, prompt_skeleton:str, text_file:str) -> RelationCollection:
    """Executes the extraction process by invoking the model with a combined prompt and text."""

    prompt = prompt_skeleton+text_file

    structured_data = model.invoke(prompt)

    return structured_data