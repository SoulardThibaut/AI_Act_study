from pydantic import BaseModel, Field


class ClassOntology(BaseModel):
    """Schema for a single discovered class."""

    name: str = Field(description="The name of the discovered class.")
    definition: str = Field(description="A definition to explain how this class behaves for an end user.")

class ClassCollection(BaseModel):
    """Container for a collection of discovered classes."""

    classes_ontology: list[ClassOntology] 

def set_structured_output(model:BaseModel) -> BaseModel:
    """Configures an LLM to return data according to the ClassCollection schema."""
    
    return model.with_structured_output(ClassCollection)

def apply_prompt(model:BaseModel, prompt_skeleton:str, text_file:str) -> ClassCollection:
    """Executes the extraction process by invoking the model with a combined prompt and text."""

    prompt = prompt_skeleton+text_file

    structured_data = model.invoke(prompt)

    return structured_data