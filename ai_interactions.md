# AI Interactions Log (Stretch Feature Matrix Logs)

---

## Agent Workflow Documentation (SF7)

**What task did you give the agent?**
"Refactor the core `pawpal_system.py` file to support advanced time-blocking overlapping duration conflict checks, add a 'next available slot' recommender algorithm, and add dictionary parsing models to enable robust JSON persistence."

**What did the agent do?**
1. Appended `_parse_time` and `_format_time` helpers to convert standard string times (`HH:MM`) into integer counter tracks from midnight.
2. Built the custom `detect_overlapping_conflicts` method to catch intersecting activity windows based on task duration.
3. Implemented the iterative `find_next_available_slot` loop to locate open gaps for conflicting tasks.
4. Added `to_dict` and `from_dict` serialization routines to all core dataclasses.

**What did you have to verify or fix manually?**
I manually adjusted the interval checking logic to ensure that if a secondary task starts exactly when a prior task finishes (e.g., Task A runs 08:00–08:30 and Task B starts at 08:30), it is correctly treated as a clean handoff rather than an overlapping conflict.

---

## Prompt Comparison Matrix (SF11)

| Feature Axis | Option A: Claude 3.5 Sonnet | Option B: Gemini 1.5 Pro |
| :--- | :--- | :--- |
| **Model / Tool Used** | Claude 3.5 Sonnet via Workspace API | Gemini 1.5 Pro via Browser Console |
| **Prompt Provided** | *"Show me a robust approach to calculate the next occurrence of a task using Python's timedelta if frequency is daily or weekly."* | *"Write python code to advance a due date string by one day or one week based on frequency."* |
| **Response Summary** | Generated an elegant, safe method that handles edge cases cleanly using native `date.fromisoformat()` and `timedelta`. | Provided a functional snippet that relied heavily on external `dateutil.relativedelta` dependencies. |
| **What was useful** | Leveraged clean, native standard libraries that integrated perfectly with our existing dataclasses without requiring additional dependencies. | Correctly calculated the calendar offsets. |
| **Problems Noticed** | Left the initial `due_date` field empty by default, which required manual initialization to `date.today()`. | Required adding extra external dependencies to our project's `requirements.txt`. |
| **Decision** | **Selected Option A Architecture**: Built Sonnet's implementation directly into `CareTask.next_occurrence()`. This approach keeps our system lightweight and reliable by avoiding unnecessary third-party package dependencies. | Rejected due to unnecessary external library dependencies. |

**Which approach did you use in your final implementation and why?**
I chose the native standard-library approach provided by Option A. This keeps the execution space clean, avoids external library bloat, and runs lightning-fast within both our CLI scripts and Streamlit app modules.