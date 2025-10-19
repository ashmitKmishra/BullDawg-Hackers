import React, { useState } from 'react';
import './PDFUpload.css';

const PDFUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError(null);
    } else {
      setError('Please select a valid PDF file');
      setSelectedFile(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a PDF file first');
      return;
    }

    setUploading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:3001/upload-pdf', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(`Upload failed: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const formatAnalysis = (analysis) => {
    if (!analysis) return null;

    return (
      <div className="analysis-result">
        <h3>Insurance Plans Analysis</h3>
        
        {analysis.summary && (
          <div className="summary-section">
            <h4>Summary</h4>
            <p>{analysis.summary}</p>
          </div>
        )}

        {analysis.total_plans_found && (
          <div className="stats-section">
            <h4>Total Plans Found: {analysis.total_plans_found}</h4>
          </div>
        )}

        {analysis.categories && (
          <div className="categories-section">
            <h4>Categories</h4>
            {Object.entries(analysis.categories).map(([category, plans]) => (
              plans && plans.length > 0 && (
                <div key={category} className="category-group">
                  <h5>{category.replace(/_/g, ' ').toUpperCase()}</h5>
                  <ul>
                    {plans.map((plan, index) => (
                      <li key={index}>
                        {typeof plan === 'string' ? plan : JSON.stringify(plan, null, 2)}
                      </li>
                    ))}
                  </ul>
                </div>
              )
            ))}
          </div>
        )}

        {analysis.recommendations && analysis.recommendations.length > 0 && (
          <div className="recommendations-section">
            <h4>Recommendations</h4>
            <ul>
              {analysis.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}

        {analysis.raw_response && (
          <div className="raw-response-section">
            <h4>Raw Analysis</h4>
            <pre>{analysis.raw_response}</pre>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="pdf-upload-container">
      <div className="upload-section">
        <h2>Upload Benefits PDF</h2>
        <p>Upload your benefits document to analyze and categorize insurance plans</p>
        
        <div className="file-input-container">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            className="file-input"
            id="pdf-file"
          />
          <label htmlFor="pdf-file" className="file-input-label">
            {selectedFile ? selectedFile.name : 'Choose PDF File'}
          </label>
        </div>

        {selectedFile && (
          <div className="file-info">
            <p>Selected: {selectedFile.name}</p>
            <p>Size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
          </div>
        )}

        <button
          onClick={handleUpload}
          disabled={!selectedFile || uploading}
          className="upload-button"
        >
          {uploading ? 'Processing...' : 'Upload & Analyze'}
        </button>

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}
      </div>

      {uploading && (
        <div className="loading-section">
          <div className="loading-spinner"></div>
          <p>Processing your PDF...</p>
          <p>This may take a moment while we extract and analyze the content.</p>
        </div>
      )}

      {result && (
        <div className="result-section">
          <h3>Processing Complete!</h3>
          {result.data && formatAnalysis(result.data.analysis)}
        </div>
      )}
    </div>
  );
};

export default PDFUpload;
