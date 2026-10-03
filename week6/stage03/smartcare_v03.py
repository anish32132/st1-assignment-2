# =====================================================================
# SmartCare v0.3 - Stage 3 Lab (Week 6)
# Introduction to Software Technology
# Student name: Anish Atmakur
# Student ID: U3319971
# Tutorial group: 4483
#
# Part G - Python class skeletons for the approved domain model.
# Part H - Model-code consistency check.
#
# These are SKELETONS. The lab says not to implement full behaviour
# yet, so only the responsibilities written on the CRC cards are coded.
# Anything deferred is marked with a DEFERRED comment and the reason.
#
# Carried forward from Week 5:
#   BR-01  required text fields cannot be blank or whitespace only
#   BR-02  a practitioner cannot hold two SCHEDULED appointments
#          at the same date and time
#   BR-03  a new appointment starts with status SCHEDULED
#   BR-04  cancelling sets status CANCELLED and keeps the record
#   BR-05  each patient has a unique patient ID
#
# Run:  python smartcare_v03.py
# =====================================================================


# The two appointment statuses confirmed in Week 5.
# COMPLETED is still an open question (OQ-01), so it is not added here.
STATUS_SCHEDULED = "SCHEDULED"
STATUS_CANCELLED = "CANCELLED"


def has_text(value):
    """BR-01 - a required text field must contain real characters.
    Reused from Week 5 so the rule is written in one place only."""
    return bool(value) and bool(str(value).strip())


# ---------------------------------------------------------------------
# CLASS: Patient
# CRC responsibilities: know its own identity and name; validate its
# own required fields (BR-01, FR-11); report its details (FR-02).
# Collaborators: Appointment
# ---------------------------------------------------------------------

class Patient:

    def __init__(self, patient_id, name):
        self.patient_id = patient_id
        self.name = name

    def is_valid(self):
        """FR-11, BR-01 - both required fields must contain text."""
        return has_text(self.patient_id) and has_text(self.name)

    def details(self):
        """FR-02 - report this patient's stored details."""
        return f"{self.patient_id} - {self.name}"

    # DEFERRED: uniqueness of patient_id (BR-05) is not checked here.
    # One Patient cannot see the other patients, so the rule belongs to
    # whatever holds the collection. That is a later stage.


# ---------------------------------------------------------------------
# CLASS: Practitioner
# CRC responsibilities: know its own name; validate its own required
# field (BR-01, FR-11).
# Collaborators: Appointment
# ---------------------------------------------------------------------

class Practitioner:

    def __init__(self, name):
        self.name = name

    def is_valid(self):
        """FR-11, BR-01 - the name must contain text."""
        return has_text(self.name)

    # DEFERRED: no details() operation. Unlike FR-02 for a patient,
    # no requirement asks for practitioner details to be displayed, so
    # adding one would be an unsupported feature.

    # DEFERRED: specialty is mentioned in the Week 6 lecture as a
    # possible attribute, but the SmartCare client has never asked for
    # it, so it is not modelled. Adding it would be an unsupported
    # feature.


# ---------------------------------------------------------------------
# CLASS: Appointment
# CRC responsibilities: know its patient, practitioner, time and
# status; start as SCHEDULED (BR-03); cancel itself while keeping the
# record (BR-04, FR-08, FR-09); say whether it clashes with one other
# appointment (BR-02).
# Collaborators: Patient, Practitioner
# ---------------------------------------------------------------------

class Appointment:

    def __init__(self, appointment_id, patient, practitioner, time):
        self.appointment_id = appointment_id
        self.patient = patient
        self.practitioner = practitioner
        self.time = time
        self.status = STATUS_SCHEDULED        # BR-03

    # DEFERRED: Appointment does not validate its own fields. The CRC
    # card does not give it that responsibility, so adding is_valid()
    # here would put an operation in the code that the model does not
    # show. Blank-field checking for an appointment (BR-01, FR-11)
    # happens where appointments are created, in a later stage.

    def is_scheduled(self):
        return self.status == STATUS_SCHEDULED

    def cancel(self):
        """FR-08, FR-09, BR-04 - mark as cancelled. The record is kept,
        never deleted, so the appointment history stays complete."""
        if self.status == STATUS_CANCELLED:
            raise ValueError("Appointment is already cancelled")
        self.status = STATUS_CANCELLED

    def clashes_with(self, other):
        """BR-02 - does this appointment clash with one other one?
        Only SCHEDULED appointments block a time slot.

        DEFERRED: checking a new booking against EVERY stored
        appointment is a cross-object workflow. The Week 6 lecture puts
        that in a service in a later stage, so it is not done here."""
        return (self.is_scheduled()
                and other.is_scheduled()
                and self.practitioner is other.practitioner
                and self.time == other.time)


# =====================================================================
# PART H - MODEL-CODE CONSISTENCY CHECK
#
# The lecture lists four things to check: class names align with the
# UML, attributes reflect modelled state, methods reflect
# responsibilities, and no unsupported classes or features appear.
# =====================================================================

print("=" * 62)
print("SmartCare v0.3 - DOMAIN MODEL SKELETONS")
print("=" * 62)

# --- Build one small example of each class ---
patient = Patient("P001", "Alice Smith")
practitioner = Practitioner("Dr. Jane Roe")
appointment = Appointment(1, patient, practitioner, "2024-07-21 10:00 AM")

print()
print("Example objects created from the model:")
print("  Patient:      " + patient.details())
print("  Practitioner: " + practitioner.name)
print(f"  Appointment:  #{appointment.appointment_id} | {appointment.patient.name} | "
      f"{appointment.practitioner.name} | {appointment.time} | {appointment.status}")


print()
print("-" * 62)
print("PART H - MODEL-CODE CONSISTENCY CHECK")
print("-" * 62)

# Each entry: class, the attributes the UML shows, the operations the
# UML shows. The check confirms the code matches the diagram.
model = [
    (Patient, patient,
     ["patient_id", "name"],
     ["is_valid", "details"]),
    (Practitioner, practitioner,
     ["name"],
     ["is_valid"]),
    (Appointment, appointment,
     ["appointment_id", "patient", "practitioner", "time", "status"],
     ["is_scheduled", "cancel", "clashes_with"]),
]

all_consistent = True

for cls, example, attributes, operations in model:
    print()
    print(f"{cls.__name__}")

    # Direction 1 - everything the UML shows must exist in the code.
    for attribute in attributes:
        ok = hasattr(example, attribute)
        all_consistent = all_consistent and ok
        print(f"  attribute {attribute:<16} {'present' if ok else 'MISSING FROM CODE'}")
    for operation in operations:
        ok = callable(getattr(cls, operation, None))
        all_consistent = all_consistent and ok
        print(f"  operation {operation + '()':<16} {'present' if ok else 'MISSING FROM CODE'}")

    # Direction 2 - the code must not contain anything the UML does not
    # show. Checking only direction 1 would let an undocumented method
    # slip through, which is how the model and the code drift apart.
    extra_attributes = [a for a in vars(example) if not a.startswith("_")
                        and a not in attributes]
    extra_operations = [m for m in vars(cls) if not m.startswith("_")
                        and callable(getattr(cls, m)) and m not in operations]
    for extra in extra_attributes:
        all_consistent = False
        print(f"  attribute {extra:<16} IN CODE BUT NOT IN THE UML")
    for extra in extra_operations:
        all_consistent = False
        print(f"  operation {extra + '()':<16} IN CODE BUT NOT IN THE UML")
    if not extra_attributes and not extra_operations:
        print("  no undocumented attributes or operations")

print()
print("Relationships in the UML:")
print(f"  Appointment -> Patient       {'present' if isinstance(appointment.patient, Patient) else 'MISSING'}")
print(f"  Appointment -> Practitioner  {'present' if isinstance(appointment.practitioner, Practitioner) else 'MISSING'}")

print()
print("No unsupported classes added:")
print("  classes defined in this file = Patient, Practitioner, Appointment")
print("  This matches the UML exactly. No Manager, Controller, Engine or")
print("  Database class was added, as none is supported by a requirement.")


# =====================================================================
# VERIFICATION - the CRC responsibilities actually behave as modelled
# =====================================================================

print()
print("-" * 62)
print("VERIFICATION OF MODELLED RESPONSIBILITIES")
print("-" * 62)


def check(number, description, traces, passed):
    global all_consistent
    all_consistent = all_consistent and passed
    print()
    print(f"Check {number} - {description}")
    print(f"  Traces to: {traces}")
    print(f"  Outcome:   {'PASS' if passed else 'FAIL'}")


check(1, "A new appointment starts as SCHEDULED",
      "BR-03, FR-06", appointment.is_scheduled())

check(2, "A blank patient name makes the Patient invalid",
      "BR-01, FR-11", Patient("P002", "   ").is_valid() is False)

check(3, "A valid patient reports itself as valid",
      "FR-01, FR-11", patient.is_valid() is True)

# BR-02 - two appointments, same practitioner, same time
other = Appointment(2, Patient("P002", "Bob Johnson"), practitioner, "2024-07-21 10:00 AM")
check(4, "Two SCHEDULED appointments at the same time clash",
      "BR-02, FR-07", appointment.clashes_with(other) is True)

appointment.cancel()
check(5, "Cancelling sets CANCELLED and keeps the record",
      "BR-04, FR-08, FR-09",
      appointment.status == STATUS_CANCELLED
      and appointment.time == "2024-07-21 10:00 AM"
      and appointment.patient is patient)

check(6, "A cancelled appointment no longer blocks the time slot",
      "BR-02, BR-04", appointment.clashes_with(other) is False)

print()
print("=" * 62)
if all_consistent:
    print("RESULT: the code is consistent with the UML model, and all")
    print("modelled responsibilities behave as designed.")
else:
    print("RESULT: an inconsistency was found. See the FAIL lines above.")
print("=" * 62)
