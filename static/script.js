const button = document.querySelector('button');
const form = document.querySelector('form');
const input = document.querySelector('input');
// const cashflipForm = document.getElementById('cashflip-form');
// const cashflipBtn = document.getElementById('cashflip-btn');
// const result = document.getElementById('result');

// button.addEventListener('click', () => {
//   const value = input.value;
//   alert(`You entered: ${value}`);
// });

// form.addEventListener('submit', (event) => {
//   event.preventDefault();
//   const value = input.value;
//   alert(`You submitted: ${value}`);
// });

// cashflipForm.addEventListener('submit', (event) => {
//   event.preventDefault();
//   const amount = document.getElementById('amount').value;
//   fetch('/api/cashflip', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ amount })
//   })
//   .then(response => response.json())
//   .then(data => {
//     result.textContent = `You ${data.result} $${data.amount}`;
//   })
//   .catch(error => console.error(error));
// });
