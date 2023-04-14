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


function calculateAmount() {
    // get input values
    const principal = parseFloat(document.getElementsByName("principal")[0].value);
    const time = parseFloat(document.getElementsByName("time")[0].value);
    const rate = parseFloat(document.getElementsByName("interest_rate")[0].value) / 100;

    // calculate monthly payment
    const amount = (principal+(principal * rate * time))/time;
    const label = document.getElementById("increase_size");
    if (isNaN(amount))
    {
        label.textContent = `GHc0/mon`;
    }
    else{
        // display result
    label.textContent = `GHc${amount.toFixed(2)}/mon`;
    }
    
  }