const BASE_URL = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

// ✅ Upload a PDF with role + job
export async function uploadPDFWithPersona(file, role, jobdesc) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("role", role);
  formData.append("jobdesc", jobdesc);
  const res = await fetch(`${BASE_URL}/upload`, { method: "POST", body: formData });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

// ✅ Get uploaded files list
export async function getUploads() {
  const response = await fetch(`${BASE_URL}/uploads`, { method: "GET" });
  if (!response.ok) throw new Error(await response.text());
  return response.json();
}

// ✅ Utility: get file URL
export function fileUrl(filename) {
  return `${BASE_URL}/pdfs/${encodeURIComponent(filename)}`;
}
