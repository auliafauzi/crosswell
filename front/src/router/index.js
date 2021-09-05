import Vue from 'vue'
import Router from 'vue-router'

//apps
// import Dashboard from '../views/apps/Dashboard.vue'
// import CryptoDashboard from '../views/apps/CryptoDashboard.vue'
// import EcommerceDashboard from '../views/apps/ecommerce/Dashboard.vue'
// import Calendar from '../views/apps/Calendar.vue'
// import Contacts from '../views/apps/Contacts.vue'
// import Gallery from '../views/apps/Gallery.vue'
// import Cards from '../views/apps/Cards.vue'
// import Mail from '../views/apps/Mail.vue'
// import Timeline from '../views/apps/Timeline.vue'
// import Ecommerce from './ecommerce'

//pages
import Login from '../views/pages/authentication/Login.vue'
import Login2 from '../views/pages/authentication/Login2.vue'
// import Register from '../views/pages/authentication/Register.vue'
// import ForgotPassword from '../views/pages/authentication/ForgotPassword.vue'
// import Profile from '../views/pages/Profile.vue'
import NotFound from '../views/pages/NotFound.vue'
// import Invoice from '../views/pages/Invoice.vue'
// import Company from '../views/pages/CompanyList.vue'
// import UploadBatch from '../views/pages/UploadBatch.vue'
// import UserList from '../views/pages/UserList.vue'
// import WhiteList from '../views/pages/WhiteList.vue'
import Home from '../views/pages/Home.vue'
import Post from '../views/pages/Post.vue'
import Map from '../views/pages/Map.vue'
import UserManagement from '../views/pages/UserManagement.vue'
// import PromoEngine from '../views/pages/PromoEngine.vue'


//ui
// import Themes from '../views/ui/Themes.vue'
// import Icons from '../views/ui/Icons/Icons.vue'
// import MdIcons from '../views/ui/Icons/MdIcons.vue'
// import FlagIcons from '../views/ui/Icons/FlagIcons.vue'
// import MultiLanguage from '../views/ui/MultiLanguage.vue'
// import HelperClasses from '../views/ui/HelperClasses.vue'
// import Typography from '../views/ui/Typography.vue'
import layout from './layout'
// import editors from './editors'
// import charts from './charts'
// import maps from './maps'
// import tables from './tables'
// import element from './element'

import layouts from '../layout'
import store from '../store'
import axios from "axios"
import {getToken} from '../utils';

Vue.use(Router)


const router = new Router({
	// mode: 'history',
	//base: '/sub-path/',
	routes: [
		{
			path: '/',
			redirect:'/home',
			name: 'base',
			component: Home,
			meta: {
				layout: layouts.contenOnly
			}
		},
		{
			path: '/home',
			name: 'home',
			component: Home,
			meta: {
				layout: layouts.navTop,
				searchable: true
			}
		},
		{
			path : '/post/:id',
			name : 'post',
			component: Post,
			meta: {
				layout: layouts.navTop,
				searchable: true
			},
			props: (route) => {
        const id = Number.parseInt(route.params.id);
        return { id }
      },
		},
		{
			path: '/map',
			name: 'map',
			component: Map,
			meta: {
				layout: layouts.navTop,
				searchable: true
			}
		},
		{
			path: '/userManagement',
			name: 'userManagement',
			component: UserManagement,
			meta: {
				layout: layouts.navTop,
				searchable: true
			}
		},

		// {
		// 	path: '/promoEngine',
		// 	name: 'promoEngine',
		// 	component: PromoEngine,
		// 	meta: {
		// 		layout: layouts.navLeft,
		// 		searchable: true
		// 	}
		// },

		// {
		// 	path: '/ecommerce-dashboard',
		// 	name: 'ecommerce-admin-dashboard',
		// 	component: EcommerceDashboard,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		title: 'eCommerce admin dashboard',
		// 		tags: ['app', 'Ecommerce']
		// 	}
		// },
		// {
		// 	path: '/crypto-dashboard',
		// 	alias: '/dashboards',
		// 	name: 'crypto-dashboard',
		// 	component: CryptoDashboard,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		tags: ['app', 'Crypto']
		// 	}
		// },
		//
		// {
		// 	path: '/calendar',
		// 	name: 'calendar',
		// 	component: Calendar,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		tags: ['app']
		// 	}
		// },
		// {
		// 	path: '/contacts',
		// 	name: 'contacts',
		// 	component: Contacts,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		tags: ['users', 'address', 'book', 'app']
		// 	}
		// },
		// {
		// 	path: '/gallery',
		// 	name: 'gallery',
		// 	component: Gallery,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		tags: ['photo', 'app']
		// 	}
		// },
		// {
		// 	path: '/cards',
		// 	name: 'cards',
		// 	component: Cards,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		tags: ['app', 'todo']
		// 	}
		// },
		// {
		// 	path: '/mail',
		// 	name: 'mail',
		// 	component: Mail,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		title: 'Mail',
		// 		tags: ['app', 'email', 'inbox']
		// 	}
		// },
		// Ecommerce,
		// {
		// 	path: '/timeline',
		// 	name: 'timeline',
		// 	component: Timeline,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		tags: ['app']
		// 	}
		// },
		// {
		// 	path: '/themes',
		// 	name: 'themes',
		// 	component: Themes,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		tags: ['ui']
		// 	}
		// },
		// {
		// 	path: '/icons',
		// 	name: 'icons',
		// 	component: Icons,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft
		// 	},
		// 	children: [
		// 		{
		// 			path: 'md-icons',
		// 			name: 'md-icons',
		// 			component: MdIcons,
		// 			meta: {
		// 				auth: true,
		// 				layout: layouts.navLeft,
		// 				searchable: true,
		// 				title: 'Material Design Icons',
		// 				tags: ['material design']
		// 			}
		// 		},
		// 		{
		// 			path: 'flag-icons',
		// 			name: 'flag-icons',
		// 			component: FlagIcons,
		// 			meta: {
		// 				auth: true,
		// 				layout: layouts.navLeft,
		// 				searchable: true,
		// 				title: 'Flag Icons',
		// 				tags: ['list', 'ui']
		// 			}
		// 		}
		// 	]
		// },
		// {
		// 	path: '/multi-language',
		// 	name: 'multi-language',
		// 	component: MultiLanguage,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		tags: ['ui', 'translate']
		// 	}
		// },
		// {
		// 	path: '/helper-classes',
		// 	name: 'helper-classes',
		// 	component: HelperClasses,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		title: 'Helper Classes',
		// 		tags: ['ui']
		// 	}
		// },
		// {
		// 	path: '/typography',
		// 	name: 'typography',
		// 	component: Typography,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		title: 'Typography',
		// 		tags: ['ui']
		// 	}
		// },
		layout,
		// editors,
		// charts,
		// maps,
		// tables,
		// element,
		// {
		// 	path: '/profile',
		// 	name: 'profile',
		// 	component: Profile,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		tags: ['pages']
		// 	}
		// },
		// {
		// 	path: '/invoice',
		// 	name: 'invoice',
		// 	component: Invoice,
		// 	meta: {
		// 		auth: true,
		// 		layout: layouts.navLeft,
		// 		searchable: true,
		// 		tags: ['pages']
		// 	}
		// },
		{
			path: '/login',
			name: 'loginOld',
			component: Login,
			meta: {
				layout: layouts.contenOnly
			}
		},
		// {
		// 	path: '/login2',
		// 	name: 'login2',
		// 	component: Login2,
		// 	meta: {
		// 		layout: layouts.contenOnly
		// 	}
		// },
		// {
		// 	path: '/register',
		// 	name: 'register',
		// 	component: Register,
		// 	meta: {
		// 		layout: layouts.contenOnly
		// 	}
		// },
		// {
		// 	path: '/forgot-password',
		// 	name: 'forgot-password',
		// 	component: ForgotPassword,
		// 	meta: {
		// 		layout: layouts.contenOnly
		// 	}
		// },
		{
			path: '/logout',
			beforeEnter (to, from, next) {
				auth.logout()
				next({path:'/'})
			}
		},
		{
			path: '*',
			name: 'not-found',
			component: NotFound,
			meta: {
				layout: layouts.contenOnly
			}
		}
	]
})


const l = {
	contenOnly(){
		store.commit('setLayout', layouts.contenOnly)
	},
	navLeft(){
		store.commit('setLayout', layouts.navLeft)
	},
	navRight(){
		store.commit('setLayout', layouts.navRight)
	},
	navTop(){
		store.commit('setLayout', layouts.navTop)
	},
	navBottom(){
		store.commit('setLayout', layouts.navBottom)
	},
	set(layout){
		store.commit('setLayout', layout)
	}
}

//insert here login logic
const auth = {
	loggedIn() {
		return store.getters.isLogged
	},
	logout() {
		var headers = {
			'Content-Type': 'application/json',
			'Authorization': 'Bearer ' + getToken()
			// 'Authorization': `Bearer ${this.token}`
			// 'Authorization': getToken()
		}
		axios.delete("https://antares.pede.id//sg-web-service/v1/logout", {headers,
		})
		localStorage.clear();
		store.commit('setLogout')
	}
}

router.beforeEach((to, from, next) => {
	let authrequired = false
	if(to && to.meta && to.meta.auth)
		authrequired = true

	//console.log('authrequired', authrequired, to.name)

	if(authrequired) {
		if(auth.loggedIn()) {
			if(to.name === 'login') {
				window.location.href = '/'
				return false
			} else {
				next()
			}
		} else {
			if(to.name !== 'login'){
				window.location.href = '/'
				return false
			}
			next()
		}
	} else {
		if(auth.loggedIn() && to.name === 'login'){
			window.location.href = '/'
			return false
		} else {
			next()
		}
	}

	if(to && to.meta && to.meta.layout){
		l.set(to.meta.layout)
	}
})

router.afterEach((to, from) => {
	setTimeout(()=>{
		store.commit('setSplashScreen', false)
	}, 500)
})

export default router
