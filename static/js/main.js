document.addEventListener('alpine:init', () => {
    
    // Компонент для всплывающих уведомлений (тостов)
    Alpine.data('toastComponent', () => ({
        toasts: [],
        counter: 0,
        addToast(detail) {
            const id = this.counter++;
            this.toasts.push({ id: id, message: detail.message, type: detail.type || 'info', visible: true });
            setTimeout(() => { this.removeToast(id); }, 5000);
        },
        removeToast(id) {
            const toast = this.toasts.find(t => t.id === id);
            if (toast) { toast.visible = false; }
        }
    }));

    // Компонент поиска
    Alpine.data('searchComponent', () => ({
        searchOpen: false,
        query: '',
        suggestions: [], 
        isLoading: false,
        
        openSearch() {
            this.searchOpen = true;
            this.$nextTick(() => this.$refs.searchInput.focus());
        },
        closeSearch() {
            this.searchOpen = false;
        },
        
        async fetchSuggestions() {
            if (this.query.length < 2) {
                this.suggestions = [];
                return;
            }
            this.isLoading = true;
            try {
                const response = await fetch(`/api/search-suggest/?q=${encodeURIComponent(this.query)}`);
                const data = await response.json();
                this.suggestions = data;
            } catch (error) {
                console.error('Ошибка получения подсказок:', error);
                this.suggestions = [];
            } finally {
                this.isLoading = false;
            }
        },
        
        highlightMatch(suggestion) {
            if (!this.query) return suggestion;
            const regex = new RegExp(`(${this.query})`, 'gi');
            return suggestion.replace(regex, '<strong class="text-lavender-deep">$1</strong>');
        },
        
        init() {
            this.$watch('query', () => this.fetchSuggestions());
        }
    }));

    // Компонент для управления страницей корзины
    Alpine.data('cartPage', (initialItems) => ({
        items: initialItems,
        totalPrice: 0,
        itemCount: 0, 

        init() {
            this.recalculateTotals();
        },
        
        recalculateTotals() {
            let count = 0;
            let total = 0;
            this.items.forEach(item => {
                count += item.quantity;
                total += item.price * item.quantity;
            });
            this.itemCount = count;
            this.totalPrice = total;
        },

        updateQuantity(item, newQuantity) {
            if (newQuantity < 1) { this.removeItem(item); return; }
            item.quantity = newQuantity;

            const formData = new FormData();
            formData.append('quantity', newQuantity);
            formData.append('update', 'True');
            
            const updateUrl = `/cart/add/${item.id}/`;
            
            fetch(updateUrl, { 
                method: 'POST', 
                body: formData, 
                headers: { 
                    'X-CSRFToken': getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest' 
                }
            })
            .then(res => res.json()).then(data => {
                if (data.status === 'ok') {
                    this.totalPrice = parseFloat(data.cart_total.replace(/\s/g, ''));
                    this.recalculateTotals(); 
                    window.dispatchEvent(new CustomEvent('update-cart-count', { detail: { count: data.cart_count } }));
                }
            });
        },
        removeItem(itemToRemove) {
            fetch(itemToRemove.removeUrl, { 
                method: 'POST', 
                headers: { 
                    'X-CSRFToken': getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest' 
                }})
            .then(res => res.json()).then(data => {
                if (data.status === 'ok') {
                    this.items = this.items.filter(i => i.id !== itemToRemove.id);
                    this.totalPrice = parseFloat(data.cart_total.replace(/\s/g, '') || 0);
                    this.recalculateTotals();
                    window.dispatchEvent(new CustomEvent('update-cart-count', { detail: { count: data.cart_count } }));
                    window.dispatchEvent(new CustomEvent('show-toast', { detail: { message: `"${data.product_name}" удален`, type: 'info' } }));
                }
            });
        },
        formatPrice(price) { return price.toLocaleString('ru-RU', { minimumFractionDigits: 0, maximumFractionDigits: 0 }) + ' ₽'; }
    }));

    // НОВЫЙ КОМПОНЕНТ: Слайдер для диапазона цен
    Alpine.data('priceRangeSlider', (initialMin, initialMax, absMin, absMax) => ({
        minPrice: initialMin,
        maxPrice: initialMax,
        absMin: absMin,
        absMax: absMax,
        minPercent: 0,
        maxPercent: 100,

        init() {
            this.updatePercentages();
        },

        updatePercentages() {
            this.minPercent = ((this.minPrice - this.absMin) / (this.absMax - this.absMin)) * 100;
            this.maxPercent = ((this.maxPrice - this.absMin) / (this.absMax - this.absMin)) * 100;
        },

        updateMin() {
            if (this.minPrice >= this.maxPrice) {
                this.minPrice = this.maxPrice - 1;
            }
            this.updatePercentages();
        },

        updateMax() {
            if (this.maxPrice <= this.minPrice) {
                this.maxPrice = this.minPrice + 1;
            }
            this.updatePercentages();
        }
    }));
});

const getCsrfToken = () => document.querySelector('meta[name="csrf-token"]').getAttribute('content');


document.addEventListener('DOMContentLoaded', () => {
    // Логика для кнопки "Наверх"
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    let hideTimeout; 
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                clearTimeout(hideTimeout);
                scrollTopBtn.classList.remove('hidden');
                setTimeout(() => scrollTopBtn.classList.remove('opacity-0'), 10);
            } else {
                scrollTopBtn.classList.add('opacity-0');
                hideTimeout = setTimeout(() => scrollTopBtn.classList.add('hidden'), 300);
            }
        });
    }

    document.body.addEventListener('click', e => {
        const wishlistBtn = e.target.closest('.wishlist-btn-v2');
        if (!wishlistBtn) return;
        e.preventDefault();

        const isAdded = wishlistBtn.querySelector('i').classList.contains('fas');
        const url = isAdded ? wishlistBtn.dataset.removeUrl : wishlistBtn.dataset.addUrl;
        
        fetch(url, { 
            method: 'POST', 
            headers: { 
                'X-CSRFToken': getCsrfToken(), 
                'X-Requested-With': 'XMLHttpRequest' 
            }
        })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            return res.json();
        })
        .then(data => {
            if (data.status === 'ok') {
                const icon = wishlistBtn.querySelector('i');
                icon.classList.toggle('far');
                icon.classList.toggle('fas');
                window.dispatchEvent(new CustomEvent('update-wishlist-count', { detail: { count: data.count } }));
            } else {
                console.error("Ошибка при обновлении избранного:", data);
            }
        })
        .catch(error => {
            console.error('Сетевая ошибка или ошибка JS при обновлении избранного:', error);
            window.dispatchEvent(new CustomEvent('show-toast', { detail: { message: `Сетевая ошибка`, type: 'error' } }));
        });
    });

    document.body.addEventListener('click', e => {
        const addToCartBtn = e.target.closest('.add-to-cart-btn');
        if (!addToCartBtn) return;
        e.preventDefault();

        const url = addToCartBtn.dataset.url;
        const formData = new FormData();
        formData.append('quantity', '1');
        formData.append('update', 'False');
        
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 
                'X-CSRFToken': getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest' 
            }
        })
        .then(res => {
             if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            return res.json();
        })
        .then(data => {
            if (data.status === 'ok') {
                window.dispatchEvent(new CustomEvent('update-cart-count', { detail: { count: data.cart_count } }));
                window.dispatchEvent(new CustomEvent('show-toast', { detail: { message: `Товар "${data.product_name}" добавлен`, type: 'success' } }));
            } else {
                window.dispatchEvent(new CustomEvent('show-toast', { detail: { message: `Ошибка: ${data.error || 'не удалось добавить товар'}`, type: 'error' } }));
            }
        }).catch(err => {
            console.error('Ошибка при добавлении в корзину:', err);
            window.dispatchEvent(new CustomEvent('show-toast', { detail: { message: `Сетевая ошибка`, type: 'error' } }));
        });
    });

    // Эффект "пузырьков" для кнопок
    document.body.addEventListener('click', e => {
        const rippleBtn = e.target.closest('.ripple-btn');
        if (!rippleBtn) return;

        const circle = document.createElement('span');
        const diameter = Math.max(rippleBtn.clientWidth, rippleBtn.clientHeight);
        const radius = diameter / 2;

        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${e.clientX - (rippleBtn.getBoundingClientRect().left + radius)}px`;
        circle.style.top = `${e.clientY - (rippleBtn.getBoundingClientRect().top + radius)}px`;
        circle.classList.add('ripple');
        
        const ripple = rippleBtn.getElementsByClassName('ripple')[0];
        if (ripple) {
            ripple.remove();
        }
        
        rippleBtn.appendChild(circle);
    });
});