<template>
  <div id="app">
    <div v-if="login">
      <el-header>
        <el-menu router :default-active="'/'" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item>
            <i class="fa fa-home fa-2x"></i>
          </el-menu-item>
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/meeting">会议</el-menu-item>
          <el-menu-item index="/nothing">问卷</el-menu-item>
          <el-menu-item index="/manage">成员管理</el-menu-item>
          <!-- <el-submenu index="2">
            <template slot="title">我的工作台</template>
            <el-menu-item index="2-1">选项1</el-menu-item>
            <el-menu-item index="2-2">选项2</el-menu-item>
            <el-menu-item index="2-3">选项3</el-menu-item>
            <el-submenu index="2-4">
              <template slot="title">选项4</template>
              <el-menu-item index="2-4-1">选项1</el-menu-item>
              <el-menu-item index="2-4-2">选项2</el-menu-item>
              <el-menu-item index="2-4-3">选项3</el-menu-item>
            </el-submenu>
          </el-submenu>
          <el-menu-item index="3" disabled>消息中心</el-menu-item>
          <el-menu-item index="4">
            <a href="https://www.ele.me" target="_blank">订单管理</a>
          </el-menu-item>-->
          <span class="pull-right">
            <el-menu-item @click="Logout">
              <i class="fa fa-sign-out fa-2x"></i>
            </el-menu-item>
          </span>
        </el-menu>
      </el-header>
      <br>
      <el-main>
        <router-view>Main</router-view>
      </el-main>
      <!-- <el-footer>Footer</el-footer> -->
    </div>
    <div v-else>
      <LoginView></LoginView>
    </div>
  </div>
</template>
<script>
import LoginView from "@/components/login.vue";
import { mapMutations, mapGetters } from "vuex";

export default {
  name: "App",
  components: {
    LoginView: LoginView
  },
  computed: {
    ...mapGetters(["isLogin", "logining"])
  },
  data() {
    return {
      login: this.checkLogin()
    };
  },
  watch: {
    isLogin() {
      this.login = this.checkLogin();
    }
  },
  methods: {
    ...mapMutations(["clearUserInfo"]),
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    checkLogin() {
      return this.isLogin || localStorage.getItem("token") ? true : false;
    },
    Logout() {
      this.clearUserInfo();
      this.$router.push({ path: "/" });
      this.$message({
        message: "退出成功",
        type: "success"
      });
    }
  },
  mounted() {}
};
</script>

<style lang="scss">
.el-table {
  .primary-row {
    background: #ebf4f9;
  }
  .warning-row {
    background: oldlace;
  }
  .success-row {
    background: #f0f9eb;
  }
  .danger-row {
    background: #f9ebeb;
  }
}

.pull-left {
  float: left;
  text-align: left;
}
.pull-right {
  float: right;
  text-align: right;
}
.pull-center {
  display: flex;
  align-items: center;
  justify-content: space-around;
  text-align: center;
}
.margin5 {
  margin-left: 5%;
  margin-right: 5%;
}
.margin10 {
  margin-left: 10%;
  margin-right: 10%;
}
.margin15 {
  margin-left: 15%;
  margin-right: 15%;
}
.margin20 {
  margin-left: 20%;
  margin-right: 20%;
}
.inline {
  white-space: nowrap;
}
</style>
