import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom

const CourseList = () => {
  const [courses, setCourses] = useState([]);
  const [selectedCourseId, setSelectedCourseId] = useState(null); // Track selected course ID

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await fetch('http://localhost:8001/courses');
        if (!response.ok) {
          throw new Error('Failed to fetch courses');
        }
        const data = await response.json();
        setCourses(data);
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    };

    fetchCourses();
  }, []);

  const handleCourseSelect = (courseId) => {
    setSelectedCourseId(courseId); // Update selected course ID on selection
  };

  return (
    <div>
      <div style={{ marginBottom: '20px' }}> {/* Add margin bottom to create space between heading and course list */}
        <h1 style={{ textAlign: 'center',fontSize: '34px'  }}>Course List</h1> {/* Center the heading */}
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
        {courses.map((course) => (
          <div key={course.id} style={{ border: '1px solid #ccc', padding: '10px' }}>
            <Link to={`/courses/${course.id}`} onClick={() => handleCourseSelect(course.id)} style={{ textDecoration: 'none', color: '#333' }}>
              <h3>{course.title}</h3>
              <p><strong>Description:</strong> {course.description}</p>
              <p><strong>Platform:</strong> {course.platform}</p>
              <p><strong>Level:</strong> {course.level}</p>
              <p><strong>Price:</strong> {course.is_paid ? `$${course.price}` : 'Free'}</p>
            </Link>
          </div>
        ))}
      </div>

      {selectedCourseId && (
        <div style={{ marginTop: '30px' }}>
          <h2>Selected Course Details</h2>
          <p><strong>Title:</strong> {courses.find((c) => c.id === selectedCourseId).title}</p>
          <p><strong>Description:</strong> {courses.find((c) => c.id === selectedCourseId).description}</p>
          <p><strong>Platform:</strong> {courses.find((c) => c.id === selectedCourseId).platform}</p>
          <p><strong>Level:</strong> {courses.find((c) => c.id === selectedCourseId).level}</p>
          <p><strong>Price:</strong> {courses.find((c) => c.id === selectedCourseId).is_paid ? `$${courses.find((c) => c.id === selectedCourseId).price}` : 'Free'}</p>
        </div>
      )}
    </div>
  );
};

export default CourseList;
