<template>
  <div class="modal fade" id="upload-form-modal" tabindex="-1" role="dialog" aria-labelledby="search-form-title"
    aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg" role="document" style=" pointer-events:auto">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="search-form-title">上传类案</h5>
        </div>
        <div class="modal-body">
            <div class="form-group">
            <el-upload
            id="upload"
            ref="upload"
            :limit="1"
            :file-list="fileList"
            action="#"
            :auto-upload="false"
            :on-change="upload_change"
            :on-remove="upload_remove"
            :on-exceed="upload_exceed"
            >        
        <el-button slot="trigger" size="large" type="primary">选取文件</el-button></el-upload>
            </div>
        <div class="form-group">
        <div slot="tip" class="el-upload-tip">只限文本文件</div>
        </div>
      
      
        </div>
        <div class="modal-footer" style="text-align: center">
          <button type="button" class="btn btn-primary" v-on:click="confrim" data-dismiss="modal">开始匹配</button>
          <button type="button" class="btn btn-warning" data-dismiss="modal">取消</button>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script>
  export default {
    name: "UploadForm",
    data() {
      return {
        fileList: [],
        upload_List: [],
      };
    },
    methods: {
        confrim(){
            this.$emit("getFile", this.upload_List);
        },
      upload_change: function(file, fileList) {
      // 判断 > 5M
      if (file.size > 1048576 * 5) {
        fileList.pop();
        this.$message.warning(`您上传的${file.name}大于5M。`);
        return false;
      }
      if (file.name.endsWith(".txt") == false) {
        fileList.pop();
        this.$message.warning(`您上传的${file.name}不是文本文件。`);
        return false;
      }
      this.fileList = JSON.parse(JSON.stringify(fileList));
      this.upload_List.push(file);
    },
    upload_remove(file, fileList) {
      this.fileList = JSON.parse(JSON.stringify(fileList));
      this.upload_List.forEach((item, index) => {
        if (item.name == file.name) {
          this.upload_List.splice(index, 1);
        }
      });
    },
    upload_exceed(files, fileList) {
      this.$message.warning("您最多只能上传1个文件!")
    },
    }
  }
</script>