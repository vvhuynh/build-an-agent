// AI Grocery Agent Web Application JavaScript

// Global variables
let currentChatResponse = '';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 AI Grocery Agent Web Interface initialized');
    
    // Load recipe browser and store information
    loadRecipeBrowser();
    loadStoreInformation();
    
    // Set up form handlers
    setupFormHandlers();
});

// Set up form event handlers
function setupFormHandlers() {
    // Shopping form submission
    const shoppingForm = document.getElementById('shoppingForm');
    if (shoppingForm) {
        shoppingForm.addEventListener('submit', function(e) {
            e.preventDefault();
            generateShoppingList();
        });
    }
    
    // Chat form submission
    const chatMessage = document.getElementById('chatMessage');
    if (chatMessage) {
        chatMessage.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendChat();
            }
        });
    }
}

// Generate shopping list
async function generateShoppingList() {
    const foodItem = document.getElementById('foodItem').value.trim();
    const budget = document.getElementById('budget').value;
    const maxStores = document.getElementById('maxStores').value;
    const priceRange = document.getElementById('priceRange').value;
    
    if (!foodItem) {
        showMessage('Please enter a food item to cook!', 'error');
        return;
    }
    
    // Show loading state
    showLoading(true);
    hideResults();
    
    try {
        const response = await fetch('/api/shop', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                food_item: foodItem,
                budget: budget ? parseFloat(budget) : null,
                max_stores: parseInt(maxStores),
                price_range: priceRange
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayShoppingList(data.shopping_list);
            showResults();
        } else {
            showMessage('Error generating shopping list: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showMessage('Network error. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
}

// Send chat message
async function sendChat() {
    const messageInput = document.getElementById('chatMessage');
    const message = messageInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Clear input
    messageInput.value = '';
    
    // Show loading state
    const chatResponse = document.getElementById('chatResponse');
    const chatText = document.getElementById('chatText');
    
    chatResponse.classList.remove('d-none');
    chatText.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>AI is thinking...';
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            chatText.innerHTML = data.response;
        } else {
            chatText.innerHTML = 'Sorry, I encountered an error. Please try again.';
        }
    } catch (error) {
        console.error('Error:', error);
        chatText.innerHTML = 'Network error. Please try again.';
    }
}

// Quick shop function
function quickShop(foodItem) {
    document.getElementById('foodItem').value = foodItem;
    generateShoppingList();
}

// Quick chat function
function quickChat(question) {
    document.getElementById('chatMessage').value = question;
    sendChat();
}

// Load recipe browser
async function loadRecipeBrowser() {
    const recipeBrowser = document.getElementById('recipeBrowser');
    
    try {
        const response = await fetch('/api/recipes');
        const data = await response.json();
        
        if (data.success) {
            let html = '';
            for (const [category, recipes] of Object.entries(data.recipes)) {
                html += `<div class="recipe-category">
                    <h6><i class="fas fa-utensils me-2"></i>${category}</h6>
                    <div>`;
                
                recipes.forEach(recipe => {
                    html += `<span class="recipe-item" onclick="quickShop('${recipe}')">${recipe}</span>`;
                });
                
                html += `</div></div>`;
            }
            recipeBrowser.innerHTML = html;
        } else {
            recipeBrowser.innerHTML = '<p class="text-muted">Failed to load recipes</p>';
        }
    } catch (error) {
        console.error('Error loading recipes:', error);
        recipeBrowser.innerHTML = '<p class="text-muted">Failed to load recipes</p>';
    }
}

// Load store information
async function loadStoreInformation() {
    const storeInfo = document.getElementById('storeInfo');
    
    try {
        const response = await fetch('/api/stores');
        const data = await response.json();
        
        if (data.success) {
            let html = '';
            for (const [store, description] of Object.entries(data.stores)) {
                html += `<div class="store-item">
                    <div class="store-name">${store}</div>
                    <p class="store-description">${description}</p>
                </div>`;
            }
            storeInfo.innerHTML = html;
        } else {
            storeInfo.innerHTML = '<p class="text-muted">Failed to load store information</p>';
        }
    } catch (error) {
        console.error('Error loading stores:', error);
        storeInfo.innerHTML = '<p class="text-muted">Failed to load store information</p>';
    }
}

// Display shopping list
function displayShoppingList(shoppingList) {
    const shoppingListElement = document.getElementById('shoppingList');
    if (shoppingListElement) {
        shoppingListElement.textContent = shoppingList;
    }
}

// Show/hide loading state
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (loading) {
        if (show) {
            loading.classList.remove('d-none');
        } else {
            loading.classList.add('d-none');
        }
    }
}

// Show/hide results
function showResults() {
    const results = document.getElementById('results');
    if (results) {
        results.classList.remove('d-none');
        results.classList.add('fade-in');
    }
}

function hideResults() {
    const results = document.getElementById('results');
    if (results) {
        results.classList.add('d-none');
        results.classList.remove('fade-in');
    }
}

// Show message
function showMessage(message, type = 'info') {
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type === 'error' ? 'danger' : 'info'} message-${type}`;
    messageDiv.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : 'info-circle'} me-2"></i>
        ${message}
    `;
    
    // Insert at the top of the main container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(messageDiv, container.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 5000);
    }
}

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Utility function to debounce API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add smooth scrolling for better UX
function smoothScrollTo(element) {
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Handle keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit shopping form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const shoppingForm = document.getElementById('shoppingForm');
        if (shoppingForm) {
            generateShoppingList();
        }
    }
    
    // Escape to clear forms
    if (e.key === 'Escape') {
        const foodItem = document.getElementById('foodItem');
        const chatMessage = document.getElementById('chatMessage');
        if (foodItem) foodItem.value = '';
        if (chatMessage) chatMessage.value = '';
    }
});

// Add tooltips for better UX
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});

// Export functions for global access
window.generateShoppingList = generateShoppingList;
window.sendChat = sendChat;
window.quickShop = quickShop;
window.quickChat = quickChat; 