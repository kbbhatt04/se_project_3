import React, { useState, useEffect } from "react";
import { Progress } from "@material-tailwind/react";
import { useParams } from 'react-router-dom';

export const Learn = () => {
  const [progress, setProgress] = useState(0);
  const [chapters, setChapters] = useState([]);
  // const courseId = "66221759ceea51e8815a2b23";
  const { courseId } = useParams();
  const userId = localStorage.getItem("user_id");
  useEffect(() => {
    fetchProgress();
    fetchChapters();
  }, []);

  useEffect(() => {
    console.log(chapters);
  }, [chapters]);
  
  useEffect(() => {
    console.log(progress);
  }, [progress]);
  const fetchProgress = async () => {
    try {
      const response = await fetch(`http://localhost:8004/track_progress?course_id=${courseId}&user_id=${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error('Failed to fetch progress');
      }
      const data = await response.json();
      console.log(data.completion_percentage)
      setProgress(data.completion_percentage);
      console.log(progress)
    } catch (error) {
      console.error("Error fetching progress:", error);
    }
  };

  const fetchChapters = async () => {
    try {
      const response = await fetch(`http://localhost:8001/courses/${courseId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch chapters');
      }
      const data = await response.json();
      console.log(data)
      const urls = data.url || []; // Assuming urls is an array of URLs fetched from data
      const newChapters = urls.map((url, index) => ({
        id: index + 1,
        url,
        learned: false
      }));
      // setChapters(newChapters);
      const learnedChaptersResponse = await fetch(`http://localhost:8004/get_chapter_progress/?course_id=${courseId}&user_id=${userId}`,{
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        });
      
      if (!learnedChaptersResponse.ok) {
        throw new Error('Failed to fetch learned chapters');
      }
      const learnedChaptersData = await learnedChaptersResponse.json();
      
      const progress_details=learnedChaptersData.progress_details
      console.log(progress_details)
      Object.keys(progress_details).forEach(chapterId => {
        const index = parseInt(chapterId) - 1;
        if (index >= 0 && index < newChapters.length) {
          newChapters[index].learned = progress_details[chapterId];
        }
      });
      setChapters(newChapters);
      console.log("chapters",chapters)
    } catch (error) {
      console.error("Error fetching chapters:", error);
    }
  };

  const handleChapterToggle = async (chapterId, isChecked) => {
    try {
      const updatedChapters = chapters.map((chapter) =>
        chapter.id === chapterId ? { ...chapter, learned: isChecked } : chapter
      );
      setChapters(updatedChapters);
  
      if (isChecked) {
        const response = await fetch(
            `http://localhost:8004/add_to_progress?course_id=${courseId}&user_id=${userId}&chapter=${chapterId}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        if (!response.ok) {
          throw new Error("Failed to add chapter to progress");
        }
        console.log("Chapter added to progress:", chapterId);
      } else {
          const response = await fetch(
            `http://localhost:8004/remove_from_progress?course_id=${courseId}&user_id=${userId}&chapter=${chapterId}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );
        if (!response.ok) {
          throw new Error("Failed to remove chapter from progress");
        }
        console.log("Chapter removed from progress:", chapterId);
      }
      fetchProgress();
    } catch (error) {
      console.error("Error toggling chapter:", error);
    }
  };
  const downloadCertificate = async () => {
    try {
      const certificateResponse = await fetch(`http://localhost:8004/download_certificate?user_id=${userId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!certificateResponse.ok) {
        throw new Error('Failed to download certificate');
      }

      // Assuming the certificate is a PDF file
      const blob = await certificateResponse.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'certificate.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (error) {
      console.error('Error downloading certificate:', error);
    }
  };
  

  return (
    <div className="mx-10">
      <div className="flex flex-col gap-6">
       
        <div className="mt-10 flex flex-row justify-between content-center">
          <div className="h-4 w-full mr-2 bg-neutral-200 flex mt-3">
          <h2 className="text-s font-semibold mr-2">Progress:</h2>
          <br></br>
          <div className="h-full bg-green-300" style={{ width:`${progress}%` }}></div>
        </div>
        {progress === 100 && (
          <button onClick={downloadCertificate} className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Download Certificate
          </button>
        )}
        <p>{progress}%</p>
        </div>

        {/* Progress table */}
        <div className="w-full overflow-hidden rounded-lg shadow-md">
          <table className="w-full bg-white">
            <thead>
              <tr>
                <th className="px-4 py-2">Chapter</th>
                <th className="px-4 py-2">Video</th>
                <th className="px-4 py-2">Checkbox</th>
              </tr>
            </thead>
            <tbody>
              {chapters.map((chapter) => (
                <tr key={chapter.id}>
                  <td className="border px-4 py-2">{chapter.id}</td>
                  <td className="border px-4 py-2">
                    <iframe src={chapter.url} title={`Chapter ${chapter.id}`} className="mr-2" width="400" height="200"></iframe>
                  </td>
                  <td className="border px-4 py-2">
                    <input
                      type="checkbox"
                      checked={chapter.learned}
                      onChange={(e) =>
                        handleChapterToggle(chapter.id, e.target.checked)
                      }
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};