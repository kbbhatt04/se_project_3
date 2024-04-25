
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

const CourseReviews = () => {
  const { courseId } = useParams();
  const [reviews, setReviews] = useState([]);
  const [averageRating, setAverageRating] = useState(0);
  const [newReview, setNewReview] = useState({
    user_id: '1',
    course_id: courseId,
    rating: 3,
    review: ''
  });
  const [reviewAdded, setReviewAdded] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [reviewsPerPage] = useState(5); // Number of reviews per page

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const response = await fetch(`http://localhost:8003/get_reviews/${courseId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch reviews');
        }
        const data = await response.json();
        const [reviewsList, avgRating] = data;
        setReviews(reviewsList);
        setAverageRating(avgRating);
      } catch (error) {
        console.error('Error fetching reviews:', error);
      }
    };
  
    fetchReviews();
  }, [courseId, newReview, reviewAdded]); // Include reviewAdded in the dependency array
  
  const handleAddReview = async () => {
    console.log('Adding review...');
    try {
      const response = await fetch('http://localhost:8003/add_review', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newReview)
      });
  
      if (!response.ok) {
        throw new Error('Failed to add review');
      }
  
      const data = await response.json();
      
      // Check if the response contains the message "Review added successfully"
      if (data.message === "Review added successfully") {
        console.log('Review added successfully');
        setReviewAdded(true); // Trigger refetch of reviews
  
        // Reset the new review form
        setNewReview({
          user_id: '1',
          course_id: courseId,
          rating: 0,
          review: ''
        });
      } else {
        throw new Error('Failed to add review: ' + data.message);
      }
    } catch (error) {
      console.error('Error adding review:', error);
    }
  };
  
  const handleChange = (event) => {
    const { name, value } = event.target;
    
    if (name === 'rating') {
      const rating = parseInt(value, 10);
      if (!isNaN(rating) && rating >= 1 && rating <= 5) {
        setNewReview({
          ...newReview,
          [name]: rating
        });
      }
      else {
        setNewReview({
          ...newReview,
          [name]: 1
        });
      }
    } else {
      setNewReview({
        ...newReview,
        [name]: value
      });
    }
  };
  

  // Logic for pagination
  const indexOfLastReview = currentPage * reviewsPerPage;
  const indexOfFirstReview = indexOfLastReview - reviewsPerPage;
  const currentReviews = reviews.slice(indexOfFirstReview, indexOfLastReview);

  // Change page
  const paginate = pageNumber => setCurrentPage(pageNumber);

  return (
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px', backgroundColor: '#f9f9f9' }}>
      <h1 style={{ fontSize: '24px', marginBottom: '10px' }}>Reviews for Course</h1>
      <div style={{ fontSize: '18px', marginBottom: '10px' }}>Average Rating: {averageRating}</div>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {currentReviews.map((review, index) => (
          <li key={index} style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
            <p style={{ fontWeight: 'bold', marginBottom: '5px' }}>User ID: {review.user_id}</p>
            <p>Rating: {review.rating}</p>
            <p>Review: {review.review}</p>
          </li>
        ))}
      </ul>
      <div>
        <h2 style={{ fontSize: '20px', marginBottom: '10px' }}>Add Review</h2>
        <input
          type="number"
          name="rating"
          value={newReview.rating}
          onChange={handleChange}
          placeholder="Rating"
          style={{ width: '100%', marginBottom: '10px', padding: '5px' }}
        />
        <textarea
          name="review"
          value={newReview.review}
          onChange={handleChange}
          placeholder="Review"
          style={{ width: '100%', marginBottom: '10px', padding: '5px' }}
        />
        <button
          onClick={handleAddReview}
          style={{
            backgroundColor: '#007bff',
            color: '#fff',
            border: 'none',
            padding: '10px 20px',
            cursor: 'pointer',
            fontSize: '16px'
          }}
        >
          Add Review
        </button>
      </div>
      {/* Pagination */}
      <div style={{ marginTop: '20px' }}>
        {Array.from({ length: Math.ceil(reviews.length / reviewsPerPage) }).map((_, index) => (
          <button key={index} onClick={() => paginate(index + 1)} style={{ marginRight: '5px' }}>
            {index + 1}
          </button>
        ))}
      </div>
    </div>
  );
};

export default CourseReviews;
