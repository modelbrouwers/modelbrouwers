import React from "react";
import { injectIntl } from "react-intl";

/**
 * A wrapper component for simplifying message translation without injecting
 * intl in every component: https://github.com/yahoo/react-intl/issues/781#issuecomment-418300474
 */
const Msg = injectIntl(({ id, intl }) => intl.formatMessage({ id }));
const msg = ({ id }) => <Msg id={id} />;

export default msg;
