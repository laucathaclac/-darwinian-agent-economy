"""Core data models for the DAE MVP."""
from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class Task:
    task_id: str
    title: str
    expected_revenue: float
    estimated_cost: float
    estimated_hours: float
    confidence: float
    risk: float
    source: str = "manual"

    def validate(self) -> None:
        if not self.task_id.strip() or not self.title.strip():
            raise ValueError("task_id and title are required")
        for name, value in (("expected_revenue", self.expected_revenue),
                            ("estimated_cost", self.estimated_cost),
                            ("estimated_hours", self.estimated_hours)):
            if value < 0:
                raise ValueError(f"{name} cannot be negative")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if not 0 <= self.risk <= 1:
            raise ValueError("risk must be between 0 and 1")


@dataclass(frozen=True)
class TaskScore:
    task_id: str
    score: float
    expected_net: float
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class SafetyPolicy:
    max_cost_per_task: float = 10.0
    max_daily_spend: float = 25.0
    min_confidence: float = 0.60
    max_risk: float = 0.55
    min_net_profit: float = 1.0
    max_active_agents: int = 3

    def validate(self) -> None:
        if min(self.max_cost_per_task, self.max_daily_spend, self.min_net_profit) < 0:
            raise ValueError("monetary policy limits cannot be negative")
        if not 0 <= self.min_confidence <= 1 or not 0 <= self.max_risk <= 1:
            raise ValueError("confidence and risk limits must be between 0 and 1")
        if self.max_active_agents < 1:
            raise ValueError("max_active_agents must be at least 1")


@dataclass(frozen=True)
class AgentResult:
    revenue: float
    cost: float
    verified: bool = True

    def __post_init__(self) -> None:
        if self.revenue < 0 or self.cost < 0:
            raise ValueError("revenue and cost cannot be negative")

    @property
    def net(self) -> float:
        return self.revenue - self.cost


class EvolutionAction(str, Enum):
    CONTINUE = "continue"
    PAUSE = "pause"
    REVIEW_REPLICATION = "review_replication"


@dataclass
class AgentHistory:
    agent_id: str
    results: list[AgentResult] = field(default_factory=list)
