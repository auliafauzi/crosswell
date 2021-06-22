<template>
	<div class="page-table column scrollable only-y" :class="{'flex':!isMobile, 'overflow':isMobile}">

		<div class="toolbar-box flex align-center">
			<div class="box grow">
				<el-input placeholder="Search..." prefix-icon="el-icon-search" v-model="search" size="mini" clearable class="card-shadow--medium"></el-input>
			</div>
		</div>

		<resize-observer @notify="handleResize" />

		<div class="table-box card-base card-shadow--medium box grow" id="table-wrapper" v-loading="!ready">

			<el-table :data="listInPage" style="width: 100%" :height="height" v-if="ready" @selection-change="handleSelectionChange">
				<el-table-column type="selection" width="34" fixed></el-table-column>
				<el-table-column label="Name" min-width="250" prop="full_name" :fixed="!isMobile">
					<template slot-scope="scope">
						<span class="sel-string" v-html="$options.filters.selected(scope.row.full_name, search)"></span>
					</template>
				</el-table-column>
				<el-table-column label="Birthday" min-width="100" prop="birth_day">
					<template slot-scope="scope">
						<span class="sel-string" v-html="$options.filters.selected(scope.row.birth_day, search)"></span>
					</template>
				</el-table-column>
				<el-table-column label="Email" prop="email" min-width="300">
					<template slot-scope="scope">
						<span class="sel-string" v-html="$options.filters.selected(scope.row.email, search)"></span>
					</template>
				</el-table-column>
				<el-table-column label="Gender" prop="gender" min-width="250">
					<template slot-scope="scope">
						<span class="sel-string" v-html="$options.filters.selected(scope.row.gender, search)"></span>
					</template>
				</el-table-column>
				<el-table-column label="Job title" prop="job_title" min-width="200">
					<template slot-scope="scope">
						{{ scope.row.job_title }}
					</template>
				</el-table-column>
				<el-table-column label="Company" prop="company" min-width="100"></el-table-column>
				<el-table-column label="City" prop="city" min-width="200"></el-table-column>
				<el-table-column label="Country" prop="country" min-width="150"></el-table-column>
				<el-table-column label="Address" prop="street_address" min-width="200"></el-table-column>
				<el-table-column label="Phone" prop="phone" min-width="150"></el-table-column>
				<el-table-column label="Username" prop="username" min-width="100"></el-table-column>
			</el-table>

			<el-pagination 
				v-if="ready"
				:small="pagination.small"
				:current-page.sync="pagination.page"
				:page-sizes="pagination.sizes"
				:page-size.sync="pagination.size"
				:layout="pagination.layout"
				:total="total"
			></el-pagination>
        </div>

	</div>
</template>

<script>
import users from '@/assets/data/USERS_MOCK_DATA.json'
import _ from 'lodash'
import moment from "moment-timezone"

export default {
	name: 'StyledTablePage',
	data () {
      	return {
			isMobile: false,
			ready: false,
			width: 0,
			height: 'auto',
			loading: false,
			search: '',
			pagination: {
				page: 1,
				size: 20,
				sizes: [10, 15, 20, 30, 50, 100],
				layout: 'total, ->, prev, pager, next, jumper, sizes',
				small: false
			},
			list: users,
			editMode: false,
			itemsChecked: [],
			dialogUserVisible: false,
			currentId: 0,
			moment
		}
	},
	computed: {
		listFiltered() {
			return this.list.filter((obj) => {
				let ctrl = false
				for(let k in obj) {
					if(obj[k] && obj[k].toString().toLowerCase().indexOf(this.search.toLowerCase()) !== -1) ctrl = true
				}
				return ctrl
			})
		},
		listSortered() {
			let prop = this.sortingProp
			let order = this.sortingOrder
			return [].concat(this.listFiltered.sort((item1, item2) => {
				let val1 = '';
				let val2 = '';

				val1 = item1[prop];
				val2 = item2[prop]
				if (order === 'descending') {
					return val2 < val1 ? -1 : 1
				}
				return val1 < val2 ? -1 : 1
			}))
		},
		listInPage() {
			let from = (this.currentPage - 1) * this.itemPerPage
			let to = from + (this.itemPerPage*1)
			//return this.listSortered.slice(from, to)
			return this.listFiltered.slice(from, to)
		},
		total() {
			return this.listFiltered.length
		},
		currentPage: {
			get() {
				return this.pagination.page
			},
			set(val) {
				this.pagination.page = val
			}
		},
		itemPerPage() {
			return this.pagination.size
		},
		selectedItems() {
			return this.itemsChecked.length || 0
		},
	},
	watch: {
		itemPerPage(val) {
			this.ready = false
			this.currentPage = 1

			setTimeout(() => {
				this.ready = true
			}, 500);
		},
		search(val) {
			this.currentPage = 1
		}
	},
    methods: {
		calcDims() {
			const tableWrapper = document.getElementById('table-wrapper')
			if (tableWrapper)
				this.width = tableWrapper.clientWidth

			if(!this.isMobile && tableWrapper) {
				this.height = tableWrapper.clientHeight - 44
			}

			if (this.width < 480) {
				this.pagination.small = true
				this.pagination.layout = 'prev, pager, next'
			} else if (this.width >= 480 && this.width < 700) {
				this.pagination.small = false
				this.pagination.layout = 'prev, pager, next, ->, sizes'
			} else {
				this.pagination.small = false
				this.pagination.layout = 'total, ->, prev, pager, next, jumper, sizes'
			}

			this.ready = true
		},
		handleResize: _.throttle(function (e) {
			this.ready = false
			this.width = 0
			setTimeout(this.calcDims, 1000)
		}, 500),
		handleSelectionChange(val) {
			this.itemsChecked = val;
		},
		init() {	
			if(window.innerWidth <= 768) 
				this.isMobile = true	
		}
	},
	filters: {
		selected: function (value, sel) {
			if (!value) return ''
			if (!sel) return value

			value = value.toString()
			sel = sel.toString()

			const startIndex = value.toLowerCase().indexOf(sel.toLowerCase());
			if (startIndex !== -1) {
				const endLength = sel.length;
				const matchingString = value.substr(startIndex, endLength);
				return value.replace(matchingString, `<span class="sel">${matchingString}</span>`);
			}
			//return value.toString().replace(new RegExp(sel,"gim"), `<span class="sel">${sel}</span>`)
			return value
		}
	},
	created() {
		this.init()
	},
	mounted() {
		//ie fix
		if(!window.Number.parseInt) window.Number.parseInt = parseInt
		
		this.calcDims()
	}
}
</script>

<style lang="scss" scoped>
@import '../../../assets/scss/_variables';

.page-table {
	&.overflow {
		overflow: auto;
	}
	
	.toolbar-box {
		&.hidden {
			visibility: hidden;
		}
	}

	.table-box {
		overflow: hidden;

		&.hidden {
			visibility: hidden;
		}
	}
}
</style>

<style lang="scss">
@import '../../../assets/scss/_variables';

.page-table {

	.toolbar-box {
		margin-bottom: 10px;

		.card-shadow--medium {
			&.el-input, &.el-select {
				border-radius: 4px;

				input {
					border-color: transparent;

					&:hover {
						border-color: #C0C4CC;
					}
					&:focus {
						border-color: $text-color-accent;
					}
				}
			}

			&.el-button {
				border-color: transparent;
			}
		}
	}

	.clickable {
		cursor: pointer;
		text-decoration: underline;
		font-weight: bold;
	}

	.sel-string {
		.sel {
			background: transparentize($text-color, 0.8);
			border-radius: 5px;
			//text-transform: uppercase;
		}
	}

	.el-table th.is-leaf, .el-table td {
		border-bottom: 1px solid rgba(235, 238, 245, 0.3);
	}
	.el-table th {
		background-color: lighten(darken($background-color, 1%), 2%); 
	}
	.el-table-column--selection .cell {
		padding-left: 10px;
		padding-right: 10px;
	}

	.el-pagination {
		padding: 8px;

		.el-pagination__sizes {
			margin: 0;

			.el-input {
				margin-right: 0;
			}
		}
	}

}

@media (max-width: 768px) {
	.page-table {
		.toolbar-box {
			display: block;
			overflow: hidden;
			font-size: 80%;
			padding-bottom: 10px;
		
			& > * {
				display: inline-block;
				min-width: 120px;
				height: 22px;
				//background: rgba(0, 0, 0, 0.04);
				margin-bottom: 16px;
			}
		}
	}
}
</style>


