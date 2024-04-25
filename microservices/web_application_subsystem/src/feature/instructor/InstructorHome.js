import React, { useState, useEffect } from "react";

const InstructorHome = () => {
  const [courseTitle, setcourseTitle] = useState("");
  const [courseDescription, setcourseDescription] = useState("");
  const [courseLevel, setcourseLevel] = useState("");
  const [instructorCourses, setInstructorCourses] = useState([]);
  const userId = 1;

  useEffect(() => {
    // Fetch instructor's courses from API
    const fetchInstructorCourses = async () => {
      try {
        const response = await fetch(`http://localhost:8002/instructor_courses/${userId}`);
        if (!response.ok) {
          throw new Error("Failed to fetch instructor courses");
        }
        const data = await response.json();
        setInstructorCourses(data);
      } catch (error) {
        console.error("Error fetching instructor courses:", error);
      }
    };
    fetchInstructorCourses();
  }, [userId]);

  const addCourse = async () => {
    try {
      const courseData = {
        title: courseTitle,
        description: courseDescription,
        level: courseLevel,
        instructor: "1",
        platform: "EduMerge",
        num_enrolled_students: 0,
        num_chapters: 3,
        is_paid: false,
        price: 200.0,
        id: "",
        url: [
          "https://www.youtube.com/embed/xAcTmDO6NTI?si=7aXWGbJg-K75nNOI",
          "https://www.youtube.com/embed/xAcTmDO6NTI?si=7aXWGbJg-K75nNOI",
          "https://www.youtube.com/embed/xAcTmDO6NTI?si=7aXWGbJg-K75nNOI"
        ]
      };

      const response = await fetch("http://localhost:8002/add_course/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(courseData)
      });

      if (!response.ok) {
        throw new Error("Failed to add course");
      }

      // Handle the response if needed
      const responseData = await response.json();
      console.log(responseData); // Log the response data
      // Optionally, you can display a success message to the user
    } catch (error) {
      console.error("Error adding course:", error);
      // Optionally, you can display an error message to the user
    }
  };

  return (
    <div className="flex">
      {/* First half: Displaying instructor's courses in a grid */}
      <div className="w-1/2 p-4">
        <h1 className="text-3xl font-bold mb-5">Your Courses</h1>
        <div className="grid grid-cols-3 gap-4">
          {instructorCourses.map(course => (
            <div key={course.id} className="border p-2">
              <h2 className="font-bold">{course.title}</h2>
              <p>{course.description}</p>
              <p>Level: {course.level}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Second half: Add Course form */}
      <div className="w-1/2 p-4">
        <h1 className="text-3xl font-bold mb-5">Add Course</h1>
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
              onClick={addCourse}
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