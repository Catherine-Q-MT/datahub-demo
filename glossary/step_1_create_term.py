# Inlined from /metadata-ingestion/examples/library/create_term.py
import logging

from datahub.emitter.mce_builder import make_term_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter

# Imports for metadata model classes
from datahub.metadata.schema_classes import GlossaryTermInfoClass

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



term_urn = make_term_urn("countryCode")
term_properties_aspect = GlossaryTermInfoClass(
    definition="3 letter Country code. ISO 3166-1 alpha-3",
    name="Code",
    termSource="",
)

event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
    entityUrn=term_urn,
    aspect=term_properties_aspect,
)

# Create rest emitter
rest_emitter = DatahubRestEmitter(gms_server="http://localhost:8080")
rest_emitter.emit(event)
log.info(f"Created term {term_urn}")

def create_glossary_term_event(name:str, term_urn:str, definition:str, term_source:str="")->MetadataChangeProposalWrapper:
    # note that glossary terms can also be ingested with a receipe card which is useful 
    # for getting different types of users to populate datahaub with information
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

   