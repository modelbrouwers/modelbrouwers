import React from "react";
import PropTypes from "prop-types";
import useAsync from "react-use/esm/useAsync";

import { Album, AlbumConsumer } from "../../data/albums/album";

const albumConsumer = new AlbumConsumer();

const AlbumSelect = ({ onChange, selected = null }) => {
    const {
        loading,
        error,
        value: albums,
    } = useAsync(async () => {
        const albums = await albumConsumer.list();
        if (albums.length && !selected) {
            onChange(albums[0]);
        }
        return albums;
    }, []);

    if (error) return error.message;

    return (
        <select
            name="album"
            value={selected ? selected.id.toString() : ""}
            onChange={(event) => {
                const album = albums.find(
                    (album) => album.id.toString() === event.target.value
                );
                onChange(album);
            }}
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
    selected: PropTypes.instanceOf(Album),
};

export default AlbumSelect;
