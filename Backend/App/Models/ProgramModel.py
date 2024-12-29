from typing import Optional

from Backend.App.Models.Model import Model


class ProgramModel(Model):
    table_name = "installed_programs"

    client_uuid: str
    name: str
    current_version: str
    available_version: Optional[str]

    unique_field = ""

    def to_dict(self) -> dict:
        """
        Convert the object to a dictionary for JSON serialization.
        """
        return {
            "client_uuid": self.client_uuid,
            "name": self.name,
            "current_version": self.current_version,
            "available_version": self.available_version
        }
