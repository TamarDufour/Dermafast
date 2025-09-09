# Component: AuthForm

**File:** `DermaFast/frontend/src/components/AuthForm.jsx`

**Description:**
The `AuthForm` component provides a user interface for both user registration and login. It can switch between "Sign In" and "Sign Up" modes. The form collects a national ID and a password from the user. It communicates with a backend API to authenticate or create a user.

**Props:**
*   `onLogin`: A function that is called upon successful login. It receives the user's `nationalId` as an argument.

**State:**
*   `nationalId` (string): Stores the value of the national ID input field.
*   `password` (string): Stores the value of the password input field.
*   `isLoginMode` (boolean): Toggles between login (true) and registration (false) modes. Defaults to `true`.
*   `loading` (boolean): Indicates whether an API request is in progress. Used to disable form elements and show a loading indicator.
*   `message` (string): Stores feedback messages to display to the user (e.g., success or error messages).
*   `messageType` (string): Determines the style of the feedback message. Can be `'success'` or `'error'`.

**Functionality:**
*   **Mode Toggling:** Users can switch between login and registration forms using a button. This action resets the form fields and any displayed messages.
*   **Form Submission:**
    *   When submitted, the form sends a POST request to either `/api/login` or `/api/register` on the backend, depending on the current mode.
    *   The request body includes the `national_id` and `password`.
    *   On successful login, it calls the `onLogin` prop with the `nationalId`.
    *   On successful registration, it clears the form and switches to login mode.
*   **Error Handling:** It handles API errors and network issues, displaying appropriate error messages to the user.
*   **Loading State:** A loading spinner is shown on the submit button while the API request is pending.



