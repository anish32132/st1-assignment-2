# SmartCare v0.4 - Stage 4 Lab (Week 7)
# Introduction to Software Technology
# Student name: Anish Atmakur
# Student ID: U3319971
# Tutorial group: 4483

from enum import Enum
from typing import Optional


class AppointmentStatus(Enum):
    SCHEDULED = "SCHEDULED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class InvalidStatusTransitionError(Exception):
    """Raised when an appointment has an invalid status transition."""


def require_text(value: Optional[str], field_name: str) -> str:
    if value is None or not str(value).strip():
        raise ValueError(f"{field_name} cannot be empty")
    return str(value).strip()


class Patient:

    def __init__(self, patient_id: str, name: str) -> None:
        self._patient_id: str = require_text(patient_id, "Patient ID")
        self._name: str = require_text(name, "Patient name")

    @property
    def patient_id(self) -> str:
        return self._patient_id

    @property
    def name(self) -> str:
        return self._name

    def details(self) -> str:
        return f"{self._patient_id} - {self._name}"


class Practitioner:

    def __init__(self, practitioner_id: str, name: str, specialty: str) -> None:
        self._practitioner_id: str = require_text(
            practitioner_id, "Practitioner ID"
        )
        self._name: str = require_text(name, "Practitioner name")
        self._specialty: str = require_text(specialty, "Specialty")

    @property
    def practitioner_id(self) -> str:
        return self._practitioner_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def specialty(self) -> str:
        return self._specialty


class Appointment:

    def __init__(self, appointment_id: int, patient: Patient,
                 practitioner: Practitioner, time: str) -> None:
        if not isinstance(patient, Patient):
            raise ValueError("Appointment requires a Patient")
        if not isinstance(practitioner, Practitioner):
            raise ValueError("Appointment requires a Practitioner")

        self._appointment_id: int = appointment_id
        self._patient: Patient = patient
        self._practitioner: Practitioner = practitioner
        self._time: str = require_text(time, "Appointment time")
        self._status: AppointmentStatus = AppointmentStatus.SCHEDULED

    @property
    def appointment_id(self) -> int:
        return self._appointment_id

    @property
    def patient(self) -> Patient:
        return self._patient

    @property
    def practitioner(self) -> Practitioner:
        return self._practitioner

    @property
    def time(self) -> str:
        return self._time

    @property
    def status(self) -> AppointmentStatus:
        return self._status

    def is_scheduled(self) -> bool:
        return self._status is AppointmentStatus.SCHEDULED

    def cancel(self) -> None:
        if self._status is not AppointmentStatus.SCHEDULED:
            raise InvalidStatusTransitionError(
                f"Cannot cancel an appointment with status {self._status.value}"
            )
        self._status = AppointmentStatus.CANCELLED

    def clashes_with(self, other: "Appointment") -> bool:
        return (self.is_scheduled()
                and other.is_scheduled()
                and self._practitioner is other.practitioner
                and self._time == other.time)


def report(number: int, description: str, traces: str,
           expected: str, actual: str, passed: bool) -> bool:
    print()
    print(f"Check {number} - {description}")
    print(f"  Traces to: {traces}")
    print(f"  Expected:  {expected}")
    print(f"  Actual:    {actual}")
    print(f"  Outcome:   {'PASS' if passed else 'FAIL'}")
    return passed


print("=" * 64)
print("SmartCare v0.4 - OBJECT-ORIENTED DOMAIN LAYER")
print("=" * 64)

all_passed = True


# Create valid objects
patient = Patient("P001", "Alice Smith")
practitioner = Practitioner("DR01", "Dr. Jane Roe", "General Practice")
appointment = Appointment(1, patient, practitioner, "2024-07-21 10:00 AM")

print()
print("Valid objects created:")
print(f"  Patient:      {patient.details()}")
print(f"  Practitioner: {practitioner.practitioner_id} | "
      f"{practitioner.name} | {practitioner.specialty}")
print(f"  Appointment:  #{appointment.appointment_id} | {appointment.patient.name} | "
      f"{appointment.practitioner.name} | {appointment.time} | "
      f"{appointment.status.value}")

all_passed &= report(
    1, "A new appointment starts as SCHEDULED",
    "BR-03, FR-06",
    "status is AppointmentStatus.SCHEDULED",
    f"status is {appointment.status}",
    appointment.status is AppointmentStatus.SCHEDULED)


# Invalid input
try:
    Patient("P002", "   ")
    result, passed = "stored with no error", False
except ValueError as error:
    result, passed = f"ValueError -> {error}", True

all_passed &= report(
    2, "A whitespace-only patient name is refused",
    "BR-01, FR-11", "ValueError", result, passed)

try:
    Practitioner("DR02", "Dr. John Doe", "")
    result, passed = "stored with no error", False
except ValueError as error:
    result, passed = f"ValueError -> {error}", True

all_passed &= report(
    3, "A blank specialty is refused",
    "BR-01, Stage 4 Lab Part C", "ValueError", result, passed)

try:
    Appointment(2, "not a patient", practitioner, "2024-07-21 11:00 AM")
    result, passed = "stored with no error", False
except ValueError as error:
    result, passed = f"ValueError -> {error}", True

all_passed &= report(
    4, "An Appointment refuses something that is not a Patient",
    "UML association", "ValueError", result, passed)


# Encapsulation
try:
    appointment.status = AppointmentStatus.COMPLETED
    result, passed = "the status was overwritten from outside", False
except AttributeError as error:
    result, passed = f"AttributeError -> {error}", True

all_passed &= report(
    5, "Status cannot be set directly from outside the object",
    "Encapsulation, BR-03, BR-04",
    "AttributeError, because status is read-only", result, passed)


# Cancel a scheduled appointment
appointment.cancel()

all_passed &= report(
    6, "Cancelling sets CANCELLED and keeps the object",
    "BR-04, FR-08, FR-09",
    "status CANCELLED and the object still readable",
    f"status {appointment.status.value}, patient still "
    f"{appointment.patient.name}, time still {appointment.time}",
    appointment.status is AppointmentStatus.CANCELLED
    and appointment.patient is patient)


# Illegal repeated transition
try:
    appointment.cancel()
    result, passed = "cancelled twice with no error", False
except InvalidStatusTransitionError as error:
    result, passed = f"InvalidStatusTransitionError -> {error}", True

all_passed &= report(
    7, "Cancelling an already cancelled appointment is refused",
    "BR-04, legal state transitions",
    "InvalidStatusTransitionError", result, passed)


# BR-02 checks
second = Appointment(3, Patient("P003", "Bob Johnson"),
                     practitioner, "2024-07-21 10:00 AM")
third = Appointment(4, Patient("P004", "Chris Lee"),
                    practitioner, "2024-07-21 10:00 AM")

all_passed &= report(
    8, "Two SCHEDULED appointments at the same time clash",
    "BR-02, FR-07", "True", str(second.clashes_with(third)),
    second.clashes_with(third) is True)

all_passed &= report(
    9, "A cancelled appointment no longer blocks the slot",
    "BR-02, BR-04", "False", str(appointment.clashes_with(second)),
    appointment.clashes_with(second) is False)


# UML-to-code trace
print()
print("-" * 64)
print("UML-TO-CODE TRACE")
print("-" * 64)

model = [
    (Patient, patient, ["patient_id", "name"], ["details"]),
    (Practitioner, practitioner,
     ["practitioner_id", "name", "specialty"], []),
    (Appointment, appointment,
     ["appointment_id", "patient", "practitioner", "time", "status"],
     ["is_scheduled", "cancel", "clashes_with"]),
]

for cls, example, properties, operations in model:
    print()
    print(cls.__name__)

    for name in properties:
        ok = isinstance(getattr(cls, name, None), property)
        all_passed &= ok
        print(f"  property  {name:<16} {'read-only' if ok else 'NOT A PROPERTY'}")

    for name in operations:
        ok = callable(getattr(cls, name, None))
        all_passed &= ok
        print(f"  operation {name + '()':<16} {'present' if ok else 'MISSING'}")

    if not operations:
        print("  operations        none modelled, none implemented")

    declared = set(properties) | set(operations)
    extra = [m for m in vars(cls)
              if not m.startswith("_") and m not in declared]

    for name in extra:
        all_passed = False
        print(f"  member    {name:<16} IN CODE BUT NOT IN THE UML")

    if not extra:
        print("  no undocumented members")

    public_state = [a for a in vars(example) if not a.startswith("_")]
    all_passed &= (len(public_state) == 0)
    print(f"  state is private: {len(public_state)} public attributes")


print()
print("Classes defined: Patient, Practitioner, Appointment")
print("Plus AppointmentStatus and InvalidStatusTransitionError.")
print("No database, UI, notification or service class was added.")

print()
print("=" * 64)

if all_passed:
    print("RESULT: all behaviour checks passed and the implementation")
    print("matches the approved design.")
else:
    print("RESULT: a problem was found. See the FAIL lines above.")

print("=" * 64)