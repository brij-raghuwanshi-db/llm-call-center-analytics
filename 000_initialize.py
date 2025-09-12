# Databricks notebook source
catalog_name = 'users'
schema_name = 'brijendra_raghuwanshi'
source_location = f'/Volumes/{catalog_name}/{schema_name}/conversation_demo_data'


demo_file = f'{source_location}/anonymized_conversation_data.json'

demo_table = f'{catalog_name}.{schema_name}.conversation_demo'
print(demo_table)


VECTOR_SEARCH_ENDPOINT_NAME="dbdemos_vs_endpoint"

source_table_for_embedding = "each_participant_summary"

#The table we'd like to index
embedded_table_fullname = f"{catalog_name}.{schema_name}.each_conversation_participant_summary_embedded"
# Where we want to store our index
vs_index_fullname = f"{catalog_name}.{schema_name}.each_conversation_participant_summary_vsi"

volume_folder = f'/Volumes/{catalog_name}/{schema_name}/conversation_summmary_checkpoint'