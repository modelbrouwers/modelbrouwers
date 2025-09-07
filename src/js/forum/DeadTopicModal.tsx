import {FormattedMessage} from 'react-intl';

import Modal from '@/components/modals/Modal';

export interface DeadTopicModalProps {
  message: string;
  onRequestClose: () => void;
  replyTopicUrl: string;
}

const DeadTopicModal: React.FC<DeadTopicModalProps> = ({
  message,
  onRequestClose,
  replyTopicUrl,
}) => (
  <Modal isOpen onRequestClose={onRequestClose}>
    <div style={{display: 'flex', flexDirection: 'column', blockSize: '100%'}}>
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '1em',
          justifyContent: 'center',
          alignItems: 'center',
          flexGrow: 1,
          fontSize: '1rem',
          paddingInline: '10px',
        }}
      >
        <div>{message}</div>
        <a href={replyTopicUrl}>
          <FormattedMessage
            description="Dead topic: reply anyway URL label"
            defaultMessage="I want to reply anyway."
          />
        </a>
      </div>
    </div>
  </Modal>
);

export default DeadTopicModal;
