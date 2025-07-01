import {FormattedMessage} from 'react-intl';

import Modal from '@/components/modals/Modal';

export interface AlbumSelectionErrorModalProps {
  onRequestClose: () => void;
}

const AlbumSelectionErrorModal: React.FC<AlbumSelectionErrorModalProps> = ({onRequestClose}) => (
  <Modal
    isOpen
    onRequestClose={onRequestClose}
    title={
      <FormattedMessage
        description="Albums upload: album selection error modal title"
        defaultMessage="Incorrect album selection"
      />
    }
  >
    <p>
      <FormattedMessage
        description="Albums upload: album selection error"
        defaultMessage="You must select exactly one album to upload the photos to."
      />
    </p>

    <div className="modal__footer modal__footer--reverse">
      <button type="button" className="btn bg-main-grey" onClick={onRequestClose}>
        <FormattedMessage description="Modal close button" defaultMessage="Close" />
      </button>
    </div>
  </Modal>
);

export default AlbumSelectionErrorModal;
