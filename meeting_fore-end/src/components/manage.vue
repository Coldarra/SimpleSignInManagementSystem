<template>
  <div id="manage">
    <input ref="excelinput" type="file" accept=".xls, .xlsx" style="display:none;" @change="getExcel">
    <el-card shadow="hover" v-loading="loading_excel">
      <div slot="header" class="clearfix">
        <span>用户信息</span>
        <el-button @click="getUsers" type="text">
          &nbsp;
          <i class="el-icon-refresh"></i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        </el-button>
        <el-button-group class="pull-right">
          <!-- <el-button style="float: right; padding: 3px 3px" type="text">下载成员信息</el-button> -->
          <el-button style="float: right; padding: 3px 3px" type="text" @click="downloadExcelTemplate">下载模板</el-button>
          <el-button style="float: right; padding: 3px 3px" type="text" @click="choiceExcel">批量添加</el-button>
          <el-button style="float: right; padding: 3px 3px" type="text" @click="openUserDialog">添加用户</el-button>
        </el-button-group>
      </div>
      <div>
        <el-table
          :data="filterusers.slice((currentPage-1)*pageSize,currentPage*pageSize)"
          style="width: 100%"
          v-loading="loading_users"
          id="UsersInfo"
        >
          <el-table-column prop="username" label="姓名" sortable>
            <template slot-scope="scope">
              <span class="inline">{{ scope.row.username}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="phonenumber" label="手机号" width="140" sortable></el-table-column>
          <el-table-column prop="gender" label="性别" sortable></el-table-column>
          <el-table-column prop="company" label="班级" sortable>
            <template slot-scope="scope">{{ scope.row.company || "无"}}</template>
          </el-table-column>
          <el-table-column prop="studentid" label="学号" sortable>
            <template slot-scope="scope">{{ scope.row.studentid || "无"}}</template>
          </el-table-column>
          <el-table-column prop="email" label="邮箱" sortable></el-table-column>
          <el-table-column prop="about" label="备注" sortable></el-table-column>
          <el-table-column align="right">
            <template slot="header" slot-scope="scope">
              <el-input v-model="search" size="mini" placeholder="输入关键字搜索"/>
            </template>
            <template slot-scope="scope">
              <span class="inline">
                <el-button type="primary" @click="openUserDialog(scope.row)" plain circle icon="el-icon-edit"></el-button>
                <el-button type="danger" @click="removeUser(scope.row)" plain circle icon="el-icon-delete"></el-button>
              </span>
            </template>
          </el-table-column>
        </el-table>
        <br>
        <div class="pull-center">
          <el-pagination
            background
            layout="sizes, prev, pager, next, jumper"
            :page-size="pageSize"
            :total="filterusers.length"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          ></el-pagination>
        </div>
      </div>
    </el-card>

    <el-dialog
      title="添加成员"
      :visible.sync="dialog_appendUser"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      v-loading="loading_appendUser"
      width="30%"
    >
      <el-form ref="userForm" :model="userForm" :rules="rules" label-width="72px">
        <el-form-item label="姓名" prop="username">
          <el-input v-model="userForm.username" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phonenumber">
          <el-input v-model="userForm.phonenumber" type="number" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-input v-model="userForm.gender" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="班级" prop="company">
          <el-input v-model="userForm.company" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="学号" prop="studentid">
          <el-input v-model="userForm.studentid" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" type="email" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="about">
          <el-input v-model="userForm.about" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialog_appendUser = false">取 消</el-button>
        <el-button type="primary" @click="appendUser">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>


<script>
import XLSX from "xlsx";
const UserForm = {
  username: "",
  phonenumber: "",
  gender: "",
  company: "",
  studentid: "",
  email: "",
  about: ""
};
export default {
  name: "manage",
  data() {
    return {
      search: "",
      users: [],
      filterusers: [],
      loading: false,
      loading_users: false,
      dialog_appendUser: false,
      loading_appendUser: false,
      loading_excel: false,
      userForm: Object.assign({}, UserForm),
      rules: {
        name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
        phonenumber: [
          { required: true, message: "请输入手机号", trigger: "blur" },
          { min: 11, message: "请输入11位手机号", trigger: "blur" },
          { max: 11, message: "请输入11位手机号", trigger: "blur" }
        ]
      },
      pageSize: 10,
      currentPage: 1
    };
  },
  computed: {},
  methods: {
    getUsers() {
      this.loading_users = true;
      this.$ajax.post("/api/user/all").then(res => {
        this.loading_users = false;
        if (res.data.ret == "0") {
          this.users = res.data.data.users;
        }
      });
    },
    removeUser(user) {
      this.loading_users = true;
      this.$ajax
        .post("/api/user/remove", { phonenumber: user.phonenumber })
        .then(res => {
          this.loading_users = false;
          if (res.data.ret == "0") {
            this.$message({
              message: "删除成功",
              type: "success"
            });
            this.users = res.data.data.users;
          }
        });
    },

    appendUser() {
      this.$refs["userForm"].validate(valid => {
        if (valid) {
          this.loading_appendUser = true;
          this.$ajax.post("/api/user/append", this.userForm).then(res => {
            this.loading_appendUser = false;
            if (res.data.ret == "0") {
              this.$message({
                message: "添加成功",
                type: "success"
              });
              this.dialog_appendUser = false;
              this.users = res.data.data.users;
              this.userForm = {};
            } else {
            }
          });
        } else {
          // console.log("error submit!!");
          return false;
        }
      });
    },
    openUserDialog(user) {
      this.userForm = Object.assign({}, user || UserForm);
      this.dialog_appendUser = true;
    },

    handleCurrentChange(val) {
      this.currentPage = val;
    },
    handleSizeChange(val) {
      this.pageSize = val;
    },

    choiceExcel() {
      this.$refs.excelinput.dispatchEvent(new MouseEvent("click"));
    },
    getExcel() {
      //获取到管理员上传的excel文件
      this.loading_excel = true;
      var fileObj = this.$refs.excelinput.files[0];
      var reader = new FileReader();
      reader.readAsBinaryString(fileObj);
      reader.onload = ev => {
        const data = ev.target.result;
        const workbook = XLSX.read(data, {
          type: "binary"
        });
        const wsname = workbook.SheetNames[0]; //取第一张表
        console.log(workbook.Sheets[wsname]);

        const ws = XLSX.utils.sheet_to_json(workbook.Sheets[wsname]); //生成json表格内容
        console.log(ws);
        this.$ajax
          .post("/api/user/add", {
            users: JSON.stringify(ws)
          })
          .then(res => {
            this.loading_excel = false;
            this.$refs.excelinput.value = "";
            if (res.data.ret == "0") {
              this.$message({
                message: "添加成功",
                type: "success"
              });
              this.users = res.data.data.users;
            } else {
            }
          });
      };
      reader.onerror = function(error) {
        console.log("Error: ", error);
      };
    },
    downloadExcelTemplate() {
      const workbook = {
          SheetNames: ["Sheet1"],
          Sheets: {
            Sheet1: {
              "!ref": "A1:F1", // 必须要有这个范围才能输出，否则导出的 excel 会是一个空表
              A1: { v: "姓名" },
              B1: { v: "手机号" },
              C1: { v: "性别" },
              D1: { v: "班级" },
              D1: { v: "学号" },
              E1: { v: "邮箱" },
              F1: { v: "备注" }
            }
          }
        },
        filename = "用户信息." + new Date().getTime() + ".xlsx";
      XLSX.writeFile(workbook, filename);
    },
    updateFilterUsers() {
      this.filterusers = this.users.filter(
        data =>
          !this.search ||
          data.username.includes(this.search) ||
          data.phonenumber.includes(this.search) ||
          data.gender.includes(this.search) ||
          data.company.includes(this.search) ||
          data.studentid.includes(this.search) ||
          data.email.includes(this.search) ||
          data.about.includes(this.search)
      );
    }
  },
  mounted() {
    console.log("manage");
    this.getUsers();
  },
  watch: {
    users() {
      this.updateFilterUsers();
    },
    search() {
      this.updateFilterUsers();
    }
  }
};
</script>
