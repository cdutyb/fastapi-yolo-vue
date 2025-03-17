<template>
  <section class="profile-container">
    <h1 class="profile-title">Your Profile</h1>
    <hr class="divider"/>

    <!-- User Information -->
    <div class="user-info">
      <p><strong>Full Name:</strong> <span>{{ user.full_name }}</span></p>
      <p><strong>Username:</strong> <span>{{ user.username }}</span></p>
      <p><button @click="deleteAccount()" class="btn btn-danger">Delete Account</button></p>
    </div>

    <!-- School Information -->
    <hr class="divider"/>
    <h2 class="section-title">学校信息</h2>
    <div class="school-info">
      <p><strong>学校名字:</strong> <span>{{ schoolInfo.name }}</span></p>
      <p><strong>系别:</strong> <span>{{ schoolInfo.department }}</span></p>
      <p><strong>年级:</strong> <span>{{ schoolInfo.yearOfStudy }}</span></p>

      <!-- School Environment Images with horizontal scroll -->
      <div class="school-image-container" ref="imageContainer">
        <div class="school-images" ref="imageScroll" @scroll="onScroll">
          <div class="image-wrapper" v-for="(image, index) in schoolInfo.images" :key="index">
            <img :src="image" alt="School Environment" class="school-image"/>
          </div>
        </div>
      </div>
    </div>

    <!-- Group Members -->
    <hr class="divider"/>
    <h2 class="section-title">小组成员</h2>
    <div class="group-members-container">
      <div v-for="(member, index) in groupMembers" :key="index" class="group-member">
        <p><strong>成员 {{ index + 1 }}:</strong></p>
        <p>名字: {{ member.name }}</p>
        <p>学号: {{ member.studentId }}</p>
      </div>
    </div>
  </section>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'ProfileView',
  created() {
    this.$store.dispatch('viewMe');
  },
  computed: {
    ...mapGetters({ user: 'stateUser' }),
    schoolInfo() {
      return {
        name: '成都理工大学',
        department: '智能科学与技术',
        yearOfStudy: '2022',
        images: [
          require('@/assets/2.jpg'),
          require('@/assets/1.jpg'),
          require('@/assets/3.jpg'),
        ],
      };
    },
    groupMembers() {
      return [
        { name: 'John Doe', studentId: '2023012345' },
        { name: 'Jane Smith', studentId: '2023012346' },
        { name: 'Alice Johnson', studentId: '2023012347' },
      ];
    },
  },
  methods: {
    ...mapActions(['deleteUser']),
    async deleteAccount() {
      try {
        await this.deleteUser(this.user.id);
        await this.$store.dispatch('logOut');
        this.$router.push('/');
      } catch (error) {
        console.error(error);
      }
    },

    onScroll() {
      const container = this.$refs.imageContainer;
      const scrollLeft = container.scrollLeft;
      const maxScrollLeft = container.scrollWidth - container.clientWidth;

      // Check if we've reached the end, then reset to the start
      if (scrollLeft === maxScrollLeft) {
        container.scrollLeft = 0;
      }
    },
  },
});
</script>
<style scoped>
/* Profile Container */
.profile-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 30px;
  background: linear-gradient(135deg, #A3B7C7, #D0E0F0); /* 淡蓝色渐变背景 */
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-size: cover;
  background-position: center;
  position: relative;
  z-index: 10;
  overflow: hidden;
}

/* 页面标题 */
.profile-title {
  text-align: center;
  font-size: 2.4em;
  color: #2C3E50; /* 深蓝色 */
  margin-bottom: 15px;
}

/* Divider */
.divider {
  border-top: 2px solid #5B8FB9; /* 柔和蓝色的边框 */
  margin: 20px 0;
}

/* 用户信息卡片 */
.user-info {
  background: linear-gradient(145deg, #ffc7a6, #ffbfb9); /* 橙色渐变背景 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-left: 8px solid #5B8FB9; /* 左侧边框，用柔和蓝色 */
}

.user-info p {
  margin: 12px 0;
  font-size: 1.1em;
  color: #2C3E50; /* 深蓝色文字 */
}

/* 删除账户按钮 */
.btn {
  padding: 10px 25px;
  background-color: #FF6F61; /* 温暖的橙色 */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1em;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #FF914D; /* 橙色渐变 */
}

/* 小节标题 */
.section-title {
  font-size: 1.8em;
  color: #2C3E50; /* 深蓝色 */
  margin-bottom: 20px;
  font-weight: bold;
}

/* 学校信息卡片 */
.school-info {
  padding: 20px;
  background: linear-gradient(145deg, #A1D8C1, #C8D3D9); /* 清新的蓝绿色渐变 */
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-left: 8px solid #5B8FB9; /* 左侧边框，增加深蓝色对比 */
}

.school-info p {
  margin: 10px 0;
  font-size: 1.2em;
  color: #2C3E50; /* 深蓝色文字 */
}

/* 学校图片滚动容器 */
.school-image-container {
  margin-top: 15px;
  position: relative;
  overflow-x: auto;
  padding: 10px 0;
  display: flex;
  justify-content: center;
}

.school-images {
  display: flex;
  gap: 15px;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
}

.image-wrapper {
  flex-shrink: 0;
  width: 320px;
  height: 180px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  background-color: #ffffff; /* 保持图片区域的背景为白色 */
}

.school-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* 小组成员卡片 */
.group-members-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  justify-content: space-between;
}

.group-member {
  width: 30%;
  padding: 15px;
  background: linear-gradient(145deg, #D6B4A0, #F1D0C1); /* 柔和的粉色渐变 */
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.group-member:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.group-member p {
  margin: 8px 0;
  font-size: 1.1em;
  color: #34495e; /* 温和的深灰色 */
}
</style>
