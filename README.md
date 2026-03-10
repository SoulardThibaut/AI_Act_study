# EU AI Act Semantic Pipeline: Exploratory Study

This repository presents an exploratory study on the rapid transformation of the **EU AI Act's** dense legal prose into a structured, machine-interpretable ontology. Utilizing a modular agentic pipeline, the project demonstrates how AI-human collaboration can bridge the gap between complex legal text and semantic knowledge graphs.

## Core Methodology

The construction follows a **justified extraction workflow** to ensure technical auditability and principled modeling choices:

* **Targeted Preprocessing**: Parsed official HTML text using **Article 3** definitions as seeds to orient the model toward key legal structures.
* **Latent Role Discovery**: Deployed a specialized agent (`agent_generate_classes.py`) to identify "Latent Classes"—such as **Deemed Providers** and specific **Status Conditions**—that are critical for litigation but often missed by standard extraction.
* **Semantic Alignment**: Conceptually anchored extracted classes and predicates to established standards like **AIRO**, **VAIR**, and **schema.org**.
* **Minimalist Constraint Logic**: Implemented a flexible modeling approach using `schema:domainIncludes` and `schema:rangeIncludes` to capture complex legal relationships without over-constraining the initial graph.
* **Justified Provenance**: Every AI-generated triple includes specific provenance (`prov:wasAttributedTo "LLM"`) and reasoning justifications, allowing legal experts to audit the model's logic in natural language.



## Project Structure

* **`main.ipynb`**: The primary orchestration notebook managing the modular workflow and `langChain` integration.
* **`agent_generate_classes.py`**: Identifies latent and implied legal classes critical for regulatory reasoning.
* **`agent_generate_predicates.py`**: Extracts functional RDF relations (edges) such as `providesDocumentationTo`.
* **`agent_generate_hierarchy.py`**: Synthesizes flat terminology into a formal subsumption hierarchy (e.g., `Importer` $\sqsubseteq$ `Operator`).
* **`ontology_generated.ttl`**: The final proof-of-concept ontology in Turtle format.

## Conclusion

This study shows the possibility for the rapid transformation of the EU AI Act into a machine-interpretable format via a modular, agent-based pipeline. It proves that while AI can efficiently navigate the vast breadth of regulatory data, a human-in-the-loop remains essential for the final, principled fusion of complex legal knowledge.
