'use strict';
(() => {
  const token = new URLSearchParams(window.location.hash.slice(1)).get('t') || '';
  if (!/^[a-f0-9]{64}$/i.test(token)) {
    document.getElementById('error').hidden = false;
    document.getElementById('detail').hidden = true;
    return;
  }
  document.getElementById('token').value = token;
  document.getElementById('confirm-form').hidden = false;
  // Keep the bearer token in the fragment, not in a server request or referrer.
  document.getElementById('confirm-form').addEventListener('submit', () => {
    const button=document.getElementById('confirm-button');
    button.disabled = true;
    button.textContent='CONFIRMING RECEIPT…';
  });
})();
