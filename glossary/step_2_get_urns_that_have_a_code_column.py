#find the domain 
#find entites in the domain that have a col 'code'
#associate the glossary term to them
# Inlined from /metadata-ingestion/examples/library/dataset_query_domain.py
from datahub.emitter.mce_builder import make_dataset_urn
from typing import Dict, List

# read-modify-write requires access to the DataHubGraph (RestEmitter is not enough)
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph

# Imports for metadata model classes
from datahub.metadata.schema_classes import DomainsClass, ContainerClass, DatasetPropertiesClass, BrowsePathsV2Class
from string import Template


gms_endpoint = "http://localhost:8080"
graph = DataHubGraph(DatahubClientConfig(server=gms_endpoint))

domain_urn = 'urn:li:domain:renewable_raw_data'
# you can get properties about a domain using some of the inbuilt methods like below:
# domain_properties = graph.get_domain_properties(domain_urn)

# you can also search by name if you dont have the urn to hand by calling graph.get_domain_urn_by_name

def get_entities_associated_to_domain(domain_urn:str, graph: DataHubGraph)->List[str]:
    
    
    settings = {"domain_urn":domain_urn}
    query_string = """query getDomain {
    domain(urn:"$domain_urn") {
      urn
      properties {
        name
        description
      }

      entities{
        total
        searchResults{entity{
          urn
        }}
        
      }
    }
  }"""
    query = Template(query_string).substitute(**settings)
    entities_associated_to_domain = graph.execute_graphql(query=query)
    entity_list = entities_associated_to_domain['domain']['entities']['searchResults']
    urn_list = []
    for val in entity_list:
        urn_list.append(val['entity']['urn'])
    return urn_list

query_to_get_field_names_for_a_dataset = """ 
  query {
  dataset(urn: "urn:li:dataset:(urn:li:dataPlatform:s3,datahub-cq/raw_data/wind-generation.csv,PROD)") {
    schemaMetadata {
      fields {
        fieldPath
        description
      }
    }
  }
}"""

result = graph.execute_graphql(query_to_get_field_names_for_a_dataset)
print(result)
fields_list = result.get('dataset').get('schemaMetadata').get('fields')

gloassary_urn = "urn:li:glossaryTerm:81b95797-70dd-4656-9d9a-22b1e2d0dc6b"