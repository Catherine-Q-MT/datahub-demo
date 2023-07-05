import logging
import time
from typing import Optional

from datahub.emitter.mce_builder import make_dataset_urn, make_term_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper

# read-modify-write requires access to the DataHubGraph (RestEmitter is not enough)
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph

from datahub.metadata.schema_classes import (
    AuditStampClass,
    GlossaryTermAssociationClass,
    GlossaryTermsClass,
)

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

gms_endpoint = "http://localhost:8080"
graph = DataHubGraph(DatahubClientConfig(server=gms_endpoint))

dataset_urn = "urn:li:dataset:(urn:li:dataPlatform:s3,datahub-cq/raw_data/wind-generation.csv,PROD)"

def get_current_terms_associated_to_dataset(dataset_urn:str)->Optional[GlossaryTermsClass]:

    current_terms = graph.get_aspect(
        entity_urn=dataset_urn, aspect_type=GlossaryTermsClass
    )
    return current_terms

# print(current_terms)
#  term_to_add = "urn:li:glossaryTerm:81b95797-70dd-4656-9d9a-22b1e2d0dc6b"

def add_term_to_entities(term_urn:str)->Optional[MetadataChangeProposalWrapper]:  
    term_association_to_add = GlossaryTermAssociationClass(urn=term_urn)
    # an audit stamp that basically says we have no idea when these terms were added to this dataset
    # change the time value to (time.time() * 1000) if you want to specify the current time of running this code as the time
    unknown_audit_stamp = AuditStampClass(time=(time.time() * 1000), actor="urn:li:corpuser:ingestion")
    need_write = False
    if current_terms:
        if term_urn not in [x.urn for x in current_terms.terms]:
            # terms exist, but this term is not present in the current terms
            current_terms.terms.append(term_association_to_add)
            need_write = True
    else:
        # create a brand new terms aspect
        current_terms = GlossaryTermsClass(
            terms=[term_association_to_add],
            auditStamp=unknown_audit_stamp,
        )
        need_write = True

    if need_write:
        event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
            entityUrn=dataset_urn,
            aspect=current_terms,
        )
        return event
    else:
        log.info(f"Term {term_to_add} already exists, omitting write")
