# Component: RadioGroup & RadioGroupItem

**File:** `DermaFast/frontend/src/components/ui/radio-group.jsx`

**Description:**
This file exports two components, `RadioGroup` and `RadioGroupItem`, which are used together to create a set of radio buttons. They are built on top of `@radix-ui/react-radio-group` for accessibility and functionality, and styled with Tailwind CSS.

### `RadioGroup`
The container for a set of `RadioGroupItem`s. It manages the state of the radio group.

**Props:**
*   `className` (string, optional): Additional CSS classes to be applied to the group container.
*   ...props: Any other props are passed down to the underlying `@radix-ui/react-radio-group` `Root` component. This includes `value` and `onValueChange` for controlled components, or `defaultValue` for uncontrolled ones.

### `RadioGroupItem`
A single radio button within the `RadioGroup`.

**Props:**
*   `className` (string, optional): Additional CSS classes.
*   `value` (string, required): A unique value for the radio item within the group.
*   ...props: Passed to the underlying `@radix-ui/react-radio-group` `Item` component. This includes `id` and `disabled`.

**Usage Example:**

```jsx
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";

<RadioGroup defaultValue="comfortable">
  <div className="flex items-center space-x-2">
    <RadioGroupItem value="default" id="r1" />
    <Label htmlFor="r1">Default</Label>
  </div>
  <div className="flex items-center space-x-2">
    <RadioGroupItem value="comfortable" id="r2" />
    <Label htmlFor="r2">Comfortable</Label>
  </div>
  <div className="flex items-center space-x-2">
    <RadioGroupItem value="compact" id="r3" />
    <Label htmlFor="r3">Compact</Label>
  </div>
</RadioGroup>
```

**Dependencies:**
*   `@radix-ui/react-radio-group`: The underlying primitive component that provides the core radio group functionality.
*   `lucide-react`: Provides the `Circle` icon for the selected radio button's indicator.
*   `@/lib/utils`: Contains the `cn` utility function for merging Tailwind CSS classes.

