"""Ephemeral memory policy primitives; no persistence or conversation storage."""

from dataclasses import dataclass


@dataclass(slots=True)
class SessionMemory:
    """Count turns for one process without retaining user-provided content."""

    turns_seen: int = 0
    long_term_enabled: bool = False
    sensitive_data_enabled: bool = False

    def record_turn(self) -> None:
        """Increment a session-local counter only."""
        if self.long_term_enabled or self.sensitive_data_enabled:
            raise ValueError("This prototype does not permit persistent or sensitive memory")
        self.turns_seen += 1
