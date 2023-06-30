#find the domain 
#find entites in the domain that have a col 'code'
#associate the glossary term to them
# Inlined from /metadata-ingestion/examples/library/dataset_query_domain.py
from datahub.emitter.mce_builder import make_dataset_urn
from typing import Dict

# read-modify-write requires access to the DataHubGraph (RestEmitter is not enough)
from datahub.ingestion.graph.client import DatahubClientConfig, DataHubGraph

# Imports for metadata model classes
from datahub.metadata.schema_classes import DomainsClass, ContainerClass, DatasetPropertiesClass, BrowsePathsV2Class



gms_endpoint = "http://localhost:8080"
graph = DataHubGraph(DatahubClientConfig(server=gms_endpoint))

domain_urn = 'urn:li:domain:renewable_raw_data'
# you can get properties about a domain using some of the inbuilt methods like below:
# domain_properties = graph.get_domain_properties(domain_urn)

# you can also search by name if you dont have the urn to hand by calling graph.get_domain_urn_by_name

entities_associated_to_domain = graph.execute_graphql(query="""query getDomain {
  domain(urn: "urn:li:domain:renewable_raw_data") {
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
}""")


entity_list = entities_associated_to_domain['domain']['entities']['searchResults']
urn_list = []
for val in entity_list:
    urn_list.append(val['entity']['urn'])

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

