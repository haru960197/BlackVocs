from bson import ObjectId
from typing import Any
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema: 
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(), 
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId), 
                core_schema.no_info_plain_validator_function(cls.validate), 
            ])
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: core_schema.CoreSchema, handler) -> JsonSchemaValue:
        return {"type": "string"}

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
