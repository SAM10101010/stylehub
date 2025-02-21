let currentIndex = 0;
const productsContainer = document.querySelector('.carousel-container');
const itemWidth = 200 + 20; // Assuming each product card is 200px wide with 20px gap

// Sample data for most popular products
const mostPopularProducts = [
    { name: 'Sweatshirt', price: '$49.99', image: 'https://via.placeholder.com/200' },
    { name: 'Sweatpant', price: '$59.99', image: 'https://via.placeholder.com/200' },
    { name: 'Oversize Sweater', price: '$69.99', image: 'https://via.placeholder.com/200' },
    { name: 'Mini Skirt', price: '$79.99', image: 'https://via.placeholder.com/200' }
];

function initializeProducts() {
    const productList = document.getElementById('product-list');
    productList.innerHTML = ''; // Clear previous products

    mostPopularProducts.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product-item');
        productDiv.innerHTML = `
            <span class="favorite" onclick="toggleFavorite(this)">&#9825;</span>
            <img src="${product.image}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>${product.price}</p>
        `;
        productList.appendChild(productDiv);
    });
}

function moveCarousel(direction) {
    const productItems = document.querySelectorAll('.product-item');
    const maxIndex = Math.ceil((productItems.length - 4) / 4);

    currentIndex += direction;

    if (currentIndex < 0) {
        currentIndex = 0;
    } else if (currentIndex > maxIndex) {
        currentIndex = maxIndex;
    }

    const translateX = -currentIndex * 4 * itemWidth;
    productsContainer.style.transform = `translateX(${translateX}px)`;
}

function toggleFavorite(element) {
    element.classList.toggle('filled');
    if (element.classList.contains('filled')) {
        element.innerHTML = '&#9829;';
    } else {
        element.innerHTML = '&#9825;';
    }
}

// Initialize the products when the page loads
document.addEventListener('DOMContentLoaded', initializeProducts);