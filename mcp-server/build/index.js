#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ErrorCode, ListToolsRequestSchema, McpError, } from '@modelcontextprotocol/sdk/types.js';
import axios from 'axios';
// GraphQL API配置
const GRAPHQL_ENDPOINT = 'http://127.0.0.1:8000/graphql';
// 大学名称映射
const UNIVERSITY_MAPPING = {
    'UNSW': 'UNSW',
    'USYD': 'USYD',
    'UTS': 'UTS',
    'MACQUARIE': 'MACQUARIE',
    'WSU': 'WSU'
};
class SydneyRentalMCP {
    server;
    axiosInstance;
    constructor() {
        this.server = new Server({
            name: 'sydney-rental-mcp',
            version: '0.1.0',
        }, {
            capabilities: {
                tools: {},
            },
        });
        this.axiosInstance = axios.create({
            baseURL: GRAPHQL_ENDPOINT,
            headers: {
                'Content-Type': 'application/json',
            },
            timeout: 30000,
        });
        this.setupToolHandlers();
        // 错误处理
        this.server.onerror = (error) => console.error('[MCP Error]', error);
        process.on('SIGINT', async () => {
            await this.server.close();
            process.exit(0);
        });
    }
    setupToolHandlers() {
        // 列出可用工具
        this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
            tools: [
                {
                    name: 'search_properties_structured',
                    description: '使用结构化参数精准搜索悉尼租房信息，支持大学通勤时间筛选',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            university: {
                                type: 'string',
                                enum: ['UNSW', 'USYD', 'UTS', 'MACQUARIE', 'WSU'],
                                description: '目标大学'
                            },
                            max_commute_minutes: {
                                type: 'number',
                                description: '最大通勤时间(分钟)',
                                minimum: 1,
                                maximum: 120
                            },
                            bedrooms: {
                                type: 'number',
                                description: '卧室数量 (0=studio, 1=一房, 2=二房等)',
                                minimum: 0,
                                maximum: 5
                            },
                            max_rent_pw: {
                                type: 'number',
                                description: '最大周租金(AUD)',
                                minimum: 100
                            },
                            min_rent_pw: {
                                type: 'number',
                                description: '最小周租金(AUD)',
                                minimum: 100
                            },
                            property_type: {
                                type: 'string',
                                enum: ['apartment', 'studio', 'house', 'townhouse'],
                                description: '房产类型'
                            },
                            furnished: {
                                type: 'boolean',
                                description: '是否需要家具'
                            }
                        }
                    }
                },
                {
                    name: 'get_property_detail',
                    description: '获取指定房源的详细信息',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            listing_id: {
                                type: 'string',
                                description: '房源ID'
                            }
                        },
                        required: ['listing_id']
                    }
                },
                {
                    name: 'compare_universities',
                    description: '比较多个大学附近的房源情况',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            universities: {
                                type: 'array',
                                items: {
                                    type: 'string',
                                    enum: ['UNSW', 'USYD', 'UTS', 'MACQUARIE', 'WSU']
                                },
                                description: '要比较的大学列表',
                                minItems: 2,
                                maxItems: 5
                            },
                            bedrooms: {
                                type: 'number',
                                description: '卧室数量筛选',
                                minimum: 0,
                                maximum: 5
                            },
                            max_rent_pw: {
                                type: 'number',
                                description: '最大周租金筛选',
                                minimum: 100
                            }
                        },
                        required: ['universities']
                    }
                }
            ],
        }));
        // 处理工具调用
        this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
            switch (request.params.name) {
                case 'search_properties_structured':
                    return this.handleStructuredSearch(request.params.arguments);
                case 'get_property_detail':
                    return this.handlePropertyDetail(request.params.arguments);
                case 'compare_universities':
                    return this.handleUniversityComparison(request.params.arguments);
                default:
                    throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${request.params.name}`);
            }
        });
    }
    async handleStructuredSearch(args) {
        try {
            const params = this.validateSearchParams(args);
            let results = [];
            let searchStats = {
                totalFound: 0,
                avgRent: 0,
                minDistance: 0,
                searchType: ''
            };
            if (params.university) {
                // 使用大学通勤搜索
                const commuteData = await this.searchByUniversity(params);
                results = commuteData.properties;
                searchStats = commuteData.stats;
            }
            else {
                // 使用通用搜索
                const generalData = await this.searchGeneral(params);
                results = generalData.properties;
                searchStats = generalData.stats;
            }
            const formattedResponse = this.formatSearchResults(results, searchStats, params);
            return {
                content: [
                    {
                        type: 'text',
                        text: formattedResponse,
                    },
                ],
            };
        }
        catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `❌ 搜索出错: ${error instanceof Error ? error.message : '未知错误'}`,
                    },
                ],
                isError: true,
            };
        }
    }
    async handlePropertyDetail(args) {
        try {
            if (!args.listing_id) {
                throw new Error('需要提供listing_id参数');
            }
            const query = `
        query GetPropertyDetail($listingId: String!) {
          all_properties(filters: {listing_id: $listingId}, limit: 1) {
            items {
              listing_id
              address
              suburb
              state
              postcode
              property_type
              rent_pw
              bond
              bedrooms
              bathrooms
              parking_spaces
              available_date
              inspection_times
              agency_name
              agent_name
              agent_phone
              agent_email
              property_headline
              property_description
              has_air_conditioning
              is_furnished
              has_balcony
              has_dishwasher
              has_laundry
              has_built_in_wardrobe
              has_gym
              has_pool
              has_parking
              allows_pets
              latitude
              longitude
            }
          }
        }
      `;
            const response = await this.axiosInstance.post('', {
                query,
                variables: { listingId: args.listing_id }
            });
            const properties = response.data?.data?.all_properties?.items || [];
            if (properties.length === 0) {
                return {
                    content: [
                        {
                            type: 'text',
                            text: `❌ 未找到房源ID: ${args.listing_id}`,
                        },
                    ],
                };
            }
            const property = properties[0];
            const formattedDetail = this.formatPropertyDetail(property);
            return {
                content: [
                    {
                        type: 'text',
                        text: formattedDetail,
                    },
                ],
            };
        }
        catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `❌ 获取房源详情出错: ${error instanceof Error ? error.message : '未知错误'}`,
                    },
                ],
                isError: true,
            };
        }
    }
    async handleUniversityComparison(args) {
        try {
            if (!args.universities || !Array.isArray(args.universities) || args.universities.length < 2) {
                throw new Error('需要提供至少2个大学进行比较');
            }
            const comparisonResults = [];
            for (const university of args.universities) {
                const searchParams = {
                    university: university,
                    bedrooms: args.bedrooms,
                    max_rent_pw: args.max_rent_pw
                };
                try {
                    const data = await this.searchByUniversity(searchParams);
                    comparisonResults.push({
                        university,
                        stats: data.stats,
                        sampleProperties: data.properties.slice(0, 3) // 取前3个样本
                    });
                }
                catch (error) {
                    comparisonResults.push({
                        university,
                        error: `搜索失败: ${error instanceof Error ? error.message : '未知错误'}`
                    });
                }
            }
            const formattedComparison = this.formatUniversityComparison(comparisonResults, args);
            return {
                content: [
                    {
                        type: 'text',
                        text: formattedComparison,
                    },
                ],
            };
        }
        catch (error) {
            return {
                content: [
                    {
                        type: 'text',
                        text: `❌ 大学比较出错: ${error instanceof Error ? error.message : '未知错误'}`,
                    },
                ],
                isError: true,
            };
        }
    }
    validateSearchParams(args) {
        const params = {};
        if (args.university) {
            if (!Object.keys(UNIVERSITY_MAPPING).includes(args.university)) {
                throw new Error(`不支持的大学: ${args.university}`);
            }
            params.university = args.university;
        }
        if (args.max_commute_minutes !== undefined) {
            params.max_commute_minutes = Number(args.max_commute_minutes);
        }
        if (args.bedrooms !== undefined) {
            params.bedrooms = Number(args.bedrooms);
        }
        if (args.max_rent_pw !== undefined) {
            params.max_rent_pw = Number(args.max_rent_pw);
        }
        if (args.min_rent_pw !== undefined) {
            params.min_rent_pw = Number(args.min_rent_pw);
        }
        if (args.property_type) {
            params.property_type = args.property_type;
        }
        if (args.furnished !== undefined) {
            params.furnished = Boolean(args.furnished);
        }
        return params;
    }
    async searchByUniversity(params) {
        const query = `
      query GetUniversityCommute($universityName: UniversityNameEnum!, $limit: Int!) {
        get_university_commute_profile(university_name: $universityName, limit: $limit) {
          directWalkOptions {
            items {
              property {
                listing_id
                address
                suburb
                rent_pw
                bedrooms
                bathrooms
                property_type
                available_date
              }
              walkTimeToUniversityMinutes
            }
            totalCount
          }
        }
      }
    `;
        const limit = 3000; // 默认限制
        const response = await this.axiosInstance.post('', {
            query,
            variables: {
                universityName: params.university,
                limit
            }
        });
        if (response.data?.errors) {
            throw new Error(`GraphQL错误: ${response.data.errors[0]?.message || '未知错误'}`);
        }
        const walkOptions = response.data?.data?.get_university_commute_profile?.directWalkOptions;
        if (!walkOptions) {
            throw new Error('无法获取通勤数据');
        }
        let properties = walkOptions.items || [];
        // 应用筛选条件
        properties = this.applyFilters(properties, params);
        // 计算统计信息
        const stats = this.calculateStats(properties, 'university');
        return { properties, stats };
    }
    async searchGeneral(params) {
        const query = `
      query GetAllProperties($limit: Int!) {
        all_properties(limit: $limit) {
          items {
            listing_id
            address
            suburb
            rent_pw
            bedrooms
            bathrooms
            property_type
            available_date
          }
          totalCount
        }
      }
    `;
        const limit = 3000;
        const response = await this.axiosInstance.post('', {
            query,
            variables: { limit }
        });
        if (response.data?.errors) {
            throw new Error(`GraphQL错误: ${response.data.errors[0]?.message || '未知错误'}`);
        }
        const allProperties = response.data?.data?.all_properties?.items || [];
        // 转换为CommuteProperty格式
        let properties = allProperties.map((prop) => ({
            property: prop
        }));
        // 应用筛选条件
        properties = this.applyFilters(properties, params);
        // 计算统计信息
        const stats = this.calculateStats(properties, 'general');
        return { properties, stats };
    }
    applyFilters(properties, params) {
        return properties.filter(item => {
            const prop = item.property;
            // 卧室数筛选
            if (params.bedrooms !== undefined && prop.bedrooms !== params.bedrooms) {
                return false;
            }
            // 租金范围筛选
            if (params.min_rent_pw !== undefined && prop.rent_pw < params.min_rent_pw) {
                return false;
            }
            if (params.max_rent_pw !== undefined && prop.rent_pw > params.max_rent_pw) {
                return false;
            }
            // 通勤时间筛选
            if (params.max_commute_minutes !== undefined && item.walkTimeToUniversityMinutes !== undefined) {
                if (item.walkTimeToUniversityMinutes > params.max_commute_minutes) {
                    return false;
                }
            }
            // 房产类型筛选
            if (params.property_type && prop.property_type &&
                prop.property_type.toLowerCase() !== params.property_type.toLowerCase()) {
                return false;
            }
            return true;
        });
    }
    calculateStats(properties, searchType) {
        const totalFound = properties.length;
        const rents = properties.map(p => p.property.rent_pw).filter(r => r > 0);
        const avgRent = rents.length > 0 ? Math.round(rents.reduce((a, b) => a + b, 0) / rents.length) : 0;
        const walkTimes = properties
            .map(p => p.walkTimeToUniversityMinutes)
            .filter(t => t !== undefined);
        const minDistance = walkTimes.length > 0 ? Math.min(...walkTimes) : 0;
        return {
            totalFound,
            avgRent,
            minDistance,
            searchType
        };
    }
    formatSearchResults(properties, stats, params) {
        let result = '🎯 搜索条件:\n';
        if (params.university) {
            result += `大学: ${params.university}\n`;
        }
        if (params.max_commute_minutes) {
            result += `通勤时间: ≤${params.max_commute_minutes}分钟\n`;
        }
        if (params.bedrooms !== undefined) {
            const bedroomText = params.bedrooms === 0 ? 'Studio' : `${params.bedrooms}房`;
            result += `房型: ${bedroomText}\n`;
        }
        if (params.max_rent_pw) {
            result += `价格: ≤$${params.max_rent_pw}/周\n`;
        }
        if (params.min_rent_pw) {
            result += `最低价格: ≥$${params.min_rent_pw}/周\n`;
        }
        result += `\n📍 找到 ${stats.totalFound} 个符合条件的房源:\n\n`;
        if (properties.length === 0) {
            result += '❌ 无符合条件的房源\n\n';
            result += '💡 建议调整条件:\n';
            result += '• 增加预算范围\n';
            result += '• 延长通勤时间\n';
            result += '• 考虑其他房型\n';
            return result;
        }
        // 显示前10个结果
        const displayProperties = properties.slice(0, 10);
        displayProperties.forEach((item, index) => {
            const prop = item.property;
            const bedroomText = prop.bedrooms === 0 ? 'Studio' : `${prop.bedrooms}房${prop.bathrooms}卫`;
            result += `[${index + 1}] 房源信息\n`;
            result += `💰 $${prop.rent_pw}/周 | 🏠 ${bedroomText} | 📍 ${prop.suburb}\n`;
            if (item.walkTimeToUniversityMinutes) {
                result += `🚶 步行${item.walkTimeToUniversityMinutes}分钟到${params.university}\n`;
            }
            if (prop.available_date) {
                result += `📅 可入住: ${prop.available_date}\n`;
            }
            result += `🏡 地址: ${prop.address}\n`;
            result += `🔗 房源ID: ${prop.listing_id}\n`;
            result += '---\n';
        });
        if (properties.length > 10) {
            result += `\n... 还有 ${properties.length - 10} 个房源未显示\n`;
        }
        result += '\n📈 搜索统计:\n';
        if (stats.avgRent > 0) {
            result += `• 平均租金: $${stats.avgRent}/周\n`;
        }
        if (stats.minDistance > 0) {
            result += `• 最近距离: ${stats.minDistance}分钟步行\n`;
        }
        result += `• 搜索类型: ${stats.searchType === 'university' ? '大学通勤' : '通用搜索'}\n`;
        return result;
    }
    formatPropertyDetail(property) {
        let result = `🏠 房源详细信息\n\n`;
        result += `📋 基本信息:\n`;
        result += `• 房源ID: ${property.listing_id}\n`;
        result += `• 地址: ${property.address}\n`;
        result += `• 区域: ${property.suburb}, ${property.state} ${property.postcode}\n`;
        if (property.property_type) {
            result += `• 房产类型: ${property.property_type}\n`;
        }
        result += `\n💰 租金信息:\n`;
        result += `• 周租金: $${property.rent_pw}\n`;
        if (property.bond) {
            result += `• 押金: $${property.bond}\n`;
        }
        result += `\n🏠 房屋配置:\n`;
        result += `• 卧室: ${property.bedrooms}间\n`;
        result += `• 卫生间: ${property.bathrooms}间\n`;
        if (property.parking_spaces) {
            result += `• 停车位: ${property.parking_spaces}个\n`;
        }
        if (property.available_date) {
            result += `\n📅 可入住时间: ${property.available_date}\n`;
        }
        if (property.inspection_times) {
            result += `\n🏠 看房时间: ${property.inspection_times}\n`;
        }
        result += `\n👤 联系信息:\n`;
        if (property.agency_name) {
            result += `• 中介: ${property.agency_name}\n`;
        }
        if (property.agent_name) {
            result += `• 经纪人: ${property.agent_name}\n`;
        }
        if (property.agent_phone) {
            result += `• 电话: ${property.agent_phone}\n`;
        }
        if (property.agent_email) {
            result += `• 邮箱: ${property.agent_email}\n`;
        }
        if (property.property_headline) {
            result += `\n📝 房源标题:\n${property.property_headline}\n`;
        }
        if (property.property_description) {
            result += `\n📄 房源描述:\n${property.property_description.substring(0, 300)}${property.property_description.length > 300 ? '...' : ''}\n`;
        }
        // 房屋设施
        const features = [];
        if (property.has_air_conditioning)
            features.push('空调');
        if (property.is_furnished)
            features.push('带家具');
        if (property.has_balcony)
            features.push('阳台');
        if (property.has_dishwasher)
            features.push('洗碗机');
        if (property.has_laundry)
            features.push('洗衣设施');
        if (property.has_built_in_wardrobe)
            features.push('内置衣柜');
        if (property.has_gym)
            features.push('健身房');
        if (property.has_pool)
            features.push('游泳池');
        if (property.has_parking)
            features.push('停车位');
        if (property.allows_pets)
            features.push('允许宠物');
        if (features.length > 0) {
            result += `\n✨ 房屋设施:\n• ${features.join('、')}\n`;
        }
        if (property.latitude && property.longitude) {
            result += `\n📍 坐标: ${property.latitude}, ${property.longitude}\n`;
        }
        return result;
    }
    formatUniversityComparison(results, params) {
        let result = '📊 大学附近房源对比\n\n';
        if (params.bedrooms !== undefined) {
            const bedroomText = params.bedrooms === 0 ? 'Studio' : `${params.bedrooms}房`;
            result += `房型: ${bedroomText}\n`;
        }
        if (params.max_rent_pw) {
            result += `预算: ≤$${params.max_rent_pw}/周\n`;
        }
        result += '\n';
        // 创建对比表格
        result += '大学'.padEnd(15) + '房源数量'.padEnd(12) + '平均租金'.padEnd(12) + '最短通勤\n';
        result += '='.repeat(50) + '\n';
        results.forEach(item => {
            if (item.error) {
                result += `${item.university.padEnd(15)}错误: ${item.error}\n`;
            }
            else {
                const stats = item.stats;
                const avgRentStr = stats.avgRent > 0 ? `$${stats.avgRent}/周` : 'N/A';
                const minDistanceStr = stats.minDistance > 0 ? `${stats.minDistance}分钟` : 'N/A';
                result += `${item.university.padEnd(15)}${stats.totalFound.toString().padEnd(12)}${avgRentStr.padEnd(12)}${minDistanceStr}\n`;
            }
        });
        result += '\n💡 详细信息:\n';
        results.forEach(item => {
            if (!item.error && item.sampleProperties.length > 0) {
                result += `\n🎓 ${item.university} 样本房源:\n`;
                item.sampleProperties.slice(0, 2).forEach((prop, index) => {
                    const property = prop.property;
                    const bedroomText = property.bedrooms === 0 ? 'Studio' : `${property.bedrooms}房`;
                    result += `${index + 1}. $${property.rent_pw}/周 - ${bedroomText} - ${property.suburb}`;
                    if (prop.walkTimeToUniversityMinutes) {
                        result += ` (步行${prop.walkTimeToUniversityMinutes}分钟)`;
                    }
                    result += '\n';
                });
            }
        });
        return result;
    }
    async run() {
        const transport = new StdioServerTransport();
        await this.server.connect(transport);
        console.error('Sydney Rental MCP server running on stdio');
    }
}
const server = new SydneyRentalMCP();
server.run().catch(console.error);
//# sourceMappingURL=index.js.map