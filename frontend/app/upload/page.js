"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { FaUpload, FaTimes } from "react-icons/fa";

export default function UploadPage() {
  const router = useRouter();
  const [files, setFiles] = useState([]);
  const totalPages = 3;
  const currentPage = 2; // Upload step

  const handleFileChange = (e) => {
    setFiles((prev) => [...prev, ...Array.from(e.target.files)]);
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
            {/* Circle */}
            <div
              className={`w-10 h-10 flex items-center justify-center rounded-full font-semibold z-10
                ${page < currentPage ? "bg-green-600 text-white" : ""}
                ${page === currentPage ? "bg-red-600 text-white" : ""}
                ${page > currentPage ? "bg-gray-300 text-gray-700" : ""}
              `}
            >
              {page}
            </div>

            {/* Short Line */}
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
          Upload PDFs for analysis based on your selected persona.
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

      {/* File List */}
      {files.length > 0 && (
        <div className="mt-6 w-full max-w-2xl bg-gray-50 border border-gray-200 rounded-xl p-4 shadow-sm">
          <h3 className="text-md font-semibold mb-3 text-gray-700">Uploaded Files:</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {files.map((file, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between bg-white px-3 py-2 rounded-lg shadow-sm border border-gray-200"
              >
                <span className="text-gray-700 truncate max-w-[140px]">{file.name}</span>
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

      {/* Buttons */}
      <div className="mt-12 flex w-full max-w-2xl justify-between">
        <button
          onClick={() => router.push("/")}
          className="px-6 py-3 rounded-xl bg-gray-200 text-gray-800 font-semibold hover:bg-gray-300 transition"
        >
          ← Back to Persona
        </button>
        <button
          onClick={() => router.push("/analysis")}
          disabled={files.length === 0}
          className={`px-6 py-3 rounded-xl font-semibold shadow-md transition
            ${files.length === 0
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
