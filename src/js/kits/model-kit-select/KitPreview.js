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
    const thumb = kit.box_image ? kit.box_image.small : undefined;
    const [thumbImg, setThumbImg] = useState(thumb || DEFAULT_THUMB);
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
                    alt="boxart"
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

const KitPreviews = ({
    htmlName,
    inputType = "checkbox",
    selected = [],
    kits = [],
    onToggle
}) => {
    return (
        <>
            {kits.map(kit => (
                <KitPreview
                    key={kit.id}
                    htmlName={htmlName}
                    inputType={inputType}
                    kit={kit}
                    selected={selected.includes(kit.id)}
                    onToggle={onToggle}
                />
            ))}
        </>
    );
};

KitPreviews.propTypes = {
    htmlName: PropTypes.string.isRequired,
    inputType: PropTypes.oneOf(["checkbox", "radio"]).isRequired,
    selected: PropTypes.arrayOf(PropTypes.number),
    kits: PropTypes.arrayOf(PropTypes.object),
    onToggle: PropTypes.func.isRequired
};

export { KitPreviews, KitPreview };
