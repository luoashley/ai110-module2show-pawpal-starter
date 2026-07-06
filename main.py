"""CLI demo for PawPal+.

Temporary testing ground: builds an owner with a couple of pets and some
tasks, then prints today's schedule to the terminal to verify the logic layer.
"""

from pawpal_system import Owner, Pet, CareTask, Priority


def main() -> None:
    # Owner has 90 minutes of care time available today.
    jordan = Owner(name="Jordan", available_minutes=90, preferences="mornings free")

    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)
    jordan.add_pet(mochi)
    jordan.add_pet(luna)

    # Add tasks with different preferred times, durations, and priorities.
    mochi.add_task(CareTask("Morning walk", 30, Priority.HIGH, "exercise", "08:00"))
    mochi.add_task(CareTask("Evening walk", 30, Priority.MEDIUM, "exercise", "18:00"))
    luna.add_task(CareTask("Feed", 10, Priority.HIGH, "feeding", "07:30"))
    luna.add_task(CareTask("Brush coat", 20, Priority.LOW, "grooming", "12:00"))
    mochi.add_task(CareTask("Give medication", 5, Priority.HIGH, "health", "09:00"))

    # Scheduler flow: pull every task across the owner's pets, then plan the day.
    schedule = jordan.create_schedule(date="2026-07-05")
    schedule.generate_plan(jordan.get_all_tasks())

    print(schedule.explain_plan())


if __name__ == "__main__":
    main()
