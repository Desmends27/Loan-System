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

const progressBar = document.querySelector('.progress');
const max = 100; // maximum progress value
let progress = 0; // current progress value

function updateProgress(value) {
  progress = value;
  progressBar.style.width = `${progress}%`;
}

// example usage
updateProgress(50); // sets progress to 50%

function calculateAmount() {
    // get input values
    const principal = parseFloat(document.getElementsByName("principal")[0].value);
    const time = parseFloat(document.getElementsByName("time")[0].value);
    const rate = parseFloat(document.getElementsByName("interest_rate")[0].value) / 100;

    // calculate monthly payment
    const n = time * 12;
    const r = rate / 12;
    const amount = (principal * r * (1 + r) ** n) / ((1 + r) ** n - 1);
    const label = document.getElementById("increase_size");
    if (isNaN(amount))
    {
        label.textContent = `$0/mon`;
    }
    else{
        // display result
    label.textContent = `$${amount.toFixed(2)}/mon`;
    }
    
  }