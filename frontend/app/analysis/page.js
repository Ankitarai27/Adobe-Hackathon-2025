"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { FaLightbulb, FaHeadphones, FaList } from "react-icons/fa";

export default function AnalysisPage() {
  const [activeTab, setActiveTab] = useState("insights");
  const [showModal, setShowModal] = useState(false);
  const router = useRouter();

  const highlights = [
    { title: "Introduction", snippet: "Covers the basics of AI.", page: 1 },
    { title: "Legal Implications", snippet: "Compliance challenges.", page: 5 },
    { title: "Methodology", snippet: "Approach to data collection.", page: 6 },
  ];

  const insights = {
    insights: [
      "This research connects with ethical AI trends.",
      "Business strategy overlaps with uploaded docs.",
    ],
    contradictions: ["Conflicting timelines in compliance sections."],
    inspirations: ["Link methodology with your medical dataset analysis."],
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Top Bar */}
      <div className="flex items-center justify-between px-8 py-4 bg-white shadow-sm border-b">
        <h1 className="text-xl font-bold text-red-600">
          Adobe Document Intelligence
        </h1>
        <div className="text-gray-700 font-medium">
          Legal Professional • Compliance Review
        </div>
        <div className="flex items-center gap-4">
          {/* Podcast Mode */}
          <button className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition">
            <FaHeadphones /> Podcast Mode
          </button>

          {/* Insights Button */}
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center gap-2 px-4 py-2 bg-yellow-100 text-yellow-800 rounded-lg hover:bg-yellow-200 transition shadow-md"
          >
            <FaLightbulb className="text-yellow-500 animate-pulse" /> Insights
          </button>
        </div>
      </div>

      {/* Main Layout */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-72 bg-white border-r px-5 py-6 overflow-y-auto hidden md:block">
          <h2 className="font-semibold mb-4 flex items-center gap-2 text-gray-800">
            <FaList /> Document Outline
          </h2>
          <ul className="space-y-3 text-gray-700">
            <li className="cursor-pointer hover:text-red-600">
              Introduction (p.1)
            </li>
            <li className="cursor-pointer hover:text-red-600">
              Background & Motivation (p.2)
            </li>
            <li className="cursor-pointer hover:text-red-600">
              Problem Statement (p.4)
            </li>
            <li className="cursor-pointer hover:text-red-600">
              Methodology (p.6)
            </li>
          </ul>
        </aside>

        {/* PDF Viewer + Panels */}
        <main className="flex-1 p-8 overflow-y-auto">
          {/* Back Button */}
          <div className="mb-6">
            <button
              onClick={() => router.push("/upload")}
              className="px-6 py-2 rounded-lg bg-gray-200 text-gray-800 font-semibold hover:bg-gray-300 transition"
            >
              ← Back to Upload
            </button>
          </div>

          {/* PDF Viewer */}
          <div className="h-[500px] bg-gray-200 rounded-xl shadow-inner flex items-center justify-center text-gray-600 mb-10">
            [ PDF Viewer Here ]
          </div>

          {/* Highlights */}
          <section className="mb-10">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800">
              Relevant Highlights
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {highlights.map((h, i) => (
                <div
                  key={i}
                  className="p-5 bg-white border rounded-xl shadow-sm hover:shadow-md transition flex flex-col justify-between"
                >
                  <div>
                    <h3 className="font-semibold text-gray-900">
                      {h.title} (p.{h.page})
                    </h3>
                    <p className="text-gray-600 text-sm mt-2">{h.snippet}</p>
                  </div>
                  <button className="mt-3 text-sm text-red-600 hover:underline self-start">
                    Jump →
                  </button>
                </div>
              ))}
            </div>
          </section>
        </main>
      </div>

      {/* Insights Modal */}
      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
          <div className="bg-white rounded-2xl shadow-lg w-full max-w-2xl p-6 relative">
            {/* Close Button */}
            <button
              onClick={() => setShowModal(false)}
              className="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>

            <h2 className="text-2xl font-semibold mb-4 text-gray-800 flex items-center gap-2">
              <FaLightbulb className="text-yellow-500" /> AI-Generated Insights
            </h2>

            {/* Tabs */}
            <div className="flex gap-6 border-b mb-4">
              {["insights", "contradictions", "inspirations"].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`pb-2 capitalize font-medium transition ${
                    activeTab === tab
                      ? "border-b-2 border-yellow-500 text-yellow-600"
                      : "text-gray-500 hover:text-gray-700"
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <ul className="space-y-3 text-gray-700">
              {insights[activeTab].map((item, i) => (
                <li key={i}>• {item}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
