import React from "react";
import PropTypes from "prop-types";

import Dropzone from "react-dropzone-uploader";

import { csrfToken } from "../../csrf";

const ENDPOINT = "/api/v1/kits/boxart/";
const MAX_SIZE = 1024 * 1024 * 10; // 10 MB

const BoxartUpload = ({ onComplete }) => {
    const getUploadParams = ({ file, meta }) => {
        const body = new FormData();
        body.append("image", file);
        return {
            url: ENDPOINT,
            headers: {
                "X-CSRFToken": csrfToken,
                Accept: "application/json"
            },
            body
        };
    };

    const handleChangeStatus = ({ meta, file, xhr }, status) => {
        if (status === "done") {
            const response = JSON.parse(xhr.response);
            onComplete(response);
        }
    };

    const inputContent = (
        <div className="button--blue">
            <i className="fa fa-upload" /> Upload a file
        </div>
    );

    return (
        <Dropzone
            getUploadParams={getUploadParams}
            onChangeStatus={handleChangeStatus}
            accept="image/*"
            multiple={false}
            maxSizeBytes={MAX_SIZE}
            autoUpload
            canCancel={false}
            canRestart={false}
            canRemove={false}
            inputWithFilesContent={null}
            submitButtonDisabled
            PreviewComponent={null}
        />
    );
};

BoxartUpload.propTypes = {
    onComplete: PropTypes.func.isRequired
};

export default BoxartUpload;
