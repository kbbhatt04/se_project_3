import React from "react";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  return (
    <div>
      <header className="h-24 bg-sky-400 flex flex-row justify-between items-end pl-2">
        <img src="EduMerge_transparent.png" alt="" className="h-20" />
        <ul className="flex flex-row items-end mb-3 mr-5 text-white text-lg font-semibold">
          <li className="ml-4">
            <NavLink
              exact
              to="/"
              className={({ isActive }) => (isActive ? "underline" : undefined)}
            >
              Home
            </NavLink>
          </li>
          <li className="ml-4">
            <NavLink
              exact
              to="/login"
              className={({ isActive }) => (isActive ? "underline" : undefined)}
            >
              Login
            </NavLink>
          </li>
          <li className="ml-4">Explore</li>
          <li className="ml-4">Learn</li>
          <li className="ml-4">About</li>
        </ul>
      </header>
    </div>
  );
};

export default Navbar;
