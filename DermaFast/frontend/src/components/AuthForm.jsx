import { useState } from 'react'
import { Button } from "@/components/ui/button"

const AuthForm = ({ onLogin }) => {
  const [nationalId, setNationalId] = useState('')
  const [password, setPassword] = useState('')
  const [isLoginMode, setIsLoginMode] = useState(true)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('') // 'success' or 'error'

  const API_BASE_URL = 'http://localhost:8000'

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const endpoint = isLoginMode ? '/api/login' : '/api/register'
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          national_id: nationalId,
          password: password,
        }),
      })

      const data = await response.json()

      if (response.ok) {
        setMessage(data.message)
        setMessageType('success')
        
        if (isLoginMode) {
          // Call the login callback with the national ID
          onLogin(nationalId)
        } else {
          // Clear form on successful registration and switch to login mode
          setNationalId('')
          setPassword('')
          setIsLoginMode(true)
        }
      } else {
        setMessage(data.detail || 'An error occurred')
        setMessageType('error')
      }
    } catch (error) {
      setMessage('Network error. Please check if the backend is running.')
      setMessageType('error')
    } finally {
      setLoading(false)
    }
  }

  const toggleMode = () => {
    setIsLoginMode(!isLoginMode)
    setMessage('')
    setNationalId('')
    setPassword('')
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {isLoginMode ? 'Sign in to DermaFast' : 'Create DermaFast Account'}
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            {isLoginMode ? "Don't have an account?" : 'Already have an account?'}{' '}
            <button
              type="button"
              onClick={toggleMode}
              className="font-medium text-indigo-600 hover:text-indigo-500 focus:outline-none focus:underline transition ease-in-out duration-150"
            >
              {isLoginMode ? 'Sign up' : 'Sign in'}
            </button>
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="national-id" className="sr-only">
                National ID
              </label>
              <input
                id="national-id"
                name="national-id"
                type="text"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="National ID"
                value={nationalId}
                onChange={(e) => setNationalId(e.target.value)}
                disabled={loading}
              />
            </div>
            <div>
              <label htmlFor="password" className="sr-only">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
              />
            </div>
          </div>

          {message && (
            <div className={`text-sm text-center ${
              messageType === 'error' 
                ? 'text-red-600 bg-red-50 border border-red-200 rounded-md p-3' 
                : 'text-green-600 bg-green-50 border border-green-200 rounded-md p-3'
            }`}>
              {message}
            </div>
          )}

          <div>
            <Button
              type="submit"
              disabled={loading || !nationalId || !password}
              className="w-full"
            >
              {loading ? (
                <div className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {isLoginMode ? 'Signing in...' : 'Creating account...'}
                </div>
              ) : (
                isLoginMode ? 'Sign in' : 'Create Account'
              )}
            </Button>
          </div>

          <div className="text-center">
            <p className="text-xs text-gray-500">
              {isLoginMode 
                ? 'Enter your national ID and password to access your account'
                : 'Create a new account with your national ID and password'
              }
            </p>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AuthForm
