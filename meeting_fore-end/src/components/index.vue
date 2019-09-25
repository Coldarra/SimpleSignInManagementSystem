<template>
  <div id="index">
    <meetingdetail v-if="recent_meeting_id" :mid="recent_meeting_id"></meetingdetail>
  </div>
</template>


<script>
import meetingdetail from "./meeting_detail.vue";

export default {
  name: "index",
  components: {
    meetingdetail
  },
  data() {
    return {
      recent_meeting_id: ""
    };
  },
  computed: {},
  methods: {
    getRecentMeeting() {
      console.log("getRecentMeeting");
      
      this.$ajax.post("/api/meeting/recent").then(res => {
        if (res.data.ret == "0") {
          this.recent_meeting_id = res.data.data.meeting.id;
        }
      });
    }
  },
  mounted() {
    this.getRecentMeeting();
  }
};
</script>
