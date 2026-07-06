"""PawPal+ logic layer.

Backend classes for the PawPal+ pet care planning assistant. This module
holds the domain model (Owner, Pet, CareTask) and the scheduling logic
(DailySchedule). Based on diagrams/uml_draft.mmd.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Priority(str, Enum):
    """Task priority levels; Enum keeps scheduling reliable and comparable."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def rank(self) -> int:
        """Return a numeric weight (higher = more important) for sorting."""
        return {Priority.LOW: 0, Priority.MEDIUM: 1, Priority.HIGH: 2}[self]


@dataclass
class CareTask:
    """A single unit of pet care, e.g. feeding, walking, or medication."""

    title: str
    duration_minutes: int
    priority: Priority
    category: str
    preferred_time: str
    pet_name: str = ""
    completed: bool = False

    def update_task(self, title: str, duration: int, priority: Priority) -> None:
        """Update this task's title, duration, and priority in place."""
        self.title = title
        self.duration_minutes = duration
        self.priority = priority

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def is_high_priority(self) -> bool:
        """Return True if this task is high priority."""
        return self.priority == Priority.HIGH


@dataclass
class Pet:
    """A pet and the care tasks associated with it."""

    name: str
    species: str
    age: int
    care_tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Attach a care task to this pet, stamping it with the pet's name."""
        task.pet_name = self.name
        self.care_tasks.append(task)

    def remove_task(self, task_title: str) -> None:
        """Remove all care tasks matching the given title."""
        self.care_tasks = [t for t in self.care_tasks if t.title != task_title]

    def get_tasks(self) -> List[CareTask]:
        """Return this pet's care tasks."""
        return self.care_tasks

    def update_info(self, name: str, species: str, age: int) -> None:
        """Update this pet's basic information."""
        self.name = name
        self.species = species
        self.age = age


@dataclass
class Owner:
    """A pet owner, their preferences, and the pets they own."""

    name: str
    available_minutes: int
    preferences: str
    pets: List[Pet] = field(default_factory=list)
    schedules: List["DailySchedule"] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove all pets matching the given name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def update_preferences(self, preferences: str) -> None:
        """Update this owner's care preferences."""
        self.preferences = preferences

    def get_pets(self) -> List[Pet]:
        """Return this owner's pets."""
        return self.pets

    def get_all_tasks(self) -> List[CareTask]:
        """Return every care task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.get_tasks()]

    def create_schedule(self, date: str) -> "DailySchedule":
        """Create a DailySchedule seeded with this owner's time budget and track it."""
        schedule = DailySchedule(date=date, available_minutes=self.available_minutes)
        self.schedules.append(schedule)
        return schedule


@dataclass
class DailySchedule:
    """A plan of care tasks for a single day, built from time/priority constraints."""

    date: str
    available_minutes: int
    scheduled_tasks: List[CareTask] = field(default_factory=list)
    skipped_tasks: List[CareTask] = field(default_factory=list)

    def generate_plan(self, tasks: List[CareTask]) -> None:
        """Greedily fit highest-priority incomplete tasks into the time budget."""
        self.scheduled_tasks = []
        self.skipped_tasks = []
        remaining = self.available_minutes
        # Highest priority first, then shortest task to fit more in.
        ordered = sorted(
            tasks, key=lambda t: (-t.priority.rank, t.duration_minutes)
        )
        for task in ordered:
            if task.completed:
                continue
            if task.duration_minutes <= remaining:
                self.add_scheduled_task(task)
                remaining -= task.duration_minutes
            else:
                self.skip_task(task)
        # Present the day ordered by the owner's preferred time.
        self.scheduled_tasks.sort(key=lambda t: t.preferred_time)

    def add_scheduled_task(self, task: CareTask) -> None:
        """Add a task to the scheduled list."""
        self.scheduled_tasks.append(task)

    def skip_task(self, task: CareTask) -> None:
        """Move a task to the skipped list (did not fit the plan)."""
        self.skipped_tasks.append(task)

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the day's scheduled and skipped tasks."""
        used = sum(t.duration_minutes for t in self.scheduled_tasks)
        lines = [
            f"Today's Schedule ({self.date})",
            f"Time budget: {used}/{self.available_minutes} min used",
            "",
        ]
        if self.scheduled_tasks:
            lines.append("Scheduled:")
            for t in self.scheduled_tasks:
                lines.append(
                    f"  {t.preferred_time}  {t.title} for {t.pet_name} "
                    f"({t.duration_minutes} min, {t.priority.value} priority)"
                )
        else:
            lines.append("Scheduled: nothing fit the time budget.")
        if self.skipped_tasks:
            lines.append("")
            lines.append("Skipped (not enough time):")
            for t in self.skipped_tasks:
                lines.append(
                    f"  {t.title} for {t.pet_name} "
                    f"({t.duration_minutes} min, {t.priority.value} priority)"
                )
        return "\n".join(lines)
