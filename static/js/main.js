document.addEventListener('alpine:init', () => {

    // Глобальное хранилище для управления модальными окнами
    Alpine.store('modal', {
        isOpen: false,
        productId: null,

        open(id) {
            this.productId = id;
            this.isOpen = true;
        },
        close() {
            this.isOpen = false;
            // Сбрасываем ID после закрытия, чтобы избежать показа старых данных
            setTimeout(() => { this.productId = null; }, 300); 
        }
    });

    // Компонент для всплывающих уведомлений (тостов)
    Alpine.data('toastComponent', () => ({
        toasts: [],
        counter: 0,
        addToast(detail) {
            const id = this.counter++;
            const existingToast = this.toasts.find(t => t.message === detail.message);
            if (existingToast) return;

            this.toasts.push({
                id: id,
                message: detail.message,
                type: detail.type || 'info',
                visible: true
            });
            setTimeout(() => {
                this.removeToast(id);
            }, 5000);
        },
        removeToast(id) {
            const toast = this.toasts.find(t => t.id === id);
            if (toast) {
                toast.visible = false;
                setTimeout(() => {
                    this.toasts = this.toasts.filter(t => t.id !== id);
                }, 300);
            }
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
            this.query = '';
            this.suggestions = [];
        },

        async fetchSuggestions() {
            if (this.query.length < 2) {
                this.suggestions = [];
                return;
            }
            this.isLoading = true;
            try {
                const response = await fetch(`/api/search-suggest/?q=${encodeURIComponent(this.query)}`);
                if (!response.ok) throw new Error('Search API error');
                this.suggestions = await response.json();
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

        submitSearch() {
            if (this.query.length > 0) {
                this.$refs.searchForm.submit();
            }
        },

        init() {
            this.$watch('query', () => this.fetchSuggestions());
        }
    }));

    // Новый, улучшенный компонент для модального окна
    Alpine.data('quickViewModal', () => ({
        isLoading: false,
        product: null,
        
        init() {
            this.$watch('$store.modal.productId', (newId) => {
                if (newId) {
                    this.loadProduct(newId);
                } else {
                    this.product = null;
                }
            });
        },

        async loadProduct(productId) {
            this.isLoading = true;
            this.product = null;
            try {
                const response = await fetch(`/api/products/${productId}/`);
                if (!response.ok) throw new Error('Product not found');
                this.product = await response.json();
            } catch (error) {
                console.error('Quick view error:', error);
                this.$store.modal.close();
                window.dispatchEvent(new CustomEvent('show-toast', { detail: { message: 'Не удалось загрузить товар', type: 'error' } }));
            } finally {
                this.isLoading = false;
            }
        },

        formatPrice(price) { return parseFloat(price).toLocaleString('ru-RU', { minimumFractionDigits: 0, maximumFractionDigits: 0 }) + ' ₽'; }
    }));

    // Компонент для галереи на странице товара
    Alpine.data('productGallery', (initialImage) => ({
        mainImage: initialImage,
        changeImage(newImage) {
            if (this.mainImage !== newImage) {
                this.mainImage = newImage;
            }
        }
    }));
    
    // Компонент для каталога и AJAX фильтрации/пагинации
    Alpine.data('catalogFilter', () => ({
        isLoading: false,
        
        async fetchAndUpdate(url) {
            this.isLoading = true;
            try {
                const response = await fetch(url, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const html = await response.text();
                
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                const newContent = doc.getElementById('shop-content-wrapper').innerHTML;
                document.getElementById('shop-content-wrapper').innerHTML = newContent;

                window.history.pushState({}, '', url);
            } catch (error) {
                console.error("Filter/Pagination error:", error);
                window.location.href = url;
            } finally {
                setTimeout(() => { this.isLoading = false }, 300);
            }
        },

        applyFilters(event) {
            event.preventDefault();
            const form = event.target.closest('form');
            const params = new URLSearchParams(new FormData(form));
            const newUrl = `${window.location.pathname}?${params.toString()}`;
            this.fetchAndUpdate(newUrl);
        },

        init() {
            const formElement = this.$el.querySelector('form');
            if (formElement) {
                formElement.addEventListener('submit', (e) => this.applyFilters(e));
            }
            
            // Слушаем кастомное событие от пагинации
            window.addEventListener('filter-navigate', (event) => {
                this.fetchAndUpdate(event.detail.url);
            });
        }
    }));
});

// --- Глобальные функции ---
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

async function handleUserAction(button, entity, action, params = {}) {
    const productId = button.dataset.productId;
    if (!productId) return;

    const url = `/api/action/${entity}/${action}/`;
    const body = { product_id: productId, ...params };

    button.classList.add('is-loading');
    button.disabled = true;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `API Error: ${response.statusText}`);
        }

        if (data.status === 'ok') {
            window.dispatchEvent(new CustomEvent('show-toast', { detail: { message: data.message, type: 'success' } }));

            // Обновляем счетчики и иконки
            if (entity === 'wishlist') {
                const icon = button.querySelector('i.icon-default');
                if (icon) {
                    const isAdded = data.action === 'added';
                    icon.classList.toggle('far', !isAdded);
                    icon.classList.toggle('fas', isAdded);
                    icon.classList.toggle('text-sale-pink', isAdded);
                }
                window.dispatchEvent(new CustomEvent('update-wishlist-count', { detail: { count: data.wishlist_count } }));
            }
            if (entity === 'cart') {
                window.dispatchEvent(new CustomEvent('update-cart-count', { detail: { count: data.cart_unique_items_count } }));
            }
            if (entity === 'comparison') {
                const icon = button.querySelector('i.icon-default');
                if (icon) {
                    const isAdded = data.action === 'added';
                    icon.classList.toggle('text-lavender-dark', isAdded);
                }
                window.dispatchEvent(new CustomEvent('update-comparison-count', { detail: { count: data.comparison_count } }));
            }

        } else {
            window.dispatchEvent(new CustomEvent('show-toast', { detail: { message: data.error || 'Произошла ошибка', type: 'error' } }));
        }

    } catch (error)
        {
        console.error(`Action error (${entity}/${action}):`, error);
        window.dispatchEvent(new CustomEvent('show-toast', { detail: { message: error.message || 'Сетевая ошибка', type: 'error' } }));
    } finally {
        button.classList.remove('is-loading');
        button.disabled = false;
    }
}


document.addEventListener('DOMContentLoaded', () => {
    // Логика для кнопки "Наверх"
    const scrollTopBtn = document.getElementById('scrollTopBtn');
    if (scrollTopBtn) {
        let hideTimeout;
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