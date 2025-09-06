# Component: HomePage

**File:** `DermaFast/frontend/src/components/HomePage.jsx`

**Description:**
The `HomePage` component serves as the main dashboard for a logged-in user. It displays a welcome message with the user's name and provides navigation to other parts of the application, such as checking a mole or filling out a questionnaire. It also includes a logout button.

**Props:**
*   `username` (string): The name of the logged-in user to be displayed in the welcome message.
*   `onLogout` (function): A callback function that is executed when the user clicks the "Logout" button.

**Functionality:**
*   **User Welcome:** Displays a personalized welcome message to the user.
*   **Navigation:** Contains links to two main features:
    *   "Check a Mole" (`/check-mole`): Navigates the user to the `CheckMolePage`.
    *   "Fill out Mole Questionnaire" (`/questionnaire`): Navigates the user to the `MoleQuestionnairePage`.
*   **Logout:** The "Logout" button, when clicked, calls the `onLogout` function to handle the user's session termination.

**Dependencies:**
*   `react-router-dom`: The `Link` component is used for navigation between pages.
*   `@/components/ui`:
    *   `Card`, `CardContent`, `CardDescription`, `CardFooter`, `CardHeader`, `CardTitle` are used for the page layout and structure.
    *   `Button` is used for the navigation links and the logout action.

