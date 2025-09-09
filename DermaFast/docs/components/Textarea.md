# Component: Textarea

**File:** `Der-maFast/frontend/src/components/ui/textarea.jsx`

**Description:**
A styled, multi-line text input component. It is a wrapper around the standard HTML `<textarea>` element with pre-applied styling from Tailwind CSS.

**Props:**
*   `className` (string, optional): Additional CSS classes to be applied to the textarea element.
*   ...props: Any other props are passed down to the underlying `<textarea>` element. This includes props like `value`, `onChange`, `placeholder`, `disabled`, `rows`, `name`, etc.

**Usage Example:**

```jsx
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

<div>
  <Label htmlFor="message">Your Message</Label>
  <Textarea placeholder="Type your message here." id="message" />
</div>
```

**Dependencies:**
*   `@/lib/utils`: Contains the `cn` utility function for merging Tailwind CSS classes.



