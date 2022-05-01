import React from "react";
import PropTypes from "prop-types";
import { FormattedMessage } from "react-intl";
import classNames from "classnames";

import YesNo from "./YesNo";

const ParticipantRow = ({ index, username, model_name, finished, topic }) => (
    <tr className={index % 2 === 0 ? "row2" : "row1"}>
        <td className="num">{index + 1}</td>
        <td className="brouwer">{username}</td>
        <td className="model-name">{model_name}</td>
        <td className={classNames("completed", { finished: finished })}>
            <YesNo>{finished}</YesNo>
        </td>
        <td className="topic">
            {topic ? <a href={topic.url}>{topic.title}</a> : null}
        </td>
    </tr>
);

ParticipantRow.propTypes = {
    index: PropTypes.number.isRequired,
    username: PropTypes.string.isRequired,
    model_name: PropTypes.string.isRequired,
    finished: PropTypes.bool.isRequired,
    topic: PropTypes.shape({
        url: PropTypes.string.isRequired,
        title: PropTypes.string.isRequired,
    }),
};

const GroupBuildParticipantsTable = ({ participants = [] }) => {
    if (!participants.length) return null;

    return (
        <>
            <h4>
                <FormattedMessage
                    description="Groupbuild inset in forum post, participants title"
                    defaultMessage="Participants"
                />
            </h4>

            <table className="tablebg">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>
                            <FormattedMessage
                                description="GB participants table, brouwer header."
                                defaultMessage="Brouwer"
                            />
                        </th>
                        <th>
                            <FormattedMessage
                                description="GB participants table, model header."
                                defaultMessage="Model"
                            />
                        </th>
                        <th>
                            <FormattedMessage
                                description="GB participants table, finished header."
                                defaultMessage="Finished?"
                            />
                        </th>
                        <th>
                            <FormattedMessage
                                description="GB participants table, topic header."
                                defaultMessage="Topic"
                            />
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {participants.map((participant, index) => (
                        <ParticipantRow
                            key={participant.id}
                            index={index}
                            {...participant}
                        />
                    ))}
                </tbody>
            </table>
        </>
    );
};

GroupBuildParticipantsTable.propTypes = {
    participants: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.number.isRequired,
            username: PropTypes.string.isRequired,
            model_name: PropTypes.string.isRequired,
            finished: PropTypes.bool.isRequired,
            topic: PropTypes.shape({
                url: PropTypes.string.isRequired,
                title: PropTypes.string.isRequired,
            }),
        })
    ),
};

export default GroupBuildParticipantsTable;
