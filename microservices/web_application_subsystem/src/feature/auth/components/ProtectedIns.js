import { Navigate } from "react-router-dom";
function ProtectedIns({ children }) {
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");
  if (!token||(role !== "instructor" && role !== "student")) {
    return <Navigate to="/login" replace={true} />;
}
if (role !== "instructor") {
    return <Navigate to="/" replace={true} />;
    }
  return children;
}
export default ProtectedIns;
