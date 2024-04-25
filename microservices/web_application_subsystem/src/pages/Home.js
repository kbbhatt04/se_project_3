import React from 'react';
import CourseList from '../feature/course/CourseList';
import Footer from '../feature/common/Footer';
import Navbar from '../feature/navbar/Navbar';

export const Home = () => {
  return (
    <div style={{ padding: '0 20px', paddingBottom: '20px' }}> {/* Add padding to the sides */}
      <Navbar></Navbar>
      <div style={{ marginBottom: '20px' }}> {/* Add margin bottom to create space between navbar and course list */}
        <CourseList></CourseList>
      </div>
      <Footer></Footer>
    </div>
  );
};
