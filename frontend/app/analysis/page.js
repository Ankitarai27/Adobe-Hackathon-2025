"use client";
import { useSearchParams, useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { FaLightbulb, FaHeadphones, FaList } from "react-icons/fa";

export default function AnalysisPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const paramRole = searchParams.get("role");
  const paramJob = searchParams.get("job");

  const role = useMemo(
    () =>
      paramRole ||
      (typeof window !== "undefined"
        ? sessionStorage.getItem("personaRole")
        : ""),
    [paramRole]
  );
  const job = useMemo(
    () =>
      paramJob ||
      (typeof window !== "undefined"
        ? sessionStorage.getItem("personaJob")
        : ""),
    [paramJob]
  );

  const [snippets, setSnippets] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [files, setFiles] = useState([]);
  const [audioUrl, setAudioUrl] = useState(null); // ✅ NEW

  const BASE_URL = process.env.NEXT_PUBLIC_API_BASE;

  // ✅ Fetch uploaded files
  useEffect(() => {
    if (!role) return;
    fetch(`${BASE_URL}/uploads/${role}`)
      .then((res) => res.json())
      .then((data) => {
        setFiles(Array.isArray(data) ? data : []);
      })
      .catch((err) => console.error("Error fetching uploads:", err));
  }, [BASE_URL, role]);

  // ✅ Fetch snippets
  useEffect(() => {
    if (!selectedFile) return;
    fetch(`${BASE_URL}/snippets/${selectedFile}`)
      .then((res) => res.json())
      .then((data) => {
        setSnippets(data.snippets || []);
        setAudioUrl(null); // ✅ Reset audio if new file selected
      })
      .catch((err) => console.error("Error fetching snippets:", err));
  }, [BASE_URL, selectedFile]);

  // ✅ Podcast generation
  const handleGeneratePodcast = async () => {
    if (!selectedFile) return;
    try {
      const res = await fetch(`${BASE_URL}/snippets/audio/${selectedFile}`);
      const data = await res.json();
      if (data.audio_url) {
        setAudioUrl(`${BASE_URL}${data.audio_url}`);
      } else {
        alert("Failed to generate audio");
      }
    } catch (err) {
      console.error("Podcast generation error:", err);
      alert("Error generating podcast");
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Top Bar */}
      <div className="flex justify-between items-center p-4 bg-white shadow-sm border-b">
        <h1 className="text-lg md:text-xl font-bold text-red-600">
          Adobe Document Intelligence
        </h1>
        <div className="text-gray-700 font-medium">
          {role} • {job}
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleGeneratePodcast}
            className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            <FaHeadphones /> Podcast Mode
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-yellow-100 text-yellow-800 rounded-lg hover:bg-yellow-200">
            <FaLightbulb className="text-yellow-500 animate-pulse" /> Insights
          </button>
        </div>
      </div>

      {/* Layout */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-72 bg-white border-r px-5 py-6 hidden md:block">
          <h2 className="font-semibold mb-4 flex items-center gap-2 text-gray-800">
            <FaList /> Uploaded Documents
          </h2>
          <ul className="space-y-3 text-gray-700">
            {files.length > 0 ? (
              files.map((f, idx) => (
                <li
                  key={idx}
                  onClick={() => setSelectedFile(f.filename)}
                  className={`cursor-pointer truncate ${
                    selectedFile === f.filename
                      ? "text-red-600 font-semibold"
                      : "hover:text-red-600"
                  }`}
                >
                  {f.filename} ({f.jobdesc})
                </li>
              ))
            ) : (
              <li className="text-gray-500 italic">No files uploaded yet.</li>
            )}
          </ul>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8 overflow-y-auto">
          <button
            onClick={() => router.push("/upload")}
            className="mb-6 px-6 py-2 rounded-lg bg-gray-200 hover:bg-gray-300"
          >
            ← Back to Upload
          </button>

          {selectedFile ? (
            <div className="bg-white shadow-md rounded-xl p-6 space-y-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                Extracted Sections & Snippets
              </h2>

              {snippets.length > 0 ? (
                <ul className="space-y-4">
                  {snippets.map((s, idx) => (
                    <li
                      key={idx}
                      className="p-4 border rounded-lg bg-gray-50 hover:bg-gray-100 cursor-pointer"
                    >
                      <p className="font-semibold text-gray-800">
                        {s.section} (p.{s.page})
                      </p>
                      <p className="text-gray-600 text-sm mt-1">
                        {s.snippet}
                      </p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500 italic">
                  No snippets available for this document.
                </p>
              )}

              {/* ✅ AUDIO PLAYER */}
              {audioUrl && (
                <div className="mt-6">
                  <h3 className="text-lg font-semibold text-gray-700 mb-2">
                    Audio Podcast
                  </h3>
                  <audio controls src={audioUrl} className="w-full" />
                </div>
              )}
            </div>
          ) : (
            <p className="text-gray-500 italic">
              Select a document from the left to view snippets.
            </p>
          )}
        </main>
      </div>
    </div>
  );
}
