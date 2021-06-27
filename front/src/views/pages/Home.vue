<template>
	<div class="page-layout-sidebar-right scrollable only-y">

    <template v-if="SuccessToogle">
      <b-row>
        <b-col sm="12">
          <b-alert show variant="success">{{SuccessMassage}}</b-alert>
        </b-col>
      </b-row>
    </template>
    <template v-if="AlertToggle">
      <b-row>
        <b-col sm="12">
          <b-alert show variant="danger">{{AlertMassage}}</b-alert>
        </b-col>
      </b-row>
    </template>

    <b-button variant="outline-primary" @click="openPostContentDialog()" size="sm" class="mr-1" style= "margin-bottom: 10px" >
      Post Something...
    </b-button>
		<div class="flex" v-for="i in contentList">
			<div class="box grow card-base card-shadow--small p-24" style= "margin-bottom: 10px; cursor: pointer;" @click="goTo(i.content_id)">
				<!-- <div style=" max-width: 1100px; margin: 0 auto; "> -->
				<div style=" max-width: 1100px;">
          <!-- <p style="font-size: 10px;">
            {{i.user_id}}
          <p> -->
					<!-- <p class="mt-18">
						<img src="@/assets/images/photo1.jpg" class="demo-img" alt="demo image">
					</p> -->
          <p style="font-size: 10px;">
            {{i.date}}
          </p>
					<h1 class="mt-8">{{i.title}}</h1>
					<p class="mt-0">
						{{i.content}}
					</p>
					<p style="font-size: 10px;">
            {{i.count_comment}}
          </p>

				</div>
			</div>
			<!-- <div class="sidebar scrollable" :class="{'open':sidebarOpen}">
				<el-button size="small" class="close-btn" @click="sidebarOpen = false">close</el-button>
				<ul>
					<li v-for="i in 20" :key="i">Sidebar Item {{i}}</li>
				</ul>
			</div> -->
		</div>

    <b-modal id="NewPostModal"
       title="Post Something"
       v-model="postModalToggle"
       size="lg"
       ok-title="Ok"
       @ok="checkBeforeSubmit">

       <div class="page-quill scrollable">
     		<div class="card-base card-shadow--medium">
          <b-form-input type="text"
                  placeholder="Title"
                  v-model="TitleContent"
                  aria-describedby="input-live-help input-live-feedback"
                  :state="titleState"
                  style="margin-bottom 20px"
                  >
          </b-form-input>
          <b-form-invalid-feedback id="input-live-feedback">
            Fill The Title
          </b-form-invalid-feedback>
            <h @click="openInsertToggle" style="cursor:pointer">Insert Coordinate</h>
     			<VuePellEditor
     				:actions="dialogOptions"
     				:content="dialogContent"
     				:placeholder="dialogPlaceholder"
     				v-model="Content"
     				:styleWithCss="false"
     				editorHeight="400px"
     			/>
     		</div>
     	</div>

    </b-modal>

    <b-modal id="UploadImageModal"
       title = "Upload Image"
       v-model="UploadImageToggle"
       size="sm"
       ok-title="Ok">
      <label>
        <input type="file" id="image" accept=".jpg, .png, .gif" ref="image" v-on:change="handleFileUpload('image')"/>
      </label>
    </b-modal>
    <b-modal id="UploadFileModal"
       title = "Upload File"
       v-model="UploadFileToggle"
       size="sm"
       ok-title="Ok">
      <label>
        <input type="file" id="file" accept=".pdf, .xls, .doc, .docx, .xlsx" ref="file" v-on:change="handleFileUpload('file')"/>
      </label>
    </b-modal>
    <b-modal id="InsertCoordinateModal"
       title = "Insert Coordinate"
       v-model="InsertCoornateToggle"
       size="sm"
       ok-title="Ok">
       <b-form-input type="text"
               placeholder="Longitude"
               v-model="Longitude">
       </b-form-input>
       <b-form-input type="text"
               placeholder="Latitude"
               v-model="Latitude">
       </b-form-input>
    </b-modal>

	</div>
</template>

<script>
import axios from "axios";
// import {getToken, getUserDataInSession2, BASE_URL} from '../../utils';
export default {
	name: 'LayoutSidebarRight',
  computed : {
    titleState(){
      return this.TitleContent.length > 0 ? true : false
    }
  },
	data() {
		return {
			list : ['test1', 'test2', 'test3'],
      user_id : 2,
      contentList : [],
      TitleContent : "",
      Longitude : "",
      Latitude : "",
      image :  "",
      file : "",
      postModalToggle : false,
      UploadImageToggle : false,
      UploadFileToggle : false,
      InsertCoornateToggle : false,
      SuccessToogle : false,
      AlertToggle : false,
      SuccessMassage : "",
      AlertMassage : "",
      dialogContent: '',
      dialogOptions: [
        {
					name: 'image',
					result: () => {
					this.UploadImageToggle = true
					}
				},
        {
          // name: 'file',
					icon: 'File_Upload',
					title: 'File Upload',
					result: () => {
					this.UploadFileToggle = true
					}
				},
        {
					icon: '',
					title: 'Insert Coordinate',
					result: () => {
					this.UploadFileToggle = true
					}
				}
			],
      Content: '',
      titlePlaceholder: "Title",
      dialogPlaceholder: "Write Something....",
			sidebarOpen: false
		}
	},
  mounted() {
    this.getData()
  },
  methods : {
    getData() {
      // this.token = getToken()
      var headers = {
        'Content-Type': 'application/json',
        // 'Authorization': `Bearer ${this.token}`
      }
      // axios.get(`${BASE_URL}/companies?page=${this.currentPage}&size=${this.perPage}`,{
      axios.get(`http://127.0.0.1:5000/api/v1/contentList`,{
            headers
            },
        ).then(response => {
          if (response.status === 200) {
            if (response.data.code === 401) {
              this.errorAlert = true;
              this.errorMessage = response.data.message;
              setTimeout(() => {this.errorMessage= '',console.log(response.data.message),window.location.href = this.HomeLocation}, 2000);
            } else {
              this.contentList = response.data.message
            }
          }
        })
    },
    submitContent() {
      // this.token = getToken()
      this.Content = this.Content.replace('<div>','');
      this.Content = this.Content.replace('</div>','');
      const formData = new FormData();
      formData.append('file', this.file);
      formData.append('image', this.image);
      formData.append('title', this.TitleContent);
      formData.append('content', this.Content);
      formData.append('longitude', this.Longitude);
      formData.append('latitude', this.Latitude);
      // for (var pair of formData.entries()) {
      //   console.log(pair[0]+ ', ' + pair[1]);
      // }
      var headers = {
        'Content-Type': 'multipart/form-data',
        // 'Authorization': `Bearer ${this.token}`
      };
      axios.post(`http://127.0.0.1:5000/api/v1/postContent/${this.user_id}`,
        formData,{headers}).then((response) => {
        // console.log(response.data.result)
        if (response.status === 200) {
          if (response.data.status === "Success") {
            // this.$refs.file.files[0] = ''
            this.image = '';
            this.file = '';
            // this.clearFiles()
            // this.successMessage = 'File Upload Has Been Completed ';
            this.successMessage = response.data.status + response.data.message
            this.successUploadFile = true;
            setTimeout(() => {this.successUploadFile = false, this.file = '', location.reload()}, 3000);
          } else {
            this.errorMessage = 'Internal Server Error';
            this.errorUploadFile = true;
            setTimeout(() => {this.errorUploadFile = false, this.file = ''}, 5000);
          }
					this.getData()
        } else {
          this.errorMessage = 'Internal Server Error';
          this.errorUploadFile = true;
          setTimeout(() => {this.errorUploadFile = false, this.file = ''}, 5000);
        }
      }).catch((error) => {
        if (error.response !== undefined) {
          this.success = false;
          // setAlert(this, error.response);
        }
      });
    },
    goTo(content_id) {
      console.log(content_id)
      this.$router.push({name: 'post', params: { id: content_id } })
    },
    openPostContentDialog() {
      this.postModalToggle = true;
    },
    openInsertToggle() {
      this.InsertCoornateToggle = true;
    },
    handleFileUpload(type){
      if (type == 'file'){
        this.file = this.$refs.file.files[0];
        // this.$refs.file.files = null;
      }
      else if (type == 'image'){
        this.image = this.$refs.image.files[0];
        // this.$refs.file.files = null;
      }
      console.log("this type : ", type)
      console.log("image: ", this.image)
      console.log("file: ", this.file)
    },
    checkBeforeSubmit(){
      if (this.TitleContent == "") {
        this.AlertMassage = "Please Fill the Title"
        this.AlertToggle = true
        setTimeout(() => {this.AlertToggle = false, this.AlertMassage = ''}, 3000);
      }
      else if (this.Content == "") {
        this.AlertMassage = "Please Fill the Content"
        this.AlertToggle = true
        setTimeout(() => {this.AlertToggle = false, this.AlertMassage = ''}, 3000);
      }
      else {
        this.submitContent()
      }
    }

  },
}
</script>

<style lang="scss" scoped>
@import '../../assets/scss/_variables';

.page-layout-sidebar-right {
	.page-header {
		margin-bottom: 20px;
		min-height: 60px;

		.menu-btn {
			color: $background-color;
			font-size: 20px;
			display: none;
			cursor: pointer;
		}
	}

	.demo-img {
		width: 100%;
		max-width: 500px;
		margin-bottom: 10px;
		border-radius: 4px;
	}

	.sidebar {
		box-sizing: border-box;
		padding: 24px;
		margin-right: -24px;
		//text-align: right;
		min-width: 250px;

		.close-btn {
			display: none;
			width: 100%;
			margin-bottom: 10px;
		}

		ul {
			width: 100%;
			list-style: none;
			padding: 0;
			margin: 0;
		}
		li {
			box-sizing: border-box;
			width: 100%;
			list-style: none;
			padding: 15px 20px;
			border-bottom: 1px solid transparentize($text-color, .9);
			cursor: pointer;
			position: relative;

			&::after {
				content: '';
				display: block;
				width: 0%;
				height: 100%;
				background: $text-color;
				position: absolute;
				top: 0;
				left: 0;
				opacity: 0;
				transition: all .5s;
			}

			&:hover {
				&::after {
					width: 100%;
					opacity: .3;
				}
			}
		}
	}
}

@media (max-width: 768px) {
	.page-layout-sidebar-right {
		.page-header {
			.menu-btn {
				display: block;
			}
		}
		.sidebar {
			.close-btn {
				display: block;
			}

			margin: 0;
			text-align: center;
			position: absolute;
			background: white;
			color: #000;
			top: 5px;
			right: -100%;
			opacity: 0;
			bottom: 5px;
			box-shadow: -40px 0px 160px 80px rgba(0, 0, 0, 0.3);
			border-top-left-radius: 4px;
			border-bottom-left-radius: 4px;
			transition: all .5s;

			li {
				border-bottom: 1px solid #eee;
			}

			&.open {
				opacity: 1;
				right: 0;
				z-index: 999;
			}
		}
	}
}
</style>
