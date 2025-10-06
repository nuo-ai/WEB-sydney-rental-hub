import http from 'http';
import express from 'express';
import cors from 'cors';
import { z } from 'zod';
import axios from 'axios';

// Express App Setup
const app = express();
app.use(cors());
app.use(express.json());

// GraphQL API配置
const GRAPHQL_ENDPOINT = 'http://127.0.0.1:8000/graphql';
const GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY || 'YOUR_GOOGLE_MAPS_API_KEY';

const axiosInstance = axios.create({
  baseURL: GRAPHQL_ENDPOINT,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
});

// --- GraphQL 帮助函数 ---

const getPropertyDetails = async (propertyId: string) => {
  const query = `
    query GetPropertyDetails($id: String!) {
      property(id: $id) {
        id
        address
        suburb
        postcode
        rent_pw
        bedrooms
        bathrooms
        parking_spaces
        property_type
        available_date
        bond_amount
        is_furnished
        description
        image_url
        image_url_1, image_url_2, image_url_3, image_url_4, image_url_5
        inspection_times
        latitude
        longitude
      }
    }
  `;
  try {
    const response = await axiosInstance.post('', { query, variables: { id: propertyId } });
    if (response.data.errors) {
      throw new Error(`GraphQL Error: ${JSON.stringify(response.data.errors)}`);
    }
    return response.data.data.property;
  } catch (error) {
    console.error(`Error fetching property ${propertyId} from GraphQL:`, error);
    throw error;
  }
};

// --- API Endpoints ---

// 1. 获取房源详情
app.get('/api/properties/:id', async (req, res) => {
  const { id } = req.params;
  if (!id) {
    return res.status(400).json({ error: { message: 'Property ID is required' } });
  }

  try {
    const propertyData = await getPropertyDetails(id);
    if (!propertyData) {
      return res.status(404).json({ error: { message: `Property with ID ${id} not found` } });
    }
    res.json({ data: propertyData });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
    res.status(500).json({ error: { message: `Failed to fetch property details: ${errorMessage}` } });
  }
});

// 2. 获取通勤路线
const directionsSchema = z.object({
  origin: z.string(),
  destination: z.string(),
  mode: z.enum(['DRIVING', 'WALKING', 'BICYCLING', 'TRANSIT']),
});

app.get('/api/directions', async (req, res) => {
  const validation = directionsSchema.safeParse(req.query);
  if (!validation.success) {
    return res.status(400).json({ error: validation.error.format() });
  }

  const { origin, destination, mode } = validation.data;
  const url = `https://maps.googleapis.com/maps/api/directions/json?origin=${origin}&destination=${destination}&mode=${mode.toLowerCase()}&key=${GOOGLE_MAPS_API_KEY}`;

  try {
    const response = await axios.get(url);
    if (response.data.status !== 'OK') {
      throw new Error(`Google Maps API Error: ${response.data.status} - ${response.data.error_message || ''}`);
    }
    const route = response.data.routes[0];
    if (!route) {
        return res.json({ duration: 'N/A', distance: 'N/A', error: 'No route found' });
    }
    const leg = route.legs[0];
    res.json({
      duration: leg.duration.text,
      distance: leg.distance.text,
    });
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to fetch directions';
    console.error(errorMessage);
    res.status(500).json({ error: '无法计算通勤时间', duration: 'N/A', distance: 'N/A' });
  }
});

// --- Server Startup ---

// Vercel Serverless Function 导出
export default app;

// 本地开发服务器
if (process.env.NODE_ENV !== 'production') {
  const port = process.env.PORT || 3001;
  const server = http.createServer(app);
  server.listen(port, () => {
    console.log(`Express server for REST API running on port ${port}`);
  });
}
