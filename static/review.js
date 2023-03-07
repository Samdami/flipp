const form = document.querySelector('#review-form');
const nameInput = document.querySelector('#name');
const ratingInput = document.querySelector('#rating');
const reviewInput = document.querySelector('#review');
const reviewList = document.querySelector('#review-list');

form.addEventListener('submit', function(event) {
  event.preventDefault();
  
  const name = nameInput.value;
  const rating = ratingInput.value;
  const review = reviewInput.value;
  
  const listItem = document.createElement('li');
  const ratingStars = '★'.repeat(rating) + '☆'.repeat(5 - rating);
  
  listItem.innerHTML = `
    <h4>${name} - ${ratingStars}</h4>
    <p>${review}</p>
  `;
  
  reviewList.appendChild(listItem);
  
  nameInput.value = '';
  ratingInput.value = '';
  reviewInput.value = '';
});
