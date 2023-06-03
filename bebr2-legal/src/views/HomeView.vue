<template>
  <div class="search-page" @click="userClick=false">
    <div class="search-box" :class="{ 'search-box-up': isSearching }">
      <div class="search-bar-top">
      <input class="search-bar" list="datalist" @keyup="suggestions=[]" maxlength="30" type="text" v-model="searchTerm" placeholder="请输入搜索关键词" />
  <ul id="datalist" class="recommend" v-if="userClick" @click.stop="userClick=!userClick">
        <li class="list-group-item recommend-item" v-for="(suggestion, index) in suggestions" :key="index" @mousedown="fillIn(suggestion)">
  {{ suggestion }}
        </li>
        </ul>
      </div>
      <button class="search-btn search-btn-style" @click="startSearch" title="搜索"></button>
      <button class="plus-btn search-btn-style" data-toggle="modal" data-target="#search-form-modal" title="精细搜索"></button>
       
      <SearchForm @getValue="getVal"/>
      <button class="match-btn search-btn-style" data-toggle="modal" data-target="#upload-form-modal" title="类案检索"></button>
      <UploadForm @getFile="match"/>
    </div>
    <div class="search-results" v-show="showResults" style="margin-top:35px">
      <h5 class="search-results-tips">{{tips}}</h5>
      <ul>
        <li v-for="result in searchResults.slice((pageNum - 1) * pageSize, pageNum*pageSize)" :key="result.docid">
          <div class="result-item"
                @click="showDetail(result)">
            <div class="result-info">
              <p class="title" v-html="showKeyWord(result.title)"></p>
              <p class="type">案件类别：{{ result.ajlbsimple }}案件&nbsp;&nbsp;年份：{{ result.year }}&nbsp;&nbsp;案由：{{result.reason}}</p>
              <p class="text-top" v-html="showKeyWord(result.text)"></p>
            </div>
          </div>
        </li>
        <div style="text-align:center">
        <el-pagination
      layout="prev, pager, next"
      style="justify-content: center;"
      @current-change="changePageNum"
      :current-page="pageNum"
      :page-size="pageSize"
      :total="total">
    </el-pagination>
        </div>
      </ul>
      
      <div style="margin: 40px;"></div>
    </div>
  </div>
</template>


<script>
  import {startSakura} from "@/js/flowers.js"
  import SearchForm from "@/components/SearchForm.vue";
  import UploadForm from "@/components/UploadForm.vue";
  import API from "@/utils/API.js"
  import {debounce} from 'lodash'; 
  export default {
    components: {
      SearchForm,
      UploadForm
    },
    data() {
      return {
        searchTerm: '',
        segsearchTerm: [],
        dontrecommend: false,
        isSearching: false,
        showAdvanced: false,
        category: 'all',
        date: null,
        resultHovered: null,
        searchResults: [
        ],
        addsearch: false,
        addform: null,
        tips: "",
        show: false,
        suggestions: [],
        userClick: false,

        total: 0,
        pageNum: 1,
        pageSize: 10,
      }
    },

    mounted() {
      startSakura()
    },
    
    watch: {
    searchTerm: {
      handler: debounce(function (val) {
        if (!this.dontrecommend)
          this.recommend(val)
      }, 200), // 绑定一个防抖的函数
      // 搜索框发生变化立即侦听
      immediate: true
    },
    },
    methods: {
      // 分页
      changePageNum: function (val) {
           this.pageNum = val;
      },
      // 补全填充
      fillIn(suggestion) {
        this.searchTerm = suggestion
        this.suggestions = []
        this.startSearch()
    },
    // 查询补全，与后端交互
      recommend() {
        if (this.searchTerm.length > 0) {
        this.userClick = true
        this.suggestions = []
        var xhr = new XMLHttpRequest();
        xhr.open(API.RECOMMEND["method"], API.RECOMMEND["path"] + "?query=" + this.searchTerm, true)
        var that_ = this;
        xhr.onload = function (e) {
          if (xhr.readyState === 4) {
            if (xhr.status === 200) {
              var result = JSON.parse(xhr.responseText);
              if (result.code == 200) {
                if (that_.isSearching) {
                  that_.suggestions = result.suggestions;
                } else {
                  that_.suggestions = result.suggestions.slice(0, 5); 
                }
                
              }
              console.log(that_.searchTerm)
              console.log(that_.suggestions)
            } else {
              console.error(xhr.statusText);
            }
          }
        };
          xhr.onerror = function (e) {
            console.error(xhr.statusText);
          };
        xhr.send();
      } else {
        this.suggestions = []
      }
      },
      // 高亮显示关键词
      showKeyWord(val) {
        let keyWordArr = this.segsearchTerm;
        keyWordArr = keyWordArr.filter(e => e != ' ');
        let str = val;
        if(keyWordArr) {
          keyWordArr.forEach(e => {
              let regStr = '' + `(${e})`;
              let reg = new RegExp(regStr,"g");
              str = str.replace(reg, '<span style="color:red;">'+ e +'</span>')
          })
        }
        return str;
    },
    // 类案检索，与后端交互
      match(val) {
        var formData = new FormData();
        formData.append("file", val[0].raw);
        console.log(formData.get("file"))
        var xhr = new XMLHttpRequest();
        xhr.open(API.MATCH["method"], API.MATCH["path"], true)
        var that_ = this;
        xhr.onload = function (e) {
          if (xhr.readyState === 4) {
            if (xhr.status === 200) {
              var result = JSON.parse(xhr.responseText);
              if (result.code == 200) {
                that_.searchResults = JSON.parse(JSON.stringify(result.result));
                that_.tips = "花费时间：" + result.time + "秒";
                that_.segsearchTerm = [];
                that_.total = that_.searchResults.length;
              } else {
                console.log(result)
                that_.tips = "抱歉，匹配失败！";
                that_.searchResults = [];
                that_.total = that_.searchResults.length;
                that_.segsearchTerm = [];
              }
              console.log(that_.searchResults)
              // 发起搜索请求，获取结果
              that_.isSearching = true;
              that_.show = true;
            } else {
              console.error(xhr.statusText);
            }
          }
        };
        xhr.onerror = function (e) {
          console.error(xhr.statusText);
        };
        xhr.send(formData);
      },
      // 获取精细搜索条件
      getVal(val) {
        this.addform = JSON.parse(JSON.stringify(val));
        //检查年份：
        if (this.addform.startYear != "" && this.addform.endYear != "") {
          if (this.addform.startYear > this.addform.endYear) {
            alert("起始年份不能大于结束年份！搜索时取消年份限制。");
            this.addform.year = null;
          } else {
            this.addform.year = [parseInt(this.addform.startYear), parseInt(this.addform.endYear)];
          }
        } else if (this.addform.startYear != "") {
          this.addform.year = [parseInt(this.addform.startYear), 2023];
        } else if (this.addform.endYear != "") {
          this.addform.year = [1900, parseInt(this.addform.endYear)];
        } else {
          this.addform.year = null;
        }
        // 检查其他，如果为空或者为“全部”，则置空
        if (this.addform.reason == "") {
          this.addform.reason = null;
        }
        if (this.addform.ajlbsimple == "" || this.addform.ajlbsimple == "全部" || this.addform.ajlbsimple == null) {
          this.addform.ajlbsimple = null;
        } else {
          this.addform.ajlbsimple = this.addform.ajlbsimple.split("案件")[0];
        }
        if (this.addform.province == "" || this.addform.province == "全部") {
          this.addform.province = null;
        }
        if (this.addform.province == "最高法院") {
          this.addform.province = "最高";
        }
        if (this.addform.wsmc == "" || this.addform.wsmc == "全部") {
          this.addform.wsmc = null;
        }
        if (this.addform.wszzdw == "" || this.addform.wszzdw == "全部") {
          this.addform.wszzdw = null;
        }

      },
      // 发起搜索请求，与后端交互
      startSearch() {
        
        if (this.searchTerm == "" && this.addform == null) {
          alert("请输入搜索关键词，或添加搜索条件！");
          return;
        } else {
          if (this.searchTerm == "") {
            // 检查addform是不是都是null
            var flag = true;
            for (var key in this.addform) {
              if (key == "startYear" || key == "endYear") {
              continue;
            }
              if (this.addform[key] != null) {
                flag = false;
                break;
              }
            }
            if (flag) {
              alert("请输入搜索关键词，或添加搜索条件！");
              return;
            }
          }
        }
        var query = null;
        if (this.searchTerm != "") {
          query = this.searchTerm;
        }
        var data = {
          "text": query}
        if (this.addform != null) {
          for (var key in this.addform) {
            
            if (this.addform[key] != null) {
              data[key] = this.addform[key];
            }
          }
        }
        var xhr = new XMLHttpRequest();
        xhr.open(API.SEARCH["method"], API.SEARCH["path"], true)
        xhr.setRequestHeader('content-type', 'application/json'); 
        var that_ = this;
        xhr.onload = function (e) {
          that_.dontrecommend = false;
          if (xhr.readyState === 4) {
            if (xhr.status === 200) {
              var result = JSON.parse(xhr.responseText);
              if (result.code != 200) {
                that_.tips = "抱歉，搜索失败！";
                that_.searchResults = [];
                that_.segsearchTerm = [];
                that_.total = that_.searchResults.length;
              } else {
                that_.segsearchTerm = JSON.parse(JSON.stringify(result.segment))
                that_.searchResults = JSON.parse(JSON.stringify(result.result));
                that_.total = that_.searchResults.length;
                if(that_.searchResults.length==0){
                  that_.tips = "花费时间：" + result.time + "秒。抱歉，没有找到相关文书！";
              } else {
                that_.tips = "花费时间：" + result.time + "秒";
              }
              }
              console.log(that_.searchResults)
              console.log(that_.segsearchTerm)
              // 发起搜索请求，获取结果
              that_.isSearching = true;
              that_.show = true;
            } else {
              console.error(xhr.statusText);
            }
          }
        };
        xhr.onerror = function (e) {
          that_.dontrecommend = false;
          console.error(xhr.statusText);
        };
       xhr.send(JSON.stringify(data));
       this.dontrecommend = true;
        
      },
      // 显示高级搜索
      toggleAdvanced() {
        this.addsearch = true;
      },
      // 跳转到文章详情页面
      showDetail(result) {
        let text = this.$router.resolve({
          path: '/article',
          query: {
            id: result.docid
          }
        })
        window.open(text.href, '_blank')
      }
    },
    computed: {
      showResults() {
        return this.show
      }
    }
  }
</script>

<style lang="scss" scoped>
  $light: #a5ccd4;
  $dark: #87b3c0;
  .recommend {
    padding:0;
    width: 100%;
    // border: 2px solid #ccc;
    border-radius: 10px;
    margin-top: 5px;
  }
  .recommend-item {
    width:100%;
    text-align:left;
    background-color: #f2f2f2;
    cursor: pointer;
  }
  .recommend-item:hover,
  .recommend-item:focus {
    background-color: rgb(251, 240, 242);
  }
  .text-top {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: normal;
    font-size: 14px;
    font-family: 楷体;
    margin-bottom: 3px;
    color: #747373;

  }
  
  .search-page {
    --bar-width: 50%;
  }
  .search-box {
    padding-top: 18%;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 200px;
    width: 100%;
    background-color:rgba(0,0,0,0);
    transition: all 0.5s ease-in-out;
    
  }
  .search-box-up {
    padding-top: 8%;
    height: 50px;
  }
  .advanced-search {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 20px;
    padding: 20px 0;
    background-color: #f2f2f2;
  }
  .advanced-search label {
    margin-right: 10px;
  }
  .search-results {
    margin-top: 20px;
    background-color: rgba(0,0,0,0);
  }
  .search-results h2 {
    
    margin-bottom: 10px;
  }
  .search-results ul {
    list-style: none;
    padding: 0;
  }
  .search-results li {
    margin-bottom: 20px;
    cursor: pointer;
  }
  .result-item {
    display: flex;
    justify-content: center;
    background-color:rgba(0,0,0,0);
    border-bottom: 1px solid #ccc;
    margin-top: 30px;
    width: 50%;
    margin-left: calc(50% - var(--bar-width) / 2);
    transition: all 0.2s ease-in-out;
  }
  .result-item:hover {
    box-shadow: 4px 4px 4px $dark;
    transition: box-shadow 0.5s;
  }
  .result-info {
    text-align: left;
    flex-grow: 1;
  }
  .result-info .title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 3px;
    color: #333;
  }
  .result-info .type {
    font-size: 10px;
    font-family: 楷体;
    margin-bottom: 3px;
    color: #2136f7;
  }
  .result-info .date {
    font-size: 8px;
    margin-bottom: 5px;
    font-family: 楷体;
    color: #868585;
  }
  .search-bar-top {
    left: calc(50% - var(--bar-width) / 2);
    width: var(--bar-width);
    top: 40%;
    height: 42px;
  }
  .search-bar {
    left: 0;
    width: 100%;
    height: 42px;
    border-radius: 21px;
    /* box-shadow: 0 3px 5px #d2d2d2; */
    box-shadow: 2px 2px 5px $light;
    /* border: 1px solid #bbd7eb; */
    background: #ffffff;
    font-family: Open;
    color: #000000;
    text-indent: 21px;

    transition: box-shadow 0.2s;
  }
  .search-bar::-webkit-input-placeholder{
    color: #c9cecd;
  }
  .search-bar:hover {
    /* border: 2px solid #8dc9d9; */
    box-shadow: 3px 3px 8px $dark;
    transition: box-shadow 0.2s;
  }
  .search-bar:focus {
    /* border: 2px solid #8dc9d9 !important; */
    outline: 0;
    box-shadow: 3px 3px 8px $dark;
    transition: box-shadow 0.2s;
  }


  .search-btn {
    position: absolute;
    left: calc(50% + var(--bar-width) / 2);
    
    width: 42px;
    height: 42px;
    margin-left: 16px;
    /* border: 2px solid #8dc9d9; */
    border-radius: 50%;
    box-shadow: 2px 2px 5px $light;
    /* background: url("../assets/icon-search.png") #8ec3fd no-repeat center; */
    background: url("../assets/icon-search.png") white no-repeat center;
    background-size: 64% 64%;
    transition: background-color 0.2s, box-shadow 0.2s;
  }

  .plus-btn {
    position: absolute;
    left: calc(50% + var(--bar-width) / 2 + 50px);
    
    width: 42px;
    height: 42px;
    margin-left: 16px;
    /* border: 2px solid #8dc9d9; */
    border-radius: 50%;
    box-shadow: 2px 2px 5px $light;
    /* background: url("../assets/icon-search.png") #8ec3fd no-repeat center; */
    background: url("../assets/icon-plus.png") white no-repeat center;
    background-size: 64% 64%;
    transition: background-color 0.2s, box-shadow 0.2s;
  }

  .match-btn {
    position: absolute;
    left: calc(50% + var(--bar-width) / 2 + 100px);
    
    width: 42px;
    height: 42px;
    margin-left: 16px;
    /* border: 2px solid #8dc9d9; */
    border-radius: 50%;
    box-shadow: 2px 2px 5px $light;
    /* background: url("../assets/icon-search.png") #8ec3fd no-repeat center; */
    background: url("../assets/icon-addfile.png") white no-repeat center;
    background-size: 64% 64%;
    transition: background-color 0.2s, box-shadow 0.2s;
  }

  .search-btn-style:hover {
    /* border: 2px solid #f0a315; */
    /* background-color: #80b3ea; */
    box-shadow: 5px 5px 8px $dark;
    transition: box-shadow 0.3s, background-color 0.3s;
  }
  .search-btn-style:active {
    /* border: 2px solid #f0a315; */
    box-shadow: 5px 5px 8px $dark;
    transition: box-shadow 0.3s, background-color 0.3s;
  }
  .search-results-tips {
    font-family:楷体;
    color: red;
    font-size: 7px;
    text-align:left;
    margin-left: calc(50% - var(--bar-width) / 2);
    margin-bottom: 0;
  }

  mark {
  background-color: #ff0;
  color: #000;
  padding: 0 4px;
}
  
</style>