"""迁移计划核心：task / plan / decompose。"""
from .task import Subtask, Status
from .plan import MigrationPlan
from .decompose import DecomposeOptions, decompose, enrich_read_scope

__all__ = ["Subtask", "Status", "MigrationPlan", "DecomposeOptions", "decompose", "enrich_read_scope"]
