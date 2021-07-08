<template>

	<div class=flex>
	<el-menu
		:mode="mode"
		@select="goto"
		:collapse="isCollapse"
		:unique-opened="true"
		background-color="transparent"
		class="main-navigation-menu"
		:class="{'nav-collapsed':isCollapse}"
	>
	<!-- <el-menu
		:default-active.sync="activeLink"
		:mode="mode"
		@select="goto"
		:collapse="isCollapse"
		:unique-opened="true"
		background-color="transparent"
		class="main-navigation-menu"
		:class="{'nav-collapsed':isCollapse}"
	> -->

<!-- <div class="el-menu-item-group__title" style="padding-top: 4px;"><span>Apps</span></div> -->
	<!-- <el-menu-item index="/logout">
		<i class="mdi mdi-account"></i><span slot="title">Login</span>
	</el-menu-item> -->

	<!-- <el-menu-item index="/companyList" v-if="roleSuperAdmin">
		<i class="mdi mdi-atom-variant"></i><span slot="title">Company</span>
	</el-menu-item>
	<el-menu-item index="/whiteList">
		<i class="mdi mdi-ballot-outline"></i><span slot="title">Whitelist Management</span>
	</el-menu-item>
	<el-menu-item index="/uploadBatch">
		<i class="mdi mdi-attachment"></i><span slot="title">Upload Batch</span>
	</el-menu-item>
	<el-menu-item index="/userList" v-if="roleSuperAdmin">
		<i class="mdi mdi-account"></i><span slot="title">User Management</span>
	</el-menu-item> -->
	<el-menu-item index="/home">
		<i class="mdi mdi-bookshelf"></i><span slot="title">Home</span>
	</el-menu-item>
	<el-menu-item index="/map">
		<i class="mdi mdi-earth"></i><span slot="title">Map</span>
	</el-menu-item>


	</el-menu>

	<el-menu
	:mode="mode"
	@select="profileModal"
	:collapse="isCollapse"
	:unique-opened="true"
	background-color="transparent"
	class="main-navigation-menu"
	:class="{'nav-collapsed':isCollapse}"
	style="position:fixed;right:0;margin-right:50px">
		<!-- <el-menu-item>
			<i></i><span slot="title">LOGIN</span>
		</el-menu-item> -->
		<el-menu-item>
			<i class= "mdi mdi-account-circle"></i><span slot="title">{{this.profile_name}}</span>
		</el-menu-item>
	</el-menu>

	<b-modal id="Profile_Modal"
		 v-model="profileToggle"
		 size="sm"
		 ok-title="Ok"
		 @ok="handleOk">

		 <template v-if="errorAlert">
			<b-row>
				<b-col sm="12">
					<b-alert show variant="danger">{{errorMessage}}</b-alert>
				</b-col>
			</b-row>
		</template>

		 <img class="image-logo" src="@/assets/images/logo.png" alt="logo" style="width:50%; margin-left:25%; margin-bottom:20%; margin-top:10%"/>
		 <float-label class="styled">
			 <input type="user name" placeholder="User Name" maxlength="100" v-model="userName">
		 </float-label>
		 <float-label class="styled">
			 <input type="password" placeholder="Password" maxlength="100" v-model="password">
		 </float-label>

	 </b-modal>

	 <b-modal id="Logout_Modal"
 		 v-model="logoutToggle"
 		 size="sm"
 		 ok-title="Ok"
 		 @ok="handleLogout">

 		 <img class="image-logo" src="@/assets/images/logo.png" alt="logo" style="width:50%; margin-left:25%; margin-bottom:20%; margin-top:10%"/>
 		 <div>Logout?</div>

 	 </b-modal>

</div>

</template>


<script>
import { detect } from 'detect-browser';
import axios from "axios";
import { saveUserDataInSession2, getUserDataInSession2 } from '../utils';
const browser = detect()

export default {
	name: 'Nav',

	props: ['mode', 'isCollapse'],
	data() {
		return {
			profile_name: '',
			roleSuperAdmin:false,
			userRole:'',
			isIe: true,
			isEdge: true,
			activeLink: null,
			profileToggle: false,
			logoutToggle: false,
			userName:'',
			password:'',
			errorAlert: false,
			errorMessage: ''
		}
	},
	methods: {
		superAdminTrue(){
			this.roleSuperAdmin = true
		},
		goto(index, indexPath) {
			if(index.charAt(0) === '/') {
				this.$router.push(index)
				this.$emit('push-page', {page:index})
			}
		},
		profileModal(){
			if ( getUserDataInSession2('UserRole') == "0" || getUserDataInSession2('UserRole') == '' || getUserDataInSession2('UserRole') == undefined) {
				this.profileToggle = true
			} else {
				this.logoutToggle = true
			}

		},
		setLink(path) {
			this.activeLink = path
		},
		handleOk(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault()
      // Trigger submit handler
      this.login()
    },
		login(){
				if (this.userName === '') {
					// this.profileToggle = true;
					// this.$refs['Profile_Toggle'].show()
					this.errorMessage = 'Username tidak boleh kosong';
					this.errorAlert = true;
					setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
				}
				else if (this.password === '') {
					// this.profileToggle = true;
					// this.$refs['Profile_Toggle'].show()
					this.errorMessage = 'Password tidak boleh kosong';
					this.errorAlert = true;
					setTimeout(() => {this.errorAlert = false, this.errorMessage = ''}, 3000);
				}
				else {
					var headers = {
						'Content-Type': 'application/json'
					}
					axios.post(`http://127.0.0.1:5000/api/v1/login`,{
									username: this.userName,
									password: this.password
								}, headers
						).then(response => {
						console.log("response not error")
						console.log(response)
		        if (response.status === 200) {
							console.log("status = 200 ")
							console.log("response.data: " + response.data)
							if (response.data !== null) {
								console.log("ROLE: " + response.data.user_role)
								// saveUserDataInSession2('UserInfo',response.data.data)
								saveUserDataInSession2('UserName',response.data.username);
								saveUserDataInSession2('UserRole',response.data.user_role);
								saveUserDataInSession2('UserId',response.data.user_id);
								saveUserDataInSession2('token',response.data.token);
								window.location.reload();
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
							console.log("error: " + error.response)
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
		handleLogout(){
			// localStorage.removeItem(['UserName','UserRole','token'])
			localStorage.removeItem('UserName')
			localStorage.removeItem('UserRole')
			localStorage.removeItem('UserId')
			localStorage.removeItem('token')
			window.location.reload();
		}
	},
	created() {
		if(browser.name !== 'ie') this.isIe = false
		if(browser.name !== 'edge') this.isEdge = false

		this.setLink(this.$router.currentRoute.path)
		this.$router.afterEach((to, from) => {
			this.setLink(this.$router.currentRoute.path)
			//console.log('afterEach', to, from)
		})
		//console.log('this.$router.currentRoute.path', this.$router.currentRoute.path)
	},
	mounted() {
		console.log("userRole: " + getUserDataInSession2('UserRole'))

		if (getUserDataInSession2('UserRole') == "0") {
			this.profile_name = "PROFILE"
		} else {
			this.profile_name = String(getUserDataInSession2('UserName').replace(/\"/gi, ''))
		}
	}
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/_variables';

.el-menu {
	border: none;
}
.el-menu::before, .el-menu::after {
	display: none;
}
.el-submenu, .el-menu-item {
	.mdi {
		vertical-align: middle;
		margin-right: 5px;
		display: inline-block;
		width: 24px;
		text-align: center;
		font-size: 18px;
	}
}
</style>

<style lang="scss">
@import '../assets/scss/_variables';

.main-navigation-menu {
	transition: width .5s;

	&:not(.el-menu--collapse) {
		.el-submenu__title, .el-menu-item {
			height: 40px;
			line-height: 40px;
			background-color: transparent !important;
		}

		&:not(.el-menu--horizontal) {
			.el-menu-item, .el-submenu {
				position: relative;

				&::before {
					content: '';
					display: block;
					width: 0px;
					height: 1px;
					position: absolute;
					bottom: 10px;
					left: 30px;
					background: $text-color;
					z-index: 1;
					opacity: 0;
					transition: all .7s cubic-bezier(.55,0,.1,1);
				}
				&:hover {
					&::before {
						width: 100px;
						opacity: 1;
						//left: 50px;
						transform: translate(20px, 0);
					}
				}

				&.is-active {
					&::before {
						background: $text-color-accent;
					}
				}
			}
		}

		.el-submenu.is-opened {
			//background: #edf1f6 !important;
			//background: rgba(223, 228, 234, 0.38) !important;
			position: relative;

			&::after {
				content: '';
				display: block;
				width: 2px;
				position: absolute;
				top: 40px;
				bottom: 10px;
				left: 31px;
				background: $text-color;
				z-index: 1;
			}

			&::before {
				display: none;
			}

			.el-menu-item, .el-submenu {
				&::before, &::after {
					display: none;
				}
			}
		}

		.el-menu-item-group__title {
			padding: 15px 0 0px 20px;
			color: transparentize($text-color, 0.65);
		}
	}

	.el-submenu__title, .el-menu-item:not(.is-active) {
		color: $text-color;

		i {
			color: $text-color;
		}
	}

	&.el-menu--collapse {
		.el-menu-item-group__title {
			padding: 15px 0 0px 0px;
			width: 100%;
			text-align: center;
		}

		.el-submenu__title:hover, .el-menu-item:hover {
			background-color: rgba(0, 0, 0, 0.05) !important;
		}
	}

	&.el-menu--horizontal {
		white-space: nowrap;
		/*width: fit-content;
		width: max-content;*/
		overflow: hidden;
		display: table;

		& > * {
			float: inherit !important;
			display: inline-block;
		}
	}

	&.nav-collapsed {
		.el-menu-item,.el-submenu__title {
			& > span {
				display: none;
			}
		}
	}
}

.main-navigation-submenu {
	.el-menu {
		background: #fff !important;

		.el-menu-item:not(.is-active) {
			color: $text-color;
		}
		.el-menu-item:hover {
			background-color: transparentize($background-color, 0.3) !important;
		}
	}
}
</style>
