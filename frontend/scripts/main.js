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
        // 地址处理 - 完全按照参考截图格式
        const fullAddress = property.address || '地址未知';
        const addressParts = fullAddress.split(',');
        const streetAddress = addressParts[0]?.trim() || fullAddress;
        
        // 修复邮编小数点问题 - 匹配参考截图格式
        const postcode = property.postcode ? Math.floor(property.postcode) : '';
        const locationInfo = `${property.suburb || ''} NSW ${postcode}`.trim().toUpperCase();
        
        const bedrooms = property.bedrooms || 0;
        const bathrooms = property.bathrooms || 0;
        const parking = property.parking_spaces || 0;
        
        // 可用日期显示 - 完全按照参考截图格式
        let availabilityText = 'Available from: ';
        if (property.available_date) {
            const availDate = new Date(property.available_date);
            const today = new Date();
            if (availDate <= today) {
                availabilityText += 'NOW';
            } else {
                // 格式化为类似 "Fri 8 Aug" 的格式
                const dayName = availDate.toLocaleDateString('en-AU', { weekday: 'short' });
                const day = availDate.getDate();
                const month = availDate.toLocaleDateString('en-AU', { month: 'short' });
                availabilityText += `${dayName} ${day} ${month}`;
            }
        } else {
            availabilityText += 'NOW'; // 不再显示TBA，默认为NOW
        }
        
        // Inspection time 处理 - 按照参考截图格式
        let inspectionText = '';
        if (property.inspection_times && property.inspection_times.trim() !== '') {
            inspectionText = `INSPECTION: ${property.inspection_times}`;
        }
        
        // 价格显示 - 完全匹配参考截图
        const rent = property.rent_pw ? `$${property.rent_pw}` : 'Price TBA';
        
        // 改进的占位符图片 - 4:3比例
        const placeholderSvg = `<svg width="600" height="450" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#f3f4f6"/><text x="50%" y="50%" font-family="Inter, sans-serif" font-size="18" dy=".3em" fill="#9ca3af" text-anchor="middle">Property Image</text></svg>`;
        const placeholderUrl = `data:image/svg+xml,${encodeURIComponent(placeholderSvg)}`;
        
        // 改进的图片列表处理
        let imageList = [];
        const imagesData = property.images;
        if (Array.isArray(imagesData) && imagesData.length > 0) {
            imageList = imagesData.filter(url => url && typeof url === 'string' && url.trim() !== '');
        }
        const coverImage = (imageList.length > 0) ? imageList[0] : placeholderUrl;
        
        const isFavorite = favoritesManager.isFavorite(property.listing_id);
        const favoriteClass = isFavorite ? 'is-favorite' : '';
        const favoriteIcon = isFavorite ? 'fa-solid' : 'fa-regular';

        // 重新设计的轮播控制 - 修复箭头显示
        const carouselControls = imageList.length > 1 ? `
            <button class="carousel-btn absolute top-1/2 left-2 -translate-y-1/2 bg-white/90 hover:bg-white text-gray-700 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 z-10 shadow-md" data-direction="prev">
                <i class="fa-solid fa-chevron-left text-sm pointer-events-none"></i>
            </button>
            <button class="carousel-btn absolute top-1/2 right-2 -translate-y-1/2 bg-white/90 hover:bg-white text-gray-700 w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 z-10 shadow-md" data-direction="next">
                <i class="fa-solid fa-chevron-right text-sm pointer-events-none"></i>
            </button>
            <div class="image-counter absolute bottom-2 left-2 bg-black/75 text-white text-xs font-medium px-2 py-1 rounded">1 / ${imageList.length}</div>` : '';
        
        // 状态标签 - 匹配参考截图的绿色New标签
        const statusTag = property.listing_id > 2500 
            ? `<div class="property-status-tag absolute top-2 left-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded">New</div>` 
            : '';

        return `
            <div class="card-container reference-property-card bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-md transition-shadow duration-200 group">
                <!-- 图片区域 - 4:3比例 -->
                <div class="image-carousel relative aspect-[4/3] bg-gray-100 overflow-hidden" data-images='${JSON.stringify(imageList)}' data-current-index="0">
                    <a href="./details.html?id=${property.listing_id}" class="block w-full h-full">
                        <img src="${coverImage}" alt="房源图片: ${streetAddress}" 
                             class="w-full h-full object-cover image-tag"
                             onerror="this.src='${placeholderUrl}'">
                    </a>
                    ${carouselControls}
                    ${statusTag}
                    <button class="favorite-btn ${favoriteClass} absolute top-2 right-2 bg-white/90 hover:bg-white w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 shadow-sm" data-listing-id="${property.listing_id}">
                        <i class="${favoriteIcon} fa-star text-gray-400 hover:text-yellow-500 text-sm transition-colors duration-200"></i>
                    </button>
                </div>
                
                <!-- 内容区域 - 完全匹配参考截图布局 -->
                <div class="p-3">
                    <!-- 价格 - 大字体黑色 -->
                    <div class="mb-2">
                        <p class="text-xl font-bold text-black leading-tight">${rent} <span class="text-base font-normal text-gray-600">per week</span></p>
                    </div>
                    
                    <!-- 地址信息 - 两行显示 -->
                    <div class="mb-3">
                        <p class="text-base font-medium text-gray-800 leading-tight">${streetAddress},</p>
                        <p class="text-sm text-gray-600 font-medium">${locationInfo}</p>
                    </div>
                    
                    <!-- 房型信息 - 图标+数字，匹配参考截图 -->
                    <div class="flex items-center gap-3 mb-3 text-gray-600">
                        <div class="flex items-center gap-1">
                            <i class="fa-solid fa-bed text-gray-500 text-sm"></i>
                            <span class="font-medium text-gray-800 text-sm">${bedrooms}</span>
                        </div>
                        <div class="flex items-center gap-1">
                            <i class="fa-solid fa-bath text-gray-500 text-sm"></i>
                            <span class="font-medium text-gray-800 text-sm">${bathrooms}</span>
                        </div>
                        <div class="flex items-center gap-1">
                            <i class="fa-solid fa-car text-gray-500 text-sm"></i>
                            <span class="font-medium text-gray-800 text-sm">${parking}</span>
                        </div>
                    </div>
                    
                    <!-- 底部信息 - 两行显示，保留Available from -->
                    <div class="border-t border-gray-200 pt-2 space-y-1">
                        <div class="text-sm text-gray-700 font-medium">
                            ${availabilityText}
                        </div>
                        <div class="text-xs text-gray-500 font-medium min-h-[16px]">
                            ${inspectionText}
                        </div>
                    </div>
                </div>
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
