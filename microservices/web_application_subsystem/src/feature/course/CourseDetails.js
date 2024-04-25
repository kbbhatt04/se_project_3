import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'; // Import useParams for accessing route parameters

const CourseDetails = () => {
  const { courseId } = useParams(); // Get the course ID from the route path

  // Fetch course details based on courseId (implementation example)
  const [courseDetails, setCourseDetails] = useState(null);
  useEffect(() => {
    const fetchCourseDetails = async () => {
      try {
        const response = await fetch(`http://localhost:8001/courses/${courseId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch course details');
        }
        const data = await response.json();
        setCourseDetails(data);
      } catch (error) {
        console.error('Error fetching course details:', error);
      }
    };

    fetchCourseDetails();
  }, [courseId]);

  return (
    <div>
      {courseDetails ? (
        <>
          <h1>Course Details</h1>
          <strong>Title:</strong> {courseDetails.title}<br />
          <strong>Description:</strong> {courseDetails.description}<br />
          {/* Display other course details here */}
        </>
      ) : (
        <p>Loading course details...</p>
      )}
    </div>
  );
};

export default CourseDetails;