import { createBrowserRouter,RouterProvider} from "react-router-dom";
import "./App.css";
import { Home } from "./pages/Home";
import LoginPage from "./pages/LoginPage";
// import LearnerCourses from "./components/LearnerCourses";
import PageNotFound from "./pages/404";
import { CourseDetailPage } from "./pages/CourseDetailPage";
import {Learn} from "./pages/Learn"
import { Instructor } from "./pages/Instructor";
import SignupPage from "./pages/SignUpPage";
import LogoutPage from "./pages/LogoutPage";
import Protected from "./feature/auth/components/Protected";
import ProtectedIns from "./feature/auth/components/ProtectedIns";
const router = createBrowserRouter([
  {
    path: "/",
    element: <Protected><Home></Home>,</Protected>
  },
  {
    path: "/courses/:courseId",
    element:<Protected><CourseDetailPage></CourseDetailPage></Protected>
  },
  {
    path: "/login",
    element: <LoginPage></LoginPage>
  },
  {
    path: "/logout",
    element:<LogoutPage></LogoutPage>
  },
  {
    path: "/signup",
    element: <SignupPage></SignupPage>
  },
  {
    path: "/learn",
    element: <Protected><Learn></Learn></Protected>
  },
  {
    path: "/instructor",
    element:<ProtectedIns><Instructor></Instructor></ProtectedIns>
  },
  {
    path: "*",
    element: <PageNotFound></PageNotFound>,
  },
]);
function App() {
  return (
    <div className="App">
        <RouterProvider router={router}></RouterProvider>
    </div>
  );
}
export default App;
