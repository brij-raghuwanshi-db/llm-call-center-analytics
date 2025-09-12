# Databricks notebook source
# DBTITLE 1,initialize paths
# MAGIC %run ./000_initialize

# COMMAND ----------

# DBTITLE 1,Show Demo Data
import json

with open(demo_file, 'r') as file:
  data = json.load(file)
  display(data)

# COMMAND ----------

# DBTITLE 1,Pandas to Spark, since small files
import pandas as pd
import json

dir_path = source_location

files = [f.path for f in dbutils.fs.ls(dir_path) if f.path.endswith('.json')]

dfs = []
for file_path in files:
    with open(file_path[5:], 'r') as file:
        data = json.load(file)
    dfs.append(pd.json_normalize(data))

df = pd.concat(dfs, ignore_index=True)

# COMMAND ----------

# DBTITLE 1,Total Conversations
size = len(df)
size

# COMMAND ----------

from pyspark.sql.functions import col, expr

sentences_sdf = spark.createDataFrame(df[['conversation.id', 'conversation.duration', 'conversation.title', 'extensiveConversation.data.title', 'extensiveConversation.data.language_code', 'conversation.event_start_date', 'conversation.event_end_date', 'sentences', 'extensiveConversation.data.attendees', 'extensiveConversation.data.invitees']]).withColumn(
    "sentences_updated",
    expr("""
        transform(
            sentences,
            x -> concat(
                coalesce(
                    filter(
                        transform(
                            `extensiveConversation.data.attendees`,
                            a -> case
                                when a.id = x.recording_attendee_id and a.email is not null and a.email != '' then a.email
                                when a.id = x.recording_attendee_id and (a.email is null or a.email = '') and a.full_name is not null and a.full_name != '' then a.full_name
                                else null
                            end
                        ),
                        y -> y is not null
                    )[0],
                    x.recording_attendee_id
                ),
                ' : ',
                x.text
            )
        )
    """)
).drop("sentences")

sentences_sdf.write.mode('overwrite').saveAsTable(demo_table)

# COMMAND ----------

# DBTITLE 1,IMURICA conversations
spark.table(demo_table).display()

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table users.brijendra_raghuwanshi.conversation_participant_summary as
# MAGIC with participant_summary as (SELECT 
# MAGIC `conversation.id` as conversation_id, `conversation.title` as title, `conversation.event_start_date` as event_start_date, `conversation.event_end_date` as event_end_date,
# MAGIC   ai_query(
# MAGIC     -- "databricks-llama-4-maverick",
# MAGIC     'databricks-claude-3-7-sonnet',
# MAGIC "Analyze this sales call transcript and extract individual participant details. Translate the language to english wherever fits. Wherever you find imurica in the name, is a internal employee. So, note it as 'sales rep'. Return as JSON array.
# MAGIC
# MAGIC I do not want any information related to cision or their customers or the person who they are interacting with to be stored. But, we still want all of the information. So, in effort to do this, you need to change the names to fake names, the company details to fake company details. Also, the conversations if have any sensitive information, change that to something that is maintaining the context of the discussion without revealing the information
# MAGIC Do not write the mapping information to the output.
# MAGIC
# MAGIC You are a business analyst extracting individual participant performance data from business conversations (sales calls, onboarding, demos, meetings) to improve business outcomes.: "
# MAGIC || ' - TRANSCRIPT: ' || to_json(`sentences_updated`) || "
# MAGIC
# MAGIC Return format:
# MAGIC [
# MAGIC {
# MAGIC 'conversation_title': 'Conversation Title',
# MAGIC 'name': 'masked Participant ID',
# MAGIC 'role': 'Role',
# MAGIC 'performance_metrics': '[talk time percentage, engagement level, communication quality, technical competence, problem solving ability, influence effectiveness]',
# MAGIC 'sales_skills': '[consultative approach, value proposition delivery, discovery quality, objection handling, closing effectiveness, relationship building]',
# MAGIC 'customer_focus': '[client understanding, solution matching, proactive support, empathy demonstration, customer experience focus]',
# MAGIC 'platform_expertise': '[feature knowledge, demo delivery, technical problem solving, integration awareness, competitive positioning]',
# MAGIC 'communication':  '[clarity, active listening, presentation skills, facilitation ability, conflict resolution]',
# MAGIC 'strengths': '[Top 3 capabilities with specific examples, Unique value contributions, Consistent performance areas, other_strengths]',
# MAGIC 'recommendations': '[Immediate actions (24-48 hours), Short-term development (1-2 weeks), Medium-term goals (1-3 months)]',
# MAGIC 'manager_actions': '[Coaching focus areas, Resource allocation needs, Performance monitoring requirements]',
# MAGIC 'impact_assessment': '[Revenue impact, customer satisfaction contribution, Team dynamics effect, process improvement value, sales_impact_assessment]',
# MAGIC 'celebrations': '[Exceptional moments with examples, Client praise received, Problem resolution successes]',
# MAGIC 'performance_score': '[1-10]',
# MAGIC 'meeting_summary_from_my_perspective' : '[detailed summary]',
# MAGIC 'meeting_summary_from_their_perspective' : '[detailed summary]'
# MAGIC }
# MAGIC ]
# MAGIC
# MAGIC Focus on actionable insights for sales improvement.
# MAGIC ",
# MAGIC     
# MAGIC     responseFormat => '{
# MAGIC     "type": "json_schema",
# MAGIC     "json_schema": {
# MAGIC         "name": "participant_analysis",
# MAGIC         "schema": {
# MAGIC             "type": "object",
# MAGIC             "properties": {
# MAGIC                 "participants": {
# MAGIC                     "type": "array",
# MAGIC                     "items": {
# MAGIC                         "type": "object",
# MAGIC                         "properties": {
# MAGIC                             "name": {"type": "string"},
# MAGIC                             "email_id": {"type": "string"},
# MAGIC                             "role": {"type": "string"},
# MAGIC                             "performance_metrics": {
# MAGIC                                 "type": "array",
# MAGIC                                 "items": {"type": "string"}
# MAGIC                             },
# MAGIC                             "sales_skills": {
# MAGIC                                 "type": "array",
# MAGIC                                 "items": {"type": "string"}
# MAGIC                             },
# MAGIC                             "customer_focus": {
# MAGIC                                 "type": "array",
# MAGIC                                 "items": {"type": "string"}
# MAGIC                             },
# MAGIC                             "platform_expertise": {
# MAGIC                                 "type": "array",
# MAGIC                                 "items": {"type": "string"}
# MAGIC                             },
# MAGIC                             "communication": {
# MAGIC                                 "type": "array",
# MAGIC                                 "items": {"type": "string"}
# MAGIC                             },
# MAGIC                             "strengths": {
# MAGIC                                 "type": "array",
# MAGIC                                 "items": {"type": "string"}
# MAGIC                             },
# MAGIC                             "recommendations": {
# MAGIC                                 "type": "array",
# MAGIC                                 "items": {"type": "string"}
# MAGIC                             },
# MAGIC                             "manager_actions": {
# MAGIC                                 "type": "array",
# MAGIC                                 "items": {"type": "string"}
# MAGIC                             },
# MAGIC                             "impact_assessment": {
# MAGIC                                 "type": "array",
# MAGIC                                 "items": {"type": "string"}
# MAGIC                             },
# MAGIC                             "celebrations": {
# MAGIC                                 "type": "array",
# MAGIC                                 "items": {"type": "string"}
# MAGIC                             },
# MAGIC                             "meeting_summary_from_my_perspective": {"type": "string"},
# MAGIC                             "meeting_summary_from_their_perspective": {"type": "string"},
# MAGIC                             "performance_score": {"type": "integer"},
# MAGIC                             "engagement_level": {"type": "string"},
# MAGIC                             "sales_impact": {"type": "string"}
# MAGIC                         },
# MAGIC                         "required": [
# MAGIC                             "name", "role", "email_id", "performance_metrics", "sales_skills", "customer_focus", "platform_expertise", "communication", "strengths", "recommendations", "manager_actions", "impact_assessment", "celebrations", "meeting_summary_from_my_perspective", "meeting_summary_from_their_perspective", "performance_score", "engagement_level", "sales_impact"
# MAGIC                         ],
# MAGIC                         "additionalProperties": false
# MAGIC                     }
# MAGIC                 }
# MAGIC             },
# MAGIC             "required": ["participants"],
# MAGIC             "additionalProperties": false
# MAGIC         },
# MAGIC         "strict": true
# MAGIC     }
# MAGIC }'
# MAGIC   ) AS participant_analysis
# MAGIC FROM users.brijendra_raghuwanshi.conversation_demo
# MAGIC )
# MAGIC select conversation_id, title, event_start_date, event_end_date,
# MAGIC --schema_of_json(participant_analysis),
# MAGIC from_json(participant_analysis, 'STRUCT<participants: ARRAY<STRUCT<celebrations: ARRAY<STRING>, communication: ARRAY<STRING>, customer_focus: ARRAY<STRING>, email_id: STRING, engagement_level: STRING, impact_assessment: ARRAY<STRING>, manager_actions: ARRAY<STRING>, meeting_summary_from_my_perspective: STRING, meeting_summary_from_their_perspective: STRING, name: STRING, performance_metrics: ARRAY<STRING>, performance_score: BIGINT, platform_expertise: ARRAY<STRING>, recommendations: ARRAY<STRING>, role: STRING, sales_impact: STRING, sales_skills: ARRAY<STRING>, strengths: ARRAY<STRING>>>>') as participant_analysis from participant_summary

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from users.brijendra_raghuwanshi.conversation_participant_summary

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from users.brijendra_raghuwanshi.conversation_participant_summary limit 1

# COMMAND ----------

# MAGIC %sql
# MAGIC create or replace table users.brijendra_raghuwanshi.each_participant_summary
# MAGIC select 
# MAGIC   conversation_id, title, event_start_date, event_end_date,
# MAGIC   participant.name as name, 
# MAGIC   participant
# MAGIC from users.brijendra_raghuwanshi.conversation_participant_summary
# MAGIC lateral view explode(participant_analysis.participants) as participant

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from users.brijendra_raghuwanshi.each_participant_summary