import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Link } from "react-router-dom"

const HomePage = ({ username, onLogout }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Welcome, {username}</CardTitle>
          <CardDescription>What would you like to do today?</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Link to="/questionnaire" className="block">
            <Button className="w-full">Check a Mole</Button>
          </Link>
        </CardContent>
        <CardFooter>
          <Button onClick={onLogout} className="w-full" variant="destructive">
            Logout
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}

export default HomePage
