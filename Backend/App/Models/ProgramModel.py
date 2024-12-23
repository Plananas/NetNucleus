from Backend.App.Models.Model import Model


class ProgramModel(Model):
    table_name = "installed_programs"

    client_uuid: str
    program_id: str
    name: str
    version: str

    unique_field = ""

    def to_dict(self) -> dict:
        """
        Convert the object to a dictionary for JSON serialization.
        """
        return {
            "client_uuid": self.client_uuid,
            "program_id": self.program_id,
            "name": self.name,
            "version": self.version
        }
