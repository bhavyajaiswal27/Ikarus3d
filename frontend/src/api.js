import axios from 'axios';



const API = axios.create({ baseURL: "http://localhost:8000" });

export const recommend = (query, top_k=5) => API.post('/recommend', { query, top_k });
export const generateDescription = (uniq_id) => API.post('/generate-description', { uniq_id });
export const getAnalytics = () => API.get('/analytics');
