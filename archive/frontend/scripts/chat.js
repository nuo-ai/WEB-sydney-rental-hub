// AI聊天系统
class ChatSystem {
    constructor() {
        this.messages = [];
        this.isHumanMode = false;
        this.conversationId = this.generateConversationId();
        this.currentAgent = 'general'; // general, property, legal, contract, commute, service
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadChatHistory();
        this.autoResizeTextarea();
    }

    setupEventListeners() {
        // 发送消息按钮
        document.getElementById('send-button').addEventListener('click', () => this.sendMessage());
        
        // 回车发送消息
        document.getElementById('chat-input').addEventListener('keydown', (e) => this.handleKeyDown(e));
        
        // 转人工客服
        document.getElementById('transfer-to-human').addEventListener('click', () => this.transferToHuman());
        
        // 自动调整输入框高度
        document.getElementById('chat-input').addEventListener('input', () => this.autoResizeTextarea());
    }

    generateConversationId() {
        return 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    handleKeyDown(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }

    autoResizeTextarea() {
        const textarea = document.getElementById('chat-input');
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 96) + 'px';
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;

        // 清空输入框并重置高度
        input.value = '';
        this.autoResizeTextarea();

        // 添加用户消息
        this.addMessage('user', message);

        // 显示打字指示器
        this.showTypingIndicator();

        try {
            // 发送到AI后端
            await this.processUserMessage(message);
        } catch (error) {
            console.error('发送消息失败:', error);
            this.hideTypingIndicator();
            this.addMessage('ai', '抱歉，我遇到了一些技术问题。请稍后再试或点击"转人工"获得帮助。');
        }
    }

    async processUserMessage(message) {
        try {
            // 调用后端AI聊天API
            const response = await fetch('http://localhost:8000/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_id: this.conversationId,
                    context: {}
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP错误: ${response.status}`);
            }

            const data = await response.json();
            this.hideTypingIndicator();
            
            // 显示AI回复
            this.addMessage('ai', data.message);
            
            // 显示卡片（如果有）
            if (data.cards && data.cards.length > 0) {
                if (data.agent_type === 'property') {
                    this.addPropertyCards(data.cards);
                } else {
                    data.cards.forEach(card => {
                        this.addServiceCard(card);
                    });
                }
            }
            
            // 显示建议（如果有）
            if (data.suggestions && data.suggestions.length > 0) {
                this.addSuggestions(data.suggestions);
            }
            
        } catch (error) {
            console.error('API调用失败:', error);
            this.hideTypingIndicator();
            this.addMessage('ai', '抱歉，我遇到了一些技术问题。请稍后再试或点击"转人工"获得帮助。');
        }
    }

    routeToAgent(message) {
        const msg = message.toLowerCase();
        
        // 房源搜索相关
        if (msg.includes('房源') || msg.includes('房子') || msg.includes('租房') || 
            msg.includes('uts') || msg.includes('unsw') || msg.includes('usyd') || 
            msg.includes('通勤') || msg.includes('距离')) {
            return 'property';
        }
        
        // 法律咨询相关
        if (msg.includes('法律') || msg.includes('权益') || msg.includes('押金') || 
            msg.includes('房东') || msg.includes('租客') || msg.includes('违约')) {
            return 'legal';
        }
        
        // 合同审核相关
        if (msg.includes('合同') || msg.includes('条款') || msg.includes('签约') || 
            msg.includes('协议') || msg.includes('审核')) {
            return 'contract';
        }
        
        // 服务相关
        if (msg.includes('代看房') || msg.includes('搬家') || msg.includes('咨询') || 
            msg.includes('预约') || msg.includes('服务')) {
            return 'service';
        }
        
        return 'general';
    }

    async handlePropertyQuery(message) {
        this.hideTypingIndicator();
        
        // 检查是否询问大学相关
        const universities = ['uts', 'unsw', 'usyd', 'macquarie', '悉尼科技大学', '新南威尔士大学', '悉尼大学'];
        const mentionedUni = universities.find(uni => message.toLowerCase().includes(uni));
        
        if (mentionedUni) {
            this.addMessage('ai', `好的！我来为您推荐${this.getUniversityName(mentionedUni)}附近的房源。`);
            
            // 模拟获取房源数据
            setTimeout(() => {
                this.addPropertyCards([
                    {
                        id: 1,
                        image: 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=300&h=200&fit=crop',
                        price: 776,
                        address: 'Central Park Student Village',
                        commute: 'UTS步行8分钟',
                        bedrooms: 'Studio',
                        bathrooms: 1,
                        features: ['空调', '洗衣机', '高速网络']
                    },
                    {
                        id: 2,
                        image: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=300&h=200&fit=crop',
                        price: 706,
                        address: 'Redfern Student Accommodation',
                        commute: 'UTS轻轨10分钟',
                        bedrooms: 'Studio',
                        bathrooms: 1,
                        features: ['健身房', '停车位', '安保']
                    }
                ]);
                
                this.addMessage('ai', '这些房源都很适合您！想了解更多详情或预约代看房服务吗？');
            }, 1000);
        } else {
            this.addMessage('ai', '我来帮您找房源！请告诉我您的需求：\n\n• 您在哪所大学上学？\n• 预算范围是多少？\n• 偏好的区域或交通方式？');
        }
    }

    async handleLegalQuery(message) {
        this.hideTypingIndicator();
        
        // 添加法律专家标识
        this.addMessage('agent', '⚖️ 租赁法律专家为您服务');
        
        const msg = message.toLowerCase();
        let response = '';
        
        if (msg.includes('押金')) {
            response = `关于押金的法律规定：

**押金标准**：
• 一般不超过4周租金
• 必须存入政府监管账户
• 不能用作最后一期租金

**退还条件**：
• 房屋无损坏：全额退还
• 有损坏：扣除维修费后退还
• 14天内必须处理

**我们的建议**：
签约时拍照记录房屋状态，搬出时也要拍照对比。`;
        } else if (msg.includes('房东') || msg.includes('权益')) {
            response = `澳洲租客权益保护：

**房东不能**：
• 随意进入您的房间
• 无理由驱赶租客
• 歧视性对待

**您的权利**：
• 安静享用权
• 维修要求权
• 隐私保护权

**需要帮助时**：
• 联系当地租客协会
• 申请仲裁服务
• 寻求法律援助`;
        } else {
            response = `我是您的租赁法律顾问！我可以帮您解答：

• 租房合同条款解释
• 押金和租金相关法规
• 租客权益保护
• 房东责任义务
• 违约和纠纷处理

请具体告诉我您遇到的问题？`;
        }
        
        this.addMessage('ai', response);
        
        // 添加服务卡片
        setTimeout(() => {
            this.addServiceCard({
                type: 'legal',
                title: '⚖️ 专业法律咨询',
                description: '复杂案例人工法律顾问',
                price: '$99',
                features: ['30分钟专业咨询', '书面意见书', '中文全程服务'],
                action: '预约咨询'
            });
        }, 500);
    }

    async handleContractQuery(message) {
        this.hideTypingIndicator();
        
        this.addMessage('agent', '📋 合同审核专家为您服务');
        
        const response = `我可以帮您审核租房合同！

**AI快速审核**：
• 30秒识别关键条款
• 标注潜在风险点
• 提供修改建议
• 生成审核报告

**常见风险条款**：
• 过高的违约金
• 不合理的维修责任
• 模糊的押金条款
• 限制性使用规定

上传您的合同，我来为您详细分析！`;
        
        this.addMessage('ai', response);
        
        // 添加合同审核服务卡片
        setTimeout(() => {
            this.addServiceCard({
                type: 'contract',
                title: '📋 AI合同审核',
                description: '智能识别风险条款',
                price: '$25',
                features: ['30秒快速分析', '风险点标注', '修改建议', '专业报告'],
                action: '上传合同'
            });
        }, 500);
    }

    async handleServiceQuery(message) {
        this.hideTypingIndicator();
        
        const msg = message.toLowerCase();
        
        if (msg.includes('代看房')) {
            this.addMessage('ai', '我来为您介绍代看房服务！这是我们最受欢迎的服务。');
            
            setTimeout(() => {
                this.addServiceCard({
                    type: 'inspection',
                    title: '🏠 专业代看房服务',
                    description: '专业顾问实地看房拍摄',
                    price: '$35',
                    features: ['专业拍摄录像', '详细评估报告', '2小时内完成', '微信实时沟通'],
                    action: '立即预约'
                });
                
                this.addMessage('ai', '我们的专业顾问会:\n• 实地拍摄高清照片和视频\n• 检查房屋设施和周边环境\n• 提供详细的书面报告\n• 微信实时沟通看房过程\n\n需要为哪个房源预约代看房服务？');
            }, 800);
        } else {
            this.addMessage('ai', '我们提供全方位的租房服务！');
            
            setTimeout(() => {
                this.addMultipleServiceCards([
                    {
                        type: 'inspection',
                        title: '🏠 代看房服务',
                        description: '专业实地看房录像',
                        price: '$35',
                        action: '立即预约'
                    },
                    {
                        type: 'moving',
                        title: '🚚 学生搬家',
                        description: '小件物品搬运',
                        price: '$89起',
                        action: '获取报价'
                    },
                    {
                        type: 'consultation',
                        title: '💼 签约陪同',
                        description: '中文全程陪同',
                        price: '$59',
                        action: '预约服务'
                    }
                ]);
            }, 500);
        }
    }

    async handleGeneralQuery(message) {
        // 模拟AI思考时间
        await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000));
        
        this.hideTypingIndicator();
        
        const msg = message.toLowerCase();
        let response = '';
        
        if (msg.includes('你好') || msg.includes('hello')) {
            response = '您好！很高兴为您服务 😊 我是您的专属租房助手，可以帮您找房源、安排看房、解答法律问题。您想了解什么？';
        } else if (msg.includes('价格') || msg.includes('多少钱')) {
            response = `我们的服务价格透明公开：

🏠 **代看房服务**: $35/次
📋 **合同审核**: $25/份  
⚖️ **法律咨询**: $99/次
🚚 **搬家服务**: $89起
💼 **签约陪同**: $59/次

所有服务都是一次性收费，无隐藏费用！需要了解具体哪项服务？`;
        } else if (msg.includes('大学') || msg.includes('学校')) {
            response = `我们主要服务这些大学的学生：

🏫 **悉尼科技大学** (UTS)
🏫 **新南威尔士大学** (UNSW)  
🏫 **悉尼大学** (USYD)
🏫 **麦考瑞大学** (Macquarie)

请告诉我您在哪所大学，我来为您推荐附近的优质房源！`;
        } else {
            response = `我理解您的问题。作为专业的租房助手，我可以帮您：

🔍 **智能找房**: 根据大学推荐房源
🏠 **代看房服务**: $35专业实地看房  
📋 **合同审核**: AI快速识别风险条款
⚖️ **法律咨询**: 专业租房法律建议
🚚 **配套服务**: 搬家、签约陪同等

您最想了解哪方面？`;
        }
        
        this.addMessage('ai', response);
    }

    addMessage(type, content) {
        const messagesContainer = document.getElementById('chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.innerHTML = `<div>${content}</div>`;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // 保存到历史记录
        this.messages.push({ type, content, timestamp: new Date() });
        this.saveChatHistory();
    }

    addPropertyCards(properties) {
        const messagesContainer = document.getElementById('chat-messages');
        
        properties.forEach(property => {
            const cardDiv = document.createElement('div');
            cardDiv.className = 'message ai';
            cardDiv.innerHTML = `
                <div class="property-card-mini">
                    <img src="${property.image}" alt="房源图片" class="w-full h-32 object-cover">
                    <div class="p-3">
                        <div class="flex justify-between items-start mb-2">
                            <div class="text-lg font-bold text-textPrice">$${property.price}/周</div>
                            <div class="text-xs text-gray-500">${property.commute}</div>
                        </div>
                        <div class="text-sm font-medium text-textPrimary mb-1">${property.address}</div>
                        <div class="flex items-center gap-4 text-xs text-textSecondary mb-3">
                            <span>${property.bedrooms}</span>
                            <span>${property.bathrooms}浴</span>
                        </div>
                        <div class="action-buttons">
                            <button class="action-btn" onclick="bookInspection(${property.id})">代看房 $35</button>
                            <button class="action-btn secondary" onclick="viewDetails(${property.id})">查看详情</button>
                        </div>
                    </div>
                </div>
            `;
            messagesContainer.appendChild(cardDiv);
        });
        
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    addServiceCard(service) {
        const messagesContainer = document.getElementById('chat-messages');
        const cardDiv = document.createElement('div');
        cardDiv.className = 'message ai';
        
        const featuresHtml = service.features ? 
            service.features.map(feature => `<li class="text-xs">• ${feature}</li>`).join('') : '';
        
        cardDiv.innerHTML = `
            <div class="service-card-mini">
                <div class="flex justify-between items-start mb-2">
                    <div class="text-sm font-bold text-blue-800">${service.title}</div>
                    <div class="text-lg font-bold text-blue-600">${service.price}</div>
                </div>
                <div class="text-xs text-blue-700 mb-2">${service.description}</div>
                ${featuresHtml ? `<ul class="mb-3 text-blue-600">${featuresHtml}</ul>` : ''}
                <button class="action-btn w-full" onclick="bookService('${service.type}')">${service.action}</button>
            </div>
        `;
        
        messagesContainer.appendChild(cardDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    addMultipleServiceCards(services) {
        services.forEach((service, index) => {
            setTimeout(() => {
                this.addServiceCard(service);
            }, index * 300);
        });
    }

    addSuggestions(suggestions) {
        const messagesContainer = document.getElementById('chat-messages');
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.className = 'message ai';
        
        const suggestionsHtml = suggestions.map(suggestion => 
            `<button class="suggestion-btn" onclick="chatSystem.sendSuggestion('${suggestion}')">${suggestion}</button>`
        ).join('');
        
        suggestionsDiv.innerHTML = `
            <div class="suggestions-container">
                <div class="text-sm text-gray-600 mb-2">您可能想了解：</div>
                <div class="suggestions-grid">
                    ${suggestionsHtml}
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(suggestionsDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    sendSuggestion(suggestion) {
        // 模拟用户点击建议
        document.getElementById('chat-input').value = suggestion;
        this.sendMessage();
    }

    getUniversityName(uniCode) {
        const names = {
            'uts': '悉尼科技大学',
            'unsw': '新南威尔士大学', 
            'usyd': '悉尼大学',
            'macquarie': '麦考瑞大学',
            '悉尼科技大学': '悉尼科技大学',
            '新南威尔士大学': '新南威尔士大学',
            '悉尼大学': '悉尼大学'
        };
        return names[uniCode.toLowerCase()] || uniCode;
    }

    showTypingIndicator() {
        document.getElementById('typing-indicator').style.display = 'flex';
        const messagesContainer = document.getElementById('chat-messages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    hideTypingIndicator() {
        document.getElementById('typing-indicator').style.display = 'none';
    }

    transferToHuman() {
        this.isHumanMode = true;
        
        // 更新UI状态
        document.getElementById('status-indicator').classList.add('human');
        document.getElementById('chat-status-text').textContent = '人工客服小张正在为您服务';
        document.getElementById('transfer-to-human').style.display = 'none';
        
        // 添加转接消息
        this.addMessage('ai', '正在为您转接人工客服...');
        
        setTimeout(() => {
            this.addMessage('agent', '👨‍💼 您好！我是客服小张，刚才的对话我都看到了。我来为您提供更专业的服务！');
        }, 1500);
    }

    saveChatHistory() {
        try {
            localStorage.setItem(`chat_${this.conversationId}`, JSON.stringify(this.messages));
        } catch (e) {
            console.log('保存聊天记录失败:', e);
        }
    }

    loadChatHistory() {
        try {
            const saved = localStorage.getItem(`chat_${this.conversationId}`);
            if (saved) {
                this.messages = JSON.parse(saved);
            }
        } catch (e) {
            console.log('加载聊天记录失败:', e);
        }
    }
}

// 全局函数
function goBack() {
    window.history.back();
}

function bookInspection(propertyId) {
    chatSystem.addMessage('user', `我想预约房源${propertyId}的代看房服务`);
    setTimeout(() => {
        chatSystem.addMessage('ai', '好的！我来为您安排代看房服务。请提供以下信息：\n\n• 您的姓名和联系方式\n• 希望看房的时间\n• 特别关注的问题\n\n我们会在收到预约后2小时内安排专业顾问实地看房。');
    }, 500);
}

function viewDetails(propertyId) {
    // 跳转到房源详情页
    window.location.href = `details.html?id=${propertyId}`;
}

function bookService(serviceType) {
    const serviceNames = {
        'inspection': '代看房服务',
        'legal': '法律咨询', 
        'contract': '合同审核',
        'moving': '搬家服务',
        'consultation': '签约陪同'
    };
    
    const serviceName = serviceNames[serviceType] || '服务';
    chatSystem.addMessage('user', `我想预约${serviceName}`);
    
    setTimeout(() => {
        chatSystem.addMessage('ai', `好的！我来为您安排${serviceName}。\n\n请提供：\n• 联系方式\n• 具体需求\n• 期望时间\n\n我们会尽快与您联系确认详情！`);
    }, 500);
}

// 初始化聊天系统
let chatSystem;
document.addEventListener('DOMContentLoaded', () => {
    chatSystem = new ChatSystem();
});
