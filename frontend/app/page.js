"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { FaUserGraduate, FaGavel, FaBriefcase, FaStethoscope, FaCode } from "react-icons/fa";

export default function HomePage() {
  const router = useRouter();

  const roles = [
    { title: "PhD Researcher in AI", desc: "Academic researcher focusing on ML and AI", icon: <FaUserGraduate className="text-3xl text-red-600 mx-auto mb-3" /> },
    { title: "Software Engineer", desc: "Professional developer working on technical implementations", icon: <FaCode className="text-3xl text-red-600 mx-auto mb-3" /> },
    { title: "Legal Professional", desc: "Lawyer reviewing documents for compliance", icon: <FaGavel className="text-3xl text-red-600 mx-auto mb-3" /> },
    { title: "Medical Researcher", desc: "Healthcare professional analyzing literature", icon: <FaStethoscope className="text-3xl text-red-600 mx-auto mb-3" /> },
    { title: "Business Analyst", desc: "Strategic analyst evaluating trends and opportunities", icon: <FaBriefcase className="text-3xl text-red-600 mx-auto mb-3" /> },
  ];

  const [selectedRole, setSelectedRole] = useState(null);
  const totalPages = 3;
  const currentPage = 1;

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 flex flex-col items-center px-6 py-12">
      
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

      {/* Header */}
      <div className="text-center max-w-2xl mb-12">
        <h1 className="text-4xl font-extrabold text-red-600 tracking-tight">
          Adobe Document Intelligence
        </h1>
        <p className="text-gray-600 mt-4 text-lg leading-relaxed">
          
        </p>
      </div>

      {/* Select Role */}
      <div className="w-full max-w-5xl mb-16">
        <h2 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
          Select Your Role
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {roles.map((role, index) => (
            <div
              key={index}
              onClick={() => setSelectedRole(index)}
              className={`
                rounded-2xl p-6 text-center transition transform cursor-pointer
                ${selectedRole === index
                  ? "border-2 border-red-600 shadow-lg"
                  : "border border-gray-200 shadow-sm"}
                hover:border-red-600 hover:shadow-lg hover:-translate-y-1
                bg-white
              `}
            >
              {role.icon}
              <h3 className="text-lg font-semibold text-gray-900">{role.title}</h3>
              <p className="text-gray-500 text-sm mt-2">{role.desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Job Description */}
      <div className="w-full max-w-3xl mb-10">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4 text-center">
          Job Description
        </h2>
        <textarea
          placeholder="Enter your job description here..."
          className="w-full p-5 border border-gray-200 rounded-2xl shadow-sm focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500 text-gray-700 resize-none"
          rows="6"
        ></textarea>
      </div>

      {/* Next Button */}
      <div className="w-full max-w-3xl flex justify-end">
        <button
          onClick={() => router.push("/upload")} // 🚀 Go to Step 2
          className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-xl shadow-md transition"
        >
          Next →
        </button>
      </div>
    </div>
  );
}
