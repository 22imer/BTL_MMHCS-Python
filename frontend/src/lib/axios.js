import axios from "axios";

// Dynamically determine API base URL based on current location
// In development: use same hostname as frontend but with backend port (3000)
// In production: use relative path (same origin)
const getApiBaseUrl = () => {
  if (import.meta.env.MODE === "development") {
    const protocol = window.location.protocol; // http: or https:
    const hostname = window.location.hostname;
    return `${protocol}//${hostname}:3000`;
  }
  return window.location.origin;
};

const API_BASE_URL = getApiBaseUrl();

export const axiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  withCredentials: true,
});

// Utility function to convert relative image URLs to absolute backend URLs
export const getImageUrl = (imagePath) => {
  if (!imagePath) return null;
  // If it's already an absolute URL, return it as is
  if (imagePath.startsWith("http://") || imagePath.startsWith("https://")) {
    return imagePath;
  }
  // If it's a data URL (base64), return it as is
  if (imagePath.startsWith("data:")) {
    return imagePath;
  }
  // Otherwise, prepend the backend URL
  return `${API_BASE_URL}${imagePath}`;
};
