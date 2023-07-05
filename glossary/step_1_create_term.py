# Inlined from /metadata-ingestion/examples/library/create_term.py
import logging

from datahub.emitter.mce_builder import make_term_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter

# Imports for metadata model classes
from datahub.metadata.schema_classes import GlossaryTermInfoClass

def create_glossary_term_event(name:str, urn_name: str, definition:str, term_source:str="")->MetadataChangeProposalWrapper:
    # note that glossary terms can also be ingested with a receipe card which is useful 
    # for getting different types of users to populate datahaub with information

    term_urn = make_term_urn(urn_name)
    term_properties_aspect = GlossaryTermInfoClass(
        definition=definition,
        name=name,
        termSource=term_source,
    )

    event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
    entityUrn=term_urn,
    aspect=term_properties_aspect,
    )
    return event

   