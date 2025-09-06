# Component: CheckMolePage

**File:** `DermaFast/frontend/src/components/CheckMolePage.jsx`

**Description:**
The `CheckMolePage` component provides a user interface for users to upload an image of a mole for analysis. It displays instructions for taking a good quality photo and includes a file input for image selection.

**State:**
*   `file` (File object | null): Stores the selected image file for the mole.
*   `message` (string): Displays messages to the user, such as the status of the file analysis or a prompt to select a file.

**Functionality:**
*   **File Selection:** Users can select an image file from their device. When a file is selected, it is stored in the `file` state, and any previous message is cleared.
*   **Analysis Trigger:** The "Analyze" button triggers the analysis process.
    *   If a file is selected, it displays a message indicating that the analysis has started (currently a placeholder).
    *   If no file is selected, it prompts the user to select a file.
*   **Instructions:** The component provides clear instructions to the user on how to take a suitable photo of a mole to ensure the best analysis results. This includes tips on focus, framing, and lighting.

**Dependencies:**
*   This component uses several UI components from `@/components/ui`:
    *   `Card`, `CardContent`, `CardDescription`, `CardFooter`, `CardHeader`, `CardTitle` for the layout.
    *   `Button` for the analyze action.
    *   `Input` for the file selection.
    *   `Label` for the file input label.

