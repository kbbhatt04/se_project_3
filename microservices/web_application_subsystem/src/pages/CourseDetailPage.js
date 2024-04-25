import React from 'react';
import Footer from '../feature/common/Footer';
import Navbar from '../feature/navbar/Navbar';
import CourseDetails from '../feature/course/CourseDetails';
import CourseReviews from '../feature/course/CourseReviews';
import { Learn } from './Learn';

export const CourseDetailPage = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar />
      <div style={{ flex: 1, padding: '20px' }}>
        <CourseDetails></CourseDetails>
        <Learn />
        <CourseReviews></CourseReviews>
      </div>
      <Footer />
    </div>
  );
};
