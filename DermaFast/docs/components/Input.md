# Component: Input

**File:** `DermaFast/frontend/src/components/ui/input.jsx`

**Description:**
A standard HTML input component with pre-applied styling from Tailwind CSS. It is a flexible component that can be used for various types of text-based inputs.

**Props:**
*   `className` (string, optional): Additional CSS classes to be applied to the input element.
*   `type` (string, optional): The type of the input, e.g., `'text'`, `'password'`, `'email'`, `'number'`. Defaults to `'text'`.
*   ...props: Any other props are passed down to the underlying `<input>` element. This includes props like `value`, `onChange`, `placeholder`, `disabled`, `name`, etc.

**Usage Example:**

```jsx
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

<div>
  <Label htmlFor="email">Email</Label>
  <Input type="email" id="email" placeholder="Enter your email" />
</div>
```

**Dependencies:**
*   `@/lib/utils`: Contains the `cn` utility function for merging Tailwind CSS classes.

