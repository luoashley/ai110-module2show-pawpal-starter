"""CLI Demonstration Script for PawPal+.

Builds a structured pet care environment, runs validation modules, and logs
outputs to showcase advanced multi-pet calculations, intervals, and sorting.
"""

from pawpal_system import Owner, Pet, CareTask, Priority


def main() -> None:
    print("======================================================================")
    print("🐾 PawPal+ Advanced Algorithmic Scheduling System Demo Engine 🐾")
    print("======================================================================\n")

    # Initialize owner profile
    jordan = Owner(name="Jordan", available_minutes=90, preferences="Mornings preferred")

    # Create distinct pet accounts (Multi-Pet support requirement)
    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)
    jordan.add_pet(mochi)
    jordan.add_pet(luna)

    # Add tasks out of chronological sequence to evaluate sorting
    mochi.add_task(CareTask("Evening run", 30, Priority.MEDIUM, "exercise", "18:00"))
    mochi.add_task(CareTask("Insulin Check", 15, Priority.HIGH, "health", "08:00"))
    luna.add_task(CareTask("Morning Feast", 15, Priority.HIGH, "feeding", "07:30"))
    luna.add_task(CareTask("Fur Grooming", 25, Priority.LOW, "grooming", "12:00"))

    # Intentional Overlapping Time Block Conflicts (Advanced Scheduling Logic)
    # Task A starts at 09:00 and runs for 20 minutes (ends 09:20)
    # Task B starts at 09:10, causing an overlapping collision
    mochi.add_task(CareTask("Ear Treatment Drop", 20, Priority.HIGH, "health", "09:00"))
    luna.add_task(CareTask("Glucose Screening", 15, Priority.HIGH, "health", "09:10"))

    # Instantiate daily planner schedule
    schedule = jordan.create_schedule(date_str="2026-07-05")
    all_tasks = jordan.get_all_tasks()

    print("--- 1. Verification of Chronological Sorting Engine ---")
    sorted_tasks = schedule.sort_by_time(all_tasks)
    for t in sorted_tasks:
        print(f"   [{t.preferred_time}] {t.title} ({t.pet_name})")

    print("\n--- 2. Verification of Granular Target Filtering (Luna Only) ---")
    luna_only = schedule.filter_tasks(all_tasks, pet_name="Luna")
    for t in luna_only:
        print(f"   • Found task: '{t.title}' assigned to {t.pet_name}")

    print("\n--- 3. Advanced Interval-Blocking Conflict Telemetry Report ---")
    overlaps = schedule.detect_overlapping_conflicts(all_tasks)
    for warning in overlaps:
        print(f"   {warning}")

    print("\n--- 4. Advanced Feature: Next Available Free Slot Query Locator ---")
    # Query for an open 30-minute block starting from 09:00
    free_slot = schedule.find_next_available_slot(all_tasks, duration_minutes=30, start_time_str="09:00")
    print(f"   💡 Next 30-minute block suggestion: Starts at {free_slot}")

    print("\n--- 5. Generated Core Decision Matrix Plan ---")
    schedule.generate_plan(all_tasks)
    print(schedule.explain_plan())

    print("\n--- 6. Storage Architecture State Persistence Sync Loop (JSON) ---")
    storage_file = "pawpal_data_backup.json"
    jordan.save_to_json(storage_file)
    print(f"   💾 State serialized and synced to '{storage_file}' successfully.")

    # Instantiate empty instance to verify data recovery pipeline
    recovered_owner = Owner(name="Temp", available_minutes=10, preferences="")
    recovered_owner.load_from_json(storage_file)
    print(f"   📂 Recovery successful! Restored Profile Name: '{recovered_owner.name}' with "
          f"{len(recovered_owner.get_all_tasks())} active structural task elements.")
    print("\n======================================================================")


if __name__ == "__main__":
    main()