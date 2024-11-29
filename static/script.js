document.addEventListener("DOMContentLoaded", () => {
    console.log("Pharmacy website loaded!");

    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartButton = document.getElementById('cart-button');
    const cartDropdown = document.getElementById('cart-dropdown');
    const cartItemsList = document.getElementById('cart-items');
    const totalSumElement = document.getElementById('total-sum');


    function updateCartDisplay() {
        cartButton.innerText = `Cart (${cart.length})`;
        cartItemsList.innerHTML = cart.map((item, index) => `
            <li>
                ${item.drugname} - ${item.price} EGP
                <button class="remove-item" data-index="${index}">Remove</button>
            </li>
        `).join('');


        const totalSum = cart.reduce((sum, item) => sum + parseFloat(item.price), 0).toFixed(2);


        totalSumElement.innerText = `Total: ${totalSum} EGP`;
    }


    cartButton.addEventListener('click', () => {
        cartDropdown.style.display = cartDropdown.style.display === 'none' ? 'block' : 'none';
    });


    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', () => {
            const medicineItem = button.closest('.medicine-item');
            const medicineName = medicineItem.querySelector('h2').innerText;
            const medicinePrice = medicineItem.querySelector('p').innerText.split(":")[1].trim();

            const newItem = { drugname: medicineName, price: medicinePrice };

            cart.push(newItem);


            localStorage.setItem('cart', JSON.stringify(cart));


            updateCartDisplay();
        });
    });


    cartItemsList.addEventListener('click', (event) => {
        if (event.target.classList.contains('remove-item')) {
            const index = event.target.getAttribute('data-index');
            cart.splice(index, 1);


            localStorage.setItem('cart', JSON.stringify(cart));


            updateCartDisplay();
        }
    });


    updateCartDisplay();
});
