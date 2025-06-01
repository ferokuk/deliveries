import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string;
const api = axios.create({
    baseURL: API_BASE_URL + '/api/v1',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});

export default api;
