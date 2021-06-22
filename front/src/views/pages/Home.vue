<template>
	<div class="page-layout-sidebar-right scrollable only-y">
    <b-button variant="outline-primary" size="sm" class="mr-1" style= "margin-bottom: 10px">
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
					<h1 class="mt-8">{{i.title}}</h1>
					<p class="mt-0">
						{{i.content}}
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
       v-model="postModalToggle"
       ok-title="Ok">

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
      contentList : [],
      postModalToggle : false,
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
                // this.dataCompany = response.data.data.user;
                // this.TotalData = Number(response.data.data.total)
                // console.log(this.contentList)
                // console.log(this.contentList[0].title)
            }
          }
        })
    },
    goTo(content_id) {
      // this.postModalToggle = true
      console.log(content_id)
      this.$router.push({name: 'post', params: { id: content_id } })
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
