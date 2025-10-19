import { useState } from 'react';
import './PDFUpload.css';

const PDFUploadModal = ({ onClose, onSuccess }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [estimatedTime, setEstimatedTime] = useState('');
  const [status, setStatus] = useState('');
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const [syncing, setSyncing] = useState(false);

  const PYTHON_BACKEND_URL = import.meta.env.VITE_PYTHON_BACKEND_URL || 'http://localhost:8000';
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError('');
    } else {
      setError('Please select a valid PDF file');
      setSelectedFile(null);
    }
  };

  const estimateProcessingTime = (fileSize) => {
    // Rough estimation: ~10-15 seconds per MB
    const sizeInMB = fileSize / (1024 * 1024);
    const estimatedSeconds = Math.ceil(sizeInMB * 12);
    
    if (estimatedSeconds < 60) {
      return `~${estimatedSeconds} seconds`;
    } else {
      const minutes = Math.floor(estimatedSeconds / 60);
      const seconds = estimatedSeconds % 60;
      return `~${minutes}m ${seconds}s`;
    }
  };

  const syncToSupabase = async (categorizedData) => {
    try {
      setSyncing(true);
      setStatus('Syncing benefits to database...');
      
      // Call the Express API to sync benefits
      const response = await fetch(`${API_URL}/sync-benefits`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ data: categorizedData })
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || 'Failed to sync benefits');
      }

      const syncResult = await response.json();
      console.log('Sync result:', syncResult);
      
      setSyncing(false);
      setStatus(`Successfully synced ${syncResult.inserted} benefits to database!`);
      
      // Call the parent success handler to refresh the benefits list
      if (onSuccess) {
        onSuccess();
      }
      
    } catch (err) {
      console.error('Sync error:', err);
      setSyncing(false);
      setError(`Sync warning: ${err.message}. Benefits may need manual sync.`);
      // Still call success to refresh the list
      if (onSuccess) {
        onSuccess();
      }
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a PDF file first');
      return;
    }

    setUploading(true);
    setProgress(0);
    setError('');
    setResults(null);
    
    const estimatedTimeStr = estimateProcessingTime(selectedFile.size);
    setEstimatedTime(estimatedTimeStr);
    setStatus('Uploading PDF...');

    try {
      // Create FormData
      const formData = new FormData();
      formData.append('file', selectedFile);

      // Start upload
      const response = await fetch(`${PYTHON_BACKEND_URL}/upload-pdf`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Upload failed: ${response.statusText}`);
      }

      setProgress(50);
      setStatus('Processing PDF with AI...');

      const data = await response.json();
      
      setProgress(90);
      setStatus('Categorizing benefits...');

      // Small delay to show the progress
      await new Promise(resolve => setTimeout(resolve, 500));

      setProgress(100);
      setStatus('PDF processed successfully!');
      setResults(data.data);

      // Auto-sync to Supabase
      if (data.data && data.data.analysis) {
        await syncToSupabase(data.data.analysis);
      }

    } catch (err) {
      console.error('Upload error:', err);
      setError(err.message || 'Failed to upload and process PDF');
      setStatus('');
    } finally {
      setUploading(false);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    const file = e.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
      setError('');
    } else {
      setError('Please drop a valid PDF file');
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-box pdf-upload-modal" onClick={(e) => e.stopPropagation()}>
        <button className="close-modal" onClick={onClose}>×</button>
        
        <h2>Upload Benefits PDF</h2>
        <p className="modal-subtitle">
          Upload a PDF document containing employee benefits and policies. 
          Our AI will extract and categorize the information automatically.
        </p>

        {!results ? (
          <>
            {/* File Upload Area */}
            <div 
              className={`pdf-drop-zone ${selectedFile ? 'has-file' : ''}`}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
            >
              <input
                type="file"
                accept="application/pdf"
                onChange={handleFileSelect}
                id="pdf-file-input"
                style={{ display: 'none' }}
              />
              
              {!selectedFile ? (
                <label htmlFor="pdf-file-input" className="drop-zone-label">
                  <div className="drop-zone-icon">📄</div>
                  <div className="drop-zone-text">
                    <strong>Click to browse</strong> or drag and drop
                  </div>
                  <div className="drop-zone-hint">PDF files only</div>
                </label>
              ) : (
                <div className="selected-file-info">
                  <div className="file-icon">📄</div>
                  <div className="file-details">
                    <div className="file-name">{selectedFile.name}</div>
                    <div className="file-size">{formatFileSize(selectedFile.size)}</div>
                  </div>
                  <button 
                    className="change-file-btn"
                    onClick={() => document.getElementById('pdf-file-input').click()}
                  >
                    Change
                  </button>
                </div>
              )}
            </div>

            {/* Error Message */}
            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}

            {/* Upload Progress */}
            {uploading && (
              <div className="upload-progress">
                <div className="progress-header">
                  <span className="progress-label">{status}</span>
                  <span className="progress-percent">{progress}%</span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-fill" 
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
                {estimatedTime && progress < 50 && (
                  <div className="estimated-time">
                    Estimated time: {estimatedTime}
                  </div>
                )}
                {syncing && (
                  <div className="sync-indicator">
                    <span className="spinner"></span>
                    Syncing to database...
                  </div>
                )}
              </div>
            )}

            {/* Upload Button */}
            <div className="modal-actions">
              <button 
                onClick={handleUpload}
                className="upload-btn"
                disabled={!selectedFile || uploading}
              >
                {uploading ? 'Processing...' : 'Upload and Process'}
              </button>
              <button 
                onClick={onClose}
                className="cancel-btn"
                disabled={uploading}
              >
                Cancel
              </button>
            </div>
          </>
        ) : (
          <>
            {/* Success Results */}
            <div className="upload-results">
              <div className="success-icon">✅</div>
              <h3>PDF Processed Successfully!</h3>
              
              <div className="results-summary">
                <div className="result-item">
                  <strong>File:</strong> {results.original_filename}
                </div>
                <div className="result-item">
                  <strong>Pages:</strong> {results.total_pages}
                </div>
                <div className="result-item">
                  <strong>Chunks Processed:</strong> {results.chunks_processed}
                </div>
              </div>

              {results.analysis && (
                <div className="benefits-preview">
                  <h4>Extracted Benefits:</h4>
                  <div className="benefits-count">
                    {Object.keys(results.analysis.benefits || {}).length} benefit categories found
                  </div>
                </div>
              )}

              <div className="sync-status">
                {syncing ? (
                  <div className="syncing">
                    <span className="spinner"></span>
                    Syncing to database...
                  </div>
                ) : (
                  <div className="synced">
                    ✓ Benefits have been synced to the database
                  </div>
                )}
              </div>
            </div>

            <div className="modal-actions">
              <button 
                onClick={onClose}
                className="done-btn"
              >
                Done
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default PDFUploadModal;
