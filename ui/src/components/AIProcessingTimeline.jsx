import React, { useEffect, useState } from 'react';
import { CheckCircle, Loader, FileText, Brain, TrendingUp, Sparkles } from 'lucide-react';
import './AIProcessingTimeline.css';

const STEPS = [
    { id: 'upload', label: 'بارگذاری رزومه', icon: FileText },
    { id: 'extract', label: 'استخراج مهارت‌ها و داده‌ها', icon: Loader },
    { id: 'analyze', label: 'تحلیل بازار توسط هوش مصنوعی', icon: Brain },
    { id: 'match', label: 'محاسبه امتیاز انطباق', icon: TrendingUp },
    { id: 'complete', label: 'تکمیل فرآیند نهایی', icon: Sparkles }
];

const AIProcessingTimeline = ({ status = 'idle', onComplete }) => {
    const [currentStepIndex, setCurrentStepIndex] = useState(0);

    useEffect(() => {
        if (status === 'processing') {
            const interval = setInterval(() => {
                setCurrentStepIndex(prev => {
                    if (prev < STEPS.length - 1) return prev + 1;
                    clearInterval(interval);
                    if (onComplete) onComplete();
                    return prev;
                });
            }, 3000); 
            return () => clearInterval(interval);
        }
        if (status === 'idle') setCurrentStepIndex(0);
        if (status === 'complete') setCurrentStepIndex(STEPS.length - 1);
    }, [status, onComplete]);

    return (
        <div className="ai-timeline-container" dir="rtl">
            <div className="ai-timeline-header">
                <Sparkles className="text-purple-500 animate-pulse" />
                <h3>گردش کار عامل هوش مصنوعی</h3>
            </div>

            <div className="ai-timeline-steps">
                {STEPS.map((step, index) => {
                    const isActive = index === currentStepIndex;
                    const isCompleted = index < currentStepIndex;
                    const Icon = step.icon;

                    return (
                        <div key={step.id} className={`timeline-step ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}>
                            <div className="step-connector">
                                <div className="step-dot">
                                    {isCompleted ? <CheckCircle size={16} /> : <div className="dot-inner" />}
                                </div>
                                {index < STEPS.length - 1 && <div className="step-line" />}
                            </div>

                            <div className="step-content">
                                <div className="step-icon-wrapper">
                                    <Icon size={20} className={isActive ? 'animate-spin-slow' : ''} />
                                </div>
                                <span className="step-label">{step.label}</span>
                                {isActive && <span className="step-status">در حال پردازش...</span>}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default AIProcessingTimeline;