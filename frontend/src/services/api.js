import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getIncidents = async () => {
  const response = await api.get('/anomalies');
  return response.data;
};

export const explainIncident = async (serviceId, focus) => {
  const response = await api.post('/ai/explain', {
    service_id: serviceId,
    focus: focus,
  });
  return response.data;
};

export default api;
