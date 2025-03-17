<template>
  <div class="container">
    <h2>YOLO 目标检测</h2>

    <!-- 选择图片 -->
    <el-upload
      v-model:file-list="imageFiles"
      multiple
      action="#"
      :auto-upload="false"
      :before-upload="handleImageSelect"
    >
      <el-button type="primary">选择图片</el-button>
    </el-upload>

    <!-- 选择视频 -->
    <el-upload
      v-model:file-list="videoFile"
      action="#"
      :auto-upload="false"
      :limit="1"
      :before-upload="handleVideoSelect"
    >
      <el-button type="primary">选择视频</el-button>
    </el-upload>

    <!-- 置信度滑块 -->
    <el-slider v-model="confThreshold" :min="0.1" :max="1.0" :step="0.05" show-input />

    <!-- 按钮 -->
    <el-button type="success" @click="uploadImages">上传图片检测</el-button>
    <el-button type="warning" @click="uploadVideo">上传视频检测</el-button>

    <!-- 结果展示 -->
    <div v-if="resultImages.length">
      <h3>检测结果（图片）</h3>
      <div class="image-grid">
        <img v-for="(image, index) in resultImages" :key="index" :src="image" alt="检测结果">
      </div>
    </div>

    <div v-if="resultVideo">
      <h3>检测结果（视频）</h3>
      <video controls :src="resultVideo" width="600"></video>
    </div>

    <!-- 选择模型 -->
    <el-select v-model="selectedModel" placeholder="选择YOLO模型">
      <el-option v-for="model in models" :key="model" :label="model" :value="model" />
    </el-select>
    <el-button type="danger" @click="changeYoloModel">切换模型</el-button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { detectImages, detectVideo, changeModel, getAvailableModels } from '@/store/modules/yolo';

export default {
  setup() {
    const imageFiles = ref([]);
    const videoFile = ref([]);
    const confThreshold = ref(0.25);
    const resultImages = ref([]);
    const resultVideo = ref('');
    const models = ref([]);
    const selectedModel = ref('');

    onMounted(async () => {
      const response = await getAvailableModels();
      models.value = response.models; // 获取所有可用的YOLO模型
    });

    const handleImageSelect = (file) => {
      imageFiles.value.push(file);
      return false;
    };

    const handleVideoSelect = (file) => {
      videoFile.value = [file];
      return false;
    };

    const uploadImages = async () => {
      if (!imageFiles.value.length) {
        alert('请先选择图片');
        return;
      }
      const filesArray = imageFiles.value.map(item => item.raw);
      const response = await detectImages(filesArray, confThreshold.value);
      resultImages.value = response.input_images.map(img => `http://localhost:8000/${response.output_directory}/${img}`);
    };

    const uploadVideo = async () => {
      if (!videoFile.value.length) {
        alert('请先选择视频');
        return;
      }
      const response = await detectVideo(videoFile.value[0].raw, confThreshold.value);
      resultVideo.value = `http://localhost:8000/${response.output_video}`;
    };

    const changeYoloModel = async () => {
      if (!selectedModel.value) {
        alert('请选择一个模型');
        return;
      }
      await changeModel(`src/core/yolo/models/${selectedModel.value}`);
      alert(`模型切换成功: ${selectedModel.value}`);
    };

    return {
      imageFiles,
      videoFile,
      confThreshold,
      resultImages,
      resultVideo,
      models,
      selectedModel,
      uploadImages,
      uploadVideo,
      changeYoloModel,
      handleImageSelect,
      handleVideoSelect
    };
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
  text-align: center;
}

.image-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.image-grid img {
  width: 200px;
  border-radius: 5px;
}
</style>
