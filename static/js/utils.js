function qtyHandler(type, selector) {
  const qtyInput = document.getElementById(selector);
  if (qtyInput) {
    let updatedQty = qtyInput.value;
    let qty = parseInt(updatedQty);
    if (type === "minus") {
      if (qty - 1 > 0) {
        updatedQty = qty - 1;
      }
    } else if (type === "plus") {
      updatedQty = qty + 1;
    }
    qtyInput.value = updatedQty;
  }
}

function setPaymentMode(paymentMode) {
  const payment_mode = document.getElementById("payment_mode");
  if (payment_mode) {
    payment_mode.value = paymentMode;
  }
}
