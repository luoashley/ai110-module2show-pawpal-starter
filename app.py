import streamlit as st
import os
from pawpal_system import Owner, Pet, CareTask, Priority, DailySchedule

st.set_page_config(page_title="PawPal+ Professional Planner", page_icon="🐾", layout="centered")

# Custom Title Block with Professional Formatting and Emojis
st.title("🐾 PawPal+ Advanced Scheduling Dashboard")
st.caption(
    "Module 2 Capstone: Intelligent Care Plan Engine featuring Multi-Pet Processing, Interval Time-Blocking, and Persistent State Synchronization.")

# Maintain single owner session data state wrapper across reactive form submissions
STORAGE_PATH = "pawpal_user_profile.json"

if "owner" not in st.session_state:
    inst = Owner(name="Jordan", available_minutes=120, preferences="Mornings free")
    if os.path.exists(STORAGE_PATH):
        try:
            inst.load_from_json(STORAGE_PATH)
        except Exception:
            pass
    st.session_state.owner = inst

owner: Owner = st.session_state.owner

# --- Persistent Configuration Panel Hub ---
with st.sidebar:
    st.header("💾 Storage Synchronization")
    if st.button("🔄 Force Save System Profile"):
        owner.save_to_json(STORAGE_PATH)
        st.success("Configuration synced locally!")

    if st.button("📂 Reload Last Backup"):
        if os.path.exists(STORAGE_PATH):
            owner.load_from_json(STORAGE_PATH)
            st.success("Profile restored!")
            st.rerun()
        else:
            st.error("No profile backup found.")

    st.divider()
    st.subheader("⚙️ Owner Parameters")
    owner.name = st.text_input("User identity name", value=owner.name)
    owner.available_minutes = st.number_input("Daily care budget (min)", min_value=1, max_value=1440,
                                              value=owner.available_minutes)
    owner.preferences = st.text_input("Care notes / constraints", value=owner.preferences)

# --- Pet Creation Form Widget ---
st.subheader("🐾 Register Companion Profiles")
with st.form("pet_submission_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        p_name = st.text_input("Pet identifier name", value="Mochi")
    with col2:
        p_species = st.selectbox("Biological Group", ["dog", "cat", "bird", "reptile", "other"])
    with col3:
        p_age = st.number_input("Age (Years)", min_value=0, max_value=40, value=3)

    if st.form_submit_button("➕ Complete Registration Profile"):
        owner.add_pet(Pet(name=p_name, species=p_species, age=int(p_age)))
        owner.save_to_json(STORAGE_PATH)
        st.success(f"Successfully configured and stored operational profile for {p_name}!")
        st.rerun()

# --- Display Registered Pets with Metric Badges ---
pets = owner.get_pets()
if pets:
    cols = st.columns(min(len(pets), 4))
    for idx, p in enumerate(pets):
        with cols[idx % len(cols)]:
            st.metric(label=f"{p.name} ({p.species})", value=f"Age: {p.age}", delta=f"{len(p.care_tasks)} Active tasks")
else:
    st.info("No companion animals registered in current configuration.")

st.divider()

# --- Task Insertion Form Widget ---
st.subheader("📋 Core Schedule Action Items")
if pets:
    with st.form("task_registration_matrix", clear_on_submit=True):
        target_name = st.selectbox("Select Target Companion", [p.name for p in pets])
        title_val = st.text_input("Activity title description", value="Routine Health Checkup")

        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            dur_val = st.number_input("Duration length (mins)", min_value=1, max_value=300, value=20)
        with tc2:
            prio_val = st.selectbox("Priority Ranking Classification", [p.value for p in Priority], index=1)
        with tc3:
            time_val = st.text_input("Preferred Time point (HH:MM)", value="09:00")

        freq_val = st.selectbox("Automated Recurrence Rule", ["none", "daily", "weekly"])
        cat_val = st.text_input("Functional structural category", value="health")

        if st.form_submit_button("⚡ Append Activity Plan Item"):
            target_pet = next(p for p in pets if p.name == target_name)
            target_pet.add_task(
                CareTask(
                    title=title_val,
                    duration_minutes=int(dur_val),
                    priority=Priority(prio_val),
                    category=cat_val,
                    preferred_time=time_val,
                    frequency=freq_val,
                    due_date="2026-07-05"
                )
            )
            owner.save_to_json(STORAGE_PATH)
            st.success(f"Appended task '{title_val}' for {target_name}.")
            st.rerun()
else:
    st.caption("Please configure a valid pet profile before managing active tasks.")

# --- Real-Time Validation Sandbox and Free Slot Recommender ---
all_tasks = owner.get_all_tasks()
if all_tasks:
    st.divider()
    st.subheader("🛠️ Validation Engine Sandbox")
    engine = DailySchedule(date="today", available_minutes=owner.available_minutes)

    overlaps = engine.detect_overlapping_conflicts(all_tasks)
    if overlaps:
        st.error("🚨 Overlapping Time-Block Conflicts Detected!")
        for clash in overlaps:
            st.markdown(clash)

        # Contextual recommendation workflow
        st.info("💡 Algorithmic Optimization Recommendation:")
        for t in all_tasks:
            if not t.completed and any(t.title in c for c in overlaps):
                rec_slot = engine.find_next_available_slot(all_tasks, t.duration_minutes, t.preferred_time)
                st.write(
                    f"• Move task *'{t.title}'* ({t.duration_minutes} min) to next free slot starting at **{rec_slot}**.")
    else:
        st.success("✅ Time-blocking verification clean: No interval intersection collisions found.")

# --- Interactive Task Matrix View with Filters ---
if pets and all_tasks:
    st.divider()
    st.subheader("🔍 Active Task Profiles Engine")

    f_col1, f_col2 = st.columns(2)
    with f_col1:
        pet_filter = st.selectbox("View Profile Filter Target", ["All Registered Animals"] + [p.name for p in pets])
    with f_col2:
        status_filter = st.selectbox("Lifecycle Status Filter Target",
                                     ["All Tasks", "Incomplete Only", "Completed Only"])

    for p in pets:
        if pet_filter != "All Registered Animals" and p.name != pet_filter:
            continue

        st.markdown(f"#### 🐾 Activity Schedule Checklist for: **{p.name}**")
        tasks_to_render = p.get_tasks()

        if status_filter == "Incomplete Only":
            tasks_to_render = [t for t in tasks_to_render if not t.completed]
        elif status_filter == "Completed Only":
            tasks_to_render = [t for t in tasks_to_render if t.completed]

        if not tasks_to_render:
            st.caption("No matching records found for this pet view segment.")
            continue

        # Present tasks ordered chronologically for structural user readability
        ordered_render = engine.sort_by_time(tasks_to_render)

        for idx, t in enumerate(ordered_render):
            cc1, cc2 = st.columns([4, 1])
            with cc1:
                chk_sym = "✅ Done" if t.completed else "⏳ Pending"
                p_badge = "🔴" if t.priority == Priority.HIGH else ("🟡" if t.priority == Priority.MEDIUM else "🟢")
                freq_lbl = f" 🔄 [{t.frequency.upper()}]" if t.frequency != "none" else ""
                st.markdown(
                    f"{p_badge} **{t.preferred_time}** — {t.title} `{t.duration_minutes} min` | `{t.category}` | {chk_sym}{freq_lbl}")
            with cc2:
                if not t.completed:
                    if st.button("Complete", key=f"action_btn_{p.name}_{t.title}_{idx}"):
                        t.mark_complete()
                        if t.frequency in ("daily", "weekly"):
                            new_task = t.next_occurrence()
                            if new_task:
                                p.add_task(new_task)
                                st.toast(f"Generated recurring copy for: {new_task.due_date}!", icon="📅")
                        owner.save_to_json(STORAGE_PATH)
                        st.success("Updated!")
                        st.rerun()

# --- Optimization Plan Engine Summary ---
st.divider()
st.subheader("🚀 Operational Resource Optimization Plan")
if st.button("⚙️ Compute Optimal Resource Schedule Allocation", disabled=not all_tasks):
    plan_instance = owner.create_schedule(date_str="2026-07-05")
    plan_instance.generate_plan(all_tasks)
    st.text_area("Scheduler Explanation Output Trace", value=plan_instance.explain_plan(), height=300)