# SmartCare v0.2 - Stage 2 Lab (Week 5)
# Introduction to Software Technology
# Student name: Anish Atmakur
# Student ID: U3319971
# Tutorial group: 4483

patients = []
practitioners = []
appointments = []

next_appointment_id = 1


# Check if a value is not empty
def has_text(value):
    return bool(value) and bool(str(value).strip())


# Patient functions
def register_patient(patient_id, name):
    if not has_text(patient_id):
        raise ValueError("Patient ID cannot be empty")

    if not has_text(name):
        raise ValueError("Patient name cannot be empty")

    if find_patient(patient_id) is not None:
        raise ValueError("Patient ID already exists")

    patients.append({
        "patient_id": str(patient_id).strip(),
        "name": str(name).strip()
    })


def find_patient(patient_id):
    for patient in patients:
        if patient["patient_id"] == str(patient_id).strip():
            return patient

    return None


# Practitioner functions
def register_practitioner(name):
    if not has_text(name):
        raise ValueError("Practitioner name cannot be empty")

    practitioners.append({
        "name": str(name).strip()
    })


def find_practitioner(name):
    for practitioner in practitioners:
        if practitioner["name"] == str(name).strip():
            return practitioner

    return None


# Appointment functions
def book_appointment(patient_id, practitioner_name, appointment_time):
    global next_appointment_id

    if not has_text(appointment_time):
        raise ValueError("Appointment time cannot be empty")

    if find_patient(patient_id) is None:
        raise ValueError("Patient is not registered")

    if find_practitioner(practitioner_name) is None:
        raise ValueError("Practitioner is not registered")

    # Check if the practitioner is already booked
    for appointment in appointments:
        if (appointment["practitioner"] == str(practitioner_name).strip()
                and appointment["time"] == str(appointment_time).strip()
                and appointment["status"] == "SCHEDULED"):

            raise ValueError("Practitioner is already booked at this time")

    appointment = {
        "appointment_id": next_appointment_id,
        "patient_id": str(patient_id).strip(),
        "practitioner": str(practitioner_name).strip(),
        "time": str(appointment_time).strip(),
        "status": "SCHEDULED"
    }

    appointments.append(appointment)
    next_appointment_id += 1

    return appointment["appointment_id"]


def cancel_appointment(appointment_id):
    for appointment in appointments:
        if appointment["appointment_id"] == appointment_id:

            if appointment["status"] == "CANCELLED":
                raise ValueError("Appointment is already cancelled")

            appointment["status"] = "CANCELLED"
            return

    raise ValueError("Appointment not found")


def appointments_for_practitioner(practitioner_name):
    result = []

    for appointment in appointments:
        if appointment["practitioner"] == str(practitioner_name).strip():
            result.append(appointment)

    return result


def history_for_patient(patient_id):
    result = []

    for appointment in appointments:
        if appointment["patient_id"] == str(patient_id).strip():
            result.append(appointment)

    return result


def display_appointments():
    if not appointments:
        print("No appointments recorded.")
        return

    for appointment in appointments:
        patient = find_patient(appointment["patient_id"])

        if patient:
            patient_name = patient["name"]
        else:
            patient_name = "Unknown"

        print(
            f"#{appointment['appointment_id']} | "
            f"{patient_name} | "
            f"{appointment['practitioner']} | "
            f"{appointment['time']} | "
            f"{appointment['status']}"
        )


# --------------------------------
# Testing the program
# --------------------------------

print("=" * 50)
print("SmartCare v0.2")
print("=" * 50)

register_patient("P001", "Alice Smith")
register_patient("P002", "Bob Johnson")

register_practitioner("Dr. John Doe")
register_practitioner("Dr. Jane Roe")

print("\nTest data added.")


# Test 1 - Blank patient name
try:
    register_patient("P003", "   ")
    print("Test 1: FAIL")
except ValueError:
    print("Test 1: PASS - Blank patient name rejected")


# Test 2 - Duplicate patient ID
try:
    register_patient("P001", "Different Person")
    print("Test 2: FAIL")
except ValueError:
    print("Test 2: PASS - Duplicate patient ID rejected")


# Test 3 - Find patient
patient = find_patient("P002")

if patient and patient["name"] == "Bob Johnson":
    print("Test 3: PASS - Patient found")
else:
    print("Test 3: FAIL")


# Test 4 - Book appointment
try:
    appointment_id = book_appointment(
        "P001",
        "Dr. Jane Roe",
        "2024-07-21 10:00 AM"
    )

    appointment = appointments[0]

    if appointment["status"] == "SCHEDULED":
        print("Test 4: PASS - Appointment booked")
    else:
        print("Test 4: FAIL")

except ValueError:
    print("Test 4: FAIL")


# Test 5 - Appointment clash
try:
    book_appointment(
        "P002",
        "Dr. Jane Roe",
        "2024-07-21 10:00 AM"
    )

    print("Test 5: FAIL")

except ValueError:
    print("Test 5: PASS - Appointment clash rejected")


# Test 6 - Cancel appointment
try:
    cancel_appointment(appointment_id)

    if appointments[0]["status"] == "CANCELLED":
        print("Test 6: PASS - Appointment cancelled")
    else:
        print("Test 6: FAIL")

except ValueError:
    print("Test 6: FAIL")


# Test 7 - Book the same time after cancellation
try:
    second_id = book_appointment(
        "P002",
        "Dr. Jane Roe",
        "2024-07-21 10:00 AM"
    )

    print("Test 7: PASS - Time slot available after cancellation")

except ValueError:
    print("Test 7: FAIL")


# Test 8 - Patient history
history = history_for_patient("P001")

if len(history) == 1 and history[0]["status"] == "CANCELLED":
    print("Test 8: PASS - Cancelled appointment kept in history")
else:
    print("Test 8: FAIL")


# Test 9 - Practitioner appointments
schedule = appointments_for_practitioner("Dr. Jane Roe")

if len(schedule) == 2:
    print("Test 9: PASS - Practitioner appointments found")
else:
    print("Test 9: FAIL")


# Test 10 - Unregistered patient
try:
    book_appointment(
        "P999",
        "Dr. John Doe",
        "2024-07-22 09:00 AM"
    )

    print("Test 10: FAIL")

except ValueError:
    print("Test 10: PASS - Unregistered patient rejected")


# Show appointments
print("\nAll appointments:")
display_appointments()