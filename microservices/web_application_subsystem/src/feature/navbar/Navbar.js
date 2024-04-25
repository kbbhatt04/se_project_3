import { Fragment, useState } from 'react'; // Import useState hook
import { Disclosure } from '@headlessui/react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
// import { selectUserInfo } from '../user/userSlice';

function NavBar({ children }) {
  // const userInfo = useSelector(selectUserInfo);
  const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem('userInfo') !== null); // Initialize isLoggedIn state based on localStorage
  return (
    <>
      { (
        <div className="min-h-full">
          <header className="bg-white shadow">
            <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center"> {/* Added flex and justify-between */}
              <div>
                <Link to="/" className="text-3xl font-bold tracking-tight text-gray-900">
                  EduMerge - Online Courses
                </Link>
              </div>
              <nav className="flex justify-center"> {/* Removed mt-4 */}
                <Link
                  to="/"
                  className="text-gray-500 hover:text-gray-900 mx-4"
                >
                  Home
                </Link>
                <Link
                  to="/instructor"
                  className="text-gray-500 hover:text-gray-900 mx-4"
                >
                  Instructor
                </Link>
                <Link
                  to="/logout"
                  className="text-gray-500 hover:text-gray-900 mx-4"
                >
                  Logout
                </Link>
              </nav>
            </div>
          </header>
          <main>
            <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
              {children}
            </div>
          </main>
        </div>
      )}
    </>
  );
}

export default NavBar;
