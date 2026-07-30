from __future__ import annotations
from typing import Dict, Type
from dqguardian.checks.base import BaseCheck
from dqguardian.checks.completeness import CompletenessCheck
from dqguardian.checks.custom_sql import CustomSQLCheck
from dqguardian.checks.freshness import FreshnessCheck
from dqguardian.checks.referential import ReferentialIntegrityCheck
from dqguardian.checks.schema import SchemaDriftCheck
from dqguardian.checks.uniqueness import UniquenessCheck
from dqguardian.checks.volume import VolumeCheck

REGISTRY: Dict[str, Type[BaseCheck]] = {
    "completeness": CompletenessCheck,
    "uniqueness": UniquenessCheck,
    "freshness": FreshnessCheck,
    "volume": VolumeCheck,
    "schema": SchemaDriftCheck,
    "referential_integrity": ReferentialIntegrityCheck,
    "custom_sql": CustomSQLCheck,
}

def get_check(check_type: str) -> Type[BaseCheck]:
    if check_type not in REGISTRY:
        raise KeyError(f"Unknown check type: {check_type}. Available: {list(REGISTRY.keys())}")
    return REGISTRY[check_type]

def list_check_types() -> list:
    return list(REGISTRY.keys())