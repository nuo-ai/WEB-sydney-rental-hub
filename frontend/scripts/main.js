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
    let locationSuggestions = []; // 存储区域建议数据
    let selectedLocations = []; // 存储选中的区域标签
    let activeFilters = {
        searchTerm: '', selectedLocations: [], minPrice: null, maxPrice: null, bedrooms: 'any', 
        bathrooms: 'any', availableDate: 'any', isFurnished: false
    };

    // --- 4. LOCATION AUTOCOMPLETE SYSTEM ---
    
    // 从房源数据中提取区域建议数据
    function buildLocationSuggestions(properties) {
        const locationMap = new Map();
        
        properties.forEach(property => {
            // 处理区域 (suburb)
            if (property.suburb) {
                const suburb = property.suburb.trim();
                const postcode = property.postcode ? Math.floor(property.postcode).toString() : '';
                const key = `${suburb}_${postcode}`;
                
                if (!locationMap.has(key)) {
                    locationMap.set(key, {
                        id: key,
                        type: 'suburb',
                        name: suburb,
                        postcode: postcode,
                        fullName: postcode ? `${suburb} NSW ${postcode}` : suburb,
                        count: 0
                    });
                }
                locationMap.get(key).count++;
            }
            
            // 处理邮编 (postcode)
            if (property.postcode) {
                const postcode = Math.floor(property.postcode).toString();
                const suburb = property.suburb ? property.suburb.trim() : '';
                const key = `postcode_${postcode}`;
                
                if (!locationMap.has(key)) {
                    locationMap.set(key, {
                        id: key,
                        type: 'postcode',
                        name: postcode,
                        suburb: suburb,
                        fullName: suburb ? `${postcode} (${suburb})` : postcode,
                        count: 0
                    });
                }
                locationMap.get(key).count++;
            }
        });
        
        return Array.from(locationMap.values()).sort((a, b) => b.count - a.count);
    }
    
    // 智能搜索匹配算法
    function searchLocationSuggestions(query, suggestions, maxResults = 8) {
        if (!query || query.length < 1) return [];
        
        const normalizedQuery = query.toLowerCase().trim();
        const results = [];
        
        suggestions.forEach(suggestion => {
            let score = 0;
            const name = suggestion.name.toLowerCase();
            const fullName = suggestion.fullName.toLowerCase();
            
            // 完全匹配 (最高分)
            if (name === normalizedQuery) score += 100;
            if (fullName === normalizedQuery) score += 100;
            
            // 开头匹配 (高分)
            if (name.startsWith(normalizedQuery)) score += 80;
            if (fullName.startsWith(normalizedQuery)) score += 70;
            
            // 包含匹配 (中等分)
            if (name.includes(normalizedQuery)) score += 40;
            if (fullName.includes(normalizedQuery)) score += 30;
            
            // 首字母匹配 (例如 "syd" 匹配 "Sydney")
            const words = name.split(/\s+/);
            const initials = words.map(word => word[0]).join('').toLowerCase();
            if (initials.includes(normalizedQuery)) score += 20;
            
            // 模糊匹配 (低分)
            if (normalizedQuery.length >= 3) {
                const fuzzyMatch = normalizedQuery.split('').some(char => name.includes(char));
                if (fuzzyMatch) score += 10;
            }
            
            // 根据房源数量调整分数 (热门区域优先)
            score += Math.log10(suggestion.count + 1) * 5;
            
            if (score > 0) {
                results.push({ ...suggestion, score });
            }
        });
        
        return results
            .sort((a, b) => b.score - a.score)
            .slice(0, maxResults);
    }
    
    // 选择区域标签
    function selectLocation(location) {
        // 检查是否已经选中
        const existingIndex = selectedLocations.findIndex(loc => loc.id === location.id);
        if (existingIndex !== -1) return;
        
        selectedLocations.push(location);
        activeFilters.selectedLocations = selectedLocations;
        
        updateLocationTags();
        clearSearchInput();
        hideLocationSuggestions();
        applyFiltersAndRender();
    }
    
    // 移除选中的区域标签
    function removeLocation(locationId) {
        selectedLocations = selectedLocations.filter(loc => loc.id !== locationId);
        activeFilters.selectedLocations = selectedLocations;
        
        updateLocationTags();
        applyFiltersAndRender();
    }
    
    // 更新区域标签显示
    function updateLocationTags() {
        const searchContainer = document.querySelector('.search-container');
        let tagsContainer = searchContainer.querySelector('.location-tags');
        
        if (!tagsContainer) {
            tagsContainer = document.createElement('div');
            tagsContainer.className = 'location-tags flex flex-wrap gap-2 mb-2';
            searchContainer.insertBefore(tagsContainer, searchInput.parentElement);
        }
        
        tagsContainer.innerHTML = selectedLocations.map(location => `
            <span class="location-tag inline-flex items-center gap-1 bg-accentPrimary text-white px-2 py-1 rounded-md text-sm font-medium">
                <i class="fa-solid fa-map-marker-alt text-xs"></i>
                <span>${location.name}</span>
                <button class="remove-location-btn text-white/80 hover:text-white" data-location-id="${location.id}">
                    <i class="fa-solid fa-times text-xs"></i>
                </button>
            </span>
        `).join('');
        
        // 添加删除标签事件监听
        tagsContainer.querySelectorAll('.remove-location-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                removeLocation(btn.dataset.locationId);
            });
        });
        
        // 更新搜索框占位符
        if (selectedLocations.length > 0) {
            searchInput.placeholder = '继续搜索区域...';
        } else {
            searchInput.placeholder = '输入区域或邮编，例如 "Ultimo" 或 "2007"';
        }
    }
    
    // 清空搜索输入框
    function clearSearchInput() {
        searchInput.value = '';
        activeFilters.searchTerm = '';
    }
    
    // 显示位置建议列表
    function showLocationSuggestions(suggestions) {
        const searchContainer = document.querySelector('.search-container');
        let suggestionsContainer = searchContainer.querySelector('.location-suggestions');
        
        if (!suggestionsContainer) {
            suggestionsContainer = document.createElement('div');
            suggestionsContainer.className = 'location-suggestions absolute top-full left-0 right-0 bg-white border border-borderDefault rounded-lg shadow-lg z-50 max-h-64 overflow-y-auto';
            searchContainer.appendChild(suggestionsContainer);
        }
        
        if (suggestions.length === 0) {
            suggestionsContainer.innerHTML = '<div class="p-3 text-textSecondary text-sm">没有找到匹配的区域</div>';
        } else {
            suggestionsContainer.innerHTML = suggestions.map((suggestion, index) => `
                <div class="suggestion-item p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0" data-location-id="${suggestion.id}" data-index="${index}">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid ${suggestion.type === 'suburb' ? 'fa-map-marker-alt' : 'fa-hashtag'} text-accentPrimary text-sm"></i>
                            <div>
                                <div class="font-medium text-textPrimary">${suggestion.fullName}</div>
                                <div class="text-xs text-textSecondary">${suggestion.count} 套房源</div>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
        }
        
        suggestionsContainer.style.display = 'block';
        
        // 添加点击事件监听
        suggestionsContainer.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', () => {
                const locationId = item.dataset.locationId;
                const location = suggestions.find(s => s.id === locationId);
                if (location) selectLocation(location);
            });
        });
    }
    
    // 隐藏位置建议列表
    function hideLocationSuggestions() {
        const suggestionsContainer = document.querySelector('.location-suggestions');
        if (suggestionsContainer) {
            suggestionsContainer.style.display = 'none';
        }
    }

    // --- 5. CORE FUNCTIONS ---

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
        
        // 在 applyFiltersAndRender 函数中的区域筛选部分
        // 区域筛选 - 支持多选
        if (activeFilters.selectedLocations && activeFilters.selectedLocations.length > 0) {
            filteredProperties = filteredProperties.filter(property => {
                return activeFilters.selectedLocations.some(location => {
                    if (location.type === 'suburb') {
                        return property.suburb && property.suburb.toLowerCase() === location.name.toLowerCase();
                    } else if (location.type === 'postcode') {
                        const propertyPostcode = property.postcode ? Math.floor(property.postcode).toString() : '';
                        return propertyPostcode === location.name;
                    }
                    return false;
                });
            });
        }
        
        // 文本搜索 (在已选择区域的基础上进一步筛选)
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
            // 重置所有筛选器，包括选中的区域
            selectedLocations = [];
            activeFilters = { 
                searchTerm: '', 
                selectedLocations: [], 
                minPrice: null, 
                maxPrice: null, 
                bedrooms: 'any', 
                bathrooms: 'any', 
                availableDate: 'any', 
                isFurnished: false 
            };
            
            // 重置UI状态
            if (priceSlider && priceSlider.noUiSlider) priceSlider.noUiSlider.set([minRent, maxRent]);
            dateSelect.value = 'any';
            furnishedToggle.checked = false;
            document.querySelectorAll('.filter-btn.active').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.filter-btn[data-value="any"]').forEach(b => b.classList.add('active'));
            
            // 清空搜索框和标签
            searchInput.value = '';
            updateLocationTags();
            hideLocationSuggestions();
            
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
    
    // 防抖函数
    function debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }
    
    function setupEventListeners() {
        listingsContainer.addEventListener('click', handleInteraction);
        
        // 自动补全搜索框事件
        let currentSuggestionIndex = -1;
        
        // 防抖处理输入事件
        const debouncedSearch = debounce((query) => {
            if (query.trim()) {
                const suggestions = searchLocationSuggestions(query, locationSuggestions);
                showLocationSuggestions(suggestions);
                currentSuggestionIndex = -1;
            } else {
                hideLocationSuggestions();
            }
        }, 300);
        
        searchInput.addEventListener('input', (event) => {
            const query = event.target.value;
            activeFilters.searchTerm = query;
            
            console.log('🔍 搜索输入:', query, '选中区域数量:', selectedLocations.length, '建议数据:', locationSuggestions.length);
            
            // 如果没有选中的区域，显示自动补全
            if (selectedLocations.length === 0) {
                console.log('📝 触发自动补全搜索...');
                debouncedSearch(query);
            } else {
                // 如果有选中区域，只做文本筛选
                console.log('🏷️ 基于选中区域进行文本筛选...');
                applyFiltersAndRender();
                hideLocationSuggestions();
            }
        });
        
        // 键盘导航支持
        searchInput.addEventListener('keydown', (event) => {
            const suggestionsContainer = document.querySelector('.location-suggestions');
            const suggestions = suggestionsContainer?.querySelectorAll('.suggestion-item') || [];
            
            switch (event.key) {
                case 'ArrowDown':
                    event.preventDefault();
                    if (suggestions.length > 0) {
                        currentSuggestionIndex = Math.min(currentSuggestionIndex + 1, suggestions.length - 1);
                        updateSuggestionHighlight(suggestions, currentSuggestionIndex);
                    }
                    break;
                    
                case 'ArrowUp':
                    event.preventDefault();
                    if (suggestions.length > 0) {
                        currentSuggestionIndex = Math.max(currentSuggestionIndex - 1, -1);
                        updateSuggestionHighlight(suggestions, currentSuggestionIndex);
                    }
                    break;
                    
                case 'Enter':
                    event.preventDefault();
                    if (currentSuggestionIndex >= 0 && suggestions[currentSuggestionIndex]) {
                        suggestions[currentSuggestionIndex].click();
                    } else if (selectedLocations.length === 0 && searchInput.value.trim()) {
                        // 如果没有选择建议但有输入文本，继续文本搜索
                        applyFiltersAndRender();
                    }
                    break;
                    
                case 'Escape':
                    event.preventDefault();
                    hideLocationSuggestions();
                    currentSuggestionIndex = -1;
                    searchInput.blur();
                    break;
            }
        });
        
        // 点击外部隐藏建议列表
        document.addEventListener('click', (event) => {
            const searchContainer = document.querySelector('.search-container');
            if (!searchContainer?.contains(event.target)) {
                hideLocationSuggestions();
                currentSuggestionIndex = -1;
            }
        });
        
        filterButton.addEventListener('click', () => toggleFilterPanel(true));
    }
    
    // 更新建议项高亮状态
    function updateSuggestionHighlight(suggestions, activeIndex) {
        suggestions.forEach((suggestion, index) => {
            if (index === activeIndex) {
                suggestion.classList.add('bg-gray-100');
                suggestion.scrollIntoView({ block: 'nearest' });
            } else {
                suggestion.classList.remove('bg-gray-100');
            }
        });
    }

    // --- 6. INITIALIZATION ---

    // 在文件顶部添加自动补全实例变量
    let locationAutocomplete = null;
    
    // 修改初始化函数
    async function initialize() {
        if (!listingsContainer) return;
        listingsContainer.innerHTML = '<p class="text-center text-textSecondary py-10">正在加载房源...</p>';
        await loadFilterPanel();
        
        // 获取房源数据
        const properties = await fetchData(activeFilters); 
        if (properties) {
            allProperties = properties;
            
            // 🚀 初始化自动补全功能
            console.log('🔄 初始化自动补全功能...');
            if (searchInput && window.LocationAutocomplete) {
                locationAutocomplete = new LocationAutocomplete(searchInput, {
                    maxResults: 10,
                    debounceDelay: 200,
                    minQueryLength: 2
                });
                
                // 构建区域索引
                locationAutocomplete.buildLocationIndex(properties);
                
                // 监听选择事件
                searchInput.addEventListener('locationSelected', (e) => {
                    const { selectedLocations } = e.detail;
                    activeFilters.selectedLocations = selectedLocations;
                    applyFiltersAndRender();
                });
                
                // 监听移除事件
                searchInput.addEventListener('locationRemoved', (e) => {
                    const { selectedLocations } = e.detail;
                    activeFilters.selectedLocations = selectedLocations;
                    applyFiltersAndRender();
                });
                
                console.log('✅ 自动补全功能初始化完成');
            } else {
                console.error('❌ 自动补全初始化失败：缺少必要元素或类');
            }
            
            setupFilterPanelEventListeners();
            applyFiltersAndRender(); 
            setupEventListeners();
        }
    }
    
    // 移除或注释掉原有的自动补全相关函数，因为现在由 LocationAutocomplete 类处理
    // 保留 applyFiltersAndRender 函数中的区域筛选逻辑
    initialize();
});
