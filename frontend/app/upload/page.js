"use client";
import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { FaUpload, FaTimes, FaHistory } from "react-icons/fa";

export default function UploadPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const role = searchParams.get("role");
  const job = searchParams.get("job");

  const [files, setFiles] = useState([]);
  const [uploaded, setUploaded] = useState([]);
  const totalPages = 3;
  const currentPage = 2;

  const BASE_URL = process.env.NEXT_PUBLIC_API_BASE;

  useEffect(() => {
    fetch(`${BASE_URL}/uploads`)
      .then((res) => res.json())
      .then((data) => {
        console.log("Uploads from backend:", data);
        setUploaded(data || []);
      })
      .catch((err) => console.error("Error fetching uploads:", err));
  }, [BASE_URL]);

  const handleFileChange = async (e) => {
    const newFiles = Array.from(e.target.files);
    setFiles((prev) => [...prev, ...newFiles]);

    for (const file of newFiles) {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("role", role);
      formData.append("jobdesc", job);

      try {
        const res = await fetch(`${BASE_URL}/upload`, {
          method: "POST",
          body: formData,
        });

        if (!res.ok) {
          const txt = await res.text();
          console.error("Upload failed:", txt);
          continue;
        }

        const data = await res.json();
        console.log("Upload response:", data);

        // ✅ Store PDF URL for Analysis page
        const fileUrl = `${BASE_URL}/pdfs/${data.filename}`;
        sessionStorage.setItem("analysisMainFile", fileUrl);

        // Refresh uploaded list
        const refreshed = await fetch(`${BASE_URL}/uploads`);
        const uploads = await refreshed.json();
        setUploaded(uploads || []);
      } catch (err) {
        console.error("Upload failed:", err);
      }
    }
  };

  const removeFile = (index) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center px-6 py-12">
      {/* Stepper */}
      <div className="flex items-center mb-10">
        {[1, 2, 3].map((page, index) => (
          <div key={page} className="flex items-center">
            <div
              className={`w-10 h-10 flex items-center justify-center rounded-full font-semibold z-10
                ${page < currentPage ? "bg-green-600 text-white" : ""}
                ${page === currentPage ? "bg-red-600 text-white" : ""}
                ${page > currentPage ? "bg-gray-300 text-gray-700" : ""}
              `}
            >
              {page}
            </div>
            {index < totalPages - 1 && (
              <div
                className={`w-16 h-1 mx-2 ${
                  page < currentPage ? "bg-green-600" : "bg-gray-300"
                }`}
              ></div>
            )}
          </div>
        ))}
      </div>

      {/* Title */}
      <div className="text-center max-w-2xl mb-12">
        <h1 className="text-3xl font-bold text-gray-800">Upload Your Documents</h1>
        <p className="text-gray-500 mt-3 text-lg">
          Upload PDFs for analysis based on your persona{" "}
          <span className="font-semibold">{role}</span> and job{" "}
          <span className="font-semibold">{job}</span>.
        </p>
      </div>

      {/* Upload Box */}
      <label
        htmlFor="file-upload"
        className="w-full max-w-2xl border-2 border-dashed border-gray-300 rounded-2xl p-12 flex flex-col items-center justify-center cursor-pointer bg-gray-50 hover:bg-gray-100 transition"
      >
        <FaUpload className="text-4xl text-red-600 mb-4" />
        <span className="text-lg font-medium text-gray-700">
          Drag & drop your PDFs here
        </span>
        <span className="text-sm text-gray-500 mt-1">or click to browse files</span>
        <input
          id="file-upload"
          type="file"
          accept="application/pdf"
          multiple
          className="hidden"
          onChange={handleFileChange}
        />
      </label>

      {/* Current File List */}
      {files.length > 0 && (
        <div className="mt-6 w-full max-w-2xl bg-gray-50 border border-gray-200 rounded-xl p-4 shadow-sm">
          <h3 className="text-md font-semibold mb-3 text-gray-700">Currently Selected:</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {files.map((file, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between bg-white px-3 py-2 rounded-lg shadow-sm border border-gray-200"
              >
                <span className="text-gray-700 truncate max-w-[140px]">
                  {file.name}
                </span>
                <button
                  onClick={() => removeFile(idx)}
                  className="text-red-500 hover:text-red-700 transition"
                  title="Remove file"
                >
                  <FaTimes />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Uploaded Files */}
      {uploaded.length > 0 && (
        <div className="mt-8 w-full max-w-2xl bg-white border border-gray-200 rounded-xl p-4 shadow-sm">
          <h3 className="flex items-center gap-2 text-md font-semibold text-gray-700 mb-3">
            <FaHistory className="text-gray-600" /> Uploaded Files
          </h3>
          <ul className="space-y-2 text-gray-700">
            {uploaded.map((file, idx) => (
              <li key={idx} className="px-3 py-2 border rounded-lg bg-gray-50">
                {file.filename}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Buttons */}
      <div className="mt-12 flex w-full max-w-2xl justify-between">
        <button
          onClick={() => router.push(`/`)}
          className="px-6 py-3 rounded-xl bg-gray-200 text-gray-800 font-semibold hover:bg-gray-300 transition"
        >
          ← Back to Persona
        </button>
        <button
          onClick={() =>
            router.push(`/analysis?role=${role}&job=${job}`)
          }
          disabled={uploaded.length === 0}
          className={`px-6 py-3 rounded-xl font-semibold shadow-md transition
            ${uploaded.length === 0
              ? "bg-gray-300 text-gray-500 cursor-not-allowed"
              : "bg-red-600 text-white hover:bg-red-700"}
          `}
        >
          Start Analysis →
        </button>
      </div>
    </div>
  );
}
