from pydantic import BaseModel, Field


class AnchoringRelation(BaseModel):
    """Schema for a single discovered class."""

    name: str = Field(description="The name of the relation (subClassOf, higherClassOf or equivalentClass).")
    subject: str = Field(description="The name of the Extracted Class.")
    object: str = Field(description="The name of the External Class.")
    object_iri: str = Field(description="The IRI of the External Class.")
    justification: str = Field(description="A brief justification of why this mapping is legally and logically accurate.")

class AnchoringCollection(BaseModel):
    """Container for a collection of discovered classes."""

    anchoring_relations: list[AnchoringRelation] 

def set_structured_output(model:BaseModel) -> BaseModel:
    """Configures an LLM to return data according to the ClassCollection schema."""
    
    return model.with_structured_output(AnchoringCollection)

def apply_prompt(model:BaseModel, prompt_skeleton:str) -> AnchoringCollection:
    """Executes the extraction process by invoking the model with a combined prompt and text."""

    prompt = prompt_skeleton

    structured_data = model.invoke(prompt)

    return structured_data