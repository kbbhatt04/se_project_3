import React from "react";
import { Progress } from "@material-tailwind/react";

export const Learn = () => {
  return (
    <div className="mx-10">
      <div className="flex flex-row">
        <div className="border-r-2 border-black">
          <h1 className="text-3xl font-bold mb-4 mt-10 text-left">
            CourseTitle
          </h1>

          <iframe
            width="1120"
            height="560"
            src="https://www.youtube.com/embed/xAcTmDO6NTI?si=7aXWGbJg-K75nNOI"
            title="YouTube video player"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
            referrerpolicy="strict-origin-when-cross-origin"
            allowfullscreen
            className="mr-2"
          ></iframe>
        </div>

        <div className="pl-2 flex flex-col">
        {/* progress bar */}
        <div className="mt-10 flex flex-row justify-between content-center">

          <div className="h-1 w-full mr-2 bg-neutral-200 flex mt-3">
            <div className="h-1 bg-green-300" style={{ width: "45%" }}></div>
          </div>
          <p>45%</p>
        </div>
          {/* list of chapters */}
          <div className="text-left flex justify-between border-b-2 py-2">
            <div>
              <h1>Chapter 1</h1>
              <p className="font-bold">
                Introduction to CS and Programming Using Python
              </p>
            </div>
            {/* insert a checkbox */}
            <input type="checkbox" />
          </div>
        </div>
      </div>
    </div>
  );
};
