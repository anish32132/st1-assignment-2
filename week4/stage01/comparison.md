# SmartCare Stage 1 - Comparison

Student name: Anish Atmakur
Student ID: U3319971
Tutorial group: 4483


## Part B - At least five limitations

After running both programs, these are the limitations I identified:

1. No validation of the appointment time. Any text is accepted, including "tomorrow" or "99:99". The program has no idea what a valid time is.

2. Nothing prevents a clashing booking. The same practitioner can be booked twice at exactly the same time. That is the clinic's existing duplicate-booking problem, reproduced rather than fixed.

3. No unique identifiers. Patients and practitioners exist only as names, so two people called "Alice Smith" cannot be told apart, and a typo creates what looks like a different person.

4. No appointment status and no way to cancel. The clinic's inconsistent appointment status information problem is not addressed.

5. No persistence. Every appointment is lost when the program ends, so there is still no reliable appointment history.

6. Validation is incomplete. Only patient_name is checked, and only for falsy values. The practitioner and the time are never checked at all.

7. appointments is a global list. Any part of the program can change it, which makes the code harder to test and harder to reuse.

8. No search. A receptionist cannot look up one patient's appointments or one practitioner's day.


## Part E - Compare Human and AI Versions

| Question | Human version | AI version |
| --- | --- | --- |
| Easy to understand? | Yes. Short, one dictionary per appointment, two functions with obvious names. The f-string print line is a little dense for a beginner. | Yes, and in places easier. It has docstrings and numbers each appointment with enumerate. It is longer for the same job. |
| Runs successfully? | Yes. Both appointments are stored and printed. | Yes. Both appointments are added and listed with a status. |
| Uses only required features? | Yes. It stores exactly the three fields the brief asked for: patient name, practitioner name and appointment time. | No. It added a fourth field, status: "Booked", that was never requested. It did correctly avoid a database and a GUI, as the prompt demanded. |
| Adds assumptions? | Few. It assumes the time is a correctly formatted string and that a name is enough to identify a person. | More. It assumes every appointment starts as "Booked", that a confirmation message should be printed from inside the function, and that the caller wants the list passed in and returned. |
| Handles errors? | Partly. It raises ValueError for an empty patient name, but accepts None for the practitioner and the time, and accepts a whitespace-only name. | No, and it fails worse. It has no validation at all: a blank name is stored silently. With patient_name=None it appends the record first and then crashes with TypeError, so the bad record is already in the list when the program stops. |
| Could I explain it? | Yes, I can explain how the appointments are stored in a list of dictionaries. The book_appointment function creates and stores an appointment, while display_appointments loops through the list and prints each appointment. I also understand that raise ValueError stops an invalid patient name from being stored, and that .strip() makes the check reject names containing only spaces. | Yes, I can explain that the AI version uses a list passed into the function and stores each appointment as a dictionary. It also adds a status field and prints a confirmation message. I understand that it does not validate the input, which means invalid values can still be stored. |

Overall comparison:

The AI version reads more tidily in some areas, and passing the list into the function is better practice than using a global list. However, it also added a feature that was not requested and removed the validation included in the human version. Its failure mode is also worse because invalid data can be added before the program crashes. This shows why the AI output still needed to be checked and tested.


## Part F - Verify Behaviour

The handout lists four required scenarios. I also added Check 5 as an optional extra because the existing patient name check still had a weakness that could be tested.

All checks run against the before version of book_appointment.

| # | Scenario | Input | Expected | Actual | Outcome |
| --- | --- | --- | --- | --- | --- |
| 1 | Normal appointment | ("Chris Lee", "Dr. John Doe", "2024-07-21 09:00 AM") | Stored, no error | Stored. Total appointments = 3 | PASS |
| 2 | Blank patient name | ("", "Dr. Jane Roe", "2024-07-21 09:30 AM") | ValueError | ValueError: Patient name cannot be empty | PASS |
| 3 | Two appointments, same practitioner/time | Two bookings for Dr. Jane Roe at 2024-07-21 10:00 AM | Refused or reported | Both stored. Bookings for that practitioner/time = 2 | FAIL |
| 4a | Strange input: patient_name=None | patient_name=None | ValueError | ValueError: Patient name cannot be empty | PASS |
| 4b | Strange input: appointment_time=None | appointment_time=None | ValueError | Stored, no error raised | FAIL |
| 5 | Optional extra: whitespace-only name | ("   ", "Dr. Jane Roe", "2024-07-21 11:30 AM") | ValueError | Stored, no error raised | FAIL |

### What the failures mean

- Check 3 shows the prototype reproduces the clinic's duplicate-booking problem instead of solving it.
- Check 4b shows only the patient name is ever validated. An appointment with no time is stored without an error.
- Check 5 shows why the existing check is weaker than it looks. if not patient_name is false for "   " because a string of spaces is truthy in Python.


## Part G - Improve One Thing

The handout says to choose exactly one controlled improvement and gives if not patient_name: raise ValueError(...) as its example. That exact line is already in the task1enhanced code, so it cannot be my improvement. Check 5 showed the line still lets a whitespace-only name through.

My one improvement is to strengthen that existing check so a patient name made only of whitespace is rejected too.

```python
def book_appointment_improved(patient_name, practitioner_name, appointment_time):
    if not patient_name or not str(patient_name).strip():
        raise ValueError("Patient name cannot be empty")
    appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time
    }
    improved_appointments.append(appointment)
```

Why this one: it is a genuine defect found by testing, it is one condition on one
field, it needs no new information from the client, and I can explain exactly why
it works.

### What I deliberately did not change, to keep the improvement controlled

| Not changed | Status | Why |
| --- | --- | --- |
| Validation of practitioner_name | NOT implemented | Part G allows exactly one improvement. |
| Validation of appointment_time (Check 4b) | NOT implemented | Doing it properly needs the clinic's required time format first, otherwise I would be inventing one. |
| Clash detection (Check 3) | NOT implemented | Needs a confirmed rule on whether a practitioner may ever hold two appointments at once. |
| Appointment IDs and status | NOT implemented | The clinic has not said what identifiers or statuses it uses. |
| Saving to a file or database | NOT implemented | Explicitly prohibited by the lab brief at this stage. |

### Re-checks after the change

| Re-check | Expected | Actual | Outcome |
| --- | --- | --- | --- |
| Whitespace-only name "   " | Now rejected | ValueError: Patient name cannot be empty | PASS - fixed |
| Blank name "" | Still rejected | ValueError: Patient name cannot be empty | PASS |
| Normal booking ("Grace Wong", "Dr. John Doe", "2024-07-22 02:00 PM") | Still works | Stored. Total improved appointments = 1 | PASS - no regression |

