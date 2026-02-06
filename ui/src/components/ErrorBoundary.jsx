import React from 'react';

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null, errorInfo: null };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error("ErrorBoundary caught an error", error, errorInfo);
        this.setState({ error, errorInfo });
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{ padding: '2rem', color: 'white', backgroundColor: '#1e293b', minHeight: '100vh' }}>
                    <h1>Something went wrong.</h1>
                    <details style={{ whiteSpace: 'pre-wrap', marginTop: '1rem' }}>
                        <summary>Error Details</summary>
                        <p>{this.state.error && this.state.error.toString()}</p>
                        <br />
                        <p>{this.state.errorInfo && this.state.errorInfo.componentStack}</p>
                    </details>
                    <button
                        onClick={() => window.location.href = '/'}
                        style={{
                            marginTop: '2rem',
                            padding: '0.8rem 1.5rem',
                            backgroundColor: '#8b5cf6',
                            color: 'white',
                            border: 'none',
                            borderRadius: '6px',
                            cursor: 'pointer'
                        }}
                    >
                        Go Home
                    </button>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;
