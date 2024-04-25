import { useState, useEffect } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";

export default function Signup() {
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [redirect, setRedirect] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm();

  useEffect(() => {
    if (redirect) {
      const timer = setTimeout(() => {
        setRedirect(false);
      }, 2000);

      return () => clearTimeout(timer);
    }
  }, [redirect]);

const onSubmit = async (data) => {
  try {
    setIsLoading(true);
    const response = await fetch("http://localhost:8000/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: data.email,
        role: data.role,
        password: data.password,
      }),
    });

    const responseData = await response.json();
    if (!response.ok) {
      if (response.status === 409) {
        // Email already exists
        setError("Email already exists");
      } else {
        throw new Error(responseData.detail || "Something went wrong");
      }
    } else {
      setSuccessMessage("User signed up successfully");
      setError(null);
      setIsLoading(false);
      setRedirect(true); // Redirect after 2 seconds
    }
  } catch (error) {
    setError(error.message);
    setIsLoading(false);
  }
};

  if (redirect) {
    return (
      <div>
        <p>Singup successfully Redirecting to login page...</p>
      </div>
    );
  }

  return (
    <>
      <div className="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          {/* Your logo and title here */}
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Create your account
          </h2>
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Email address
                </label>
                <div className="mt-1">
                  <input
                    {...register("email", {
                      required: "Email is required",
                      pattern: {
                        value: /\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b/gi,
                        message: "Invalid email format",
                      },
                    })}
                    id="email"
                    type="email"
                    autoComplete="email"
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="Email address"
                  />
                  {errors.email && (
                    <p className="mt-2 text-sm text-red-500">{errors.email.message}</p>
                  )}
                </div>
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                  Password
                </label>
                <div className="mt-1">
                  <input
                    {...register("password", {
                      required: "Password is required",
                      minLength: {
                        value: 8,
                        message: "Password must have at least 8 characters",
                      },
                    })}
                    id="password"
                    type="password"
                    autoComplete="new-password"
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="Password"
                  />
                  {errors.password && (
                    <p className="mt-2 text-sm text-red-500">{errors.password.message}</p>
                  )}
                </div>
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                  Confirm password
                </label>
                <div className="mt-1">
                  <input
                    {...register("confirmPassword", {
                      validate: (value) =>
                        value === watch("password") || "The passwords do not match",
                    })}
                    id="confirmPassword"
                    type="password"
                    autoComplete="new-password"
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    placeholder="Confirm password"
                  />
                  {errors.confirmPassword && (
                    <p className="mt-2 text-sm text-red-500">{errors.confirmPassword.message}</p>
                  )}
                </div>
              </div>

              <div>
                <label htmlFor="role" className="block text-sm font-medium text-gray-700">
                  Role
                </label>
                <div className="mt-1">
                  <select
                    {...register("role", { required: "Role is required" })}
                    id="role"
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    defaultValue=""
                  >
                    <option value="" disabled hidden>Select Role</option>
                    <option value="admin">Admin</option>
                    <option value="student">Student</option>
                    <option value="instructor">Instructor</option>
                  </select>
                  {errors.role && (
                    <p className="mt-2 text-sm text-red-500">{errors.role.message}</p>
                  )}
                </div>
              </div>

              <div>
                <button
                  type="submit"
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  {isLoading ? "Creating Account..." : "Sign up"}
                </button>
              </div>
            </form>

            {error && (
              <div className="mt-6">
                <p className="text-red-500">{error}</p>
              </div>
            )}

            <div className="mt-6">
              <p className="mt-2 text-center text-sm text-gray-600">
                Already have an account?{" "}
                <Link to="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
                  Log in
                </Link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
