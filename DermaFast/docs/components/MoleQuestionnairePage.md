# Component: MoleQuestionnairePage

**File:** `DermaFast/frontend/src/components/MoleQuestionnairePage.jsx`

**Description:**
The `MoleQuestionnairePage` component presents a series of questions to the user about a mole. These questions are based on the "ABCDE" rule for skin cancer detection (Asymmetry, Border, Color, Diameter, Evolution). The user's answers are collected and submitted to a Supabase backend.

**Props:**
*   `nationalId` (string): The national ID of the user, which is included in the questionnaire submission.

**State:**
*   `answers` (object): An object that stores the user's answers to the questions. The keys are the question IDs, and the values are either `'yes'` or `'no'`.
*   `error` (string): Stores an error message to be displayed if the user tries to submit the form without answering all questions.

**Functionality:**
*   **Displays Questions:** Renders a list of predefined questions about the mole.
*   **Collects Answers:** For each question, the user can select "Yes" or "No" using radio buttons. The component updates its `answers` state as the user makes selections.
*   **Form Submission:**
    *   When the "Submit Questionnaire" button is clicked, the component first validates that all questions have been answered.
    *   If validation passes, it constructs a submission object containing the `national_id` and the answers (converted to booleans).
    *   It then inserts this data into the `mole_questionnaires` table in the Supabase database.
    *   After a successful submission, it shows an alert to the user and navigates them to the `/check-mole` page.
*   **Error Handling:** If the form is submitted with unanswered questions, an error message is displayed. It also handles and logs errors that may occur during the submission to Supabase.

**Dependencies:**
*   `react-router-dom`: The `useNavigate` hook is used for redirecting the user after a successful submission.
*   `@/supabase`: The Supabase client is imported to interact with the database.
*   `@/components/ui`:
    *   `Card`, `CardContent`, `CardDescription`, `CardFooter`, `CardHeader`, `CardTitle` are used for the layout.
    *   `Button` for the form submission.
    *   `Label` for question text and radio button labels.
    *   `RadioGroup`, `RadioGroupItem` for the "Yes/No" options.



