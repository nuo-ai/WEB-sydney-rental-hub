// --- Sydney Student Rental Hub - Main JavaScript (Final Version) ---

import config from './config.js';

document.addEventListener('DOMContentLoaded', () => {

    // --- 0. UI ENHANCEMENT SYSTEM ---
    class UIEnhancer {
        constructor() {
            this.isEnhanced = localStorage.getItem('ui-enhanced') === 'true';
            this.init();
        }
        
        init() {
            this.createToggleButton();
            if (this.isEnhanced) {
                this.enableEnhancements();
            }
        }
        
        createToggleButton() {
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'ui-toggle-btn';
            toggleBtn.textContent = this.isEnhanced ? '回到原版' : '启用增强UI';
            toggleBtn.onclick = () => this.toggle();
            document.body.appendChild(toggleBtn);
        }
        
        toggle() {
            this.isEnhanced = !this.isEnhanced;
            localStorage.setItem('ui-enhanced', this.isEnhanced);
            
            if (this.isEnhanced) {
                this.enableEnhancements();
            } else {
                this.disableEnhancements();
            }
            
            // 更新按钮文字
            document.querySelector('.ui-toggle-btn').textContent = 
                this.isEnhanced ? '回到原版' : '启用增强UI';
        }
        
        enableEnhancements() {
            document.body.classList.add('ui-enhanced');
            // 重新渲染房源卡片以应用新样式
            if (window.lastFilteredProperties) {
                this.updateExistingCards();
            }
        }
        
        disableEnhancements() {
            document.body.classList.remove('ui-enhanced');
        }
        
        updateExistingCards() {
            // 为现有卡片添加必要的CSS类
            const cards = document.querySelectorAll('.card-container');
            cards.forEach(card => {
                card.classList.add('property-card');
                
                // 更新价格显示
                const priceElement = card.querySelector('.text-2xl.font-extrabold');
                if (priceElement) {
                    priceElement.classList.add('property-price');
                    const unitElement = priceElement.querySelector('span');
                    if (unitElement) {
                        unitElement.classList.add('property-price-unit');
                    }
                }
                
                // 更新地址显示
                const addressPrimary = card.querySelector('.text-lg.font-semibold');
                if (addressPrimary) {
                    addressPrimary.classList.add('property-address-primary');
                }
                
                const addressSecondary = card.querySelector('.text-base.text-textSecondary');
                if (addressSecondary) {
                    addressSecondary.classList.add('property-address-secondary');
                }
                
                // 更新房型信息
                const featuresContainer = card.querySelector('.flex.items-center.gap-4.mt-3');
                if (featuresContainer) {
                    featuresContainer.classList.add('property-features');
                    
                    const featureItems = featuresContainer.querySelectorAll('.flex.items-center.gap-2');
                    featureItems.forEach(item => {
                        item.classList.add('feature-item');
                        const number = item.querySelector('.font-bold');
                        if (number) {
                            number.classList.add('feature-number');
                        }
                        const icon = item.querySelector('i');
                        if (icon) {
                            icon.classList.add('feature-icon');
                        }
                    });
                }
                
                // 更新图片容器
                const imageCarousel = card.querySelector('.image-carousel img');
                if (imageCarousel) {
                    imageCarousel.parentElement.classList.add('property-image');
                }
            });
        }
    }

    // 初始化UI增强器
    const uiEnhancer = new UIEnhancer();

    // --- 1. FAVORITES UTILITIES ---
    const favoritesManager = {
        key: 'rentalHubFavorites',
        getFavorites() {
            return JSON.parse(localStorage.getItem(this.key)) || [];
        },
        isFavorite(id) {
            return this.getFavorites().includes(String(id));
        },
        toggleFavorite(id, buttonElement) {
            const favorites = this.getFavorites();
            const icon = buttonElement.querySelector('i');
            if (favorites.includes(String(id))) {
                const updatedFavorites = favorites.filter(favId => favId !== String(id));
                localStorage.setItem(this.key, JSON.stringify(updatedFavorites));
                buttonElement.classList.remove('is-favorite');
                icon.classList.replace('fa-solid', 'fa-regular');
            } else {
                favorites.push(String(id));
                localStorage.setItem(this.key, JSON.stringify(favorites));
                buttonElement.classList.add('is-favorite');
                icon.classList.replace('fa-regular', 'fa-solid');
            }
        }
    };

    // --- 2. CONFIGURATION & DOM ELEMENTS ---
    const API_URL = config.API_URL;
    const listingsContainer = document.querySelector('#listings-container');
    const searchInput = document.getElementById('search-input');
    const filterButton = document.getElementById('filter-button');
    const resultsSummaryContainer = document.getElementById('results-summary-container');
    const filterPanelContainer = document.getElementById('filter-panel-container');
    
    // --- 3. STATE MANAGEMENT ---
    let allProperties = []; 
    let activeFilters = {
        searchTerm: '', minPrice: null, maxPrice: null, bedrooms: 'any', 
        bathrooms: 'any', availableDate: 'any', isFurnished: false
    };

    // --- 4. CORE FUNCTIONS ---

    async function fetchData(filters = {}) {
        // 构建查询参数字符串
        const params = new URLSearchParams();
        if (filters.suburb) params.append('suburb', filters.suburb);
        if (filters.bedrooms_min) params.append('bedrooms_min', filters.bedrooms_min);
        if (filters.rent_min) params.append('rent_min', filters.rent_min);
        if (filters.rent_max) params.append('rent_max', filters.rent_max);
        // 可以根据需要添加更多筛选参数
        params.append('page_size', 100); // 后端限制最大为100

        const url = `${API_URL}/properties?${params.toString()}`;
        console.log('🔍 正在请求URL:', url);

        try {
            const response = await fetch(url);
            console.log('📡 响应状态:', response.status, response.statusText);

            if (!response.ok) {
                throw new Error(`网络响应错误: ${response.status} ${response.statusText}`);
            }

            const result = await response.json();
            console.log('📊 API响应结果:', result);

            if (result.error) {
                throw new Error(`API 错误: ${result.error.message}`);
            }
            
            console.log('✅ 成功获取房源数据，数量:', result.data?.length || 0);
            // RESTful API 返回的数据结构是 result.data
            return result.data;

        } catch (error) {
            console.error('❌ 从 RESTful API 获取数据失败:', error);
            renderError('无法连接到房源数据库。请检查您的网络连接或稍后再试。');
            return null;
        }
    }

    async function applyFiltersAndRender() {
        // university search is deprecated
        if (!allProperties || allProperties.length === 0) {
            renderError('没有找到匹配的房源。请尝试其他关键词或调整筛选条件。');
            return;
        }
        var propertiesData = allProperties;
        
        let filteredProperties = [...propertiesData];
        const searchTerm = activeFilters.searchTerm.toLowerCase();
        if (searchTerm) {
            filteredProperties = filteredProperties.filter(p =>
                (p.address || '').toLowerCase().includes(searchTerm) ||
                (p.suburb || '').toLowerCase().includes(searchTerm) ||
                (p.postcode || '').toLowerCase().includes(searchTerm)
            );
        }
        if (activeFilters.minPrice) {
            filteredProperties = filteredProperties.filter(p => (p.rent_pw ? parseInt(p.rent_pw, 10) >= activeFilters.minPrice : true));
        }
        if (activeFilters.maxPrice) {
            filteredProperties = filteredProperties.filter(p => (p.rent_pw ? parseInt(p.rent_pw, 10) <= activeFilters.maxPrice : true));
        }
        if (activeFilters.bedrooms !== 'any') {
            if (activeFilters.bedrooms === 'studio/1') {
                filteredProperties = filteredProperties.filter(p => p.bedrooms === 0 || p.bedrooms === 1);
            } else if (String(activeFilters.bedrooms).includes('+')) {
                const minBeds = parseInt(activeFilters.bedrooms, 10);
                filteredProperties = filteredProperties.filter(p => (p.bedrooms ? parseInt(p.bedrooms, 10) >= minBeds : false));
            } else {
                filteredProperties = filteredProperties.filter(p => String(p.bedrooms) === activeFilters.bedrooms);
            }
        }
        if (activeFilters.bathrooms !== 'any') {
            if (String(activeFilters.bathrooms).includes('+')) {
                const minBaths = parseInt(activeFilters.bathrooms, 10);
                filteredProperties = filteredProperties.filter(p => (p.bathrooms ? parseInt(p.bathrooms, 10) >= minBaths : false));
            } else {
                filteredProperties = filteredProperties.filter(p => String(p.bathrooms) === activeFilters.bathrooms);
            }
        }
        if (activeFilters.availableDate !== 'any') {
            const filterDate = new Date(activeFilters.availableDate);
            filteredProperties = filteredProperties.filter(p => {
                if (!p.available_date) return false;
                const propertyDate = new Date(p.available_date);
                return propertyDate <= filterDate;
            });
        }
        if (activeFilters.isFurnished) {
            filteredProperties = filteredProperties.filter(p => p.is_furnished === true);
        }
        renderListings(filteredProperties);
        updateResultsCount(filteredProperties.length);
    }

    function renderListings(properties) {
        if (!listingsContainer) return;
        listingsContainer.innerHTML = ''; 
        if (!properties || properties.length === 0) {
            renderError('没有找到匹配的房源。请尝试其他关键词或调整筛选条件。');
            return;
        }
        properties.forEach((property) => {
             if (property && property.listing_id) {
                listingsContainer.insertAdjacentHTML('beforeend', createListingCard(property));
             }
        });
    }

    function createListingCard(property) {
        const streetAddress = property.address || '地址未知';
        const bedrooms = property.bedrooms || 0;
        const bathrooms = property.bathrooms || 0;
        const parking = property.parking_spaces || 0;
        const availableDate = property.available_date || '待定';
        const rent = property.rent_pw ? `$${property.rent_pw}` : '价格待定';
        const placeholderSvg = `<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#E3E3E3"/><text x="50%" y="50%" font-family="Inter, sans-serif" font-size="200" dy=".3em" fill="white" text-anchor="middle">?</text></svg>`;
        const placeholderUrl = `data:image/svg+xml,${encodeURIComponent(placeholderSvg)}`;
        let imageList = [];
        const imagesData = property.images;
        if (Array.isArray(imagesData)) {
            imageList = imagesData;
        }
        const coverImage = (imageList.length > 0) ? imageList[0] : placeholderUrl;
        
        const isFavorite = favoritesManager.isFavorite(property.listing_id);
        const favoriteClass = isFavorite ? 'is-favorite' : '';
        const favoriteIcon = isFavorite ? 'fa-solid' : 'fa-regular';

        const carouselControls = imageList.length > 1 ? `
            <button class="carousel-btn absolute top-1/2 left-2 -translate-y-1/2 bg-black/40 text-white w-8 h-8 rounded-full flex items-center justify-center hover:bg-black/60 transition" data-direction="prev"><i class="fa-solid fa-chevron-left pointer-events-none"></i></button>
            <button class="carousel-btn absolute top-1/2 right-2 -translate-y-1/2 bg-black/40 text-white w-8 h-8 rounded-full flex items-center justify-center hover:bg-black/60 transition" data-direction="next"><i class="fa-solid fa-chevron-right pointer-events-none"></i></button>
            <div class="image-counter absolute bottom-2 right-2 bg-black/50 text-white text-xs font-semibold px-2 py-1 rounded-full">1 / ${imageList.length}</div>` : '';
        
        const isNew = property.listing_id > 2500; // Example logic for "New" tag
        const newTag = isNew ? `<div class="property-tag absolute top-3 left-3 bg-blue-500 text-white text-xs font-bold px-2 py-1 rounded">新房源</div>` : '';

        return `
            <div class="card-container property-card bg-bgCard rounded-lg shadow-sm overflow-hidden flex flex-col">
                <div class="image-carousel property-image relative" data-images='${JSON.stringify(imageList)}' data-current-index="0">
                    <a href="./details.html?id=${property.listing_id}" class="block h-52">
                        <img src="${coverImage}" alt="房源图片: ${streetAddress}" class="w-full h-full object-cover image-tag">
                    </a>
                    ${carouselControls}
                    ${newTag}
                    <button class="favorite-btn ${favoriteClass}" data-listing-id="${property.listing_id}">
                        <i class="${favoriteIcon} fa-heart"></i>
                    </button>
                </div>
                <div class="p-4 flex flex-col flex-grow">
                    <div class="flex-grow">
                        <p class="property-price text-2xl font-extrabold text-textPrice">${rent}<span class="property-price-unit text-base font-medium text-textSecondary"> / week</span></p>
                        <div class="mt-1">
                            <p class="property-address-primary text-lg font-semibold text-textPrimary">${streetAddress}</p>
                        </div>
                        <div class="property-features flex items-center gap-4 mt-3 text-textSecondary">
                            <div class="feature-item flex items-center gap-2">
                                <i class="feature-icon fa-solid fa-bed text-lg w-5 text-center"></i>
                                <span class="feature-number font-bold text-textPrimary">${bedrooms}</span>
                            </div>
                            <div class="feature-item flex items-center gap-2">
                                <i class="feature-icon fa-solid fa-bath text-lg w-5 text-center"></i>
                                <span class="feature-number font-bold text-textPrimary">${bathrooms}</span>
                            </div>
                            <div class="feature-item flex items-center gap-2">
                                <i class="feature-icon fa-solid fa-car text-lg w-5 text-center"></i>
                                <span class="feature-number font-bold text-textPrimary">${parking}</span>
                            </div>
                        </div>
                    </div>
                    <div class="property-footer mt-4 pt-3 border-t border-borderDefault flex justify-between items-center">
                         <div class="flex items-center gap-2 text-xs text-green-600 font-bold">
                            <i class="fa-regular fa-calendar-check"></i>
                            <span>${availableDate}</span>
                        </div>
                        <span class="text-xs text-textSecondary">ID: ${property.listing_id}</span>
                    </div>
                </div>
                <style>
                    .favorite-btn { position: absolute; top: 12px; right: 12px; background: rgba(255,255,255,0.8); backdrop-filter: blur(4px); width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #2d2d2d; font-size: 18px; transition: all 0.2s; z-index: 10; cursor: pointer; border: none; }
                    .favorite-btn.is-favorite { color: #ef4444; transform: scale(1.1); }
                    .favorite-btn:hover { color: #ef4444; }
                </style>
            </div>`;
    }

    function updateResultsCount(count) {
        resultsSummaryContainer.innerHTML = `<p class="font-semibold text-textPrimary">${count} results found</p>`;
    }

    function renderError(message) {
        if (!listingsContainer) return;
        listingsContainer.innerHTML = `<div class="text-center text-textSecondary py-10"><p class="font-bold">${message}</p></div>`;
    }

    // --- 5. EVENT LISTENERS & UI BINDING ---

    function handleInteraction(event) {
        const carouselBtn = event.target.closest('.carousel-btn');
        const favoriteBtn = event.target.closest('.favorite-btn');

        if (carouselBtn) {
            event.preventDefault();
            event.stopPropagation();
            const carousel = carouselBtn.closest('.image-carousel');
            const imageTag = carousel.querySelector('.image-tag');
            const counter = carousel.querySelector('.image-counter');
            const direction = carouselBtn.dataset.direction;
            const images = JSON.parse(carousel.dataset.images);
            let currentIndex = parseInt(carousel.dataset.currentIndex, 10);
            if (direction === 'next') currentIndex = (currentIndex + 1) % images.length;
            else currentIndex = (currentIndex - 1 + images.length) % images.length;
            imageTag.src = images[currentIndex];
            if (counter) counter.textContent = `${currentIndex + 1} / ${images.length}`;
            carousel.dataset.currentIndex = currentIndex;
        }
        
        if (favoriteBtn) {
            event.preventDefault();
            event.stopPropagation();
            const listingId = favoriteBtn.dataset.listingId;
            favoritesManager.toggleFavorite(listingId, favoriteBtn);
        }
    }
    
    function toggleFilterPanel(show) {
        const panel = document.getElementById('filter-panel');
        const overlay = document.getElementById('filter-overlay');
        if (panel && overlay) {
            if (show) {
                panel.classList.remove('translate-y-full');
                overlay.classList.remove('opacity-0', 'pointer-events-none');
            } else {
                panel.classList.add('translate-y-full');
                overlay.classList.add('opacity-0', 'pointer-events-none');
            }
        }
    }
    
    function populateDateFilter() {
        const dateSelect = document.getElementById('filter-available-date');
        if (!dateSelect) return;
        const dates = allProperties.map(p => p.available_date ? new Date(p.available_date) : null).filter(Boolean).sort((a, b) => a - b);
        if (dates.length === 0) return;
        const options = [ { value: 'any', text: 'Any Date' } ];
        const today = new Date();
        if (dates.some(d => d <= today)) {
             options.push({ value: today.toISOString().split('T')[0], text: 'Available now' });
        }
        const addDays = (date, days) => { const result = new Date(date); result.setDate(result.getDate() + days); return result; };
        const formatDate = (date) => `Before ${date.toLocaleDateString('en-AU', { weekday: 'short', day: 'numeric', month: 'short' })}`;
        for (let i = 1; i <= 7; i++) {
             const futureDate = addDays(today, i);
             options.push({ value: futureDate.toISOString().split('T')[0], text: formatDate(futureDate) });
        }
        const latestDate = dates[dates.length - 1];
        if (latestDate > addDays(today, 7)) {
            options.push({ value: latestDate.toISOString().split('T')[0], text: `Up to ${latestDate.toLocaleDateString('en-AU', {day: 'numeric', month: 'short', year: 'numeric'})}` });
        }
        const uniqueOptions = options.filter((option, index, self) => index === self.findIndex((o) => o.value === option.value));
        dateSelect.innerHTML = uniqueOptions.map(opt => `<option value="${opt.value}">${opt.text}</option>`).join('');
    }

    function setupFilterPanelEventListeners() {
        const closeBtn = document.getElementById('close-filter-panel');
        const overlay = document.getElementById('filter-overlay');
        const applyBtn = document.getElementById('apply-filters');
        const resetBtn = document.getElementById('reset-filters');
        const bedroomsGroup = document.getElementById('filter-bedrooms');
        const bathroomsGroup = document.getElementById('filter-bathrooms');
        const priceSlider = document.getElementById('price-slider');
        const priceDisplay = document.getElementById('price-range-display');
        const dateSelect = document.getElementById('filter-available-date');
        const furnishedToggle = document.getElementById('filter-furnished');

        const rents = allProperties.map(p => p.rent_pw ? parseInt(p.rent_pw, 10) : 0).filter(Boolean);
        const minRent = rents.length > 0 ? Math.floor(Math.min(...rents) / 10) * 10 : 0;
        const maxRent = 5000;
        activeFilters.minPrice = minRent;
        activeFilters.maxPrice = maxRent;
        if (priceSlider && typeof noUiSlider !== 'undefined') {
            noUiSlider.create(priceSlider, { start: [minRent, maxRent], connect: true, range: { 'min': minRent, 'max': maxRent }, step: 10, format: { to: v => Math.round(v), from: v => Number(v) } });
            priceSlider.noUiSlider.on('update', (values) => {
                const [minVal, maxVal] = values;
                priceDisplay.textContent = (minVal === minRent && maxVal === maxRent) ? 'Any Price' : (maxVal === maxRent ? `$${minVal}+` : `$${minVal} - $${maxVal}`);
            });
            priceSlider.noUiSlider.on('set', (values) => {
                activeFilters.minPrice = values[0];
                activeFilters.maxPrice = (values[1] < maxRent) ? values[1] : null;
                applyFiltersAndRender();
            });
        }
        
        populateDateFilter();

        const closePanel = () => toggleFilterPanel(false);
        closeBtn?.addEventListener('click', closePanel);
        overlay?.addEventListener('click', closePanel);
        applyBtn?.addEventListener('click', closePanel);

        resetBtn?.addEventListener('click', () => {
            activeFilters = { searchTerm: searchInput.value, minPrice: null, maxPrice: null, bedrooms: 'any', bathrooms: 'any', availableDate: 'any', isFurnished: false };
            if (priceSlider && priceSlider.noUiSlider) priceSlider.noUiSlider.set([minRent, maxRent]);
            dateSelect.value = 'any';
            furnishedToggle.checked = false;
            document.querySelectorAll('.filter-btn.active').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.filter-btn[data-value="any"]').forEach(b => b.classList.add('active'));
            applyFiltersAndRender();
        });

        const handleButtonGroupClick = (group, filterKey) => {
            group?.addEventListener('click', e => {
                if (e.target.classList.contains('filter-btn')) {
                    group.querySelector('.active').classList.remove('active');
                    e.target.classList.add('active');
                    activeFilters[filterKey] = e.target.dataset.value;
                    applyFiltersAndRender();
                }
            });
        };
        
        handleButtonGroupClick(bedroomsGroup, 'bedrooms');
        handleButtonGroupClick(bathroomsGroup, 'bathrooms');
        dateSelect?.addEventListener('change', e => { activeFilters.availableDate = e.target.value; applyFiltersAndRender(); });
        furnishedToggle?.addEventListener('change', e => { activeFilters.isFurnished = e.target.checked; applyFiltersAndRender(); });
    }

    async function loadFilterPanel() {
        // 筛选面板已经直接嵌入HTML中，无需额外加载
        console.log('Filter panel is already embedded in HTML');
        return Promise.resolve();
    }
    
    function setupEventListeners() {
        listingsContainer.addEventListener('click', handleInteraction);
        searchInput.addEventListener('input', (event) => {
            activeFilters.searchTerm = event.target.value;
            applyFiltersAndRender();
        });
        filterButton.addEventListener('click', () => toggleFilterPanel(true));
    }

    // --- 6. INITIALIZATION ---

    async function initialize() {
        if (!listingsContainer) return;
        listingsContainer.innerHTML = '<p class="text-center text-textSecondary py-10">正在加载房源...</p>';
        await loadFilterPanel();
        // 现在 fetchData 可以接受筛选条件
        const properties = await fetchData(activeFilters); 
        if (properties) {
            allProperties = properties;
            // 不再将所有房源存储到localStorage，因为数据将通过API动态获取
            // localStorage.setItem('allPropertyListings', JSON.stringify(allProperties)); 
            setupFilterPanelEventListeners();
            applyFiltersAndRender(); 
            setupEventListeners();
        }
    }

    initialize();
});
