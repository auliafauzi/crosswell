<template>
	<div class="page-layout-sidebar-right scrollable only-y">
		<!-- <div class="flex"> -->

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

			<div class="box grow card-base card-shadow--small p-24" style= "margin-bottom: 20px; margin-left: 50px; margin-right: 300px; background: rgba(95, 143, 223, 0.2);">
				<!-- <div style=" max-width: 1100px; margin: 0 auto; "> -->
				<!-- <div style=" max-width: 11000px;"> -->
        <div>
          <p style="font-size: 10px;">
            {{this.content.user_id}}
          <p>
					<!-- <p class="mt-18">
						<img src="@/assets/images/photo1.jpg" class="demo-img" alt="demo image">
					</p> -->
					<h1 class="mt-8">{{this.content.title}}</h1>
					<img :src="this.image"/>
					<p class="mt-0">
						{{this.content.content}}
					</p>

				</div>
			</div>
      <div flex>
        <b-button variant="outline-primary" @click="openPostCommentDialog()" size="sm" class="mr-1" style="margin-left: 70px;">
          Leave Comment
        </b-button>
          <b-button variant="outline-primary" size="sm" class="mr-1" style="margin-left: 10px;" v-if= "user_id == this.content.user_id || this.user_role == 1">
            Edit Post
          </b-button>
          <b-button variant="outline-danger" size="sm" class="mr-1" style="margin-left: 10px;" v-if= "user_id == this.content.user_id || this.user_role == 1">
            Delete Post
          </b-button>
      </div>
      <div class="box grow card-base card-shadow--small p-24" style= "margin-bottom: 10px; margin-top: 10px; margin-left: 70px; margin-right: 300px;" v-for="i in commentList">
				<div style=" max-width: 1100px;">
          <p style="font-size: 10px;">
            {{i.user_id}}
          <p>
          <p style="font-size: 10px;">
            {{i.date}}
          <p>
					<p class="mt-0">
						{{i.comment}}
					</p>
				</div>
        <div flex>
          <b-button variant="outline-primary" size="sm" class="mr-1" v-if= "user_id == i.user_id || user_role == 1">
            Edit Comment
          </b-button>
          <b-button variant="outline-danger" size="sm" class="mr-1" v-if= "user_id == i.user_id || user_role == 1">
            Delete Comment
          </b-button>
        </div>
			</div>
		<!-- </div> -->

		<b-modal id="NewCommentModal"
       title="Post Something"
       v-model="commentModalToggle"
       size="lg"
       ok-title="Ok"
       @ok="checkBeforeSubmit">

       <div class="page-quill scrollable">
     		<div class="card-base card-shadow--medium">
     			<VuePellEditor
     				:actions="dialogOptions"
     				:content="dialogComment"
     				:placeholder="dialogPlaceholder"
     				v-model="comment"
     				:styleWithCss="false"
     				editorHeight="400px"
     			/>
     		</div>
     	</div>
		</b-modal>
	</div>
</template>

<script>
import axios from "axios";
// import {getToken, getUserDataInSession2, BASE_URL} from '../../utils';
export default {
	name: 'LayoutSidebarRight',
	data() {
		return {
			list : ['test1', 'test2', 'test3'],
      user_id : "002",
      // dummy hard coded user_role
      user_role : 2,
      //
      content : [],
      commentList : [],
      content_id : '',
      commentModalToggle : false,
			SuccessToogle : false,
			AlertToggle : false,
      tango : true,
			sidebarOpen: false,
			dialogComment: '',
      dialogOptions: [
        {
          // name: 'file',
					icon: 'Write_Comment',
					title: 'Write Comment'
					// result: () => {
					// this.UploadFileToggle = true
				}
			],
      comment: '',
      dialogPlaceholder: "Write Something...",
			image : null
		}
	},

  props: {
   id: {
    type: Number,
    required: true,
   },
  },

  mounted(){
   // this.$http.get('/post/' +this.id, function (data) {
   //    this.$set('track', data.track)
   // })
   this.content_id = this.$route.params.id
   console.log("yaa" + this.$route.params.id)
   this.getData()
  },
  methods : {
    getData() {
      var headers = {
        'Content-Type': 'application/json',
        // 'Authorization': `Bearer ${this.token}`
      }
      // axios.get(`${BASE_URL}/companies?page=${this.currentPage}&size=${this.perPage}`,{
      axios.get(`http://127.0.0.1:5000/api/v1/contentDetail/${this.$route.params.id}`,{
            headers
            },
        ).then(response => {
          if (response.status === 200) {
            if (response.data.code === 401) {
              this.errorAlert = true;
              this.errorMessage = response.data.message;
              setTimeout(() => {this.errorMessage= '',console.log(response.data.message),window.location.href = this.HomeLocation}, 2000);
            } else {
              this.content = response.data.content
            }
          }
        })
        axios.get(`http://127.0.0.1:5000/api/v1/commentList/${this.$route.params.id}`,{
              headers
              },
          ).then(response => {
            if (response.status === 200) {
              if (response.data.code === 401) {
                this.errorAlert = true;
                this.errorMessage = response.data.message;
                setTimeout(() => {this.errorMessage= '',console.log(response.data.message),window.location.href = this.HomeLocation}, 2000);
              } else {
                this.commentList = response.data.comment
              }
            }
          })
					axios.get(`http://127.0.0.1:5000/api/v1/contentImage/${this.$route.params.id}`,{
	              headers
	              },
	          ).then(response => {
	            if (response.status === 200) {
	              if (response.data.code === 401) {
	                this.errorAlert = true;
	                this.errorMessage = response.data.message;
	                setTimeout(() => {this.errorMessage= '',console.log(response.data.message),window.location.href = this.HomeLocation}, 2000);
	              } else {
	                this.image = response.data
									console.log("image: " + this.image)
	              }
	            }
	          })


    },
		submitContent() {
			this.comment = this.comment.replace('<div>','');
      this.comment = this.comment.replace('</div>','');
      var headers = {
        'Content-Type': 'application/json',
        // 'Authorization': `Bearer ${this.token}`
      };
      axios.post(`http://127.0.0.1:5000/api/v1/postComment/${this.user_id}/${this.$route.params.id}`,
        {
					comment: this.comment
				},{headers}).then((response) => {
        // console.log(response.data.result)
        if (response.status === 200) {
          if (response.data.status === "Success") {
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
        } else {
          this.errorMessage = 'Internal Server Error';
          this.errorUploadFile = true;
          setTimeout(() => {this.errorUploadFile = false, this.file = ''}, 5000);
        }
				this.getData()
      }).catch((error) => {
        if (error.response !== undefined) {
          this.success = false;
          // setAlert(this, error.response);
        }
      });
    },
    // goTo(content_id) {
    //   // this.postModalToggle = true
    //   console.log(content_id)
    //   this.$router.push({name: 'post/' + content_id})
    // },
		openPostCommentDialog() {
			this.commentModalToggle = true
		},
		checkBeforeSubmit(){
      if (this.comment == "") {
        this.AlertMassage = "Please Fill the Comment Field"
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
