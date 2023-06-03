<template>
  <div class="modal fade" id="search-form-modal" tabindex="-1" role="dialog" aria-labelledby="search-form-title"
    aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg" role="document" style=" pointer-events:auto">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="search-form-title">添加精细搜索条件</h5>
        </div>
        <div class="modal-body">
          <form>
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label for="reason">案由</label>
                  <input type="text" class="form-control" id="reason" v-model="form.reason" maxlength="20">
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-group">
                  <label for="ajlb">案件类别</label>
                  <select class="form-control" id="ajlb" v-model="form.ajlbsimple">
                    <!-- {'行政', '其他', '执行', '赔偿', '民事', None, '刑事'} -->
                    <option selected>全部</option>
                    <option>行政案件</option>
                    <option>刑事案件</option>
                    <option>执行案件</option>
                    <option>赔偿案件</option>
                    <option>民事案件</option>
                    <option>其他案件</option>
                  </select>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                    <label for="province">法院地点</label>
                  <select class="form-control" id="province" v-model="form.province">
                    <option selected>全部</option>
                    <option v-for="province in provinces" :key="province">{{province}}</option>
                  </select>
                </div>
              </div>
                <div class="col-md-6">
                <div class="form-group">
                    <label for="wsmc">文书名称</label>
                  <select class="form-control" id="wsmc" v-model="form.wsmc">
                    <option selected>全部</option>
                    <option>决定书</option>
                    <option>调解书</option>
                    <option>通知书</option>
                    <option>判决书</option>
                    <option>裁定书</option>
                  </select>
                </div>
                </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <div class="form-group">
                  <label for="wszzdw">文书制作单位</label>
                  <select class="form-control" id="wszzdw" v-model="form.wszzdw">
                    <option selected>全部</option>
                    <option>检察院</option>
                    <option>法院</option>
                    <option>司法行政</option>
                  </select>
                </div>
              </div>
              <div class="form-group col-md-3">
                <label for="startYear">起始年份</label>
                <input type="number" class="form-control" id="startYear" v-model="form.startYear" placeholder="请输入起始年份" oninput="if(value<0)value=0">
                </div>
                <div class="form-group col-md-3">
                <label for="endYear">终止年份</label>
                <input type="number" class="form-control" id="endYear" v-model="form.endYear" placeholder="请输入终止年份" oninput="if(value<0)value=0">
            </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" v-on:click="confrim" data-dismiss="modal">确认</button>
        </div>
      </div>
    </div>
  </div>
</template>



<script>
export default {
  name: "SearchForm",
  data() {
    return {
    provinces: ['最高法院', '安徽', '北京', '重庆', '福建', '广东', '广西', '甘肃', '贵州', '海南', '河北', '河南', '黑龙江', '湖北', '湖南', '吉林', '江苏', '江西', '辽宁', '内蒙古', '宁夏', '青海', '山东', '山西', '陕西', '上海', '四川', '天津', '西藏', '新疆', '云南', '浙江'],
      form: {
        reason: "",
        wsmc: "",
        ajlbsimple: "",
        province: "",
        wszzdw: "",
        startYear: "",
        endYear: "",
      },
    };
  },
  methods: {
    confrim(){
        this.$emit("getValue", this.form);
      
    }
  },
};
</script>

<style scoped>
</style>
