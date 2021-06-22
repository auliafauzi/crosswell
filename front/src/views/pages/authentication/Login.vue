<template>
	<vue-scroll class="login-page align-vertical">
		<div class="form-wrapper align-vertical-middle">



			<div class="form-box card-base card-shadow--extraLarge">

				<template v-if="errorAlert">
		      <b-row>
		        <b-col sm="12">
		          <b-alert show variant="danger">{{errorMessage}}</b-alert>
		        </b-col>
		      </b-row>
		    </template>

				<!-- <img class="image-logo" src="@/assets/images/logo.png" alt="logo"/> -->
				<!-- <div class="app-name">Partner Management</div> -->
				<!-- <img class="image-logo" src="@/assets/images/logo.png" alt="logo"/> -->
				<img class="image-logo2" src="@/assets/images/logo.png" alt="logo"/>
				<!-- <div class="app-name" @click="goto('/')">Partner Management</div> -->
				<div class="box-logo flex align-center">
					<!--<div class="letter-logo">P</div>-->
					<!-- <img class="image-logo" src="@/assets/images/logo.png" alt="logo"/> -->
					<!-- <img class="image-logo" src="@/assets/images/logo.png" alt="logo"/> -->
					<div class="app-name" @click="goto('/')">Partner Management</div>
					<!-- <button class="collapse-nav" @click="collapseNavToggle">
						<i class="mdi mdi-menu"></i>
					</button> -->
				</div>

				<float-label class="styled">
					<input type="user name" placeholder="User Name" maxlength="100" v-model="userName">
				</float-label>
				<float-label class="styled">
					<input type="password" placeholder="Password" maxlength="100" v-model="password">
				</float-label>
				<!-- <b-form-input type="text"
								placeholder="Enter password"
								v-model="password">
				</b-form-input> -->

				<div class="flex">
					<!-- <div class="box grow"><el-checkbox>Remember Me </el-checkbox></div> -->
					<div class="box grow text-left" sm="12" @click="select()"><div class = "text">Forgot Password?</div></div>
				</div>

				<div class="flex text-center center pt-30 pb-10">
					<el-button plain size="small" @click="login" class="login-btn tada animated">
						LOGIN
					</el-button>
					<!-- <el-button @click="ErrorModalShow = !ErrorModalShow">Open Modal</el-button> -->
				</div>

				<!-- <div class="text-divider mv-10"></div> -->

				<!-- <div class="flex column center pt-10 pb-10">
					<el-button plain size="small" @click="login" class="social-btn google">
						Log in with Google
					</el-button>
					<el-button plain size="small" @click="login" class="social-btn facebook">
						Log in with Facebook
					</el-button>
				</div> -->

			 <b-modal v-model="modalShow" :body-bg-variant="modal_variants"
			 :header-bg-variant="modal_variants"
			 :footer-bg-variant="modal_variants"
			 :hide-header='hideHeader'
			 :footer-class='footerClass'
			 :cancel-disabled='cancelButtonDisable'
			 :hide-footer="true"
			 :body-text-variant="text_variants">{{errorText}}</b-modal>

			</div>
		</div>

		<div>

	 	</div>

	</vue-scroll>



</template>

<script>
import axios from "axios";
import { saveUserDataInSession2, getUserDataInSession2, setToken, BASE_URL} from '../../../utils';

export default {
	name: 'Login',
	data() {
		return {
			form: {
				email: null,
				password: null,
			},
			userName: '',
			password: '',
			errorAlert: false,
			errorMessage: '',
			loginError: false,
	    expiryError: false,
	    serverError: false,
			modalShow: false,
			modal_variants: 'light',
			text_variants: 'danger',
			errorText: '',
			hideHeader: true,
			footerClass: 'p-2 border-top-0',
			cancelButtonDisable:true,
			freeText: '',
			localValue : {
				auth:'',
				role:''
			}
			// ErrorModal:{}
		}
	},
	mounted(){
		if (localStorage.getItem('reloaded')) {
        // The page was just reloaded. Clear the value from local storage
        // so that it will reload the next time this page is visited.
        localStorage.removeItem('reloaded');
    } else {
        // Set a flag so that we know not to reload the page twice.
        localStorage.setItem('reloaded', '1');
        location.reload();
    }
	// 	this.$router.go(0)
	// },
	// created(){
	// 	this.$router.go(0)
	},
	methods: {
		select() {
			console.log("forgot password")
			this.errorAlert = true;
			this.errorMessage = "Mohon Kontak System Administrator";
			setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
		},
		loginold() {
			this.$store.commit('setLogin')
			this.$router.push('dashboard')
		},
		// showModal() {
		// 	this.ErrormodalShow = true
    // },
		login(logfilename) {
			if (this.userName === '') {
				this.errorMessage = 'Username tidak boleh kosong';
				this.errorAlert = true;
				setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
			}
			else if (this.password === '') {
				this.errorMessage = 'Password tidak boleh kosong';
				this.errorAlert = true;
				setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
			}
			else {
	      // axios({
	      //   method: "post",
	      //   url: `http://0.0.0.0:3000/api/v1/login`,
				// 	// url: `${BASE_URL}/login`,
	      //   // headers: {Authorization: `Bearer ${this.state.login.access_token}`},
	      //   withCredentials: true, // True otherwise I receive another error
				// 	body: { user: this.userName, password: this.password }
	      // })
				// axios.post("http://0.0.0.0:3000/api/v1/login",{
				var headers = {
					'Content-Type': 'application/json'
				}
				axios.post(`${BASE_URL}/login`,{
								user: this.userName,
								password: this.password
							}, headers
					).then(response => {
					console.log("response not error")
					console.log(response)
	        if (response.status === 200) {
						console.log("status = 200 ")
						// if (response.data.token !== null && response.data.data.active === true) {
						if (response.data.data !== null) {
							if (response.data.data.active === true) {
								console.log("ROLE" + response.data.data.role)
								saveUserDataInSession2('UserInfo',response.data.data)
								saveUserDataInSession2('UserName',response.data.data.name)
								saveUserDataInSession2('userRole',response.data.data.role)
								saveUserDataInSession2('userCompanyId',response.data.data.company.id)
								saveUserDataInSession2('userCompanyName',response.data.data.company.name)
								if (response.data.data.company.logo != undefined) {
									saveUserDataInSession2('logoPath',response.data.data.company.logo)
								}
								setToken(response.data.data.token);
								this.localValue = getUserDataInSession2('userRole')
								if (response.data.data.role === 'HRD') {
									this.$router.push('/whiteList');
								} else {
									this.$router.push('/companyList');
								}
								// this.$router.push('/uploadBatch');
							} else {
								this.errorMessage = 'User Tidak Aktif, Mohon Kontak Administrator'
								this.errorAlert = true
								setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
							}
						} else {
							this.errorMessage = response.data.message
							this.errorAlert = true
							setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
						}
					} else if (error.response.data.code === 502){
						console.log("response not error + 502")
						this.errorMessage = 'Bad Gateway, Server Sedang Bermasalah'
						this.errorAlert = true
						setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
					} else {
						// console.log(response.data)
						this.errorMessage = response.status
						this.errorAlert = true
						setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
						}
	        }).catch((error) => {
						console.log("catch error")
						console.log(error.response)
		        if (error.response !== undefined) {
							console.log("error defined")
		          if (error.response.status === 401) {
								this.errorMessage = error.response
								this.errorAlert = true
								setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
		          } else if (error.response.status === 400){
								this.errorMessage = error.response
								this.errorAlert = true
								setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
		          } else if (error.response.status === 502){
								this.errorMessage = 'Bad Gateway, Server Sedang Bermasalah'
								this.errorAlert = true
								setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
		          } else {
								this.errorMessage = error.response
								this.errorAlert = true
								setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
							}
		        } else {
							console.log("error undefined")
							this.errorMessage = 'Server Sedang Bermasalah'
							this.errorAlert = true
							setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
		          // this.serverError = true;
		        }
		      });
			}
    },
	}
}
</script>

<style lang="scss">
@import '../../../assets/scss/_variables';
@import '../../../assets/scss/_mixins';

.text {
	font-size: 14px;
	cursor: pointer;
}

.image-logo2 {
	width: 80px;
	height: 80px;
	margin-right: 70px;
	margin-left: 100px;
	margin-bottom: 10px;
	margin-top: 30px;
	position: center;
	// filter: drop-shadow(0px 2px 2px rgba(0, 0, 0, 0.3));
}

.login-page {
	background: $text-color;
	margin-left: -30px;
	margin-right: -30px;

	.form-wrapper {
		width: 100%;
	}

	.form-box {
		width: 100%;
		max-width: 340px;
		padding: 30px;
		box-sizing: border-box;
		margin: 20px auto;

		a {
			font-size: 14px;
			color: $text-color-accent;
			text-decoration: none;
			font-weight: 500;
		}

		// .image-logo {
		// 	width: 80px;
		// 	margin: 0px auto;
		// 	margin-bottom: 30px;
		// 	display: block;
		// }

		.login-btn ,
		// .social-btn {
		// 	width: 160px;
		//
		// 	&.google {
		// 		margin-bottom: 10px;
		// 		background-color: #d73d32;
		// 		color: white;
		//
		// 		&:hover {
		// 			border-color: #d73d32;
		// 		}
		// 	}
		// 	&.facebook {
		// 		background-color: #3f5c9a;
		// 		color: white;
		//
		// 		&:hover {
		// 			border-color: #3f5c9a;
		// 		}
		// 	}
		// }

		.signin-box {
			font-size: 14px;
		}

		.image-logo {
			width: 40px;
			height: 80px;
			margin-right: 10px;
			// filter: drop-shadow(0px 2px 2px rgba(0, 0, 0, 0.3));
		}
		.box-logo {
			height: 70px;
			// width: 200px;
			padding: 20 60px;
			box-sizing: border-box;
			font-size: 16px;
			font-weight: bold;
			position: relative;
			@include text-bordered-shadow();

			.letter-logo {
				width: 50px;
				height: 30px;
				line-height: 20px;
				text-align: center;
				background: $text-color;
				color: $text-color-accent;
				border-radius: 5px;
				margin-right: 10px;
				font-weight: bolder;
				font-size: 20px;
			}

			.image-logo {
				width: 50px;
				height: 40px;
				margin-right: 10px;
				filter: drop-shadow(0px 2px 2px rgba(0, 0, 0, 0.3));
			}

			.app-name {
				margin-left: 30px;
				font-size: 18px;
				width: 200px;
				cursor: pointer;
				margin-bottom: 30px;
			}
		}
	}
}

@media (max-width: 768px) {
	.layout-container .container .view.login-page {
		margin-left: -5px;
		margin-right: -5px;
		max-width: calc(100% + 10px);
	}
}
</style>
