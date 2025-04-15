import PropTypes from 'prop-types';
import React from 'react';
import {FormattedMessage} from 'react-intl';
import useAsync from 'react-use/esm/useAsync';

import Loader from '../../components/loaders';
import {GroupBuildConsumer} from '../../data/group-build';
import GroupBuildParticipantsTable from './GroupBuildParticipantsTable';

const consumer = new GroupBuildConsumer();

const LinebreaksBr = ({text, className, component: Component = 'p'}) => (
  <Component className={className}>
    {text.split('\n').map((bit, index) => (
      <React.Fragment key={index}>
        {index === 0 ? null : <br />}
        {bit}
      </React.Fragment>
    ))}
  </Component>
);

const GroupBuildDetails = ({
  theme,
  status,
  url,
  start,
  end,
  description,
  rules,
  rules_topic,
  participants,
}) => (
  <>
    <h2>
      {theme}
      <span className="status">({status})</span>
    </h2>
    <a href={url}>
      <FormattedMessage
        description="Groupbuild inset in forum post, open main website link"
        defaultMessage="View outside of forum"
      />
    </a>

    <h4>
      <FormattedMessage
        description="Groupbuild inset in forum post, description title"
        defaultMessage="Description"
      />
    </h4>
    <p className="description">
      <strong>
        <FormattedMessage
          description="Groupbuild inset in forum post, start and end dates"
          defaultMessage="Start: {start}, end: {end}"
          values={{
            start: start,
            end: end,
          }}
        />
      </strong>
    </p>

    <LinebreaksBr text={description} className="description" />

    {rules ? (
      <>
        <h4>
          <FormattedMessage
            description="Groupbuild inset in forum post, rules title"
            defaultMessage="Rules"
          />
        </h4>
        <LinebreaksBr text={rules} className="rules" component="div" />
      </>
    ) : null}

    {rules_topic ? (
      <>
        <h4>
          <FormattedMessage
            description="Groupbuild inset in forum post, rules topic title"
            defaultMessage="Rules topic"
          />
        </h4>
        <a href={rules_topic.url}>{rules_topic.title}</a>
      </>
    ) : null}
    <GroupBuildParticipantsTable participants={participants} />
  </>
);

GroupBuildDetails.propTypes = {
  theme: PropTypes.string.isRequired,
  status: PropTypes.string.isRequired,
  url: PropTypes.string.isRequired,
  start: PropTypes.string.isRequired,
  end: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  rules: PropTypes.string,
  rules_topic: PropTypes.shape({
    url: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
  }),
  participants: PropTypes.arrayOf(
    PropTypes.shape({
      username: PropTypes.string.isRequired,
      model_name: PropTypes.string.isRequired,
      finished: PropTypes.bool.isRequired,
      topic: PropTypes.shape({
        url: PropTypes.string.isRequired,
        title: PropTypes.string.isRequired,
      }),
    }),
  ),
};

const GroupBuildInset = ({id}) => {
  const {
    loading,
    error,
    value: groupbuild,
  } = useAsync(async () => await consumer.read(`${id}/`), [id]);

  if (loading) {
    return <Loader />;
  }
  if (error) {
    console.error(error);
    return 'Something went wrong.';
  }
  return <GroupBuildDetails {...groupbuild} />;
};

GroupBuildInset.propTypes = {
  id: PropTypes.number.isRequired,
};

export default GroupBuildInset;
