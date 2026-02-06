import React from 'react';
import { TrendingUp, Shield, Sparkles, MapPin, DollarSign, Briefcase, CheckCircle, XCircle } from 'lucide-react';
import './MatchIntelligenceCard.css';

const MatchIntelligenceCard = ({ analysis }) => {
    if (!analysis) return null;

    const { summary, analysis_results } = analysis;
    const { strengths, gaps } = analysis_results || { strengths: [], gaps: [] };

    // Mock category scores for demonstration of the "breakdown" request
    // In a real app, these would come from the backend analysis
    const categories = [
        { name: 'Skills', score: 95, icon: <TrendingUp size={18} />, color: 'var(--primary-color)' },
        { name: 'Experience', score: 85, icon: <Briefcase size={18} />, color: 'var(--accent-success)' },
        { name: 'Location', score: 100, icon: <MapPin size={18} />, color: 'var(--accent-info)' },
        { name: 'Salary', score: 90, icon: <DollarSign size={18} />, color: 'var(--accent-warning)' },
    ];

    return (
        <div className="match-card-container">
            {/* Header Section */}
            <div className="match-card-header">
                <div className="match-summary">
                    <h3 className="flex items-center gap-2 text-xl font-bold">
                        <Sparkles className="text-primary" /> AI Match Analysis
                    </h3>
                    <p className="text-muted leading-relaxed mt-2">
                        {summary || "Your profile shows high potential. Our AI agents have identified key strengths that align with current market demands."}
                    </p>
                </div>
            </div>

            {/* Detailed Match Breakdown */}
            <div className="match-breakdown-section mt-6">
                <div className="flex justify-between items-center mb-4">
                    <h4 className="text-lg font-semibold">Match Breakdown</h4>
                    <button className="text-xs font-semibold text-primary hover:text-primary-800 transition-colors">
                        See Full Analysis
                    </button>
                </div>
                <div className="breakdown-grid">
                    {categories.map((cat) => (
                        <div key={cat.name} className="breakdown-item">
                            <div className="breakdown-icon" style={{ backgroundColor: cat.color + '15', color: cat.color }}>
                                {cat.icon}
                            </div>
                            <div className="breakdown-info">
                                <div className="flex justify-between items-center mb-1">
                                    <span className="breakdown-label">{cat.name}</span>
                                    <span className="breakdown-score" style={{ color: cat.color }}>{cat.score}%</span>
                                </div>
                                <div className="breakdown-bar-container">
                                    <div className="breakdown-bar" style={{ width: `${cat.score}%`, backgroundColor: cat.color }}></div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Analysis Lists */}
            <div className="match-grid mt-6">
                <div className="analysis-column strengths">
                    <div className="column-header text-green-700 bg-green-50">
                        <CheckCircle size={20} /> Key Strengths
                    </div>
                    <ul className="analysis-list">
                        {strengths.length > 0 ? strengths.map((item, i) => (
                            <li key={i}>
                                <div className="bullet-green"></div>
                                <span>{item}</span>
                            </li>
                        )) : <li className="text-muted italic">No specific strengths identified yet.</li>}
                    </ul>
                </div>

                <div className="analysis-column gaps">
                    <div className="column-header text-amber-700 bg-amber-50">
                        <XCircle size={20} /> Growth Areas
                    </div>
                    <ul className="analysis-list">
                        {gaps.length > 0 ? gaps.map((item, i) => (
                            <li key={i}>
                                <div className="bullet-amber"></div>
                                <span>{item}</span>
                            </li>
                        )) : <li className="text-muted italic">No major gaps found. Great job!</li>}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default MatchIntelligenceCard;
