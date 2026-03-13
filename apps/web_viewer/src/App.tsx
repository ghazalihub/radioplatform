import React, { useState } from 'react';
import './App.css';
import DICOMViewer from './DICOMViewer';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [imageIds, setImageIds] = useState<string[]>([]);
  const [studies, setStudies] = useState<any[]>([]);

  const searchStudies = async () => {
    try {
      const resp = await fetch(`http://localhost:8005/rs/studies?00100020=${searchQuery}`);
      const data = await resp.json();
      setStudies(data);
    } catch (e) {
      console.error("Error searching studies:", e);
    }
  };

  const loadStudy = async (studyUid: string) => {
    // In a real system, fetch series and instances to get WADO-RS URLs
    const mockImageId = `wado-rs:http://localhost:8005/rs/studies/${studyUid}/series/1.2.3/instances/1.2.3.4`;
    setImageIds([mockImageId]);
  };

  const startVoiceDictation = () => {
    alert("Voice dictation started... (Mocking Web Speech API)");
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Advanced Radiology Platform</h1>
      </header>
      <main>
        <div className="search-bar">
          <input
            type="text"
            placeholder="Enter Patient ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button onClick={searchStudies}>Search</button>
        </div>
        <div className="study-list">
          {studies.map(study => (
            <div key={study.study_instance_uid} className="study-item" onClick={() => loadStudy(study.study_instance_uid)}>
              {study.study_description} ({study.study_instance_uid})
            </div>
          ))}
        </div>
        <div className="viewer-container">
          <DICOMViewer imageIds={imageIds} />
          <div className="reporting-panel">
            <button onClick={startVoiceDictation}>Start Dictation</button>
            <textarea placeholder="Radiology Report..."></textarea>
            <button>Save Report</button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
