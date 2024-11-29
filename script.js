// script.js

// Calculate total amount
function calculateTotal() {
    const rows = document.querySelectorAll("#basket-table tbody tr");
    let total = 0;

    rows.forEach((row) => {
        const price = parseFloat(row.cells[1].innerText.replace("$", ""));
        const quantity = parseInt(row.cells[2].innerText);
        total += price * quantity;
    });

    document.querySelector(".total-amount").innerText = `Total: $${total.toFixed(2)}`;
}

// Remove item from basket
document.addEventListener("click", (event) => {
    if (event.target.classList.contains("remove-item")) {
        const row = event.target.closest("tr");
        row.remove();
        calculateTotal();
    }
});

// Toggle basket visibility
function toggleBasket() {
    const basketSection = document.getElementById("basket-section");
    basketSection.classList.toggle("hidden");
}

// Initial calculation
calculateTotal();
// script.js

// Toggle between login and register forms
function toggleForm() {
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");
    const toggleText = document.getElementById("toggle-text");

    if (registerForm.classList.contains("hidden")) {
        registerForm.classList.remove("hidden");
        loginForm.classList.add("hidden");
        toggleText.innerHTML = 'Already have an account? <a href="#" onclick="toggleForm()">Log In</a>';
    } else {
        registerForm.classList.add("hidden");
        loginForm.classList.remove("hidden");
        toggleText.innerHTML = 'Don\'t have an account? <a href="#" onclick="toggleForm()">Create one</a>';
    }
}

// Handle registration submission
function submitRegistration() {
    const firstName = document.getElementById("first-name").value.trim();
    const lastName = document.getElementById("last-name").value.trim();
    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    // Validate input fields
    if (!firstName || !lastName || !email || !password || !confirmPassword) {
        alert("All fields are required!");
        return;
    }

    // Check if passwords match
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // Mock sending data to backend
    const userData = {
        firstName,
        lastName,
        email,
        password,
    };

    console.log("User registered:", userData);

    // Show success message and switch back to login form
    alert("Account created successfully! Please log in.");
    toggleForm();
}

// Handle login submission
function submitLogin() {
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;

    if (!email || !password) {
        alert("Email and password are required!");
        return;
    }

    console.log("User logged in:", { email, password });

    // Redirect to main page (mock)
    alert("Login successful!");
    window.location.href = "main.html";

    async function submitLogin() {
        const email = document.getElementById("login-email").value.trim();
        const password = document.getElementById("login-password").value;

        if (!email || !password) {
            alert("Email and password are required!");
            return;
        }

        // Send login request to the backend
        const response = await fetch("/api/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });

        const result = await response.json();

        if (result.success) {
            // Redirect to the main page
            alert(result.message);
            window.location.href = "main.html";
        } else {
            // Show error message
            alert(result.message);
        }
    }
    // Mock data for demonstration purposes
    const products = [
        { id: 1, name: "Moisturizing Cream", type: "skin-care" },
        { id: 2, name: "Acne Wash", type: "skin-care" },
        { id: 3, name: "Paracetamol", type: "medications" },
        { id: 4, name: "Vitamin C Tablets", type: "vitamins" },
        { id: 5, name: "Baby Shampoo", type: "baby-care" },
    ];

    // Search through all products (Main Search Bar)
    function searchAll() {
        const query = document.getElementById("main-search-bar").value.toLowerCase();
        const results = products.filter((product) =>
            product.name.toLowerCase().includes(query)
        );

        if (results.length > 0) {
            alert("Search Results: " + results.map((p) => p.name).join(", "));
        } else {
            alert("No products found.");
        }
    }

    // Search within a specific category
    function searchCategory(category) {
        const query = document.getElementById("category-search-bar").value.toLowerCase();
        const results = products.filter(
            (product) =>
                product.type === category && product.name.toLowerCase().includes(query)
        );

        if (results.length > 0) {
            alert("Search Results: " + results.map((p) => p.name).join(", "));
        } else {
            alert("No products found in this category.");
        }
    }


}


