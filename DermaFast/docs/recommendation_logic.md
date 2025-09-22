# Recommendation Logic

The DermaFast application provides a recommendation to the user based on a combination of three factors:

1.  **CNN Model Analysis:** The result from our Convolutional Neural Network (CNN) which analyzes the user's mole image.
2.  **Mole Questionnaire:** The user's answers to a series of questions about their mole.
3.  **Similar Mole Selection:** The user's selection of moles from our database that they believe look similar to their own.

Based on these inputs, one of three recommendations is provided.

## Recommendation Tiers

### 1. High Urgency: "See a Plastic Surgeon"

A user is advised to see a plastic surgeon if any of the following conditions are met:

*   The **CNN model's confidence score** for the mole being malignant is **40% or higher** (a score of `>= 0.4`).
*   The user answers **"Yes" to two or more questions** in the mole questionnaire.
*   The user selects **at least one mole** from the similar moles page that is a **known melanoma**.

### 2. Medium Urgency: "See a Dermatologist"

If the conditions for a plastic surgeon recommendation are not met, the system will then check for the following conditions to recommend a visit to a dermatologist:

*   The **CNN model's confidence score** is between **20% and 40%** (a score of `> 0.2` and `< 0.4`).
*   The user answers **"Yes" to exactly one question** in the mole questionnaire.

### 3. Low Urgency: "Continue Monitoring"

If none of the conditions for the higher urgency recommendations are met, the user is advised to continue monitoring their moles and see a dermatologist for regular yearly check-ups.
