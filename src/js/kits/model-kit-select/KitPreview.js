import React, { useState } from "react";
import PropTypes from "prop-types";

const DEFAULT_THUMB = "/static/images/thumb.png";

const KitPreview = ({
    htmlName,
    inputType,
    kit,
    selected = false,
    onToggle = () => {}
}) => {
    const [thumbImg, setThumbImg] = useState(
        kit.box_image.small || DEFAULT_THUMB
    );
    const [errored, setErrored] = useState(false);

    const onThumbError = () => {
        if (errored) return;
        setThumbImg(DEFAULT_THUMB);
        setErrored(true);
    };

    const onChange = event => {
        const { checked } = event.target;
        onToggle(kit, checked);
    };

    return (
        <div className="col-xs-12 col-sm-4 col-md-3 col-xl-2 preview">
            <input
                type={inputType}
                name={htmlName}
                defaultChecked={selected}
                id={`__modelkit_${kit.id}`}
                value={kit.id}
                onChange={onChange}
            />
            <label
                htmlFor={`__modelkit_${kit.id}`}
                title={kit.name}
                className="thumbnail"
            >
                <img
                    src={thumbImg}
                    className="img-responsive"
                    onError={onThumbError}
                />
                <span className="h5">
                    <strong>
                        {kit.name}
                        {kit.kit_number ? (
                            <small>{kit.kit_number}</small>
                        ) : null}
                    </strong>
                </span>
            </label>
            <i className="fa fa-check fa-3x" />
        </div>
    );
};

KitPreview.propTypes = {
    htmlName: PropTypes.string.isRequired,
    inputType: PropTypes.oneOf(["checkbox", "radio"]).isRequired,
    kit: PropTypes.object.isRequired,
    selected: PropTypes.bool,
    onToggle: PropTypes.func
};

export { KitPreview };
