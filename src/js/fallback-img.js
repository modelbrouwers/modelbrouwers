const init = () => {
  const images = document.querySelectorAll('img[data-fallback]');
  images.forEach(imgNode => {
    const {fallback} = imgNode.dataset;
    if (!fallback) return;
    imgNode.onerror = () => {
      imgNode.onerror = null;
      imgNode.src = fallback;
    };
  });
};

if (document.readyState !== 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
