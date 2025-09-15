const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3001;

// 安全中间件
app.use(helmet());
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true
}));

// 速率限制
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分钟
  max: 100, // 每个IP限制100请求
  message: '请求过于频繁，请稍后再试'
});
app.use('/api/', limiter);

app.use(express.json());

// GraphQL客户端配置
const graphqlClient = axios.create({
  baseURL: process.env.GRAPHQL_ENDPOINT || 'http://localhost:8000/graphql',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.API_TOKEN}`
  }
});

// 健康检查
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 房源搜索API
app.post('/api/properties/search', async (req, res) => {
  try {
    const { university, max_commute_minutes, bedrooms, max_rent_pw, min_rent_pw } = req.body;
    
    // 参数验证
    if (!university || !['UNSW', 'USYD', 'UTS', 'MACQUARIE', 'WSU'].includes(university)) {
      return res.status(400).json({ error: '无效的大学参数' });
    }

    const query = `
      query GetUniversityCommute(
        $universityName: UniversityNameEnum!,
        $limit: Int!,
        $offset: Int,
        $min_rent_pw: Int,
        $max_rent_pw: Int,
        $min_bedrooms: Int,
        $max_commute_minutes: Int
      ) {
        get_university_commute_profile(
          university_name: $universityName,
          limit: $limit,
          offset: $offset,
          min_rent_pw: $min_rent_pw,
          max_rent_pw: $max_rent_pw,
          min_bedrooms: $min_bedrooms,
          max_commute_minutes: $max_commute_minutes
        ) {
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

    const response = await graphqlClient.post('', {
      query,
      variables: {
        universityName: university,
        limit: 50,
        offset: 0,
        min_rent_pw,
        max_rent_pw,
        min_bedrooms: bedrooms,
        max_commute_minutes
      }
    });

    if (response.data?.errors) {
      throw new Error(`GraphQL错误: ${response.data.errors[0]?.message}`);
    }

    const walkOptions = response.data?.data?.get_university_commute_profile?.directWalkOptions;
    const items = walkOptions?.items || [];
    const properties = items; // 信任后端口径：不在 Node 层做二次筛选

    // 计算统计信息
    const totalFound = walkOptions?.totalCount ?? properties.length;
    const rents = properties.map(p => p.property.rent_pw).filter(r => r > 0);
    const avgRent = rents.length > 0 ? Math.round(rents.reduce((a, b) => a + b, 0) / rents.length) : 0;
    const walkTimes = properties.map(p => p.walkTimeToUniversityMinutes).filter(t => t !== undefined);
    const minDistance = walkTimes.length > 0 ? Math.min(...walkTimes) : 0;

    res.json({
      properties: properties.slice(0, 20), // 限制返回数量
      stats: {
        totalFound,
        avgRent,
        minDistance,
        searchType: 'university'
      }
    });

  } catch (error) {
    console.error('搜索错误:', error);
    res.status(500).json({ 
      error: '搜索服务暂时不可用',
      details: process.env.NODE_ENV === 'development' ? error.message : undefined
    });
  }
});

// 房源详情API
app.get('/api/properties/:listingId', async (req, res) => {
  try {
    const { listingId } = req.params;
    
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
            latitude
            longitude
          }
        }
      }
    `;

    const response = await graphqlClient.post('', {
      query,
      variables: { listingId }
    });

    const properties = response.data?.data?.all_properties?.items || [];
    
    if (properties.length === 0) {
      return res.status(404).json({ error: '房源未找到' });
    }

    res.json({ property: properties[0] });

  } catch (error) {
    console.error('获取房源详情错误:', error);
    res.status(500).json({ error: '获取房源详情失败' });
  }
});

// 大学比较API
app.post('/api/universities/compare', async (req, res) => {
  try {
    const { universities, bedrooms, max_rent_pw } = req.body;
    
    if (!universities || !Array.isArray(universities) || universities.length < 2) {
      return res.status(400).json({ error: '需要提供至少2个大学进行比较' });
    }

    const results = [];
    
    for (const university of universities) {
      try {
        const searchResponse = await axios.post(`${req.protocol}://${req.get('host')}/api/properties/search`, {
          university,
          bedrooms,
          max_rent_pw
        });
        
        results.push({
          university,
          stats: searchResponse.data.stats,
          sampleProperties: searchResponse.data.properties.slice(0, 3)
        });
      } catch (error) {
        results.push({
          university,
          error: `搜索失败: ${error.message}`
        });
      }
    }

    res.json({ comparison: results });

  } catch (error) {
    console.error('大学比较错误:', error);
    res.status(500).json({ error: '大学比较服务失败' });
  }
});

// 错误处理中间件
app.use((error, req, res, next) => {
  console.error('未处理的错误:', error);
  res.status(500).json({ 
    error: '服务器内部错误',
    timestamp: new Date().toISOString()
  });
});

// 404处理
app.use((req, res) => {
  res.status(404).json({ error: '接口不存在' });
});

app.listen(PORT, () => {
  console.log(`生产环境MCP服务器运行在端口 ${PORT}`);
});

module.exports = app;
