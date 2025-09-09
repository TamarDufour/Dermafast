# Component: Button

**File:** `DermaFast/frontend/src/components/ui/button.jsx`

**Description:**
A versatile and customizable button component, built using `class-variance-authority` (CVA) for different styles and sizes. This component is based on the `shadcn/ui` button. It can be rendered as a standard HTML `<button>` or as a different component (e.g., a link) using the `asChild` prop.

**Props:**
*   `className` (string, optional): Additional CSS classes to be applied to the button.
*   `variant` (string, optional): The visual style of the button.
    *   `default`: The standard, primary button style.
    *   `destructive`: A button style used for actions that have a destructive consequence (e.g., deleting).
    *   `outline`: A button with a border and a transparent background.
    *   `secondary`: A secondary button style, less prominent than the default.
    *   `ghost`: A button with no background or border, often used for subtle actions.
    *   `link`: A button that looks like a hyperlink.
    *   Default value: `'default'`.
*   `size` (string, optional): The size of the button.
    *   `default`: The standard button size.
    *   `sm`: A smaller button.
    *   `lg`: A larger button.
    *   `icon`: A square button, typically used for icons.
    *   Default value: `'default'`.
*   `asChild` (boolean, optional): If `true`, the component will render its child component and pass the button props to it, instead of rendering a `<button>` element. This is useful for wrapping other components, like a `react-router-dom` `<Link>`, while maintaining the button's styling. Defaults to `false`.
*   ...props: Any other props are passed down to the underlying `<button>` or child component. For example, `onClick`, `disabled`, `type`, etc.

**Usage:**

**Standard Button:**
```jsx
<Button>Click me</Button>
```

**Destructive Button:**
```jsx
<Button variant="destructive">Delete</Button>
```

**Icon Button:**
```jsx
<Button variant="outline" size="icon">
  <ChevronRightIcon className="h-4 w-4" />
</Button>
```

**As a Link:**
```jsx
import { Link } from "react-router-dom";

<Button asChild>
  <Link to="/login">Login</Link>
</Button>
```

**Dependencies:**
*   `@radix-ui/react-slot`: Used to pass props to a child component when `asChild` is `true`.
*   `class-variance-authority`: For creating variant classes for the button.
*   `@/lib/utils`: Contains the `cn` utility function for merging Tailwind CSS classes.



