import React from "react";

const logError = (error, errorInfo) => {
    console.error(error, errorInfo);
};

class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        logError(error, errorInfo);
    }

    render() {
        if (!this.state.hasError) {
            return this.props.children;
        }
        return "Oops! Something went wrong.";
    }
}

export default ErrorBoundary;
