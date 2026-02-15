document.addEventListener('htmx:afterRequest', (e) => {
  if (e.detail.successful && e.target.id === 'buy-form') {
    const res = JSON.parse(e.detail.xhr.responseText);
    const el = document.getElementById('buy-result');
    el.innerHTML = 'Reservation confirmed! #' + res.id + ' • ' + res.quantity + ' ticket(s) for ' + res.buyer_name;
    e.target.reset();
  }
});