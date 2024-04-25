import { useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { useForm } from "react-hook-form";

export default function Login() {
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const handleLogin = async (data) => {
    try {
      setIsLoading(true);
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: data.email,
          password: data.password,
        }),
      });
  
      const responseData = await response.json();
  
      if (!response.ok) {
        throw new Error(responseData.detail || "Invalid credentials");
      }
      
      localStorage.setItem("token", responseData.token);
      localStorage.setItem("role", responseData.role); 
      localStorage.setItem("user_id",responseData.user_id)
      console.log("this is role",responseData.role)
      setError(null);
      setIsLoggedIn(true);
      setIsLoading(false);
      // Redirect to the home page or any other route upon successful login
    } catch (error) {
      setError(error.message);
      setIsLoading(false);
    }
  };
  

  if (isLoggedIn) {
    return <Navigate to="/" replace={true} />;
  }

  return (
    <>
      <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-sm">
          Edu Something
        </div>

        <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
          <form
            noValidate
            onSubmit={handleSubmit(handleLogin)}
            className="space-y-6"
          >
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email
              </label>
              <input
                {...register("email", { required: true })}
                type="email"
                id="email"
                autoComplete="email"
                className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
              />
              {errors.email && <p className="text-red-500">Email is required</p>}
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <input
                {...register("password", { required: true })}
                type="password"
                id="password"
                autoComplete="current-password"
                className="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
              />
              {errors.password && <p className="text-red-500">Password is required</p>}
            </div>

            {error && <p className="text-red-500">{error}</p>}

            <div>
              <button
                type="submit"
                className="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                disabled={isLoading}
              >
                {isLoading ? "Logging in..." : "Log In"}
              </button>
            </div>
          </form>

          <p className="mt-10 text-center text-sm text-gray-500">
            Not a member?{" "}
            <Link
              to="/signup"
              className="font-semibold leading-6 text-indigo-600 hover:text-indigo-500"
            >
              Create an Account
            </Link>
          </p>
        </div>
      </div>
    </>
  );
}
