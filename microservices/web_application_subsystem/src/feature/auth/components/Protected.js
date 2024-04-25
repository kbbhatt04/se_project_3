import { Navigate } from "react-router-dom";

function Protected({ children }) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");
  console.log("user data",token,role)

    if (!token||(role !== "instructor" && role !== "student")) {
        return <Navigate to="/login" replace={true} />;
    }
    if (role !== "student") {
    return <Navigate to="/instructor" replace={true} />;
    }
    // if (role !== "student") {
    //     return <Navigate to="/" replace={true} />;
    // }
  return children;
}
export default Protected;
