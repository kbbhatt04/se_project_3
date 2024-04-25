import React, { useState } from "react";

const InstructorCourse = () => {
  const [chapterTitle, setChapterTitle] = useState("");
  const [chapterDescription, setChapterDescription] = useState("");
  const [lectureVideo, setLectureVideo] = useState("");
  return (
    <div>
      <div className="text-left mx-24 mt-24">
        <h1 className="text-3xl font-bold mb-8">CourseTitle</h1>

        <div className="mb-4">
          <label
            class="block text-gray-700 text-sm font-bold mb-2"
            for="courseTitle"
          >
            Course Description
          </label>
          <p className="text-justify mr-10">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptatum
            voluptate asperiores nesciunt nobis tenetur dicta eligendi esse
            dolore, quis culpa aut sequi ipsum repellendus rem reprehenderit
            explicabo sed eos? Ea!
          </p>
        </div>
        <div className="mb-4">
          <label
            class=" text-gray-700 text-sm font-bold mb-2"
            for="courseTitle"
          >
            Course Level
          </label>{" "}
          <span className="text-justify mx-2">Beginner</span>
        </div>
      </div>

      {/* adding chapter */}
      <div className=" text-left mx-24 my-10">
        <hr className="border-black mb-2" />
        <h1 className="text-3xl font-bold mb-8">Add Chapters</h1>

        <div class="mb-4">
          <label
            class="block text-gray-700 text-sm font-bold mb-2"
            for="chapterTitle"
          >
            Chapter Title
          </label>
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="chapterTitle"
            type="text"
            placeholder="Chapter Title"
            value={chapterTitle}
            onChange={(e) => setChapterTitle(e.target.value)}
          />
        </div>
        <div class="mb-4">
          <label
            class="block text-gray-700 text-sm font-bold mb-2"
            for="chapterDescription"
          >
            Chapter Description
          </label>
          <textarea
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
            id="chapterDescription"
            type="text"
            placeholder="Chapter Description"
            value={chapterDescription}
            onChange={(e) => setChapterDescription(e.target.value)}
          />
        </div>
        <div class="mb-4">
          <label
            class="block text-gray-700 text-sm font-bold mb-2"
            for="lectureVideo"
          >
            Lecture Video
          </label>
          <input
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="lectureVideo"
            type="text"
            placeholder="lecture video url"
            value={lectureVideo}
            onChange={(e) => setLectureVideo(e.target.value)}
          />
        </div>
        <div class="flex items-center justify-end">
          <button
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
            type="button"
          >
            Add Chapter
          </button>
        </div>
      </div>

        {/* chapter list */}
        <div className="text-left mx-24 my-10">
            <hr className="border-black mb-2" />
            <h1 className="text-3xl font-bold mb-8">Chapters</h1>
            <div className="flex flex-col">
                <div className="flex flex-row justify-between">
                <p className="text-xl font-semibold">Chapter 1</p>
                <button className="text-red-500">Delete</button>
                </div>
                <p className="text-lg">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptas
                quia, ipsa quidem, dolorum, quas labore quae voluptatem
                perspiciatis quos quibusdam.
                </p>
                <iframe width="560" height="315" src="https://www.youtube.com/embed/xAcTmDO6NTI?si=7aXWGbJg-K75nNOI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
                <hr className="border-black my-2" />

            </div>
            </div>
    </div>
  );
};

export default InstructorCourse;