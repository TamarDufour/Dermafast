# Component: Checkbox

**File:** `DermaFast/frontend/src/components/ui/checkbox.jsx`

**Description:**
A customizable checkbox component, built on top of `@radix-ui/react-checkbox`. It is styled with Tailwind CSS and supports focus, disabled, and checked states.

**Props:**
*   `className` (string, optional): Additional CSS classes to be applied to the checkbox.
*   ...props: Any other props are passed down to the underlying `@radix-ui/react-checkbox` `Root` component. This includes props like `checked`, `onCheckedChange`, `disabled`, `name`, etc.

**Usage Example:**

```jsx
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

// Controlled checkbox
const [isChecked, setIsChecked] = useState(false);

<div className="flex items-center space-x-2">
  <Checkbox
    id="terms"
    checked={isChecked}
    onCheckedChange={setIsChecked}
  />
  <Label htmlFor="terms">Accept terms and conditions</Label>
</div>

// Uncontrolled checkbox with a form
<form onSubmit={...}>
  <Checkbox id="subscribe" name="subscribe" />
  <Label htmlFor="subscribe">Subscribe to newsletter</Label>
</form>
```

**Dependencies:**
*   `@radix-ui/react-checkbox`: The underlying primitive checkbox component that provides accessibility and functionality.
*   `lucide-react`: Provides the `Check` icon that is displayed when the checkbox is checked.
*   `@/lib/utils`: Contains the `cn` utility function for merging Tailwind CSS classes.



