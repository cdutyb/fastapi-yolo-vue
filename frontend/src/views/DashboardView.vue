<template>
  <div class="container">
    <h2 class="title">YOLO 目标检测系统</h2>

    <el-card class="control-panel">
      <!-- 模型选择区域 -->
      <div class="section">
        <h3 class="section-title">模型选择</h3>
        <div class="model-selection">
          <el-select
            v-model="selectedModel"
            placeholder="选择YOLO模型"
            class="model-select">
            <el-option v-for="model in models" :key="model" :label="model" :value="model" />
          </el-select>
          <el-button type="primary" @click="changeYoloModel">切换模型 (必须点)</el-button>
        </div>
      </div>

      <el-divider />

      <!-- 置信度设置区域 -->
      <div class="section">
        <h3 class="section-title">置信度阈值设置</h3>
        <div class="conf-threshold">
          <span>较低 (更多检测结果)</span>
          <el-slider
            v-model="confThreshold"
            :min="0.1"
            :max="0.9"
            :step="0.05"
            :format-tooltip="formatTooltip"
            class="slider" />
          <span>较高 (更精确结果)</span>
        </div>
        <div class="current-value">当前置信度阈值: {{ formatPercentage(confThreshold) }}</div>
      </div>

      <el-divider />

      <!-- 检测区域 -->
      <div class="detection-row">
        <!-- 图片检测区域 -->
        <div class="section detection-section">
          <h3 class="section-title">图片检测</h3>
          <div class="upload-area">
            <el-upload
              v-model:file-list="imageFiles"
              multiple
              action="#"
              :auto-upload="false"
              :before-upload="handleImageSelect"
              class="uploader"
            >
              <el-button type="primary">选择图片</el-button>
              <template #tip>
                <div class="el-upload__tip">支持jpg、png、jpeg格式，支持多张图片</div>
              </template>
            </el-upload>
            <el-button type="success" @click="uploadImages" :disabled="!imageFiles.length">
              开始检测
            </el-button>
          </div>
        </div>

        <!-- 视频检测区域 -->
        <div class="section detection-section">
          <h3 class="section-title">视频检测</h3>
          <div class="upload-area">
            <el-upload
              v-model:file-list="videoFile"
              action="#"
              :auto-upload="false"
              :limit="1"
              :before-upload="handleVideoSelect"
              class="uploader"
            >
              <el-button type="primary">选择视频</el-button>
              <template #tip>
                <div class="el-upload__tip">支持mp4、avi格式，支持一个视频</div>
              </template>
            </el-upload>
            <el-button type="success" @click="uploadVideo" :disabled="!videoFile.length">
              开始检测
            </el-button>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 图片结果对比区域 -->
    <el-card v-if="resultImages.length" class="result-card">
      <template #header>
        <div class="result-header">
          <h3>图片检测结果</h3>
        </div>
      </template>

      <div class="comparison-grid">
        <div v-for="(image, index) in resultImages" :key="index" class="comparison-item">
          <div class="comparison-pair">
            <div class="comparison-half">
              <h4>原图</h4>
              <el-image
                :src="originalImages[index]"
                fit="contain"
                :preview-src-list="[originalImages[index]]"
                @error="handleImageError">
              </el-image>
            </div>
            <div class="comparison-half">
              <h4>检测结果</h4>
              <el-image
                :src="image"
                fit="contain"
                :preview-src-list="[image]"
                @error="handleImageError">
              </el-image>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 视频结果对比区域 -->
    <el-card v-if="resultVideo" class="result-card">
      <template #header>
        <div class="result-header">
          <h3>视频检测结果</h3>
        </div>
      </template>
      <div class="video-comparison">
        <div class="comparison-half">
          <h4>原视频</h4>
          <video controls :src="originalVideo" class="result-video"></video>
        </div>
        <div class="comparison-half">
          <h4>检测结果</h4>
          <video controls :src="resultVideo" class="result-video" @error="handleVideoError"></video>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { detectImages, detectVideo, changeModel, getAvailableModels } from '@/store/modules/yolo';
import { ElMessage } from 'element-plus';
import axios from "axios";

export default {
  setup() {
    const imageFiles = ref([]);
    const videoFile = ref([]);
    const confThreshold = ref(0.25);
    const resultImages = ref([]);
    const resultVideo = ref('');
    const originalImages = ref([]);
    const originalVideo = ref('');
    const models = ref([]);
    const selectedModel = ref('');

    // 格式化百分比显示
    const formatPercentage = (value) => {
      return `${Math.round(value * 100)}%`;
    };

    // 格式化滑块悬浮提示内容
    const formatTooltip = (value) => {
      return formatPercentage(value);
    };

    // 辅助函数：构建正确的URL路径（避免双斜杠问题）
    const buildResourceUrl = (baseUrl, path, filename) => {
      // 移除URL末尾的斜杠（如果存在）
      const cleanBaseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
      // 确保路径以斜杠开头
      const cleanPath = path.startsWith('/') ? path : `/${path}`;
      return `${cleanBaseUrl}${cleanPath}/${filename}?t=${Date.now()}`;
    };

    onMounted(async () => {
      try {
        const response = await getAvailableModels();
        models.value = response.models || [];
        if (response.current_model) {
          selectedModel.value = response.current_model;
        }
      } catch (error) {
        console.error('获取模型列表失败:', error);
        ElMessage.error('获取模型列表失败');
      }
    });

    const handleImageSelect = (file) => {
      const isImage = file.type.indexOf('image/') !== -1;
      if (!isImage) {
        ElMessage.error('请上传图片类型文件!');
        return false;
      }
      return true;
    };

    const handleVideoSelect = (file) => {
      const isVideo = file.type.indexOf('video/') !== -1;
      if (!isVideo) {
        ElMessage.error('请上传视频类型文件!');
        return false;
      }
      return true;
    };

    const handleImageError = (e) => {
      console.error('图片加载失败:', e.target.src);
      ElMessage.warning('图片加载失败，请检查服务器路径或网络连接');
    };

    const handleVideoError = (e) => {
      console.error('视频加载失败:', e.target.src);
      ElMessage.warning('视频加载失败，请检查服务器路径或网络连接');
    };

    const uploadImages = async () => {
      if (!imageFiles.value.length) {
        ElMessage.warning('请先选择图片');
        return;
      }

      try {
        // 清空旧结果
        resultImages.value = [];
        originalImages.value = [];

        ElMessage.info('正在处理图片，请等候...');

        // 保存原始图片URL
        originalImages.value = imageFiles.value.map(file => URL.createObjectURL(file.raw));

        const filesArray = imageFiles.value.map(item => item.raw);
        const response = await detectImages(filesArray, confThreshold.value);

        console.log('后端响应:', response); // 调试日志

        // 使用辅助函数构建URL，避免双斜杠问题
        const baseUrl = axios.defaults.baseURL || '';
        resultImages.value = [...response.output_images.map(img =>
          buildResourceUrl(baseUrl, 'static/outputs/images', img)
        )];

        console.log('检测结果图片URLs:', resultImages.value); // 调试日志
        ElMessage.success('图片检测完成');
      } catch (error) {
        console.error('图片检测失败:', error);
        ElMessage.error('图片检测失败');
      }
    };

    const uploadVideo = async () => {
      if (!videoFile.value.length) {
        ElMessage.warning('请先选择视频');
        return;
      }

      try {
        resultVideo.value = '';
        originalVideo.value = '';
        ElMessage.info('正在处理视频，这可能需要一些时间...');

        // 保存原始视频URL
        originalVideo.value = URL.createObjectURL(videoFile.value[0].raw);

        const response = await detectVideo(videoFile.value[0].raw, confThreshold.value);

        console.log('后端响应:', response); // 调试日志

        // 使用辅助函数构建视频URL，避免双斜杠问题
        const baseUrl = axios.defaults.baseURL || '';

        resultVideo.value = buildResourceUrl(baseUrl, 'static/outputs/videos', response.output_video);

        console.log('检测结果视频URL:', resultVideo.value); // 调试日志
        ElMessage.success('视频检测完成');
      } catch (error) {
        console.error('视频检测失败:', error);
        ElMessage.error('视频检测失败');
      }
    };

    const changeYoloModel = async () => {
      if (!selectedModel.value) {
        ElMessage.warning('请选择一个模型');
        return;
      }

      try {
        ElMessage.info('正在切换模型...');
        await changeModel(selectedModel.value);
        ElMessage.success(`模型切换成功: ${selectedModel.value}`);
      } catch (error) {
        console.error('模型切换失败:', error);
        ElMessage.error('模型切换失败');
      }
    };

    return {
      imageFiles,
      videoFile,
      confThreshold,
      resultImages,
      resultVideo,
      originalImages,
      originalVideo,
      models,
      selectedModel,
      uploadImages,
      uploadVideo,
      changeYoloModel,
      handleImageSelect,
      handleVideoSelect,
      handleImageError,
      handleVideoError,
      formatPercentage,
      formatTooltip
    };
  }
};
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 1px auto;
  padding: 0 20px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
  color: #409EFF;
  font-weight: bold;
}

.control-panel {
  margin-bottom: 30px;
}

.section {
  margin-bottom: 1px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  color: #606266;
  margin-bottom: 15px;
}

.model-selection {
  display: flex;
  align-items: center;
  gap: 15px;
}

.model-select {
  width: 250px;
}

.conf-threshold {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.slider {
  margin: 0 15px;
  flex-grow: 1;
}

.current-value {
  margin-top: 5px;
  color: #606266;
  font-weight: bold;
  text-align: center;
}

/* 检测区域并排显示样式 */
.detection-row {
  display: flex;
  gap: 20px;
}

.detection-section {
  flex: 1;
  min-width: 0;
}

.upload-area {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.uploader {
  flex-grow: 1;
}

.result-card {
  margin-bottom: 30px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 原图和检测结果对比区域样式 */
.comparison-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  margin-top: 10px;
}

.comparison-pair {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.comparison-half {
  flex: 1;
  min-width: 0;
}

.comparison-half h4 {
  text-align: center;
  margin-bottom: 10px;
  color: #606266;
}

.video-comparison {
  display: flex;
  gap: 20px;
}

.result-video {
  max-width: 100%;
  border-radius: 4px;
}

.el-divider {
  margin: 24px 0;
}

@media (max-width: 768px) {
  .model-selection, .upload-area, .detection-row, .comparison-pair, .video-comparison {
    flex-direction: column;
    align-items: stretch;
  }

  .model-select {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>