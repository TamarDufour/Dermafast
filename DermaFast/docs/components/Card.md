# Component: Card

**File:** `DermaFast/frontend/src/components/ui/card.jsx`

**Description:**
This file exports a collection of components that are used to build card-based layouts. These components are based on `shadcn/ui` and provide a structured way to create cards with headers, titles, descriptions, content, and footers.

### `Card`
The main container for a card. It's a `div` with styling for borders, background, and shadow.

**Props:**
*   `className` (string, optional): Additional CSS classes to be applied to the card container.
*   ...props: Any other props are passed down to the underlying `div` element.

### `CardHeader`
A container for the card's header section. It provides padding and vertical spacing for its children.

**Props:**
*   `className` (string, optional): Additional CSS classes.
*   ...props: Passed to the underlying `div` element.

### `CardTitle`
A component for the card's title. It's a `div` with styling for font weight and tracking. It is typically placed inside a `CardHeader`.

**Props:**
*   `className` (string, optional): Additional CSS classes.
*   ...props: Passed to the underlying `div` element.

### `CardDescription`
A component for the card's description or subtitle. It's a `div` with styling for smaller, muted text. It is also typically placed inside a `CardHeader`.

**Props:**
*   `className` (string, optional): Additional CSS classes.
*   ...props: Passed to the underlying `div` element.

### `CardContent`
A container for the main content of the card. It provides padding.

**Props:**
*   `className` (string, optional): Additional CSS classes.
*   ...props: Passed to the underlying `div` element.

### `CardFooter`
A container for the card's footer. It is often used for action buttons or summary information. It provides padding and flexbox alignment.

**Props:**
*   `className` (string, optional): Additional CSS classes.
*   ...props: Passed to the underlying `div` element.

**Usage Example:**

```jsx
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>This is a description of the card.</CardDescription>
  </CardHeader>
  <CardContent>
    <p>This is the main content of the card.</p>
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

**Dependencies:**
*   `@/lib/utils`: Contains the `cn` utility function for merging Tailwind CSS classes.

