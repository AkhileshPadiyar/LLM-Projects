from pydantic import BaseModel, Field

class ResearchFindings(BaseModel):
    finding: str = Field(
        description = "One important Research Finding"
    )

    source_url : str = Field(
        description = "URL of the source supporting this finding"
    )

class ResearchReport(BaseModel):
    topic: str = Field(
        description = "The Research Topic"
    )

    summary : str = Field(
        description = "A concise summary of the research"
    )

    key_findings : list[ResearchFindings] = Field(
        description = "Key findings supported by sources"
    )

    limitations : list[str] = Field(
        description = "Limitations or gaps in the available Research"
    )