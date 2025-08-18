from agno.storage.sqlite import SqliteStorage

memory_db = SqliteStorage(
    table_name="workflow_test",
    db_file="tmp/workflow_test.db",
    mode="workflow_v2",
)
