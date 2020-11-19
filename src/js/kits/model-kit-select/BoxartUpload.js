import React from "react";
import PropTypes from "prop-types";

import Dropzone, { Input } from "react-dropzone-uploader";

import { csrfToken } from "../../csrf";

const ENDPOINT = "/api/v1/kits/boxart/";
const MAX_SIZE = 1024 * 1024 * 10; // 10 MB

const DropzoneInput = props => {
    const {
        className,
        labelClassName,
        labelWithFilesClassName,
        style,
        labelStyle,
        labelWithFilesStyle,
        getFilesFromEvent,
        accept,
        multiple,
        disabled,
        content,
        withFilesContent,
        onFiles,
        files
    } = props;

    if (files.length > 0) {
        return null;
    }

    return (
        <div className="dzu-dropzone-wrapper">
            <label
                className={
                    files.length > 0 ? labelWithFilesClassName : labelClassName
                }
                style={files.length > 0 ? labelWithFilesStyle : labelStyle}
            >
                <div className="btn button--blue">
                    <i className="fa fa-upload" /> Upload a file
                </div>
                <input
                    className={className}
                    style={style}
                    type="file"
                    accept={accept}
                    multiple={multiple}
                    disabled={disabled}
                    onChange={async e => {
                        const target = e.target;
                        const chosenFiles = await getFilesFromEvent(e);
                        onFiles(chosenFiles);
                        target.value = null;
                    }}
                />
            </label>
        </div>
    );
};

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
            InputComponent={DropzoneInput}
        />
    );
};

BoxartUpload.propTypes = {
    onComplete: PropTypes.func.isRequired
};

export default BoxartUpload;
