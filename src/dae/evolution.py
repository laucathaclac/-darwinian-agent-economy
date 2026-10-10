"""Evolution decisions are recommendations only; no agent is spawned."""
from .models import AgentHistory, EvolutionAction


def evaluate_agent(history: AgentHistory, *, min_verified_results: int = 5,
                   min_average_net: float = 2.0, max_consecutive_losses: int = 3,
                   active_agents: int = 1, max_active_agents: int = 3) -> tuple[EvolutionAction, str]:
    if min_verified_results < 1 or max_consecutive_losses < 1:
        raise ValueError("review thresholds must be positive")
    if active_agents < 1 or max_active_agents < 1:
        raise ValueError("agent counts must be positive")
    if not history.results:
        return EvolutionAction.PAUSE, "No outcome history; gather evidence before continuing."

    losses = 0
    for result in reversed(history.results):
        if result.net < 0:
            losses += 1
        else:
            break
    if losses >= max_consecutive_losses:
        return EvolutionAction.PAUSE, f"{losses} consecutive losses reached the pause threshold."

    verified = [result for result in history.results if result.verified]
    if len(verified) < min_verified_results:
        remaining = min_verified_results - len(verified)
        return EvolutionAction.CONTINUE, f"Need {remaining} more verified result(s) before replication review."

    average_net = sum(result.net for result in verified) / len(verified)
    if average_net < min_average_net:
        return EvolutionAction.CONTINUE, f"Average verified net {average_net:.2f} is below threshold {min_average_net:.2f}."
    if active_agents >= max_active_agents:
        return EvolutionAction.CONTINUE, "Agent cap reached; replication is not eligible."
    return EvolutionAction.REVIEW_REPLICATION, (
        f"Eligible for human review: {len(verified)} verified results, "
        f"average net {average_net:.2f}. No agent was created."
    )
