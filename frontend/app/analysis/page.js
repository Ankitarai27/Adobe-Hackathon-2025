import { Suspense } from "react";
import AnalysisPageClient from "./AnalysisPageClient";

export default function AnalysisPage() {
  return (
    <Suspense fallback={<div className="p-6">Loading analysis page...</div>}>
      <AnalysisPageClient />
    </Suspense>
  );
}
