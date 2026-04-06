
import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [jobDesc, setJobDesc] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!file) return;

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("resume", file);
      formData.append("job_description", jobDesc);

      const res = await axios.post("http://localhost:8000/generate-resume", formData);
      setResult(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const generatePreview = async () => {
    if (!result) return;

    const response = await fetch("http://localhost:8000/download-pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: result.content }),
    });

    const blob = await response.blob();
    setPdfUrl(URL.createObjectURL(blob));
  };

  useEffect(() => {
    if (result) generatePreview();
  }, [result]);

  const downloadFile = async (type: "pdf" | "docx") => {
    const response = await fetch(`http://localhost:8000/download-${type}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: result.content }),
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `resume.${type}`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div style={{ display: "flex", height: "100vh" }}>

      {/* LEFT: FORM — shrinks to 40% once result is ready, otherwise full width */}
      <div style={{
        width: result ? "40%" : "100%",
        padding: "20px",
        borderRight: result ? "1px solid #ccc" : "none",
        transition: "width 0.3s ease",
      }}>
        <h1>Resume Builder</h1>

        <input
          type="file"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />

        <textarea
          placeholder="Paste Job Description"
          value={jobDesc}
          onChange={(e) => setJobDesc(e.target.value)}
          style={{ width: "100%", height: "200px", marginTop: "10px" }}
        />

        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{
            marginTop: "10px",
            padding: "10px",
            width: "100%",
            cursor: loading ? "not-allowed" : "pointer",
          }}
        >
          {loading ? "Generating..." : "Generate Resume"}
        </button>

        {loading && <p>⏳ Generating resume...</p>}

        {result && (
          <div style={{ marginTop: "20px", display: "flex", gap: "10px" }}>
            <button onClick={() => downloadFile("pdf")}>Download PDF</button>
            <button onClick={() => downloadFile("docx")}>Download DOCX</button>

            ATS Score : {result.content.ats_score}
            Keywords Found : {result.content.keywords_found.join(", ")}
            Keywords Missing : {result.content.keywords_missing.join(", ")}
            Suggestions : {result.content.suggestions.join(", ")}

          </div>
        )}
      </div>

      {/* RIGHT: PREVIEW — only mounts after result exists */}
      {result && (
        <div style={{ width: "60%", padding: "20px", overflowY: "auto" }}>
          <h2>Preview</h2>

          <div style={{ marginBottom: "20px" }}>
            <h3>Text Preview</h3>
            <pre style={{ whiteSpace: "pre-wrap" }}>{result.content.optimized_resume}</pre>
          </div>

          {pdfUrl && (
            <div>
              <h3>PDF Preview</h3>
              <iframe src={pdfUrl} width="100%" height="500px" title="PDF Preview" />
            </div>
          )}
        </div>
      )}

    </div>
  );
}

export default App;