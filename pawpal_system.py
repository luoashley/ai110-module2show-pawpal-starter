"""PawPal+ Logic Layer.

Backend domain models and scheduling engines for the PawPal+ pet care assistant.
Handles complex constraints, priority matrices, time-blocking interval overlaps,
automatic task renewals, and robust JSON serialization.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum
from typing import List, Optional, Dict, Any


class Priority(str, Enum):
    """Task priority levels with intrinsic sorting weights."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def rank(self) -> int:
        """Return a numeric weight for priority-first sorting logic."""
        return {Priority.LOW: 0, Priority.MEDIUM: 1, Priority.HIGH: 2}[self]


@dataclass
class CareTask:
    """Represents an atomic care activity for a pet with scheduling metadata."""

    title: str
    duration_minutes: int
    priority: Priority
    category: str
    preferred_time: str  # Format: "HH:MM"
    frequency: str = "none"  # "none", "daily", or "weekly"
    due_date: str = ""       # Format: "YYYY-MM-DD"
    pet_name: str = ""
    completed: bool = False

    def update_task(self, title: str, duration: int, priority: Priority) -> None:
        """Update core parameters of the task in-place."""
        self.title = title
        self.duration_minutes = duration
        self.priority = priority

    def mark_complete(self) -> None:
        """Toggle completion status to True."""
        self.completed = True

    def is_high_priority(self) -> bool:
        """Check if task matches high-priority criteria."""
        return self.priority == Priority.HIGH

    def next_occurrence(self) -> Optional["CareTask"]:
        """Generate a clean, uncompleted duplicate task advanced by the target frequency delta."""
        if self.frequency not in ("daily", "weekly"):
            return None
        base_date = date.fromisoformat(self.due_date) if self.due_date else date.today()
        delta = timedelta(days=1) if self.frequency == "daily" else timedelta(weeks=1)
        return CareTask(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            preferred_time=self.preferred_time,
            frequency=self.frequency,
            due_date=(base_date + delta).isoformat(),
            pet_name=self.pet_name,
            completed=False,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize instance to a JSON-compatible dictionary."""
        return {
            "title": self.title,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority.value,
            "category": self.category,
            "preferred_time": self.preferred_time,
            "frequency": self.frequency,
            "due_date": self.due_date,
            "pet_name": self.pet_name,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CareTask":
        """Instantiate a CareTask from a structured dictionary."""
        return cls(
            title=data["title"],
            duration_minutes=data["duration_minutes"],
            priority=Priority(data["priority"]),
            category=data["category"],
            preferred_time=data["preferred_time"],
            frequency=data.get("frequency", "none"),
            due_date=data.get("due_date", ""),
            pet_name=data.get("pet_name", ""),
            completed=data.get("completed", False),
        )


@dataclass
class Pet:
    """Domain object representing a pet holding a collected series of care requirements."""

    name: str
    species: str
    age: int
    care_tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Register a task under this pet's name scope."""
        task.pet_name = self.name
        self.care_tasks.append(task)

    def remove_task(self, task_title: str) -> None:
        """Filter out tasks matching a specific title query."""
        self.care_tasks = [t for t in self.care_tasks if t.title != task_title]

    def get_tasks(self) -> List[CareTask]:
        """Retrieve full collection of tasks assigned to this pet."""
        return self.care_tasks

    def update_info(self, name: str, species: str, age: int) -> None:
        """Modify basic pet identifier properties."""
        self.name = name
        self.species = species
        self.age = age

    def to_dict(self) -> Dict[str, Any]:
        """Serialize pet identity and inner task vectors to a layout dict."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "care_tasks": [t.to_dict() for t in self.care_tasks],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pet":
        """Reconstruct a Pet object with its active task arrays from serialized models."""
        pet = cls(name=data["name"], species=data["species"], age=data["age"])
        pet.care_tasks = [CareTask.from_dict(t) for t in data.get("care_tasks", [])]
        return pet


@dataclass
class Owner:
    """Top-level controller class storing pet profiles, schedules, and preferences."""

    name: str
    available_minutes: int
    preferences: str
    pets: List[Pet] = field(default_factory=list)
    schedules: List["DailySchedule"] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a new pet under this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet profile by name matching."""
        self.pets = [p for p in self.pets if p.name.lower() != pet_name.lower()]

    def update_preferences(self, preferences: str) -> None:
        """Update general household scheduling preferences."""
        self.preferences = preferences

    def get_pets(self) -> List[Pet]:
        """Return the list of pets owned."""
        return self.pets

    def get_all_tasks(self) -> List[CareTask]:
        """Aggregate every task across all registered pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def create_schedule(self, date_str: str) -> "DailySchedule":
        """Instantiate and track a new daily planning matrix."""
        schedule = DailySchedule(date=date_str, available_minutes=self.available_minutes)
        self.schedules.append(schedule)
        return schedule

    def save_to_json(self, file_path: str) -> None:
        """Save entire configuration profile state seamlessly to a text file."""
        state = {
            "name": self.name,
            "available_minutes": self.available_minutes,
            "preferences": self.preferences,
            "pets": [p.to_dict() for p in self.pets],
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4)

    def load_from_json(self, file_path: str) -> None:
        """Restore full ecosystem state safely from a stored file descriptor."""
        with open(file_path, "r", encoding="utf-8") as f:
            state = json.load(f)
        self.name = state["name"]
        self.available_minutes = state["available_minutes"]
        self.preferences = state["preferences"]
        self.pets = [Pet.from_dict(p) for p in state.get("pets", [])]


@dataclass
class DailySchedule:
    """Algorithmic planning engine responsible for optimization matrices and conflict reports."""

    date: str
    available_minutes: int
    scheduled_tasks: List[CareTask] = field(default_factory=list)
    skipped_tasks: List[CareTask] = field(default_factory=list)

    def _parse_time(self, time_str: str) -> int:
        """Convert a standard string time 'HH:MM' into absolute minutes from midnight."""
        try:
            hours, minutes = map(int, time_str.split(":"))
            return hours * 60 + minutes
        except ValueError:
            return 0

    def _format_time(self, total_minutes: int) -> str:
        """Convert total minutes from midnight back into a standard string representation."""
        hours = (total_minutes // 60) % 24
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"

    def sort_by_time(self, tasks: List[CareTask]) -> List[CareTask]:
        """Sort tasks chronologically by preferred_time using absolute minutes mapping."""
        return sorted(tasks, key=lambda t: self._parse_time(t.preferred_time))

    def filter_tasks(self, tasks: List[CareTask], pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List[CareTask]:
        """Filter list of tasks based on matching pet names and/or completion status flags."""
        res = tasks
        if pet_name is not None:
            res = [t for t in res if t.pet_name.lower() == pet_name.lower()]
        if completed is not None:
            res = [t for t in res if t.completed == completed]
        return res

    def detect_conflicts(self, tasks: List[CareTask]) -> List[str]:
        """Basic requirement check to alert users of exact matching preferred timeslots."""
        clashes: Dict[str, List[CareTask]] = {}
        warnings = []
        for t in tasks:
            if not t.completed:
                clashes.setdefault(t.preferred_time, []).append(t)
        for t_slot, t_list in clashes.items():
            if len(t_list) > 1:
                names = ", ".join([f"'{tk.title}' ({tk.pet_name})" for tk in t_list])
                warnings.append(f"Exact Time Clashing at {t_slot}: Multiple items scheduled ({names}).")
        return warnings

    def detect_overlapping_conflicts(self, tasks: List[CareTask]) -> List[str]:
        """Advanced Scheduling Logic: Verifies time blocks and flags overlapping duration intervals."""
        warnings = []
        active_tasks = [t for t in tasks if not t.completed]
        sorted_tasks = self.sort_by_time(active_tasks)

        for i in range(len(sorted_tasks)):
            t1 = sorted_tasks[i]
            start1 = self._parse_time(t1.preferred_time)
            end1 = start1 + t1.duration_minutes

            for j in range(i + 1, len(sorted_tasks)):
                t2 = sorted_tasks[j]
                start2 = self._parse_time(t2.preferred_time)

                if start2 < end1:  # Overlap found!
                    warnings.append(
                        f"⚠️ Interval Block Overlap: '{t1.title}' ({t1.preferred_time} to {self._format_time(end1)}) "
                        f"overlaps with '{t2.title}' scheduled at {t2.preferred_time}."
                    )
                else:
                    break
        return warnings

    def find_next_available_slot(self, tasks: List[CareTask], duration_minutes: int, start_time_str: str) -> str:
        """Advanced Algorithmic Capability: Finds the next free gap large enough for a task's duration."""
        current_start = self._parse_time(start_time_str)
        active_tasks = [t for t in tasks if not t.completed]
        sorted_tasks = self.sort_by_time(active_tasks)

        while current_start < 1440:
            current_end = current_start + duration_minutes
            overlap = False

            for t in sorted_tasks:
                t_start = self._parse_time(t.preferred_time)
                t_end = t_start + t.duration_minutes
                if max(current_start, t_start) < min(current_end, t_end):
                    current_start = t_end  # Fast-forward past the block
                    overlap = True
                    break

            if not overlap:
                return self._format_time(current_start)

        return "No slots available today"

    def generate_plan(self, tasks: List[CareTask]) -> None:
        """Pack tasks greedily into the time budget based on priority ranks and durations."""
        self.scheduled_tasks = []
        self.skipped_tasks = []
        remaining_budget = self.available_minutes

        ordered_queue = sorted(tasks, key=lambda t: (-t.priority.rank, t.duration_minutes))

        for task in ordered_queue:
            if task.completed:
                continue
            if task.duration_minutes <= remaining_budget:
                self.add_scheduled_task(task)
                remaining_budget -= task.duration_minutes
            else:
                self.skip_task(task)

        self.scheduled_tasks = self.sort_by_time(self.scheduled_tasks)

    def add_scheduled_task(self, task: CareTask) -> None:
        """Add task to the verified schedule list."""
        self.scheduled_tasks.append(task)

    def skip_task(self, task: CareTask) -> None:
        """Log a task under skipped items when it exceeds remaining budget capacity."""
        self.skipped_tasks.append(task)

    def explain_plan(self) -> str:
        """Return a structured, human-readable summary breakdown of the calculated plan matrix."""
        used_minutes = sum(t.duration_minutes for t in self.scheduled_tasks)
        lines = [
            f"📅 Today's Schedule ({self.date})",
            f"⏱️ Time Budget Allocation: {used_minutes}/{self.available_minutes} min utilized",
            "",
            "🚀 Scheduled Tasks (Chronological Order):"
        ]
        if self.scheduled_tasks:
            for t in self.scheduled_tasks:
                lines.append(
                    f"  🔹 [{t.preferred_time}] {t.title} for {t.pet_name} "
                    f"({t.duration_minutes} min, {t.priority.value} priority)"
                )
        else:
            lines.append("  (No tasks fit within the remaining allocation time envelope)")

        if self.skipped_tasks:
            lines.append("")
            lines.append("⚠️ Skipped Tasks (Insufficient Remaining Allocation Time):")
            for t in self.skipped_tasks:
                lines.append(
                    f"  ❌ {t.title} for {t.pet_name} "
                    f"({t.duration_minutes} min, {t.priority.value} priority)"
                )
        return "\n".join(lines)