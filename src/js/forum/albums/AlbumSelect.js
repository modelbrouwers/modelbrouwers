import React from "react";
import PropTypes from "prop-types";
import useAsync from "react-use/esm/useAsync";

import { AlbumConsumer } from "../../data/albums/album";

const albumConsumer = new AlbumConsumer();

const AlbumSelect = ({ onChange, selected = "" }) => {
    const {
        loading,
        error,
        value: albums,
    } = useAsync(async () => {
        const albums = await albumConsumer.list();
        if (albums.length && !selected) {
            onChange(albums[0].id.toString());
        }
        return albums;
    }, []);

    if (error) return error.message;

    return (
        <select
            name="album"
            value={selected}
            onChange={(event) => onChange(event.target.value)}
        >
            {loading ? (
                <option value="">...</option>
            ) : (
                albums.map((album) => (
                    <option value={album.id.toString()} key={album.id}>
                        {album.title}
                    </option>
                ))
            )}
        </select>
    );
};

AlbumSelect.propTypes = {
    onChange: PropTypes.func.isRequired,
    selected: PropTypes.string,
};

export default AlbumSelect;
