# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample End-to-End CLI Script Output

```text
======================================================================
🐾 PawPal+ Advanced Algorithmic Scheduling System Demo Engine 🐾
======================================================================

--- 1. Verification of Chronological Sorting Engine ---
   Morning Feast (Luna)
   Insulin Check (Mochi)
   Ear Treatment Drop (Mochi)
   Glucose Screening (Luna)
   Fur Grooming (Luna)
   Evening run (Mochi)

--- 2. Verification of Granular Target Filtering (Luna Only) ---
   • Found task: 'Morning Feast' assigned to Luna
   • Found task: 'Fur Grooming' assigned to Luna
   • Found task: 'Glucose Screening' assigned to Luna

--- 3. Advanced Interval-Blocking Conflict Telemetry Report ---
   ⚠️ Interval Block Overlap: 'Ear Treatment Drop' (09:00 to 09:20) overlaps with 'Glucose Screening' scheduled at 09:10.

--- 4. Advanced Feature: Next Available Free Slot Query Locator ---
   💡 Next 30-minute block suggestion: Starts at 09:20

--- 5. Generated Core Decision Matrix Plan ---
📅 Today's Schedule (2026-07-05)
⏱️ Time Budget Allocation: 65/90 min utilized

🚀 Scheduled Tasks (Chronological Order):
  🔹 Morning Feast for Luna (15 min, high priority)
  🔹 Insulin Check for Mochi (15 min, high priority)
  🔹 Ear Treatment Drop for Mochi (20 min, high priority)
  🔹 Glucose Screening for Luna (15 min, high priority)

⚠️ Skipped Tasks (Insufficient Remaining Allocation Time):
  ❌ Evening run for Mochi (30 min, medium priority)
  ❌ Fur Grooming for Luna (25 min, low priority)

--- 6. Storage Architecture State Persistence Sync Loop (JSON) ---
   💾 State serialized and synced to 'pawpal_data_backup.json' successfully.
   📂 Recovery successful! Restored Profile Name: 'Jordan' with 6 active structural task elements.


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================================================================= test session starts ==============================================================================
platform darwin -- Python 3.13.12, pytest-9.0.3, pluggy-1.5.0 -- /Users/AshleyLuo1/miniconda3/bin/python
cachedir: .pytest_cache
rootdir: /Users/AshleyLuo1/PycharmProjects/ai110-module2show-pawpal-starter
plugins: anyio-4.10.0
collected 8 items                                                                                                                                                              

tests/test_pawpal.py::test_mark_complete_changes_status PASSED                                                                                                           [ 12%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED                                                                                                   [ 25%]
tests/test_pawpal.py::test_sorting_correctness PASSED                                                                                                                    [ 37%]
tests/test_pawpal.py::test_filtering_logic PASSED                                                                                                                        [ 50%]
tests/test_pawpal.py::test_recurrence_logic PASSED                                                                                                                       [ 62%]
tests/test_pawpal.py::test_advanced_overlapping_conflict_detection PASSED                                                                                                [ 75%]
tests/test_pawpal.py::test_find_next_available_slot PASSED                                                                                                               [ 87%]
tests/test_pawpal.py::test_json_persistence_layer PASSED                                                                                                                 [100%]

============================================================================== 8 passed in 0.02s =============================================================================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `DailySchedule.sort_by_time()` | Automatically parses `HH:MM` timestamps to guarantee chronological order. |
| Filtering | `DailySchedule.filter_tasks()` | Allows granular retrieval of scheduling arrays by completion criteria or specific pet names. |
| Conflict handling | `DailySchedule.detect_conflicts()` | Looks for identical preferred times and alerts users without crashing the application flow. |
| Recurring tasks | `CareTask.next_occurrence()` | Automatically instantiates a fresh task instance shifted by `timedelta` (1 day or 1 week) when completed. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
