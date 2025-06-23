import {useEffect, useId, useRef} from 'react';
import {FormattedMessage} from 'react-intl';

import FAIcon from '@/components/FAIcon.js';

export interface ModalProps {
  isOpen: boolean;
  onRequestClose: () => void;
  title?: React.ReactNode;
  children?: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({isOpen, onRequestClose, title, children}) => {
  const modalRef = useRef<HTMLDialogElement>(null);
  const titleId = useId();

  useEffect(() => {
    const modalElement = modalRef.current;
    if (!modalElement) return;
    if (isOpen) {
      modalElement.showModal();
    } else {
      modalElement.close();
    }
  }, [isOpen]);

  return (
    <dialog
      className="modal modal--native"
      ref={modalRef}
      onKeyDown={(event: React.KeyboardEvent<HTMLDialogElement>) => {
        if (event.key === 'Escape') {
          onRequestClose();
        }
      }}
      aria-labelledby={titleId}
    >
      {title && (
        <h2 className="modal__title" id={titleId}>
          {' '}
          {title}{' '}
        </h2>
      )}
      <button className="modal__close" onClick={() => onRequestClose()}>
        <FAIcon icon="times" extra={['fa-fw']} />
        <span className="sr-only">
          <FormattedMessage description="Modal close button" defaultMessage="Close" />
        </span>
      </button>
      <div className="modal__body">{children}</div>
    </dialog>
  );
};

export default Modal;
