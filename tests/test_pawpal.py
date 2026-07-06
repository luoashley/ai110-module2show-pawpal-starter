"""Quick tests for the PawPal+ logic layer."""

from pawpal_system import CareTask, Pet, Priority


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
