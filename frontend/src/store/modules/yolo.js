import axios from 'axios';

const API_URL = 'http://localhost:5000/yolo';  // 根据你的 FastAPI 后端地址调整

// 1. 获取可用的YOLO模型
export const getAvailableModels = async () => {
  try {
    const response = await axios.get(`${API_URL}/available_models`);
    return response.data;
  } catch (error) {
    console.error('获取模型列表失败:', error);
    throw error;
  }
};

// 2. 执行图片检测
export const detectImages = async (files, confThreshold) => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append('files', file);
  });
  formData.append('conf_threshold', confThreshold);

  try {
    const response = await axios.post(`${API_URL}/detect`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  } catch (error) {
    console.error('图片检测失败:', error);
    throw error;
  }
};

// 3. 执行视频检测
export const detectVideo = async (file, confThreshold) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('conf_threshold', confThreshold);

  try {
    const response = await axios.post(`${API_URL}/detect_video`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  } catch (error) {
    console.error('视频检测失败:', error);
    throw error;
  }
};

// 4. 切换YOLO模型
export const changeModel = async (modelPath) => {
  const formData = new FormData();
  formData.append('model_path', modelPath);

  try {
    const response = await axios.post(`${API_URL}/change_model`, formData);
    return response.data;
  } catch (error) {
    console.error('切换模型失败:', error);
    throw error;
  }
};
