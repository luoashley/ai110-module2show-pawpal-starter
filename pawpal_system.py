"""PawPal+ logic layer.

Backend classes for the PawPal+ pet care planning assistant. This module
holds the domain model (Owner, Pet, CareTask) and the scheduling logic
(DailySchedule). Skeleton generated from diagrams/uml_draft.mmd.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class CareTask:
    """A single unit of pet care, e.g. feeding, walking, or medication."""

    title: str
    duration_minutes: int
    priority: str
    category: str
    preferred_time: str
    completed: bool = False

    def update_task(self, title: str, duration: int, priority: str) -> None:
        """Update this task's editable fields."""
        ...

    def mark_complete(self) -> None:
        """Mark this task as done."""
        ...

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        ...


@dataclass
class Pet:
    """A pet and the care tasks associated with it."""

    name: str
    species: str
    age: int
    care_tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Attach a care task to this pet."""
        ...

    def remove_task(self, task_title: str) -> None:
        """Remove a care task from this pet by title."""
        ...

    def get_tasks(self) -> List[CareTask]:
        """Return this pet's care tasks."""
        ...

    def update_info(self, name: str, species: str, age: int) -> None:
        """Update this pet's basic information."""
        ...


@dataclass
class Owner:
    """A pet owner, their preferences, and the pets they own."""

    name: str
    available_minutes: int
    preferences: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        ...

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet from this owner by name."""
        ...

    def update_preferences(self, preferences: str) -> None:
        """Update this owner's care preferences."""
        ...

    def get_pets(self) -> List[Pet]:
        """Return this owner's pets."""
        ...


@dataclass
class DailySchedule:
    """A plan of care tasks for a single day, built from time/priority constraints."""

    date: str
    available_minutes: int
    scheduled_tasks: List[CareTask] = field(default_factory=list)
    skipped_tasks: List[CareTask] = field(default_factory=list)

    def generate_plan(self, tasks: List[CareTask]) -> None:
        """Choose and order tasks into a daily plan within the time budget."""
        ...

    def add_scheduled_task(self, task: CareTask) -> None:
        """Add a task to the scheduled list."""
        ...

    def skip_task(self, task: CareTask) -> None:
        """Move a task to the skipped list (did not fit the plan)."""
        ...

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why tasks were scheduled or skipped."""
        ...
