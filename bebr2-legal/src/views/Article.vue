<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-md-3">
        <div class="card">
          <div class="card-header">
            <span style="color: blue; cursor: pointer" @click="$router.push('/')"><i class="fa fa-arrow-left"></i>&nbsp;&nbsp;返回搜索</span>
          </div>
           <div class="card-header">
            案号
          </div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item" style="font-size: 14px; font-family:楷体; font-weight:bold">{{article.ah}}</li>
          </ul>
          <div class="card-header">
            文书制作单位
          </div>
          <ul class="list-group list-group-flush">
            <li class="list-group-item" style="font-family:楷体; font-weight:bold">{{article.wszzdw}}</li>
          </ul>
          <div class="card-header">
            案由
          </div>
          <ul class="list-group list-group-flush">
            <li v-for="doc in article.reason" :key="doc" class="list-group-item" style="font-family:楷体; font-weight:bold">{{doc}}</li>
          </ul>
          <div class="card-header" v-if="match[0].length==0">
            涉及法条
          </div>
          <ul class="list-group list-group-flush" v-if="match[0].length==0">
            <li v-for="doc in article.ft" :key="doc" class="list-group-item" style="font-family:楷体; font-weight:bold">{{doc}}</li>
          </ul>
           <div class="card-header">
            内容相似推荐
          </div>
          <ul class="list-group list-group-flush">
             <li v-for="doc in match[1]" :key="doc[0]" class="list-group-item" style="color:blue; font-size: 14px; font-family:楷体; cursor: pointer;" @click="goto(doc[0])" >{{doc[1]}}</li>
          </ul>
          
          <div class="card-header" v-if="match[0].length>0">
            法条一致案例
          </div>
          <ul class="list-group list-group-flush" v-for="dict in match[0]" :key="dict[0]">
            <li class="ft-block list-group-item" style="font-family:楷体; font-weight:bold">{{dict[0]}}</li>
             <li v-for="doc in dict[1]" :key="doc[0]" class="list-group-item" style="color:blue; font-size: 14px; font-family:楷体; cursor: pointer;" @click="goto(doc[0])">{{doc[1]}}</li>
          </ul>
          <div class="card-footer">
          </div>
          
      
        </div>
      </div>
      <div class="col-md-9">
        <div class="card">
          <div class="card-header">
          {{article.title}}
          </div>
          <div class="card-body">
            <ul class="list-group list-group-flush">
              <li class="list-group-item"><span style="font-size:14px;font-family:楷体"><i class="fas fa-folder"></i>&nbsp;<strong>案件类型：</strong>{{article.ajlbsimple}}&nbsp;&nbsp;</span>
            <!-- <span><i class="far fa-file-alt"></i>&nbsp;<strong>案由：</strong>{{article.reason}}&nbsp;&nbsp;</span> -->
            <span style="font-size:14px;font-family:楷体"><i class="fas fa-book-open"></i>&nbsp;<strong>文书名称：</strong>{{article.wsmc}}&nbsp;&nbsp;</span>
            <span style="font-size:14px;font-family:楷体"><i class="fas fa-gavel"></i>&nbsp;<strong>经办机构：</strong>{{article.jbjg}}&nbsp;&nbsp;</span>
            <span style="font-size:14px;font-family:楷体"><i class="far fa-calendar-alt"></i>&nbsp;<strong>年份：</strong>{{article.year}}&nbsp;&nbsp;</span></li>
            <li class="list-group-item"><p></p><p style="text-align:left" v-for="(line, index) in article.text" :key="index">{{line}}</p>
            <p style="text-align:right" v-for="(line, index) in article.text_wm" :key="index">{{line}}</p>
            </li>
            </ul>
          </div>
          <div class="card-footer">
          </div>
        </div>
      </div>
    </div>
    <p></p>
  </div>
  
</template>

<script>
import 'jquery/dist/jquery.min.js';
import 'bootstrap/dist/js/bootstrap.min.js';
import API from "@/utils/API.js"

export default {
  name: 'ArticleDisplay',
  data() {
    return {
      article: {},
      match:{}
    }
  },
  created() {

      var articleid = this.$route.query.id;
      console.log(articleid)
      var xhr = new XMLHttpRequest();
      xhr.open(API.SHOW["method"], API.SHOW["path"], false)
      xhr.setRequestHeader('content-type', 'application/json');
      xhr.send(JSON.stringify({
        "docid": articleid
      }));
      var res = JSON.parse(xhr.responseText);
      if (res.code == 200) {
        this.article = res.result;
        this.match = res.match_content;
        console.log(this.article)
        console.log(this.match)
      } else {
        alert("不存在该文书！");
        this.$router.push("/");
      }

  },
  watch: {
    '$route' (to, from) {
  this.$router.go(0);
  }
},
  methods: {
    goto(id) {
      if (id == 0) {
        return;
      }
      this.$router.push({
        path: '/article',
        query: {
          id: id
        }
      })
    },
  }
};
</script>

<style>
.card-header {
  font-size: 18px;
  font-weight: bold;
};
</style>
