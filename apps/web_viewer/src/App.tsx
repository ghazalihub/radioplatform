import React, { useState } from 'react';
import './App.css';
import DICOMViewer from './DICOMViewer';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [imageIds, setImageIds] = useState<string[]>([]);
  const [studies, setStudies] = useState<any[]>([]);

  const DICOMWEB_BASE_URL = process.env.REACT_APP_DICOMWEB_URL || 'http://localhost:8005/rs';

  const searchStudies = async () => {
    try {
      const resp = await fetch(`${DICOMWEB_BASE_URL}/studies?00100020=${searchQuery}`);
      const data = await resp.json();
      setStudies(data);
    } catch (e) {
      console.error("Error searching studies:", e);
    }
  };

  const loadStudy = async (studyUid: string) => {
    try {
      // 1. Fetch series for study
      const seriesResp = await fetch(`${DICOMWEB_BASE_URL}/studies/${studyUid}/series`);
      const seriesList = await seriesResp.json();

      if (seriesList.length > 0) {
        const firstSeries = seriesList[0];
        const seriesUid = firstSeries["0020000E"].Value[0];

        // 2. Fetch instances for series
        const instanceResp = await fetch(`${DICOMWEB_BASE_URL}/studies/${studyUid}/series/${seriesUid}/instances`);
        const instanceList = await instanceResp.json();

        if (instanceList.length > 0) {
          const newImageIds = instanceList.map((inst: any) => {
            const sopUid = inst["00080018"].Value[0];
            return `wado-rs:${DICOMWEB_BASE_URL}/studies/${studyUid}/series/${seriesUid}/instances/${sopUid}`;
          });
          setImageIds(newImageIds);
        }
      }
    } catch (e) {
      console.error("Error loading study details:", e);
    }
  };

  const startVoiceDictation = () => {
    alert("Voice dictation started... (Mocking Web Speech API)");
  };

  const isMobile = window.innerWidth <= 768;

  if (isMobile) {
    return (
      <div className="App mobile-view">
        <header className="App-header">
          <h1>RadMobile</h1>
        </header>
        <main>
          <div className="notification-banner">
            Critical finding: Brain Hemorrhage detected (Study: 1.2.840...)
          </div>
          <div className="search-bar">
            <input
              type="text"
              placeholder="Search Patient..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="viewer-container" style={{ flexDirection: 'column' }}>
            <DICOMViewer imageIds={imageIds} />
            <div className="study-list">
              {studies.map(study => (
                <div key={study.study_instance_uid} className="study-item" onClick={() => loadStudy(study.study_instance_uid)}>
                  {study.study_description}
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    );
  }

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
