from decimal import Decimal

from django.core.exceptions import ValidationError

__all__ = [
    'validate_latitude',
    'validate_longitude',
]


def _in_range(
    value: Decimal, *, min_value: Decimal, max_value: Decimal
) -> None:
    """Enforce that *value* lies between *min_value* and *max_value*."""
    if value < min_value or value > max_value:
        raise ValidationError(
            f'Value {value} must be between {min_value} and {max_value}.',
            params={'value': value},
        )


def validate_latitude(value: Decimal) -> None:
    """Validate that *value* is a geographic latitude (-90 to 90)."""
    MAX_LATITUDE_DEGREE = 90
    _in_range(
        value,
        min_value=Decimal(-MAX_LATITUDE_DEGREE),
        max_value=Decimal(MAX_LATITUDE_DEGREE),
    )


def validate_longitude(value: Decimal) -> None:
    """Validate that *value* is a geographic longitude (-180 to 180)."""
    MAX_LONGITUDE_DEGREE = 180
    _in_range(
        value,
        min_value=Decimal(-MAX_LONGITUDE_DEGREE),
        max_value=Decimal(MAX_LONGITUDE_DEGREE),
    )
