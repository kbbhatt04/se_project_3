import React, { useState } from "react";

const InstructorHome = () => {

    const [courseTitle, setcourseTitle] = useState("")
    const [courseDescription, setcourseDescription] = useState("")
    const [courseLevel, setcourseLevel] = useState("")
  return (
    <div>
      <h1 className="text-3xl font-bold m-5">Add Course</h1>
      <div class="w-full max-w-screen-md m-auto text-left">
        <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <div class="mb-4">
            <label
              class="block text-gray-700 text-sm font-bold mb-2"
              for="courseTitle"
            >
              Course Title
            </label>
            <input
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="courseTitle"
              type="text"
              placeholder="Course Title"
                value={courseTitle}
                onChange={(e) => setcourseTitle(e.target.value)}
            />
          </div>

          <div class="mb-4">
            <label
              class="block text-gray-700 text-sm font-bold mb-2"
              for="courseDescription"
            >
              Course Description
            </label>
            <textarea
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
              id="courseDescription"
              type="text"
              placeholder=" Course Description"
                value={courseDescription}
                onChange={(e) => setcourseDescription(e.target.value)}
            />
          </div>
          <div className="mb-4">
          <label
              class="block text-gray-700 text-sm font-bold mb-2"
              for="courseLevel"
            >
              Course Level
            </label>
            <select class=" w-full bg-white border border-gray-400 hover:border-gray-500 px-2 py-2 rounded shadow leading-tight focus:outline-none focus:shadow-outline" 
            id="courseLevel"
            value={courseLevel}
            onChange={(e) => setcourseLevel(e.target.value)}
            >
              <option>
                Beginner
              </option>
              <option>Intermediate</option>
              <option>Advanced</option>
            </select>
          </div>
          <div class="flex items-center justify-end">
            <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
            >
              Add Course
            </button>
           
          </div>
        </form>
       
      </div>
    </div>
  );
};

export default InstructorHome;
