const paymentMethodSelect = document.getElementById('payment-method');
const mobileMoneyFields = document.getElementById('mobile-money-fields');
const bankAccountFields = document.getElementById('bank-account-fields');

paymentMethodSelect.addEventListener('change', () => {
  if (paymentMethodSelect.value === 'mobile-money') {
    mobileMoneyFields.style.display = 'block';
    bankAccountFields.style.display = 'none';
  } else if (paymentMethodSelect.value === 'bank-account') {
    mobileMoneyFields.style.display = 'none';
    bankAccountFields.style.display = 'block';
  } else {
    mobileMoneyFields.style.display = 'none';
    bankAccountFields.style.display = 'none';
  }
});
