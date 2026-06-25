from sqlalchemy import inspect, text, update
from sqlalchemy.engine import Engine
from sqlalchemy.schema import CreateColumn

from app.agents.models import Agent


DEFAULT_VALUES = {
    "pricing_model": "free",
    "price_per_call": 0.0,
    "capabilities": [],
    "is_active": True,
    "health_status": "unknown",
    "trust_score": 0.0,
}


def sync_agent_registry_schema(engine: Engine) -> None:
    table = Agent.__table__
    table.create(bind=engine, checkfirst=True)

    inspector = inspect(engine)
    existing_columns = {
        column["name"]
        for column in inspector.get_columns(table.name)
    }
    missing_columns = [
        column
        for column in table.columns
        if column.name not in existing_columns
    ]

    if not missing_columns:
        return

    with engine.begin() as connection:
        for column in missing_columns:
            column_sql = CreateColumn(column).compile(dialect=engine.dialect)
            connection.execute(
                text(f"ALTER TABLE {table.name} ADD COLUMN {column_sql}")
            )

        default_updates = {
            name: value
            for name, value in DEFAULT_VALUES.items()
            if name in {column.name for column in missing_columns}
        }
        if default_updates:
            connection.execute(
                update(Agent)
                .where(
                    *[
                        getattr(Agent, name).is_(None)
                        for name in default_updates
                    ]
                )
                .values(**default_updates)
            )
