import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, FileText, CheckCircle, AlertCircle, ArrowRight, X } from 'lucide-react';
import api from '../services/api';
import './ResumeUpload.css';

const ResumeUpload = () => {
    const navigate = useNavigate();
    const [dragging, setDragging] = useState(false);
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);
    const [uploadSuccess, setUploadSuccess] = useState(false);

    const handleDragEnter = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(true);
    }, []);

    const handleDragLeave = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(false);
    }, []);

    const handleDragOver = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
    }, []);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(false);

        const droppedFiles = e.dataTransfer.files;
        if (droppedFiles && droppedFiles.length > 0) {
            validateAndSetFile(droppedFiles[0]);
        }
    }, []);

    const handleFileSelect = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            validateAndSetFile(e.target.files[0]);
        }
    };

    const validateAndSetFile = (selectedFile) => {
        setError(null);
        if (selectedFile.type !== 'application/pdf') {
            setError('Please upload a PDF file.');
            return;
        }
        if (selectedFile.size > 5 * 1024 * 1024) { // 5MB limit
            setError('File size exceeds the 5MB limit.');
            return;
        }
        setFile(selectedFile);
    };

    const handleRemoveFile = () => {
        setFile(null);
        setError(null);
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await api.post('/candidates/resume/analyze', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            if (response.data.status === 'success') {
                setUploadSuccess(true);
                // Redirect to profile after short delay
                setTimeout(() => {
                    navigate('/profile');
                }, 2000);
            } else {
                setError(response.data.message || 'Upload failed. Please try again.');
            }
        } catch (err) {
            console.error("Upload error", err);
            setError(err.response?.data?.message || 'An error occurred during upload.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="page-container resume-upload-page">
            <div className="container max-w-2xl mx-auto">
                <div className="upload-header text-center mb-10">
                    <h1 className="text-3xl font-bold mb-4">Upload Your Resume</h1>
                    <p className="text-muted text-lg">
                        Let our AI analyze your skills and match you with the best opportunities.
                    </p>
                </div>

                <div className="upload-card">
                    {uploadSuccess ? (
                        <div className="success-state text-center py-10">
                            <div className="success-icon-wrapper mb-6">
                                <CheckCircle size={64} className="text-green-500" />
                            </div>
                            <h2 className="text-2xl font-bold mb-2">Resume Uploaded!</h2>
                            <p className="text-muted mb-6">Redirecting to your profile...</p>
                            <div className="spinner mx-auto"></div>
                        </div>
                    ) : (
                        <>
                            <div
                                className={`drop-zone ${dragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
                                onDragEnter={handleDragEnter}
                                onDragLeave={handleDragLeave}
                                onDragOver={handleDragOver}
                                onDrop={handleDrop}
                            >
                                {file ? (
                                    <div className="file-preview">
                                        <div className="file-icon">
                                            <FileText size={48} className="text-primary" />
                                        </div>
                                        <div className="file-info">
                                            <p className="file-name">{file.name}</p>
                                            <p className="file-size">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                                        </div>
                                        <button onClick={handleRemoveFile} className="btn-icon remove-btn">
                                            <X size={20} />
                                        </button>
                                    </div>
                                ) : (
                                    <div className="empty-state">
                                        <div className="upload-icon-circle mb-4">
                                            <Upload size={32} className="text-primary" />
                                        </div>
                                        <h3 className="text-xl font-bold mb-2">Drag & Drop your resume here</h3>
                                        <p className="text-muted mb-6">or browse to upload (PDF only, max 5MB)</p>
                                        <label htmlFor="file-upload" className="btn btn-primary px-8 cursor-pointer">
                                            Browse Files
                                            <input
                                                id="file-upload"
                                                type="file"
                                                accept=".pdf"
                                                className="hidden"
                                                onChange={handleFileSelect}
                                            />
                                        </label>
                                    </div>
                                )}
                            </div>

                            {error && (
                                <div className="error-message flex items-center gap-2 mt-4 text-red-600 bg-red-50 p-3 rounded-lg">
                                    <AlertCircle size={18} />
                                    <span>{error}</span>
                                </div>
                            )}

                            <div className="actions mt-8 flex justify-end gap-4">
                                <button className="btn btn-ghost" onClick={() => navigate('/dashboard')}>
                                    Cancel
                                </button>
                                <button
                                    className="btn btn-primary px-8"
                                    onClick={handleUpload}
                                    disabled={!file || uploading}
                                >
                                    {uploading ? 'Uploading...' : 'Upload & Analyze'}
                                    {!uploading && <ArrowRight size={18} className="ml-2" />}
                                </button>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ResumeUpload;
