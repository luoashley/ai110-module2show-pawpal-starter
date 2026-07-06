# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

PawPal+ is designed to help a busy pet owner organize daily care for their pet. The system should support three core user actions:

- Add and manage pet information, such as the pet’s name, species, and basic care needs.
- Add or edit pet care tasks, including details like task name, duration, priority, and preferred time.
- Generate and view today’s care plan so the owner can see which tasks should happen, when they should happen, and why they were scheduled.

My initial UML design includes four main classes: Owner, Pet, CareTask, and DailySchedule. The Owner class stores basic owner information and preferences. The Pet class stores information about each pet and its related care tasks. The CareTask class represents an individual task such as feeding, walking, medication, grooming, or enrichment. The DailySchedule class organizes tasks into a daily plan based on time limits, task duration, and priority.

**b. Design changes**

Yes. After generating the class skeleton, I asked my AI assistant to review `pawpal_system.py` for missing relationships and logic bottlenecks. Based on that feedback I made three changes:

1. **Added a `Priority` Enum** (LOW/MEDIUM/HIGH) and used it for `CareTask.priority` instead of a plain string. Originally priority was a free-form string, which meant values like `"HIGH"`, `"high"`, or typos could slip in and break `is_high_priority()` and the sorting inside `generate_plan()`. The Enum makes the scheduling logic reliable while still printing and comparing as a string.

2. **Added a `pet_name` field to `CareTask`.** In my initial design `DailySchedule.generate_plan()` received a flat list of tasks with no link back to the pet they belonged to. That would have made `explain_plan()` unable to say *which* pet a scheduled or skipped task was for. Adding `pet_name` restores that association without forcing the scheduler to carry full `Pet` objects.

3. **Added `Owner.schedules` and an `Owner.create_schedule(date)` method.** My UML said the owner "creates" many daily schedules, but the skeleton had no code representing that relationship — a `DailySchedule` was a free-floating object. `create_schedule()` now seeds a schedule with the owner's `available_minutes` and records it in the owner's history, so `available_minutes` has a single authoritative source and past plans stay accurate even if the owner's availability changes later.

I did not adopt every suggestion. The assistant also flagged that `remove_task`/`remove_pet` assume unique titles/names and that `preferred_time` as a string is hard to sort. I chose to leave these for now: enforcing unique names is a validation concern I can handle during implementation, and a string `preferred_time` is good enough for a first pass. I'll revisit them if the scheduling logic actually needs time comparisons.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**
- **Constraints Considered**: Total remaining available minutes constraint, absolute task priority tier rank, short-job-first task duration sorting, and preferred operational execution times.
- **Decision Engine Criterion**: Priorities dictate core safety metrics (e.g., medical interventions or feeding tasks must trump a casual grooming cycle). Thus, priority rank acts as the foundational ordering parameter, and short task lengths split ties to maximize total operations accomplished.

**b. Tradeoffs**
- **Tradeoff Implemented**: Time conflicts flag basic exact matches rather than checking for overlapping blocks using real math interval structures (such as checking if an execution window runs into another task).
- **Reasoning**: It keeps the system lightweight and responsive while providing an clear reminder to the user to balance their calendar view manually.

## 3. AI Collaboration

**a. How you used AI**
- **Usage Strategy**: AI was leveraged to generate code templates for handling complex edge cases inside Python lists, draft the Mermaid syntax layout, and build the Pytest assertions.
- **Highly Effective Prompts**: *"Show me how to sort strings formatted like HH:MM using a concise Python lambda function key without requiring datetime parsing overhead."*

**b. Judgment and verification**
- **Modified Suggestion**: The AI suggested using complex external libraries like `marshmallow` or `pydantic` to write the JSON data structures, but I decided that clean native dataclass methods kept the dependencies simpler and the application easier to debug.

## 4. Testing and Verification

**a. What you tested**
- **Behaviors Covered**: Chronological sort order formatting, dynamic pet name filtration criteria, next occurrence task generator offsets via timedelta calculations, and conflict telemetry warnings.
- **Importance**: Verifying edge boundaries prevents critical pet care requirements from slipping out of visibility during resource optimization routines.

**b. Confidence**
- **Confidence Rating**: 5/5
- **Next Horizon Testing Areas**: Testing cross-over boundary dates (e.g., month-end and leap-year transitions) for recurring task updates.

## 5. Reflection

**a. What went well**
- Combining the automated scheduling logic seamlessly with Streamlit's reactive `session_state` was clean and highly satisfying.

**b. What you would improve**
- Implement full interval parsing logic so that tasks check for true block overlaps (e.g., a 60-minute walk at 08:30 conflict-flags a grooming task starting at 09:00).

**c. Key takeaway**
- I learned that acts as the lead architect means clearly mapping out data flow, interface requirements, and system relationships *before* writing code, ensuring the AI assistant acts as an efficient coding partner rather than a replacement for engineering design.