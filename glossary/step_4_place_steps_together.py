
# Inlined from /metadata-ingestion/examples/library/create_term.py
import logging

from datahub.emitter.mce_builder import make_term_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph

# Imports for metadata model classes
from datahub.metadata.schema_classes import GlossaryTermInfoClass
from step_2_get_urns_that_have_a_code_column import get_list_of_datasets_that_contain_relevent_field
from step_2_get_urns_that_have_a_code_column import get_entities_associated_to_domain

from step_1_create_term import create_glossary_term_event
# def create_glossary_term_event(name:str, term_urn:str, definition:str, term_source:str="")
def create_and_add_glossary_term():
    end_point="http://localhost:8080"
    rest_emitter = DatahubRestEmitter(gms_server=end_point)
    glossary_event=create_glossary_term_event(name="Code", urn_name='countryCode', definition="3 letter country code")
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)


    rest_emitter.emit(glossary_event)
    log.info(f"Created term {glossary_event.entityUrn}")

    domain_urn = 'urn:li:domain:renewable_raw_data'
    graph = DataHubGraph(DatahubClientConfig(server=end_point))


    entity_list = get_entities_associated_to_domain(domain_urn=domain_urn,graph=graph )
    print(entity_list)
    entity_list_with_field = get_list_of_datasets_that_contain_relevent_field(entity_list, field_to_look_for='Code', graph=graph)
    print(entity_list_with_field)



if __name__ == "__main__":
    create_and_add_glossary_term()