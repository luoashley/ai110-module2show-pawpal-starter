import streamlit as st

# Step 1: bring the logic layer into the UI.
from pawpal_system import Owner, Pet, CareTask, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant. Add pets and tasks, then generate a daily plan.")

# Step 2: persist the Owner in session_state so it survives reruns.
# Streamlit reruns the whole script on every interaction, so we only create
# the Owner once and keep reusing the stored instance after that.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=90, preferences="")

owner: Owner = st.session_state.owner

# --- Owner settings -------------------------------------------------------
st.subheader("Owner")
col_a, col_b = st.columns(2)
with col_a:
    owner.name = st.text_input("Owner name", value=owner.name)
with col_b:
    owner.available_minutes = st.number_input(
        "Available minutes today", min_value=1, max_value=1440,
        value=owner.available_minutes,
    )
owner.update_preferences(st.text_input("Preferences", value=owner.preferences))

st.divider()

# --- Add a pet ------------------------------------------------------------
st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=100, value=3)
    if st.form_submit_button("Add pet"):
        # Step 3: the UI hands the form data to Owner.add_pet().
        owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Added {pet_name}!")

pets = owner.get_pets()
if not pets:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task to a pet --------------------------------------------------
st.subheader("Add a Task")
if pets:
    with st.form("add_task_form", clear_on_submit=True):
        target_pet_name = st.selectbox("Pet", [p.name for p in pets])
        task_title = st.text_input("Task title", value="Morning walk")
        c1, c2, c3 = st.columns(3)
        with c1:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with c2:
            priority = st.selectbox("Priority", [p.value for p in Priority], index=2)
        with c3:
            preferred_time = st.text_input("Preferred time", value="08:00")
        category = st.text_input("Category", value="exercise")
        if st.form_submit_button("Add task"):
            # Find the selected Pet object and delegate to Pet.add_task().
            pet = next(p for p in pets if p.name == target_pet_name)
            pet.add_task(
                CareTask(
                    title=task_title,
                    duration_minutes=int(duration),
                    priority=Priority(priority),
                    category=category,
                    preferred_time=preferred_time,
                )
            )
            st.success(f"Added '{task_title}' to {target_pet_name}!")
else:
    st.caption("Add a pet before adding tasks.")

# --- Current pets & tasks -------------------------------------------------
if pets:
    st.subheader("Current Pets & Tasks")
    for pet in pets:
        with st.expander(f"{pet.name} ({pet.species}, age {pet.age})", expanded=True):
            tasks = pet.get_tasks()
            if tasks:
                st.table(
                    [
                        {
                            "Task": t.title,
                            "Time": t.preferred_time,
                            "Duration (min)": t.duration_minutes,
                            "Priority": t.priority.value,
                            "Done": t.completed,
                        }
                        for t in tasks
                    ]
                )
            else:
                st.caption("No tasks yet.")

st.divider()

# --- Generate the daily schedule -----------------------------------------
st.subheader("Build Schedule")
if st.button("Generate schedule", disabled=not owner.get_all_tasks()):
    schedule = owner.create_schedule(date="today")
    schedule.generate_plan(owner.get_all_tasks())
    st.text(schedule.explain_plan())
elif not owner.get_all_tasks():
    st.caption("Add at least one task to generate a schedule.")
