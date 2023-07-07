# Inlined from /metadata-ingestion/examples/library/create_term.py
import logging

from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph

from glossary.step_2_get_urns_that_have_a_code_column import get_entities_associated_to_domain
from glossary.step_2_get_urns_that_have_a_code_column import get_list_of_datasets_that_contain_relevent_field
from glossary.step_3_add_glossary_term_entities import add_term_to_entities
from step_1_create_term import create_glossary_term_event


# basic example of adding a glossary term and associating that term to datasets within a named domain
# IF they have the column name that matches our glossary term. This example doesn't cover edge cases right now
def create_and_add_glossary_term():
    domain_urn = 'urn:li:domain:renewable_raw_data'
    end_point = "http://localhost:8080"
    rest_emitter = DatahubRestEmitter(gms_server=end_point)
    glossary_event = create_glossary_term_event(name="Code", urn_name='countryCode', definition="3 letter country code")
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    rest_emitter.emit(glossary_event)
    log.info(f"Created term {glossary_event.entityUrn}")

    graph = DataHubGraph(DatahubClientConfig(server=end_point))

    dataset_list = get_entities_associated_to_domain(domain_urn=domain_urn, graph=graph)
    dataset_list_with_field = get_list_of_datasets_that_contain_relevent_field(dataset_list, field_to_look_for='Code',
                                                                               graph=graph)

    for dataset in dataset_list_with_field:
        event = add_term_to_entities(term_urn=glossary_event.entityUrn, dataset_urn=dataset)
        if event:
            rest_emitter.emit(event)
            log.info(f"created association between {glossary_event.entityUrn} and {event.entityUrn}")
            continue


if __name__ == "__main__":
    create_and_add_glossary_term()
