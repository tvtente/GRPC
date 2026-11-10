"""Contratos Pydantic: entrada validada y salida sin credenciales."""

from datetime import date as DateValue, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator


class InputSchema(BaseModel):
    # Rechaza, entre otros, un user_id enviado por el cliente.
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class UserCreate(InputSchema):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: SecretStr = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: SecretStr) -> SecretStr:
        password = value.get_secret_value()
        if not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password):
            raise ValueError("La contraseña debe contener letras y números.")
        return value


class UserLogin(InputSchema):
    username: str = Field(min_length=1, max_length=80)
    password: SecretStr = Field(min_length=1, max_length=128)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    created_at: datetime


class ExpenseCreate(InputSchema):
    description: str = Field(min_length=1, max_length=300)
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    date: DateValue
    category_id: int = Field(gt=0)

    @field_validator("date")
    @classmethod
    def date_not_in_future(cls, value: DateValue) -> DateValue:
        if value > DateValue.today():
            raise ValueError("La fecha del gasto no puede ser futura.")
        return value


class ExpenseUpdate(ExpenseCreate):
    """Edición completa del formulario; no es un parche parcial."""


class ExpenseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    description: str
    amount: Decimal
    date: DateValue
    category_id: int
    # La identidad del propietario se obtiene en el servidor, no del formulario.


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
