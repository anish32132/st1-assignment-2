# SmartCare Stage 1 - Reflection (Part H)

Student name: Anish Atmakur
Student ID: U3319971
Tutorial group: 4483

Before using AI, I built the basic appointment system myself using variables, lists, dictionaries and functions. I identified problems such as duplicate bookings, missing validation and appointments being lost when the program closes.

AI helped me understand why if not patient_name behaves differently for "" and "   ". I had assumed the check was solid. Testing showed it is not because a name made only of spaces is still treated as a non-empty string in Python. AI also helped me understand where a check for duplicate practitioner bookings could be added.

AI did make assumptions. When asked to generate an alternative, it added a status field that nobody requested and included no validation. This meant a blank name could be stored, and None could cause the program to crash after the bad record had already been added.

I verified the output by running the four scenarios from the handout plus one extra of my own. Three failed.

What remained for me was choosing one controlled improvement and recording the clash rule as a question for the clinic rather than inventing it.
