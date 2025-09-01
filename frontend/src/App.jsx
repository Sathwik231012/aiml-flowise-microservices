// frontend/src/App.jsx
import { useState } from 'react';
import './App.css'; // We'll add some basic styles

function App() {
  // State for the document upload
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  // State for the Q&A section
  const [question, setQuestion] = useState('');
  const [qaAnswer, setQaAnswer] = useState(null);

  // State for the Summarization section
  const [textToSummarize, setTextToSummarize] = useState('');
  const [summary, setSummary] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus('Please select a file first.');
      return;
    }
    setUploadStatus('Uploading...');
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/docs/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setUploadStatus(`File uploaded successfully! Chunks indexed: ${data.chunks_indexed}`);
    } catch (error) {
      setUploadStatus('Error uploading file.');
      console.error('Upload error:', error);
    }
  };
  
  const handleAskQuestion = async () => {
    if (!question) return;
    setQaAnswer({ answer: 'Thinking...', sources: [] });
    try {
      const response = await fetch('http://127.0.0.1:8000/qa/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question, top_k: 4 }),
      });
      const data = await response.json();
      setQaAnswer(data);
    } catch (error) {
      setQaAnswer({ answer: 'Error fetching answer.', sources: [] });
      console.error('QA error:', error);
    }
  };

  const handleSummarize = async () => {
    if (!textToSummarize) return;
    setSummary('Summarizing...');
    try {
      const response = await fetch('http://127.0.0.1:8000/summarize/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: textToSummarize }),
      });
      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      setSummary('Error fetching summary.');
      console.error('Summarize error:', error);
    }
  };

  return (
    <div className="App">
      <h1>AI Microservices Demo</h1>

      <div className="card">
        <h2>1. Upload a Document for RAG</h2>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload</button>
        {uploadStatus && <p><i>{uploadStatus}</i></p>}
      </div>

      <div className="card">
        <h2>2. Ask a Question (RAG)</h2>
        <p>Ask a question about the document you just uploaded.</p>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="What is the main conclusion?"
        />
        <button onClick={handleAskQuestion}>Ask</button>
        {qaAnswer && (
          <div className="response">
            <p><b>Answer:</b> {qaAnswer.answer}</p>
            {qaAnswer.sources.length > 0 && (
              <pre>{JSON.stringify(qaAnswer.sources, null, 2)}</pre>
            )}
          </div>
        )}
      </div>
      
      <div className="card">
        <h2>3. Summarize Text</h2>
        <textarea
          value={textToSummarize}
          onChange={(e) => setTextToSummarize(e.target.value)}
          placeholder="Paste a long text here to summarize..."
        ></textarea>
        <button onClick={handleSummarize}>Summarize</button>
        {summary && (
          <div className="response">
            <p><b>Summary:</b> {summary}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;