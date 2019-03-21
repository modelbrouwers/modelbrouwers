const handleValidationErrors = (err) => {
    const data = err.statusText.response.data;

    if (!err.statusCode === 400) {
        console.warn("Got a non-validation error", err);
        return data;
    }

    if (!err.statusText.response.headers['content-type'].startsWith('application/json')) {
        console.warn("Got a non-JSON response", err);
        return data;
    }

    return JSON.parse(data);
};


export { handleValidationErrors };
