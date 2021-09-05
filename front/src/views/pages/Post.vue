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

			<div class="box grow card-base card-shadow--small p-24" style= "white-space: pre-line; margin-bottom: 20px; margin-left: 50px; margin-right: 300px; background: rgba(95, 143, 223, 0.2);">
				<!-- <div style=" max-width: 1100px; margin: 0 auto; "> -->
				<!-- <div style=" max-width: 11000px;"> -->
        <div>
          <p style="font-size: 12px;">
            {{this.content.user_name}}
          <p>
						<p style="font-size: 8px;">
	            {{this.content.date}}
	          <p>
					<!-- <p class="mt-18">
						<img src="@/assets/images/photo1.jpg" class="demo-img" alt="demo image">
					</p> -->
					<h1 class="mt-8">{{this.content.title}}</h1>
					<p style="font-size: 8px;">
						{{this.content.lat}} {{this.content.long}}
					<p>
					<div v-if="this.content.image_path != null">
						<img v-if="this.content.image_path !=''" :src="this.ImagePath"/>
					</div>
					<p class="mt-0">
						{{this.content.content}}
					</p>
					<!-- <div/> -->
					<p class="mt-0" v-if="this.content.file_path != null">
						<h4 v-if="this.content.file_path != ''" style="text-decoration: underline;font-style: italic;cursor: pointer; font-size: 15px" @click="getFile()">
							Get the file
						</h4>
					</p>

				</div>
			</div>
      <div flex>
        <b-button v-if= "user_id != '' " variant="outline-primary" @click="openPostCommentDialog()" size="sm" class="mr-1" style="margin-left: 70px;">
          Leave Comment
        </b-button>
          <b-button variant="outline-primary" size="sm" class="mr-1" @click="openEditPostDialog()" style="margin-left: 10px;" v-if= "user_id == this.content.user_id || this.user_role == 1">
            Edit Post
          </b-button>
          <b-button variant="outline-danger" size="sm" class="mr-1" @click="deleteConfirm()" style="margin-left: 10px;" v-if= "user_id == this.content.user_id || this.user_role == 1">
            Delete Post
          </b-button>
      </div>
      <div class="box grow card-base card-shadow--small p-24" style= "margin-bottom: 10px; margin-top: 10px; margin-left: 70px; margin-right: 300px;" v-for="i in commentList">
				<div style=" max-width: 1100px;">
          <p style="font-size: 10px;">
            {{i.user_name}}
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
					<b-form-textarea
			      id="textarea"
			      v-model="comment"
			      placeholder="Post something..."
			      rows="19"
			    ></b-form-textarea>
     		</div>
     	</div>
		</b-modal>

		<b-modal id="EditContentModal"
       title="Edit Content"
       v-model="editContentToggle"
       size="lg"
       ok-title="Ok"
       @ok="editContent">

       <div class="page-quill scrollable">
     		<div class="card-base card-shadow--medium">
					<b-form-textarea
			      id="textarea"
			      v-model="content.content"
			      rows="19"
			    ></b-form-textarea>
     		</div>
     	</div>
		</b-modal>

		<b-modal id="confirmDeleteModal"
						v-model="DeleteToggle"
						ok-title="Ok" @ok="deletePost()">Delete this Post ?

		</b-modal>

	</div>
</template>

<script>
import axios from "axios";
import {getToken, getUserDataInSession2, BASE_URL} from '../../utils';
export default {
	name: 'LayoutSidebarRight',
	data() {
		return {
			list : ['test1', 'test2', 'test3'],
      user_id : '',
      // dummy hard coded user_role
      user_role : 2,
      //
      content : [],
      commentList : [],
      content_id : '',
      commentModalToggle : false,
			SuccessToogle : false,
			AlertToggle : false,
			DeleteToggle: false,
			editContentToggle: false,
			SuccessMassage:'',
			AlertMassage:'',
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
			image : null,
			eligible : undefined,
			ImagePath: BASE_URL + "/api/v1/contentImage/" + this.$route.params.id
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
	 try {
		 this.user_id = String(getUserDataInSession2('UserId').replace(/\"/gi, ''))
		 this.user_role = getUserDataInSession2('UserRole').replace(/[.",\/#!$%\^&\*;:{}=\-_`~()]/g,"")
		 this.token = getUserDataInSession2('token').replace(/[.",\/#!$%\^&\*;:{}=\-_`~()]/g,"")
	 } catch(err) {
		 console.log("err: ", err)
	 }

   this.content_id = this.$route.params.id
   console.log("yaa " + this.$route.params.id)
   this.getData()
	 console.log("gambar: " + BASE_URL + "/api/v1/contentImage/" + this.$route.params.id)
	 console.log("content mounted: ", this.content)
  },
  methods : {
    getData() {
      var headers = {
        'Content-Type': 'application/json',
        // 'Authorization': `Bearer ${this.token}`
      }
      // axios.get(`${BASE_URL}/companies?page=${this.currentPage}&size=${this.perPage}`,{
      axios.get(`${BASE_URL}/api/v1/contentDetail/${this.$route.params.id}`,{
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
							// this.eligible = response.data.eligible
							// console.log("eligible: ", this.eligible)
							console.log("get data content: ", this.content)
							console.log("repsonse: ", response.data.content)
            }
          }
        })
        axios.get(`${BASE_URL}/api/v1/commentList/${this.$route.params.id}`,{
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

    },
		submitComment() {
			// this.comment = this.comment.replace('<div>','');
      // this.comment = this.comment.replace('</div>','');
      var headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      };
      axios.post(`${BASE_URL}/api/v1/postComment/${this.$route.params.id}`,
        {
					comment: this.comment
				},{headers}).then((response) => {
        // console.log(response.data.result)
        if (response.status === 200) {
          if (response.data.code === 200) {
						this.SuccessMassage = "Comment posted"
						this.SuccessToogle = true
						console.log("SuccessMassage:", this.SuccessMassage)
						setTimeout(() => {this.SuccessToogle = false, this.successMessage = ''}, 3000);
          } else {
						this.AlertMassage = "Failed to post the comment"
						this.AlertToggle = true
						setTimeout(() => {this.AlertToggle = false, this.AlertMassage = ''}, 7000);
          }
        } else {
          this.AlertMassage = 'Internal Server Error';
					this.AlertToggle = true
					setTimeout(() => {this.AlertToggle = false, this.AlertMassage = ''}, 7000);
        }
				this.getData()
      }).catch((error) => {
        if (error.response !== undefined) {
          this.success = false;
          // setAlert(this, error.response);
        }
      });
    },
		editContent() {
			this.token = getUserDataInSession2('token')
			if (this.token != '') {
					this.token = getToken().replace(/[.",\/#!$%\^&\*;:{}=\-_`~()]/g,"");
			}
			console.log("submit token :", this.token )

      var headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      };
      axios.post(`${BASE_URL}/api/v1/editContent`,{
					content: this.content
				},{headers}).then((response) => {

        if (response.status === 200) {
          if (response.data.status === "success") {
						this.SuccessMassage = response.data.message
						this.SuccessToogle = true
						console.log("SuccessMassage:", this.SuccessMassage)
						setTimeout(() => {this.SuccessToogle = false, this.successMessage = '',location.reload()}, 3000);
            // setTimeout(() => {this.successUploadFile = false, this.file = '', location.reload()}, 3000);
          } else {
						this.AlertMassage = response.data.message
						this.AlertToggle = true
						setTimeout(() => {this.AlertToggle = false, this.AlertMassage = ''}, 7000);
          }
					this.getData()
        } else {
          this.AlertMassage = 'Internal Server Error';
					// this.AlertMassage = response.data.message
					this.AlertToggle = true
					setTimeout(() => {this.AlertToggle = false, this.AlertMassage = ''}, 7000);
        }
      }).catch((error) => {
        if (error.response !== undefined) {
          this.success = false;
          // setAlert(this, error.response);
        }
      });
    },
		getFile(){
			var headers = {
        // 'Content-Type': 'application/json',
				// 'Content-Type': 'multipart/form-data'
        // 'Authorization': `Bearer ${this.token}`
      }
			axios.get(`${BASE_URL}/api/v1/contentFile/${this.$route.params.id}`,{
						responseType: 'blob'
						},
				).then((response) => {
			    const url = window.URL.createObjectURL(new Blob([response.data]));
			    const link = document.createElement('a');
					let filename = response.headers["x-filename"];
			    link.href = url;
					// window.open(url)
			    link.setAttribute('download', filename);
			    document.body.appendChild(link);
			    link.click();
			})
		},
    // goTo(content_id) {
    //   // this.postModalToggle = true
    //   console.log(content_id)
    //   this.$router.push({name: 'post/' + content_id})
    // },
		openPostCommentDialog() {
			this.commentModalToggle = true
		},
		deleteConfirm(){
			this.DeleteToggle = true
		},
		openEditPostDialog(){
			this.editContentToggle = true
		},
		deletePost(){
			this.token = getUserDataInSession2('token').replace(/[.",\/#!$%\^&\*;:{}=\-_`~()]/g,"")
			var headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      };
			console.log("going delete post; token: " , this.token)
			axios.delete(`${BASE_URL}/api/v1/deleteContent/${this.$route.params.id}`, {headers}
			).then((response) => {
					if (response.status === 200) {
						if (response.data.code === 200){
							this.SuccessMassage = response.data.message
							this.SuccessToogle = true
							console.log("SuccessMassage:", this.SuccessMassage)
							setTimeout(() => {this.SuccessToogle = false, this.successMessage = '',this.$router.push("/home")}, 3000);
						}
						else {
							this.AlertMassage = response.data.message
							this.AlertToggle = true
							setTimeout(() => {this.AlertToggle = false, this.AlertMassage = ''}, 3000);
							// console.log(response.data.message)
						}
					}
					else {
						// failed to get response
						this.AlertMassage = "Internal server down"
						this.AlertToggle = true
						setTimeout(() => {this.AlertToggle = false, this.AlertMassage = ''}, 3000);
						// console.log("Internal server down")
					}
				})
		},
		checkBeforeSubmit(){
      if (this.comment == "") {
        this.AlertMassage = "Please Fill the Comment Field"
        this.AlertToggle = true
        setTimeout(() => {this.AlertToggle = false, this.AlertMassage = ''}, 3000);
      }
      else {
        this.submitComment()
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
