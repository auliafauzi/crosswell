<template>


	<div class="toolbar flex align-center justify-space-between">

		<b-modal id="companyDetail" v-model="DetailToggle" ok-title="Ok">

			<template v-if="errorAlertinDetail">
				<b-row>
					<b-col sm="12">
						<b-alert show variant="danger">{{errorMessage}}</b-alert>
					</b-col>
				</b-row>
			</template>

			<!-- <img class="logo-mini" src="@/assets/images/logo.png" alt="logo"
			height="150px"
			width="150px"/></p> -->
			<template v-if="this.ImagePath != ''">
			 <img class="logo-mini" :src=this.ImagePath alt="logo"
			 height="150px"
			 width="150px"/></p>
		 </template>
			<b-button variant="outline-primary" size="sm" @click="changeLogo()" class="mr-1">
				Change Logo
			</b-button>
			<div class="mt-3">Company:</div>
			<div class="mt-3"> <pre> {{CompanyName}}</pre> </div>
			<!-- <b-button variant="outline-primary" size="sm" @click="editModal(DataDetail.name)" class="mr-1">
				Change Name
			</b-button> -->
			<!-- <div class="mt-3">Created Date:</div>
			<div class="mt-3"><pre> {{DataDetail.createdDate}}</pre> </div>
			<div class="mt-3">Updated Date: <strong></strong></div>
			<div class="mt-3"><pre> {{DataDetail.updateDate}}<strong></strong></pre> </div>
			<div class="mt-3">Created By : <strong></strong></div>
			<div class="mt-3"><pre> {{DataDetail.createdBy}}<strong></strong></pre> </div>
			<div class="mt-3">Updated By: <strong></strong></div>
			<div class="mt-3"><pre> {{DataDetail.updatedBy}}<strong></strong></pre> </div> -->
		</b-modal>

		<div class="box-left box grow flex">
			<button @click="toggleSidebar" v-if="menuBurger !== 'right'" class="toggle-sidebar card-base card-shadow--small">
				<i class="mdi mdi-menu"></i>
			</button>

			<img class="logo-mini" src="@/assets/images/logo.png" alt="logo"/>

			<!-- <search class="hidden-xs-only"></search> -->
		</div>
		<div class="box-right flex align-center pl-10">
			<!-- <el-dropdown trigger="click" @command="onCommandLang">
				<span class="el-dropdown-link">
					<i class="flag-icon" :class="{['flag-icon-'+lang]:true}"></i>
				</span>
				<el-dropdown-menu slot="dropdown">
					<el-dropdown-item command="us"><i class="flag-icon flag-icon-us mr-15"></i>English</el-dropdown-item>
					<el-dropdown-item command="it"><i class="flag-icon flag-icon-it mr-15"></i>Italian</el-dropdown-item>
					<el-dropdown-item command="fr"><i class="flag-icon flag-icon-fr mr-15"></i>French</el-dropdown-item>
					<el-dropdown-item command="de"><i class="flag-icon flag-icon-de mr-15"></i>German</el-dropdown-item>
					<el-dropdown-item command="es"><i class="flag-icon flag-icon-es mr-15"></i>Spanish</el-dropdown-item>
					<el-dropdown-item command="cn"><i class="flag-icon flag-icon-cn mr-15"></i>Chinese</el-dropdown-item>
					<el-dropdown-item command="jp"><i class="flag-icon flag-icon-jp mr-15"></i>Japanese</el-dropdown-item>
					<el-dropdown-item command="/multi-language"><i class="mdi mdi-translate mr-15"></i>Read the docs</el-dropdown-item>
				</el-dropdown-menu>
			</el-dropdown> -->
			<button class="fullscreen-button" @click="toggleFullscreen">
				<i class="mdi mdi-fullscreen" v-if="!fullscreen"></i>
				<i class="mdi mdi-fullscreen-exit" v-if="fullscreen"></i>
			</button>
			<!-- <el-popover ref="popover" placement="bottom" :width="popoverWidth" trigger="click">
				<notification-box></notification-box>
			</el-popover>
			<el-badge :is-dot="true" class="notification-icon-badge">
				<el-button v-popover:popover icon="mdi mdi-bell" class="notification-icon"></el-button>
			</el-badge> -->
			<div class = company-logo >
				<template v-if="this.ImagePath != ''">
				 <img class="logo-mini2" :src=this.ImagePath alt="logo"/>
			 </template>
			</div>
			<div class= name-box>
				<div class="username">{{userName}}</div>
				<div class="username2">{{userInfo}}</div>
			</div>
			<!-- <span class="username"><router-link to="/profile">Admin</router-link></span> -->
			<el-dropdown trigger="click" @command="onCommandLang">
				<span class="el-dropdown-link">
					<img src="../assets/images/avatar-3.jpg" class="avatar" alt="avatar">
					<!-- <p></p> -->
					<!-- <i class="mdi mdi-account-circle" size="lg"></i> -->
				</span>
				<el-dropdown-menu slot="dropdown">
					<el-dropdown-item v-if="IsNotSuperUser" command="companyDetail"><i class="mdi mdi-account mr-10"></i> Profile</el-dropdown-item>
					<!-- <el-dropdown-item command="/calendar"><i class="mdi mdi-calendar mr-10"></i> Calendar</el-dropdown-item>
					<el-dropdown-item command="/contacts"><i class="mdi mdi-account-multiple mr-10"></i> Contacts</el-dropdown-item> -->
					<el-dropdown-item command="/logout"><i class="mdi mdi-logout mr-10"></i> Logout</el-dropdown-item>
				</el-dropdown-menu>
			</el-dropdown>

			<button @click="toggleSidebar" v-if="menuBurger === 'right'" class="toggle-sidebar toggle-sidebar__right card-base card-shadow--small">
				<i class="mdi mdi-menu"></i>
			</button>

			<b-modal id="uploadLogoModal"
							v-model="UploadLogoToggle"
							ok-title="Ok" @ok="uploadLogo()">Change logo for :  {{CompanyName}}
							<label>
								<input type="file" id="file" accept=".png,.jpg,.jpeg" ref="file" v-on:change="handleFileUpload()"/>
							</label>

			</b-modal>

		</div>
	</div>
</template>

<script>
import NotificationBox from '@/components/NotificationBox';
import Search from '@/components/Search';
import {getToken, getItem, getUserDataInSession2} from '../utils';
import axios from "axios";

export default {
	name: 'Toolbar',
	props: ['menuBurger'],
	data() {
		return {
			popoverWidth: 300,
			fullscreen: false,
			lang: 'us',
			userName : '',
			userInfo: '',
			IsNotSuperUser : false,
			DetailToggle: false,
			errorAlertinDetail: false,
			errorMessage : '',
			DataDetail: {},
			CompanyName : '',
			UploadLogoToggle : false,
			CompanyId : '',
			ImagePath : ''
		}
	},
	methods: {
		companyDetail(){
			console.log("ImagePath: " + this.ImagePath )
			this.DetailToggle = true
			console.log("DETAIL TOGGLE TRUE")
		},
		onCommandLang(lang) {
			if(lang.charAt(0) === '/')
				this.onCommand(lang)
			else if (lang === "companyDetail") {
				this.companyDetail()
			}
			else
				this.lang = lang
		},
		onCommand(path) {
			this.$router.push(path)
		},
		toggleSidebar() {
			this.$emit('toggle-sidebar')
		},
		resizePopoverWidth() {
			if(window.innerWidth <= 768) {
				this.popoverWidth = 250
			} else {
				this.popoverWidth = 300
			}
		},
		changeLogo(id){
      this.CompanyId = getUserDataInSession2("userCompanyId")
      this.UploadLogoToggle = true
    },
		handleFileUpload() {
			this.file = this.$refs.file.files[0];
		},
		uploadLogo(evt) {
			if (this.file === '' || this.file === undefined) {
				evt.preventDefault();
				// this.$refs.modalRestore.show();
				this.errorMessage = 'Please select the file to upload';
				this.errorAlert = true;
				setTimeout(() => {console.log("sleeping"),this.errorAlert = false, this.file = ''}, 5000);
			}
			else {
				this.errorRestore = false;
				this.submitFile();
			}
		},
		submitFile() {
			this.token = getToken()
			const formData = new FormData();
			formData.append('file', this.file);
			formData.append('company-id', this.CompanyId);
			console.log("id: " + this.CompanyId)
			var headers = {
				'Content-Type': 'multipart/form-data',
				'Authorization': `Bearer ${this.token}`
			};
			axios.put(`https://antares.pede.id/sg-web-service/v1/company/image`,
			formData,{ headers}).then((response) => {
				if (response.status === 200) {
					if (response.data.status === "Success") {
						this.successMessage = 'Status: ' + response.data.status + '  ||  Messsage: ' + response.data.message + '  ||    data' + response.data.data
						this.successRestore = true;
						setTimeout(() => {this.successRestore = false, this.file = ''}, 5000);
					} else if (response.data.status === false) {
						this.errorMessage = 'Status: ' + response.data.status + '  ||  Messsage: ' + response.data.message + '  ||  data' + response.data.data
						this.errorAlert = true;
						setTimeout(() => {this.errorRestore = false, this.file = ''}, 5000);
					} else {
						this.errorMessage = 'Internal Server Error';
						this.errorRestore = true;
						setTimeout(() => {this.errorRestore = false, this.file = ''}, 5000);
					}
				} else {
					this.errorMessage = 'Internal Server Error';
					this.errorRestore = true;
					setTimeout(() => {this.errorRestore = false, this.file = ''}, 5000);
				}
			}).catch((error) => {
				if (error.response !== undefined) {
					this.success = false;
					// setAlert(this, error.response);
				}
			});
		},
		toggleFullscreen() {
			this.$fullscreen.toggle(document.querySelector('body'), {
				wrap: false,
				callback: () => {this.fullscreen = this.$fullscreen.getState()}
			})
		}
	},
	components: {
		NotificationBox,
		Search
	},
	mounted() {
		console.log("ImagePath: " + getUserDataInSession2('logoPath') )
		if (getUserDataInSession2('logoPath') == '' || getUserDataInSession2('logoPath') == null){
			// this.ImagePath = getUserDataInSession2('logoPath')
			console.log("company logo empty")
		} else {
			this.ImagePath = getUserDataInSession2('logoPath').replace(/\"/gi, '')
			console.log("company logo exist")
		}
		this.fullscreen = this.$fullscreen.getState()
		this.resizePopoverWidth();
		window.addEventListener('resize', this.resizePopoverWidth);
		if (localStorage.getItem('userRole').replace(/\"/gi, '') === 'System Administrator') {
			this.userName = localStorage.getItem('UserName').replace(/\"/gi, '');
			this.userInfo = localStorage.getItem('userRole').replace(/\"/gi, '');
		}
		else {
			// console.log(localStorage.getItem('userCompanyName'))
			this.userName = localStorage.getItem('UserName').replace(/\"/gi, '');
			this.userInfo = localStorage.getItem('userCompanyName').replace(/\"/gi, '');
			this.IsNotSuperUser = true
			this.CompanyName = localStorage.getItem('userCompanyName').replace(/\"/gi, '')
		}
	},
	beforeDestroy() {
		window.removeEventListener('resize', this.resizePopoverWidth);
	}
}
</script>

<style lang="scss" scoped>
@import '../assets/scss/_variables';
@import '../assets/scss/_mixins';


.toolbar {
	width: 100%;
	height: 100%;
	padding: 0 20px;
	box-sizing: border-box;


	.username {
		margin-left: 20px;
		font-size: 20px;
		font-weight: bold;
		@include text-bordered-shadow();

		a {
			color: $text-color;
			text-decoration: none;

			&:hover {
				color: $text-color-accent;
			}
		}
	}
	.username2 {
		margin-left: 20px;
		font-size: 12px;
		font-weight: bold;
		@include text-bordered-shadow();

		a {
			color: $text-color;
			text-decoration: none;

			&:hover {
				color: $text-color-accent;
			}
		}
	}

	.avatar {
		border-radius: 50%;
		width: 35px;
		height: 35px;
		border: 1px solid #FFF;
		margin-left: 20px;
		box-sizing: border-box;
		display: block;
		cursor: pointer;
		box-shadow: 0 2px 5px 0 rgba(49,49,93,.1), 0 1px 2px 0 rgba(0,0,0,.08);
		transition: box-shadow .5s;

		&:hover {
			box-shadow: 0px 3px 10px 0 rgba(49, 49, 93, 0.08), 0px 2px 7px 0 rgba(0, 0, 0, 0.08);
		}
	}

	.notification-icon {
		font-size: 20px;
		outline: none;
		padding: 0;
		background: transparent;
		border: none;
		margin-left: 20px;
		//color: #aab7c5;
		color: transparentize($text-color, 0.7);
		@include text-bordered-shadow();

		&:hover {
			color: $text-color-accent;
		}
	}

	.toggle-sidebar {
		border: 1px solid transparent;
		height: 32px;
		min-height: 32px;
		line-height: 32px;
		width: 32px;
		min-width: 32px;
		max-width: 32px;
		box-sizing: border-box;
		text-align: center;
		margin: 0;
		outline: none;
		margin-right: 5px;
		font-size: 24px;
		padding: 0;
		cursor: pointer;
		display: inline-block;
		color: $text-color;
		background: white;
		display: none;
		opacity: 0;
		transition: all .5s;

		&__right {
			margin-right: 0px;
			margin-left: 5px;
		}

		&:hover, &:focus, &:active {
			color: $text-color-accent;
			border-color: $text-color-accent;
		}
	}

	.fullscreen-button {
		font-size: 24px;
		cursor: pointer;
		outline: none;
		padding: 0;
		background: transparent;
		border: none;
		margin-left: 20px;
		//color: #aab7c5;
		color: transparentize($text-color, 0.7);
		@include text-bordered-shadow();

		&:hover {
			color: $text-color-accent;
		}
	}

	.logo-mini {
		width: 32px;
		height: 32px;
		display: none;
	}

	.box-right {
		.company-logo {
			margin-top: 2px;
			margin-left: 10px;
			// margin-right: 10px;
			// margin-bottom: 10px;
			.logo-mini2 {
				width: 32px;
				height: 32px;
			}
		}
	}


	.el-dropdown {
		.flag-icon {
			box-shadow: 0 2px 5px 0 rgba(49,49,93,.1), 0 1px 2px 0 rgba(0,0,0,.08);
			cursor: pointer;
			border: 1px solid lighten($background-color, 20%);
			background-color: lighten($background-color, 20%);
		}
	}
}

@media (max-width: 650px) {
	.toolbar {
		.username {
			display: none;
		}
	}
}

@media (max-width: 768px) {
	.toolbar {
		padding: 0 10px;

		.toggle-sidebar {
			display: block;
			opacity: 1;
		}

		.fullscreen-button {
			display: none;
		}

		.logo-mini {
			display: inherit;
		}
	}
}
</style>
