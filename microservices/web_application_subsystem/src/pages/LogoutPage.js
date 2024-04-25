import { useEffect } from "react";
import { Navigate } from "react-router-dom";

export default function LogoutPage() {
  useEffect(() => {
    // Clear token from local storage upon component mount (logout)
    localStorage.removeItem("token");
    localStorage.removeItem("role");
  }, []);

  // Redirect to the login page after logout
  return <Navigate to="/login" replace={true} />;
}
