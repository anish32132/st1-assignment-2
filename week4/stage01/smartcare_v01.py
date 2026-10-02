# SmartCare v0.1 - Stage 1 Lab (Week 4)
# Unit: Introduction to Software Technology
#
# Student name:    Anish Atmakur
# Student ID:      U3319971
# Tutorial group:  4483


# PART B - TASK 1

print("=" * 64)
print("PART B - TASK 1")
print("=" * 64)

# Basic output
print("Welcome to SmartCare: Community Clinic Appointment Booking System!")

# First Appointment
patient1_name = 'Alice Smith'
practitioner1_name = 'Dr. John Doe'
appointment1_time = '2024-07-20 10:00 AM'
print(f"Patient: {patient1_name} | Practitioner: {practitioner1_name} | Time: {appointment1_time}")

# Second Appointment
patient2_name = 'Bob Johnson'
practitioner2_name = 'Dr. Jane Roe'
appointment2_time = '2024-07-20 11:30 AM'
print(f"Patient: {patient2_name} | Practitioner: {practitioner2_name} | Time: {appointment2_time}")


# PART B - TASK 1 ENHANCED

print()
print("=" * 64)
print("PART B - TASK 1 ENHANCED (the 'before' version)")
print("=" * 64)

appointments = []


def book_appointment(patient_name, practitioner_name, appointment_time):
    if not patient_name:
        raise ValueError("Patient name cannot be empty")
    appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time
    }
    appointments.append(appointment)


def display_appointments():
    if not appointments:
        print("No appointments recorded.")
        return
    for appointment in appointments:
        print(f"Patient: {appointment['patient']} | Practitioner: {appointment['practitioner']} | Time: {appointment['time']}")


print("Welcome to SmartCare: The Clinical Appointment Booking System!")
book_appointment('Alice Smith', 'Dr. John Doe', '2024-07-20 10:00 AM')
book_appointment('Bob Johnson', 'Dr. Jane Roe', '2024-07-20 11:30 AM')
display_appointments()


# =====================================================================
# PART D - GENERATE AN ALTERNATIVE
#
# AI-generated alternative. This section is left unmodified for the Part E comparison.
#
# AI tool used: Microsoft Copilot
# Date generated:  September 2nd 2026
# =====================================================================

print()
print("=" * 64)
print("PART D - AI-GENERATED ALTERNATIVE (unmodified)")
print("=" * 64)


def add_appointment(appointment_list, patient_name, practitioner_name, appointment_time):
    """Add one appointment to a list of appointments."""
    appointment = {
        "patient_name": patient_name,
        "practitioner_name": practitioner_name,
        "appointment_time": appointment_time,
        "status": "Booked"
    }
    appointment_list.append(appointment)
    print("Appointment added for " + patient_name)
    return appointment_list


def show_appointments(appointment_list):
    """Print every appointment in the list."""
    print("\nAll appointments:")
    for number, appointment in enumerate(appointment_list, start=1):
        print(str(number) + ". " + appointment["patient_name"] +
              " with " + appointment["practitioner_name"] +
              " at " + appointment["appointment_time"] +
              " (" + appointment["status"] + ")")


ai_appointments = []
add_appointment(ai_appointments, "Alice Smith", "Dr. John Doe", "2024-07-20 10:00 AM")
add_appointment(ai_appointments, "Bob Johnson", "Dr. Jane Roe", "2024-07-20 11:30 AM")
show_appointments(ai_appointments)


# PART F - VERIFY BEHAVIOUR
# The checks below test the BEFORE version.

print()
print("=" * 64)
print("PART F - VERIFY BEHAVIOUR (before the Part G improvement)")
print("=" * 64)

# --- 1. Normal appointment ---
print()
print("Check 1 - Normal appointment")
print("  Input:    ('Chris Lee', 'Dr. John Doe', '2024-07-21 09:00 AM')")
print("  Expected: stored, no error raised.")
try:
    book_appointment("Chris Lee", "Dr. John Doe", "2024-07-21 09:00 AM")
    print("  Actual:   stored. Total appointments =", len(appointments))
    print("  Outcome:  PASS")
except ValueError as error:
    print("  Actual:   ValueError ->", error)
    print("  Outcome:  FAIL")

# --- 2. Blank patient name ---
print()
print("Check 2 - Blank patient name")
print("  Input:    ('', 'Dr. Jane Roe', '2024-07-21 09:30 AM')")
print("  Expected: rejected with a ValueError.")
try:
    book_appointment("", "Dr. Jane Roe", "2024-07-21 09:30 AM")
    print("  Actual:   stored, no error raised.")
    print("  Outcome:  FAIL")
except ValueError as error:
    print("  Actual:   ValueError ->", error)
    print("  Outcome:  PASS")

# --- 3. Two appointments for the same practitioner/time ---
print()
print("Check 3 - Two appointments for the same practitioner/time")
print("  Input:    two bookings for Dr. Jane Roe at '2024-07-21 10:00 AM'")
print("  Expected: the clinic needs this refused or at least reported.")
book_appointment("Dana Patel", "Dr. Jane Roe", "2024-07-21 10:00 AM")
book_appointment("Evan Brown", "Dr. Jane Roe", "2024-07-21 10:00 AM")
clash_count = 0
for appointment in appointments:
    if appointment["practitioner"] == "Dr. Jane Roe" and appointment["time"] == "2024-07-21 10:00 AM":
        clash_count += 1
print("  Actual:   both stored. Bookings for that practitioner/time =", clash_count)
print("  Outcome:  FAIL")
print("  The two appointments were both stored.")

# --- 4. Strange input ---
print()
print("Check 4a - Strange input: patient_name=None")
print("  Expected: rejected with a ValueError.")
try:
    book_appointment(None, "Dr. John Doe", "2024-07-21 11:00 AM")
    print("  Actual:   stored, no error raised.")
    print("  Outcome:  FAIL")
except ValueError as error:
    print("  Actual:   ValueError ->", error)
    print("  Outcome:  PASS")

print()
print("Check 4b - Strange input: appointment_time=None")
print("  Input:    ('Fiona Hall', 'Dr. John Doe', None)")
print("  Expected: the clinic needs this rejected - an appointment with")
print("            no time is meaningless.")
try:
    book_appointment("Fiona Hall", "Dr. John Doe", None)
    print("  Actual:   stored, no error raised.")
    print("  Outcome:  FAIL - only the patient name is ever checked.")
except ValueError as error:
    print("  Actual:   ValueError ->", error)
    print("  Outcome:  PASS")

# --- 5. Whitespace-only patient name ---
print()
print("Check 5 - Whitespace-only patient name")
print("  Input:    ('   ', 'Dr. Jane Roe', '2024-07-21 11:30 AM')")
print("  Expected: the clinic needs this rejected - spaces are not a name.")
try:
    book_appointment("   ", "Dr. Jane Roe", "2024-07-21 11:30 AM")
    print("  Actual:   stored, no error raised.")
    print("  Outcome:  FAIL - 'if not patient_name' is False for '   ',")
    print("            because a string of spaces is truthy in Python.")
except ValueError as error:
    print("  Actual:   ValueError ->", error)
    print("  Outcome:  PASS")

print()
print("-" * 64)
print("Everything stored by the BEFORE version:")
display_appointments()


# PART G - ONE IMPROVEMENT
# Reject patient names that contain only whitespace.
# The other issues found in Part F are left unchanged.

print()
print("=" * 64)
print("PART G - ONE CONTROLLED IMPROVEMENT")
print("=" * 64)

improved_appointments = []


def book_appointment_improved(patient_name, practitioner_name, appointment_time):
    # The one change: ".strip()" is added so that a name made only of
    # spaces is treated the same as an empty name.
    if not patient_name or not str(patient_name).strip():
        raise ValueError("Patient name cannot be empty")
    appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time
    }
    improved_appointments.append(appointment)


print()
print("Re-check 5 - whitespace-only patient name, against the IMPROVED version")
print("  Expected: now rejected.")
try:
    book_appointment_improved("   ", "Dr. Jane Roe", "2024-07-21 11:30 AM")
    print("  Actual:   stored, no error raised.")
    print("  Outcome:  FAIL - the improvement did not work.")
except ValueError as error:
    print("  Actual:   ValueError ->", error)
    print("  Outcome:  PASS - fixed.")

print()
print("Re-check 2 - blank patient name still rejected")
try:
    book_appointment_improved("", "Dr. Jane Roe", "2024-07-21 09:30 AM")
    print("  Outcome:  FAIL")
except ValueError as error:
    print("  Actual:   ValueError ->", error)
    print("  Outcome:  PASS")

print()
print("Re-check 1 - a normal booking still works (no regression)")
try:
    book_appointment_improved("Grace Wong", "Dr. John Doe", "2024-07-22 02:00 PM")
    print("  Actual:   stored. Total improved appointments =", len(improved_appointments))
    print("  Outcome:  PASS")
except ValueError as error:
    print("  Actual:   ValueError ->", error)
    print("  Outcome:  FAIL")