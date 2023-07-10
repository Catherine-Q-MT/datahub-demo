import logging

from datahub.emitter.mce_builder import make_domain_urn
from datahub.emitter.mcp import MetadataChangeProposalWrapper
from datahub.emitter.rest_emitter import DatahubRestEmitter
from datahub.metadata.schema_classes import ChangeTypeClass, DomainPropertiesClass

from glossary.config_vars import gms_server

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

domain_urn = make_domain_urn("renewable_raw_data")
domain_properties_aspect = DomainPropertiesClass(
    name="Renewables Raw Data", description="Entities related to the raw renewables data"
)

event: MetadataChangeProposalWrapper = MetadataChangeProposalWrapper(
    entityType="domain",
    changeType=ChangeTypeClass.UPSERT,
    entityUrn=domain_urn,
    aspect=domain_properties_aspect,
)

rest_emitter = DatahubRestEmitter(gms_server=gms_server)
rest_emitter.emit(event)
log.info(f"Created domain {domain_urn}")