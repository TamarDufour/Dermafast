# Component: Label

**File:** `DermaFast/frontend/src/components/ui/label.jsx`

**Description:**
A component for rendering an accessible label for form elements like `<input>`, `<textarea>`, or `<select>`. It is built on top of `@radix-ui/react-label` and is styled with `class-variance-authority` (CVA) and Tailwind CSS.

**Props:**
*   `className` (string, optional): Additional CSS classes to be applied to the label.
*   ...props: Any other props are passed down to the underlying `@radix-ui/react-label` `Root` component. This typically includes the `htmlFor` prop, which is crucial for associating the label with a form control.

**Usage Example:**

```jsx
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

<div className="grid w-full max-w-sm items-center gap-1.5">
  <Label htmlFor="email">Email</Label>
  <Input type="email" id="email" placeholder="Email" />
</div>
```

**Dependencies:**
*   `@radix-ui/react-label`: The underlying primitive label component that provides accessibility features.
*   `class-variance-authority`: Used for creating variant classes, although this component has a single variant.
*   `@/lib/utils`: Contains the `cn` utility function for merging Tailwind CSS classes.

