import { useState } from "react";
import axios from "axios";

function App() { 
// This initializes our react app just like app = fastapi()

// Here we use a react functionality called use state which createse variables which can change overtime
// And they automatically update with the ui so no need to load them again

// Syntax is const [variable, setVariable] = useState(initialValue)
  const [file, setFile] = useState<File | null>(null);
  const [jobDesc, setJobDesc] = useState("");
  const [result, setResult] = useState<any>(null);
  // const [files, setFiles] = useState({ pdf: null, docx: null });
  // let t = "hi"

  const handleSubmit = async () => {
    if (!file) return;

    // Form data used here to send files, not easy by traditional json
    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", jobDesc);

    
    const res = await axios.post(
      "http://localhost:8000/generate-resume",
      formData
    );

    setResult(res.data);
    // setFiles({ pdf: res.data.pdf, docx: res.data.docx });

    

  };
  
const downloadFile = async (type: "pdf" | "docx") => {
  const response = await fetch(`http://localhost:8000/download-${type}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      content: result.content, 
    }),
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
    <div style={{ padding: "20px" }}>
      <h1>Perfect Resume Builder</h1>

      <input type="file" onChange={(e) =>{ setFile(e.target.files?.[0] || null)
        console.log(e)

        // t = JSON.stringify(e)
      }} />
      {/* e means event we can use anything instead of "e". It storese the changes 
      happening. .target is the property of e. e.target means where the change is happening
      here it is in the input. */}
      {/* <h1>{t}</h1> */}

      <textarea
        placeholder="Paste Job Description"
        value={jobDesc}
        onChange={(e) => setJobDesc(e.target.value)}
      />

      <button onClick={handleSubmit}>Generate Resume</button>

      {result && (
        <div>
          <button onClick={() => downloadFile("pdf")}>
            Download PDF
          </button>

          <button onClick={() => downloadFile("docx")}>
            Download DOCX
          </button>
      </div>
      )}
    </div>
  );
  
}

export default App;