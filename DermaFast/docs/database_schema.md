# Supabase Database Schema

This document outlines the database schema for the DermaFast application, hosted on Supabase.

## Table of Contents

- [users](#users)
- [moles](#moles)
- [mole_questionnaires](#mole_questionnaires)
- [question_definitions](#question_definitions)

---

## `users`

This table stores user authentication and basic profile information.

**Schema**

| Column          | Type        | Constraints                          | Description                               |
|-----------------|-------------|--------------------------------------|-------------------------------------------|
| `id`            | `uuid`      | Primary Key, Default: `gen_random_uuid()` | Unique identifier for each user.          |
| `national_id`   | `text`      | Not Null, Unique                     | The user's national identification number.|
| `password_hash` | `text`      | Not Null                             | The user's hashed password.               |
| `last_login`    | `timestamptz` | Nullable                             | Timestamp of the user's last login.       |
| `created_at`    | `timestamptz` | Not Null, Default: `now()`           | Timestamp of when the user was created.   |
| `updated_at`    | `timestamptz` | Not Null, Default: `now()`           | Timestamp of when the user was last updated.|

---

## `moles`

This table stores information about the moles uploaded by users for analysis.

**Schema**

| Column          | Type      | Constraints                     | Description                               |
|-----------------|-----------|---------------------------------|-------------------------------------------|
| `id`            | `uuid`    | Primary Key, Default: `uuid_generate_v4()` | Unique identifier for each mole entry.    |
| `user_id`       | `uuid`    | Not Null, Foreign Key to `users.id` | The user who uploaded the mole image.     |
| `image_url`     | `text`    | Not Null                        | URL of the uploaded mole image in Supabase Storage. |
| `analysis_result` | `jsonb`   | Nullable                        | The result of the mole analysis.          |
| `created_at`    | `timestamptz` | Not Null, Default: `now()`      | Timestamp of when the mole was uploaded.  |

---

## `mole_questionnaires`

This table stores the responses from the mole questionnaire submitted by users. Each `q` column corresponds to a specific question about the mole.

**Schema**

| Column        | Type        | Constraints                        | Description                                      |
|---------------|-------------|------------------------------------|--------------------------------------------------|
| `id`          | `uuid`      | Primary Key, Default: `gen_random_uuid()` | Unique identifier for each questionnaire submission. |
| `national_id` | `text`      | Not Null                           | The national ID of the user submitting the form. |
| `timestamp`   | `timestamptz` | Not Null, Default: `now()`         | Timestamp of when the questionnaire was submitted. |
| `q1`          | `boolean`   | Not Null                           | Answer to question 1.                            |
| `q2`          | `boolean`   | Not Null                           | Answer to question 2.                            |
| `q3`          | `boolean`   | Not Null                           | Answer to question 3.                            |
| `q4`          | `boolean`   | Not Null                           | Answer to question 4.                            |
| `q5`          | `boolean`   | Not Null                           | Answer to question 5.                            |

---

## `question_definitions`

This table stores the text for each question in the mole questionnaire. This allows the questions to be managed dynamically without changing the application code.

**Schema**

| Column        | Type   | Constraints  | Description                          |
|---------------|--------|--------------|--------------------------------------|
| `question_key`| `text` | Primary Key  | The key for the question (e.g., 'q1'). |
| `question_text`| `text` | Not Null     | The full text of the question.       |

**Example Data**

```sql
INSERT INTO question_definitions (question_key, question_text) VALUES
  ('q1', 'When you look at the mole, does one half look different from the other half in shape or thickness?'),
  ('q2', 'Have you noticed if the edges of the mole look ragged, notched, or blurred rather than smooth?'),
  ('q3', 'Do you see more than one color in the mole, such as brown, black, red, white, or blue?'),
  ('q4', 'Would you say it is larger than about 6 millimeters, roughly the size of a pencil eraser?'),
  ('q5', 'Has the mole changed recently in size, shape, color, or caused any new symptoms like itching, bleeding, or crusting?');
```

