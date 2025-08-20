// 自动补全区域搜索模块
class LocationAutocomplete {
    constructor(inputElement, options = {}) {
        this.input = inputElement;
        this.container = inputElement.closest('.search-container');
        this.options = {
            maxResults: 10,
            debounceDelay: 200,
            minQueryLength: 2,
            ...options
        };
        
        this.locationIndex = new Map();
        this.selectedLocations = [];
        this.currentSuggestionIndex = -1;
        this.isVisible = false;
        
        this.init();
    }
    
    init() {
        this.createContainers();
        this.bindEvents();
        this.setupKeyboardNavigation();
    }
    
    createContainers() {
        // 创建标签容器
        if (!this.container.querySelector('.location-tags')) {
            this.tagsContainer = document.createElement('div');
            this.tagsContainer.className = 'location-tags flex flex-wrap gap-2 mb-2';
            this.tagsContainer.style.display = 'none';
            this.container.insertBefore(this.tagsContainer, this.input.parentElement);
        } else {
            this.tagsContainer = this.container.querySelector('.location-tags');
        }
        
        // 创建建议容器
        if (!this.container.querySelector('.location-suggestions')) {
            this.suggestionsContainer = document.createElement('div');
            this.suggestionsContainer.className = 'location-suggestions absolute top-full left-0 right-0 bg-white border border-borderDefault rounded-lg shadow-lg z-50 max-h-64 overflow-y-auto';
            this.suggestionsContainer.style.display = 'none';
            this.suggestionsContainer.setAttribute('role', 'listbox');
            this.container.appendChild(this.suggestionsContainer);
        } else {
            this.suggestionsContainer = this.container.querySelector('.location-suggestions');
        }
    }
    
    buildLocationIndex(properties) {
        console.log('🔄 构建区域索引，房源数量:', properties.length);
        this.locationIndex.clear();
        
        properties.forEach(property => {
            // 处理区域 (suburb)
            if (property.suburb) {
                const suburb = property.suburb.trim();
                const postcode = property.postcode ? Math.floor(property.postcode).toString() : '';
                const key = `suburb_${suburb}_${postcode}`;
                
                if (!this.locationIndex.has(key)) {
                    this.locationIndex.set(key, {
                        id: key,
                        type: 'suburb',
                        name: suburb,
                        postcode: postcode,
                        fullName: postcode ? `${suburb} NSW ${postcode}` : suburb,
                        count: 0
                    });
                }
                this.locationIndex.get(key).count++;
            }
            
            // 处理邮编 (postcode)
            if (property.postcode) {
                const postcode = Math.floor(property.postcode).toString();
                const suburb = property.suburb ? property.suburb.trim() : '';
                const key = `postcode_${postcode}`;
                
                if (!this.locationIndex.has(key)) {
                    this.locationIndex.set(key, {
                        id: key,
                        type: 'postcode',
                        name: postcode,
                        suburb: suburb,
                        fullName: suburb ? `${postcode} (${suburb})` : postcode,
                        count: 0
                    });
                }
                this.locationIndex.get(key).count++;
            }
        });
        
        console.log('✅ 区域索引构建完成，包含', this.locationIndex.size, '个区域');
        this.updateInputState();
    }
    
    searchLocations(query) {
        if (!query || query.length < this.options.minQueryLength) {
            return [];
        }
        
        const normalizedQuery = query.toLowerCase().trim();
        const results = [];
        
        this.locationIndex.forEach(location => {
            let score = 0;
            const name = location.name.toLowerCase();
            const fullName = location.fullName.toLowerCase();
            
            // 完全匹配 (最高分)
            if (name === normalizedQuery) score += 100;
            if (fullName === normalizedQuery) score += 100;
            
            // 开头匹配 (高分)
            if (name.startsWith(normalizedQuery)) score += 80;
            if (fullName.startsWith(normalizedQuery)) score += 70;
            
            // 包含匹配 (中等分)
            if (name.includes(normalizedQuery)) score += 40;
            if (fullName.includes(normalizedQuery)) score += 30;
            
            // 首字母匹配
            const words = name.split(/\s+/);
            const initials = words.map(word => word[0]).join('').toLowerCase();
            if (initials.includes(normalizedQuery)) score += 20;
            
            // 根据房源数量调整分数
            score += Math.log10(location.count + 1) * 5;
            
            if (score > 0) {
                results.push({ ...location, score });
            }
        });
        
        return results
            .sort((a, b) => b.score - a.score)
            .slice(0, this.options.maxResults);
    }
    
    showSuggestions(suggestions) {
        if (suggestions.length === 0) {
            this.suggestionsContainer.innerHTML = '<div class="p-3 text-textSecondary text-sm">没有找到匹配的区域</div>';
        } else {
            this.suggestionsContainer.innerHTML = suggestions.map((suggestion, index) => `
                <div class="suggestion-item p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0" 
                     data-location-id="${suggestion.id}" 
                     data-index="${index}"
                     role="option"
                     aria-selected="false">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-2">
                            <i class="fa-solid ${suggestion.type === 'suburb' ? 'fa-map-marker-alt' : 'fa-hashtag'} text-accentPrimary text-sm"></i>
                            <div>
                                <div class="font-medium text-textPrimary">${this.highlightMatch(suggestion.fullName, this.input.value)}</div>
                                <div class="text-xs text-textSecondary">${suggestion.count} 套房源</div>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
            
            // 绑定点击事件
            this.suggestionsContainer.querySelectorAll('.suggestion-item').forEach(item => {
                item.addEventListener('click', () => {
                    const locationId = item.dataset.locationId;
                    const location = suggestions.find(s => s.id === locationId);
                    if (location) this.selectLocation(location);
                });
            });
        }
        
        this.suggestionsContainer.style.display = 'block';
        this.isVisible = true;
        this.currentSuggestionIndex = -1;
    }
    
    hideSuggestions() {
        this.suggestionsContainer.style.display = 'none';
        this.isVisible = false;
        this.currentSuggestionIndex = -1;
    }
    
    highlightMatch(text, query) {
        if (!query) return text;
        const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        return text.replace(regex, '<mark class="bg-yellow-200">$1</mark>');
    }
    
    selectLocation(location) {
        // 检查是否已经选中
        if (this.selectedLocations.find(loc => loc.id === location.id)) {
            return;
        }
        
        this.selectedLocations.push(location);
        this.updateLocationTags();
        this.clearInput();
        this.hideSuggestions();
        
        // 触发选择事件
        this.input.dispatchEvent(new CustomEvent('locationSelected', {
            detail: { location, selectedLocations: this.selectedLocations }
        }));
    }
    
    removeLocation(locationId) {
        this.selectedLocations = this.selectedLocations.filter(loc => loc.id !== locationId);
        this.updateLocationTags();
        
        // 触发移除事件
        this.input.dispatchEvent(new CustomEvent('locationRemoved', {
            detail: { locationId, selectedLocations: this.selectedLocations }
        }));
    }
    
    updateLocationTags() {
        if (this.selectedLocations.length === 0) {
            this.tagsContainer.style.display = 'none';
            this.tagsContainer.innerHTML = '';
        } else {
            this.tagsContainer.style.display = 'flex';
            this.tagsContainer.innerHTML = this.selectedLocations.map(location => `
                <span class="location-tag inline-flex items-center gap-1 bg-accentPrimary text-white px-2 py-1 rounded-md text-sm font-medium">
                    <i class="fa-solid fa-map-marker-alt text-xs"></i>
                    <span>${location.name}</span>
                    <button class="remove-location-btn text-white/80 hover:text-white ml-1" 
                            data-location-id="${location.id}"
                            aria-label="移除 ${location.name}">
                        <i class="fa-solid fa-times text-xs"></i>
                    </button>
                </span>
            `).join('');
            
            // 绑定删除事件
            this.tagsContainer.querySelectorAll('.remove-location-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.removeLocation(btn.dataset.locationId);
                });
            });
        }
        
        this.updateInputState();
    }
    
    updateInputState() {
        if (this.locationIndex.size === 0) {
            this.input.disabled = true;
            this.input.placeholder = '区域数据未加载';
        } else {
            this.input.disabled = false;
            if (this.selectedLocations.length > 0) {
                this.input.placeholder = '继续搜索区域...';
            } else {
                this.input.placeholder = '输入区域或邮编，例如 "Ultimo" 或 "2007"';
            }
        }
    }
    
    clearInput() {
        this.input.value = '';
    }
    
    bindEvents() {
        // 防抖搜索
        const debouncedSearch = this.debounce((query) => {
            if (query.trim().length >= this.options.minQueryLength) {
                const suggestions = this.searchLocations(query);
                this.showSuggestions(suggestions);
            } else {
                this.hideSuggestions();
            }
        }, this.options.debounceDelay);
        
        // 输入事件
        this.input.addEventListener('input', (e) => {
            const query = e.target.value;
            console.log('🔍 搜索输入:', query);
            debouncedSearch(query);
        });
        
        // 焦点事件
        this.input.addEventListener('focus', () => {
            if (this.input.value.trim().length >= this.options.minQueryLength) {
                const suggestions = this.searchLocations(this.input.value);
                this.showSuggestions(suggestions);
            }
        });
        
        // 点击外部隐藏
        document.addEventListener('click', (e) => {
            if (!this.container.contains(e.target)) {
                this.hideSuggestions();
            }
        });
    }
    
    setupKeyboardNavigation() {
        this.input.addEventListener('keydown', (e) => {
            if (!this.isVisible) return;
            
            const suggestions = this.suggestionsContainer.querySelectorAll('.suggestion-item');
            
            switch (e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    this.currentSuggestionIndex = Math.min(this.currentSuggestionIndex + 1, suggestions.length - 1);
                    this.updateSuggestionHighlight(suggestions);
                    break;
                    
                case 'ArrowUp':
                    e.preventDefault();
                    this.currentSuggestionIndex = Math.max(this.currentSuggestionIndex - 1, -1);
                    this.updateSuggestionHighlight(suggestions);
                    break;
                    
                case 'Enter':
                    e.preventDefault();
                    if (this.currentSuggestionIndex >= 0 && suggestions[this.currentSuggestionIndex]) {
                        suggestions[this.currentSuggestionIndex].click();
                    }
                    break;
                    
                case 'Escape':
                    e.preventDefault();
                    this.hideSuggestions();
                    this.input.blur();
                    break;
            }
        });
    }
    
    updateSuggestionHighlight(suggestions) {
        suggestions.forEach((suggestion, index) => {
            if (index === this.currentSuggestionIndex) {
                suggestion.classList.add('bg-gray-100');
                suggestion.setAttribute('aria-selected', 'true');
                suggestion.scrollIntoView({ block: 'nearest' });
            } else {
                suggestion.classList.remove('bg-gray-100');
                suggestion.setAttribute('aria-selected', 'false');
            }
        });
    }
    
    debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }
    
    // 公共方法
    getSelectedLocations() {
        return this.selectedLocations;
    }
    
    clearSelections() {
        this.selectedLocations = [];
        this.updateLocationTags();
    }
    
    destroy() {
        this.hideSuggestions();
        this.suggestionsContainer?.remove();
        this.tagsContainer?.remove();
    }
}

// 导出
window.LocationAutocomplete = LocationAutocomplete;

// 初始化函数
function initAutocomplete(inputElement, options) {
    return new LocationAutocomplete(inputElement, options);
}

function buildLocationIndex(properties) {
    // 兼容性函数，实际逻辑在 LocationAutocomplete 类中
    console.log('buildLocationIndex 函数已被 LocationAutocomplete 类替代');
    return [];
}

// 导出函数
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { LocationAutocomplete, initAutocomplete, buildLocationIndex };
}