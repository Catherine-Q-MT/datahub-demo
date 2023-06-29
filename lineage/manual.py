import datahub.emitter.mce_builder as builder
from datahub.emitter.rest_emitter import DatahubRestEmitter

# Construct a lineage object.

lineage_mce = builder.make_lineage_mce(
    [
        builder.make_dataset_urn("s3", "datahub-cq/raw_data/hydropower-consumption.csv"),  # Upstream connection or connections ( I am specifying the raw data in my pipeline)
        builder.make_dataset_urn("s3", "datahub-cq/raw_data/solar-energy-consumption.csv"),  

    ],
    builder.make_dataset_urn("s3", "uk_solar_and_hydro.csv"),  # Downstream
)

# Create an emitter to the GMS REST API. Emitters can emit information and info can be accessed via API
emitter = DatahubRestEmitter("http://localhost:8080")

# Emit metadata!
emitter.emit_mce(lineage_mce)

# solar-energy-consumption.csv