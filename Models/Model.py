import sqlite3
from typing import Any, Dict, List

# Abstract Model class
class Model:
    table_name: str = ""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def get_connection(cls):
        """Get a connection to the database."""
        return sqlite3.connect('clients.db')

    @classmethod
    def create_table(cls):
        """Dynamically create a table based on the class attributes."""
        fields = []
        for field, field_type in cls.__annotations__.items():
            sql_type = cls.python_type_to_sql_type(field_type)
            fields.append(f"{field} {sql_type}")
        fields_sql = ", ".join(fields)
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {cls.table_name} ({fields_sql})"
        with cls.get_connection() as conn:
            conn.execute(create_table_sql)

    @staticmethod
    def python_type_to_sql_type(py_type):
        """Map Python types to SQLite types."""
        type_mapping = {
            str: "TEXT",
            int: "INTEGER",
            float: "REAL",
            bool: "INTEGER",
            list: "TEXT",
        }
        return type_mapping.get(py_type, "TEXT")

    def save(self):
        """Save the current instance to the database, updating on conflict."""
        fields = list(self.__annotations__.keys())
        placeholders = ", ".join("?" for _ in fields)
        values = [self._serialize_value(getattr(self, field)) for field in fields]

        # Prepare the ON CONFLICT clause if a unique field is specified
        if self.unique_field:
            updates = ", ".join(f"{field} = excluded.{field}" for field in fields if field != self.unique_field)
            insert_sql = f"""
            INSERT INTO {self.table_name} ({', '.join(fields)})
            VALUES ({placeholders})
            ON CONFLICT({self.unique_field}) DO UPDATE SET {updates}
            """
        else:
            insert_sql = f"INSERT OR REPLACE INTO {self.table_name} ({', '.join(fields)}) VALUES ({placeholders})"

        with self.get_connection() as conn:
            conn.execute(insert_sql, values)

        return self

    @classmethod
    def get(cls, **kwargs) -> "Model":
        """Retrieve a model instance based on query parameters."""
        conditions = " AND ".join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values())

        select_sql = f"SELECT * FROM {cls.table_name} WHERE {conditions}"

        with cls.get_connection() as conn:
            cursor = conn.execute(select_sql, values)
            row = cursor.fetchone()
            if row:
                field_names = [description[0] for description in cursor.description]
                row_dict = dict(zip(field_names, row))
                return cls(**cls._deserialize_row(row_dict))
        return None

    @staticmethod
    def _serialize_value(value: Any) -> Any:
        """Serialize values for storage in the database."""
        if isinstance(value, list):
            return ",".join(value)
        if isinstance(value, bool):
            return int(value)
        return value

    @classmethod
    def _deserialize_row(cls, row: Dict[str, Any]) -> Dict[str, Any]:
        """Deserialize row values back into Python types."""
        deserialized = {}
        for field, value in row.items():
            field_type = cls.__annotations__.get(field, str)
            if field_type == bool:
                deserialized[field] = bool(value)
            elif field_type == list:
                deserialized[field] = value.split(",") if value else []
            else:
                deserialized[field] = value
        return deserialized

