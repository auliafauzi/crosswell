<template>
	<div class="page-gmaps scrollable">


		<div class="card-base card-shadow--medium">
			<h2 class="ph-20"></h2>
			<gmap-map ref="map" @click="clicked"
				:center="{lat:40.720917, lng:-74.001308}"
				:zoom="2"
				:options="{gestureHandling:'cooperative'}"
				map-type-id="satellite"
				style="width: 100%; height: 600px"
			>
				<div v-for="i in markerByContent ">
					<GmapMarker :position="{lat:i.lat, lng:i.lng}" :label="i.label" />
				</div>


			</gmap-map>
		</div>


		<h4><a href="https://github.com/xkjyeah/vue-google-maps" target="_blank"><i class="mdi mdi-link-variant"></i> reference</a></h4>

	</div>
</template>

<script>
import * as VueGoogleMaps from 'vue2-google-maps'
import axios from "axios";
import {getToken, getUserDataInSession2, BASE_URL, checkUser} from '../../utils';

export default {
	name: 'GMapsPage',
	data () {
		return {
			contentList: [],
			token : '',
			start: null,
			end: null,
			lastId: 1,
			center: {
				lat: 48.8538302,
				lng: 2.2982161
			},
			reportedCenter: {
				lat: 48.8538302,
				lng: 2.2982161
			},
			mapBounds: {},
			clustering: true,
			zoom: 7,
			gridSize: 50,
			mapType: 'terrain',
			markers: [],
			markersEven: false,
			drag: 0,
			mapClickedCount: 0,
			ifw: true,
			ifw2: false,
			ifw2text: 'You can also use the content prop to set your modal',
			mapStyle: 'green',
			circleBounds: {},
			displayCircle: false,
			displayRectangle: false,
			rectangleBounds: {
				north: 33.685,
				south: 50.671,
				east: -70.234,
				west: -116.251
			},
			originalPlPath: [
				{ lat: 37.772, lng: -122.214 },
				{ lat: 21.291, lng: -157.821 },
				{ lat: -18.142, lng: 178.431 },
				{ lat: -27.467, lng: 153.027 }
			],
			plPath: [
				{ lat: 37.772, lng: -122.214 },
				{ lat: 21.291, lng: -157.821 },
				{ lat: -18.142, lng: 178.431 },
				{ lat: -27.467, lng: 153.027 }
			],
			cobaMarker: [
				{ lng: 107.6, lat: 6.89},
				{ lat: 35.360, lng: 138.727}
			],
			markerByContent : [],
			pleditable: true,
			plvisible: false,
			pgvisible: false,
			pgPath: [
				[
					{ lat: 38.872886, lng: -77.054720 },
					{ lat: 38.872602, lng: -77.058046 },
					{ lat: 38.870080, lng: -77.058604 },
					{ lat: 38.868894, lng: -77.055664 },
					{ lat: 38.870598, lng: -77.053346 }
				],
				[
					{ lat: 38.871684, lng: -77.056780 },
					{ lat: 38.871867, lng: -77.055449 },
					{ lat: 38.870915, lng: -77.054891 },
					{ lat: 38.870113, lng: -77.055836 },
					{ lat: 38.870581, lng: -77.057037 }
				]
			],
			opgPath: [
				[
					{ lat: 38.872886, lng: -77.054720 },
					{ lat: 38.872602, lng: -77.058046 },
					{ lat: 38.870080, lng: -77.058604 },
					{ lat: 38.868894, lng: -77.055664 },
					{ lat: 38.870598, lng: -77.053346 }
				],
				[
					{ lat: 38.871684, lng: -77.056780 },
					{ lat: 38.871867, lng: -77.055449 },
					{ lat: 38.870915, lng: -77.054891 },
					{ lat: 38.870113, lng: -77.055836 },
					{ lat: 38.870581, lng: -77.057037 }
				]
			],
			scrollwheel: true
		}
	},
	mounted() {
		checkUser()
		this.token = getUserDataInSession2('token')
		if (this.token != '') {
				this.token = getToken().replace(/[.",\/#!$%\^&\*;:{}=\-_`~()]/g,"");
		}
		this.user_role = getUserDataInSession2('UserRole')
		this.getData()
		console.log('user_role: ' + this.user_role)
		console.log('user_token: ' + this.token)
  },
	computed: {
		// curvedPath () {
		// 	if (this.start && this.end) {
		// 		return _.range(100).map(i => {
		// 			const tick = i / 99
		//
		// 			/* Bezier curve -- set up the control points */
		// 			const dlat = this.end.latLng.lat() - this.start.latLng.lat()
		// 			const dlng = this.end.latLng.lng() - this.start.latLng.lng()
		//
		// 			const cp1 = {
		// 				lat: this.start.latLng.lat() + 0.33 * dlat + 0.33 * dlng,
		// 				lng: this.start.latLng.lng() - 0.33 * dlat + 0.33 * dlng,
		// 			}
		//
		// 			const cp2 = {
		// 				lat: this.end.latLng.lat() - 0.33 * dlat + 0.33 * dlng,
		// 				lng: this.end.latLng.lng() - 0.33 * dlat - 0.33 * dlng,
		// 			}
		//
		// 			/* Bezier curve formula */
		// 			return {
		// 				lat:
		// 					(tick * tick * tick) * this.start.latLng.lat() +
		// 					3 * ((1 - tick) * tick * tick) * cp1.lat +
		// 					3 * ((1 - tick) * (1 - tick) * tick) * cp2.lat +
		// 					((1 - tick) * (1 - tick) * (1 - tick)) * this.end.latLng.lat(),
		// 				lng:
		// 					(tick * tick * tick) * this.start.latLng.lng() +
		// 					3 * ((1 - tick) * tick * tick) * cp1.lng +
		// 					3 * ((1 - tick) * (1 - tick) * tick) * cp2.lng +
		// 					((1 - tick) * (1 - tick) * (1 - tick)) * this.end.latLng.lng(),
		// 			}
		// 		})
		// 	}
		// },
		activeMarkers() {
			if (this.markersEven) {
				return this.markers.filter(
					(v, k) => k % 2 == 0
				)
			} else {
				return this.markers
			}
		},
		// mapStyles() {
		// 	switch (this.mapStyle) {
		// 		case 'normal':
		// 			return []
		// 		case 'red':
		// 			return [
		// 				{
		// 					stylers: [
		// 						{ hue: '#890000' },
		// 						{ visibility: 'simplified' },
		// 						{ gamma: 0.5 },
		// 						{ weight: 0.5 }
		// 					]
		// 				},
		// 				{
		// 					elementType: 'labels',
		// 					stylers: [ { visibility: 'off' } ]
		// 				},
		// 				{
		// 					featureType: 'water',
		// 					stylers: [ { color: '#890000' } ]
		// 				}
		// 			];
		// 		default:
		// 			return [
		// 				{
		// 					stylers: [{ hue: '#899999' }, { visibility: 'on' }, { gamma: 0.5 }, { weight: 0.5 }]
		// 				},
		// 				{
		// 					featureType: 'road',
		// 					stylers: [{ visibility: 'off' }]
		// 				},
		// 				{
		// 					featureType: 'transit.line',
		// 					stylers: [{ color: '#FF0000' }]
		// 				},
		// 				{
		// 					featureType: 'poi',
		// 					elementType: 'labels.icon',
		// 					stylers: [{ visibility: 'on' }, { weight: 10 }]
		// 				},
		// 				{
		// 					featureType: 'water',
		// 					stylers: [{ color: '#8900FF' }, { weight: 9999900000 }, ]
		// 				}
		// 			];
		// 	}
		// }
	},
	methods: {
		getData() {
			console.log(this.token)
			if (this.user_role == 0){
				this.token = '0'
				console.log("HEREEE")
			}
      var headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      }
      // axios.get(`${BASE_URL}/companies?page=${this.currentPage}&size=${this.perPage}`,{
      axios.get(`${BASE_URL}/api/v1/contentList`,{
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
							console.log("contentList_length: ", this.contentList.length)
							console.log("contentList: ", this.contentList)
							for (var i = 0; i < this.contentList.length; i++) {

								// const contentObject = {
								// 	"lng": Number(response.data.message[i].long),
								// 	"lat": Number(response.data.message[i].lat)
								// }
								// this.markerByContent.push(contentObject)

								if (this.contentList[i].long != "" && this.contentList[i].lat != "") {
									if (this.contentList[i].long != null && this.contentList[i].lat != null){
										console.log("ada nih")
										const contentObject = {
											"lng": Number(response.data.message[i].long),
											"lat": Number(response.data.message[i].lat)
										}
										this.markerByContent.push(contentObject)
									}
								}

								// this.markerByContent.push(response.data.message[i].long)
								// this.markerByContent.push(response.data.message[i].lat)
							}

							// this.contentList.forEach(
							// 	this.markerByContent.push(this.contentList.long),
							// 		this.markerByContent.push(this.contentList.lat)
							// )
							console.log("marker: ", this.markerByContent)

            }
          }
        })
    },
		clicked (e) {
			if (!this.start && !this.end) {
				this.start = {
					latLng: e.latLng
				}
			} else if (this.start && !this.end) {
				this.end = {
					latLng: e.latLng
				}
			} else {
				this.start = {
					latLng: e.latLng
				}
				this.end = null
			}
		},
		// mapClicked(mouseArgs) {
		// 	console.log('map clicked', mouseArgs); // eslint-disable-line no-console
		// },
		// mapRclicked(mouseArgs) {
		// 	const createdMarker = this.addMarker()
		// 	createdMarker.position.lat = mouseArgs.latLng.lat()
		// 	createdMarker.position.lng = mouseArgs.latLng.lng()
		// },
		addMarker: function addMarker() {
			this.lastId++;
			this.markers.push({
				id: this.lastId,
				position: { lat: 48.8538302, lng: 2.2982161 },
				opacity: 1,
				draggable: true,
				enabled: true,
				clicked: 0,
				rightClicked: 0,
				dragended: 0,
				ifw: true,
				ifw2text: 'This text is bad please change me :( '
			})
			return this.markers[this.markers.length - 1]
		},
		// resetPlPath() {
		// 	this.plPath = this.originalPlPath;
		// },
		update(field, event) {
			if (field === 'reportedCenter') {
				// N.B. It is dangerous to update this.center
				// Because the center reported by Google Maps is not exactly
				// the same as the center you pass it.
				// Instead we update this.center only when the input field is changed.
				this.reportedCenter = { lat: event.lat(), lng: event.lng() }
				// If you wish to test the problem out for yourself, uncomment the following
				// and see how your browser begins to hang:
				// this.center = _.clone(this.reportedCenter)
			} else if (field === 'bounds') {
				this.mapBounds = event
			} else {
				this.$set(this, field, event)
			}
		},
		// updateChild(object, field, event) {
		// 	if (field === 'position') {
		// 		object.position = { lat: event.lat(), lng: event.lng() }
		// 	}
		// },
		// updatePolygonPaths(paths) { //eslint-disable-line no-unused-vars
		// 	console.log('updatePolygonPaths', paths)
		// },
		// updatePolylinePath(paths) { //eslint-disable-line no-unused-vars
		// 	console.log('updatePolylinePath', paths)
		// },
		// updateCircle(prop, value) {
		// 	if (prop === 'radius') {
		// 		this.radius = value
		// 	} else if (prop === 'bounds') {
		// 		this.circleBounds = value
		// 	}
		// },
		// updateRectangle(prop, value) {
		// 	if (prop === 'bounds') {
		// 		this.rectangleBounds = value
		// 	}
		// },
		// updatePlace(place) {
		// 	if (place && place.geometry && place.geometry.location) {
		// 		var marker = this.addMarker()
		// 		marker.position.lat = place.geometry.location.lat()
		// 		marker.position.lng = place.geometry.location.lng()
		// 	}
		// }
	},
	components: {
		'ground-overlay': {
			render() {
				return '';
			},
			mixins: [VueGoogleMaps.MapElementMixin],
			props: ['source', 'bounds', 'opacity'],
			deferredReady: function() {
				this.$overlay = new google.maps.GroundOverlay(
					this.source,
					this.bounds
				)
				this.$overlay.setOpacity(this.opacity)
				this.$overlay.setMap(this.$map)
			},
			destroyed: function() {
				if(this.$overlay) this.$overlay.setMap(null)
			}
		}
	}

}
</script>

<style lang="scss" scoped>
@import '../../assets/scss/_variables';

.page-gmaps {
	.map-app {
		max-height: 500px;

		.settings-panel {
			box-sizing: border-box;
			max-width: 400px;

			ul, li, select, button {
				font-size: 10px;
			}

			h3 {
				margin-bottom: 0px;
			}
			ul {
				margin-top: 15px;
			}
			[type="checkbox"] {
				position: relative;
				top: 2px;
			}
			li {
				margin-bottom: 2px;
			}
			pre {
				max-height: 200px;
				overflow: auto;
			}

			.marker-box {
				background: $background-color;
				padding: 10px;
				box-sizing: border-box;
				list-style: none;

				li, select, button {
					font-size: 14px;
				}
			}
		}
	}
}


@media (max-width: 768px) {
	.page-gmaps {
		.map-app {
			max-height: inherit !important;
			display: block;

			.settings-panel, .map-panel {
				display: block;
				overflow: hidden;
				width: 100%;
				max-width: 100%;
				height: 400px;
			}
			.settings-panel {
				overflow: auto;
			}
		}
	}
}
</style>
<style lang="scss">
.page-gmaps {
	.map-app {

		.settings-panel {

			[type="text"] {
				background-color: rgba(255, 255, 255, 0.2);
				border: 1px solid rgba(255, 255, 255, 0.3);
			}
		}
	}
}
.gm-style .gm-style-iw {
	color: black;
}
</style>
