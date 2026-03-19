import axios from "axios";

const API_BASE_URL =
  import.meta.env.MODE === "development"
    ? "http://localhost:3000"
    : window.location.origin;

export const axiosInstance = axios.create({
  baseURL:
    import.meta.env.MODE === "development"
      ? "http://localhost:3000/api"
      : "/api",
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
