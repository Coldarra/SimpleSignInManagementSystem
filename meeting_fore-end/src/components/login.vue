<template>
  <div id="login">
    login
    <div id="loginForm">
      <!-- <h3><div class="">登录</div></h3> -->
      <el-row>
        <el-col :span="8" :offset="8">
          <el-form :model="loginForm" v-loading="loading" status-icon :rules="loginRules" ref="loginForm" label-width="100px" class="demo-loginForm">
            <el-form-item label="姓名" prop="username">
              <el-input v-model="loginForm.username"></el-input>
            </el-form-item>

            <el-form-item label="密码" prop="password">
              <el-input type="password" v-model="loginForm.password" autocomplete="off"></el-input>
            </el-form-item>

            <el-form-item>
              <el-button type="success" plain @click="submitLogin('loginForm')">登录</el-button>
              <el-button @click="resetLogin('loginForm')">重置</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
  </div>
</template>


<script>
export default {
  name: "login",
  data() {
    return {
      loginForm: {
        username: "",
        password: ""
      },
      loading: false,
      loginRules: {
        username: [
          {
            required: true,
            min: 4,
            max: 20,
            message: "请输入姓名或手机号",
            trigger: "blur"
          }
        ],
        password: [
          {
            required: true,
            min: 6,
            max: 16,
            message: "请输入6-16位密码",
            trigger: "blur"
          }
        ]
      }
    };
  },
  methods: {
    submitLogin(Form) {
      this.$refs[Form].validate(valid => {
        if (valid) {
          this.loading = true;
          this.$ajax.post("/api/user/login", this.loginForm).then(res => {
            this.loading = false;

            if (res.data.ret == "0") {
              this.$store.commit("updateUserInfo", res.data.data);
              this.$message({
                message: "登录成功",
                type: "success"
              });

              this.$router.push({ path: "/" });
            } else {
            }
          });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    resetLogin(Form) {
      this.$refs[Form].resetFields();
    },
    checkLogin() {
      const token = localStorage.getItem("token");
      if (token) {
        this.loading = true;
        this.$ajax.get("/api/user/token").then(res => {
          this.loading = false;
          if (res.data.ret == "0") {
            this.$store.commit("updateUserInfo", res.data.data);
            // if (this.$route.query.redirect) {
            //   this.$router.push({
            //     path: decodeURIComponent(this.$route.query.redirect)
            //   });
            // } else {
            //   this.$router.push({ path: "/" });
            // }
          } else {
            this.$store.commit("clearUserInfo", res.data.data);
            this.$router.push({
              path: "/login"
            });
          }
        });
      }
    }
  },
  mounted() {
    console.log(this.$route.path);

    this.checkLogin();
    console.log("login...");
  }
};
</script>

<style scoped>
#login {
  width: 100%;
}
#loginForm {
  margin-top: 12rem;

  margin-bottom: 8rem;
}
</style>