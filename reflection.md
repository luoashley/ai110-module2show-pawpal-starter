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

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
