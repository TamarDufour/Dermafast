# Supabase Database Management - schema and information

This document outlines the database schema for the DermaFast application, hosted on Supabase.

## Table of Contents

- [users](#users)
- [moles](#moles)
- [mole_questionnaires](#mole_questionnaires)
- [question_definitions](#question_definitions)

---

## `users` - Table

This table stores user authentication and basic profile information. When a user log in or creates a new user, this table updates.

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

## `moles` - Table

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

## `mole_questionnaires` - Table

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

## `question_definitions` - Table

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
## `ham_metadata` - Table
This tables includes the metadata about the pictures from HAM10000 dataset.
Each row represents a single image, along with its diagnostic and patient-related metadata.

**Schema**

| Column         | Type          | Description                                               |
| -------------- | ------------- | --------------------------------------------------------- |
| `image_id`     | `TEXT`        | Primary key. Filename (without extension) of the image.   |
| `image_url`    | `TEXT`        | Public URL to the image stored in Supabase Storage.       |
| `lesion_id`    | `TEXT`        | Identifier for the lesion (can link multiple images).     |
| `dx`           | `TEXT`        | Diagnosis (e.g., `mel`, `nv`, `bkl`).                     |
| `dx_type`      | `TEXT`        | Type of diagnosis (e.g., `histopathology`).               |
| `age`          | `REAL`        | Age of the patient (e.g., `50.0`).                        |
| `sex`          | `TEXT`        | Sex of the patient (`male`, `female`, or `unknown`).      |
| `localization` | `TEXT`        | Body location of the mole (e.g., `back`, `face`).         |
| `uploaded_at`  | `TIMESTAMPTZ` | Timestamp when the row was inserted. Defaults to `now()`. |
| `embedding`    | `FLOAT[]`     | 256-dim. embedding vector from the CNN’s dropout layer    |


# `HAM10000_for_comparison` Bucket

This Supabase Storage bucket contains a curated subset of mole images from the **HAM10000 dataset**.

## Purpose

The images in this bucket are used to:

- Compare uploaded user mole images against labeled training images.
- Support **Approximate Nearest Neighbor (ANN)** search for similar moles.
- Enable embedding-based similarity in the decision-making process.

## Content

- **870 images** selected from the original dataset. 50% for them are of melenoma.
- Stored in `.jpg` format.
- Images are named using their `image_id` (e.g., `ISIC_0031434.jpg`).
- Publicly accessible via Supabase storage.

## Storage Size

- Average size per image: ~300 KB  
- Total size: ~250 MB

## Access & Metadata

Each image in the bucket corresponds to a row in the `ham_metadata` table in the database, which includes:

- `image_id`: unique identifier
- `image_url`: full public URL to the image in this bucket
- `dx`: diagnosis label (e.g., `mel`, `nv`)
- Other metadata (e.g., `lesion_id`, `age`, `sex`, `localization`)


## `cnn_results` - Table

This table stores the output of the CNN model after a user uploads a mole image. It includes the binary classification result and the embedding vector used for similarity search.
- The `embedding` vector will later be used for **Approximate Nearest Neighbor (ANN)** retrieval to compare uploaded mole images with a training set.
- `cnn_result` represents the **likelihood** (between 0 and 1) of the mole being melanoma.

**Schema**

| Column Name | Type         | Description                                                  |
|-------------|--------------|--------------------------------------------------------------|
| `national_id`   | `Varchar(255)` | Foreign key referencing `users(id)`                    |
| `timestamp` | `TIMESTAMPTZ`| Time of prediction (defaults to `now()`)                    |
| `cnn_result`| `FLOAT`      | Pribability of the mole to be melanoma               |
| `embedding` | `FLOAT[]`    | 2D embedding vector from the CNN’s dropout layer    |

### 🔗 Relationships

- Each user can have multiple CNN results associated with different mole checks.
- The primary key for this table is a composite of `national_id` and `timestamp`.

## `similar_moles_ann_user` - Table

This table stores the `image_id`s of up to three moles that the user has identified as being most similar to their own mole.

**Schema**

| Column Name | Type         | Constraints                                       | Description                               |
|-------------|--------------|---------------------------------------------------|-------------------------------------------|
| `national_id` | `VARCHAR(255)`| Not Null, Foreign Key to `users.national_id`      | The user who made the selection.          |
| `timestamp`   | `TIMESTAMPTZ` | Not Null, Default: `now()`                        | Timestamp of the selection.               |
| `image_id1`   | `TEXT`        | Nullable                                          | The `image_id` of the first selected mole.|
| `image_id2`   | `TEXT`        | Nullable                                          | The `image_id` of the second selected mole.|
| `image_id3`   | `TEXT`        | Nullable                                          | The `image_id` of the third selected mole.|

### 🔗 Relationships

- The primary key for this table is a composite of `national_id` and `timestamp`.
- Each user can have multiple selection records, corresponding to different mole checks.


## `final_recommendation` - Table

This table stores the final recommendation for a user's mole.

**Schema**

| Column          | Type        | Constraints                          | Description                               |
|-----------------|-------------|--------------------------------------|-------------------------------------------|
| `id`            | `uuid`      | Primary Key, Default: `gen_random_uuid()` | Unique identifier for each recommendation. |
| `national_id`   | `text`      | Not Null, Foreign Key to `users.id` | The user who received the recommendation. |
| `timestamp`     | `timestamptz` | Not Null, Default: `now()`           | Timestamp of when the recommendation was made. |
| `recommendation`| `text`      | Not Null                             | The text of the recommendation.           |
| `created_at`    | `timestamptz` | Not Null, Default: `now()`           | Timestamp of when the recommendation was created. |
| `updated_at`    | `timestamptz` | Not Null, Default: `now()`           | Timestamp of when the recommendation was last updated. |


