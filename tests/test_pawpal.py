"""Automated Verification Suite for PawPal+.

Tests core classes, scheduling behaviors, and advanced features like JSON
persistence, interval overlap checks, and next available free slot search loops.
"""

import os
from pawpal_system import CareTask, Pet, DailySchedule, Owner, Priority


def test_mark_complete_changes_status():
    """Calling mark_complete() flips a task from incomplete to complete."""
    task = CareTask("Morning walk", 30, Priority.HIGH, "exercise", "08:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    """Adding a task to a pet increases that pet's task count by one."""
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(CareTask("Feed", 10, Priority.HIGH, "feeding", "07:30"))
    assert len(pet.get_tasks()) == 1


def test_sorting_correctness():
    """Verify that sort_by_time correctly orders tasks chronologically."""
    sched = DailySchedule(date="2026-07-05", available_minutes=60)
    t1 = CareTask("Night Snack", 5, Priority.LOW, "feed", "22:15")
    t2 = CareTask("Sunrise Meal", 10, Priority.HIGH, "feed", "05:45")
    t3 = CareTask("Noon Run", 20, Priority.MEDIUM, "play", "12:00")

    sorted_res = sched.sort_by_time([t1, t2, t3])
    assert sorted_res[0].preferred_time == "05:45"
    assert sorted_res[1].preferred_time == "12:00"
    assert sorted_res[2].preferred_time == "22:15"


def test_filtering_logic():
    """Verify tasks are filtered correctly by pet name and completion status."""
    sched = DailySchedule(date="2026-07-05", available_minutes=120)
    t1 = CareTask("Run", 20, Priority.HIGH, "ex", "08:00", pet_name="Mochi", completed=True)
    t2 = CareTask("Brush", 15, Priority.LOW, "groom", "09:00", pet_name="Luna", completed=False)

    tasks = [t1, t2]
    assert len(sched.filter_tasks(tasks, pet_name="Mochi")) == 1
    assert len(sched.filter_tasks(tasks, completed=False)) == 1
    assert sched.filter_tasks(tasks, completed=False)[0].pet_name == "Luna"


def test_recurrence_logic():
    """Confirm daily recurring tasks create a new task advanced by +1 day."""
    task = CareTask("Daily Vitamins", 5, Priority.HIGH, "medical", "08:00", frequency="daily", due_date="2026-07-05")
    task.mark_complete()

    nxt = task.next_occurrence()
    assert nxt is not None
    assert nxt.due_date == "2026-07-06"
    assert nxt.completed is False
    assert nxt.title == "Daily Vitamins"


def test_advanced_overlapping_conflict_detection():
    """Verify time-blocking detection correctly identifies overlapping tasks."""
    sched = DailySchedule(date="2026-07-05", available_minutes=100)
    t1 = CareTask("Mochis Hydration Care", 45, Priority.HIGH, "health", "10:00", pet_name="Mochi")
    t2 = CareTask("Luna Ear Wipe", 15, Priority.MEDIUM, "health", "10:30", pet_name="Luna")

    clashes = sched.detect_overlapping_conflicts([t1, t2])
    assert len(clashes) == 1
    assert "Interval Block Overlap" in clashes[0]


def test_find_next_available_slot():
    """Verify the algorithm accurately finds the next free time window."""
    sched = DailySchedule(date="2026-07-05", available_minutes=120)
    t1 = CareTask("Task A", 30, Priority.HIGH, "misc", "10:00", pet_name="Mochi")

    next_slot = sched.find_next_available_slot([t1], duration_minutes=20, start_time_str="10:00")
    assert next_slot == "10:30"


def test_json_persistence_layer():
    """Test saving and loading data to ensure system state persists accurately."""
    file_name = "test_persistence_temp.json"
    owner = Owner(name="Terry", available_minutes=200, preferences="Quiet hours")
    pet = Pet(name="Bella", species="bird", age=2)
    pet.add_task(CareTask("Cage Sweep", 15, Priority.MEDIUM, "hygiene", "11:00"))
    owner.add_pet(pet)

    try:
        owner.save_to_json(file_name)

        rebuilt = Owner(name="Empty", available_minutes=10, preferences="")
        rebuilt.load_from_json(file_name)

        assert rebuilt.name == "Terry"
        assert rebuilt.available_minutes == 200
        assert len(rebuilt.pets) == 1
        assert rebuilt.pets[0].name == "Bella"
        assert rebuilt.get_all_tasks()[0].title == "Cage Sweep"
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)