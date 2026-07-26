import axios from "axios";

const api_key = import.meta.env.VITE_API_KEY;
const api_base_url = import.meta.env.VITE_BASE_URL;

// axios instance
export const api = axios.create({
    baseURL: `${api_base_url}`,
    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${api_key}`
    }
});