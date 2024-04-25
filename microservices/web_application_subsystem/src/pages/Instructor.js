import React from 'react'
import InstructorHome from '../feature/instructor/InstructorHome'
import Footer from '../feature/common/Footer'
import Navbar from '../feature/navbar/Navbar'
export const Instructor = () => {
  return (
    <div>
      <Navbar>
        {/* <InstructorCourse></InstructorCourse> */}
        <InstructorHome></InstructorHome>
        <Footer></Footer>
      </Navbar>

    </div>
  )
}
