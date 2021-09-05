<template>
  <div style="overflow: scroll;">
  <div class="animated fadeIn">

  <!-- <b-card> -->
    <!-- <div class="justify-content-center row my-1"> -->
    <template v-if="errorAlert">
      <b-row>
        <b-col sm="12">
          <b-alert show variant="danger">{{errorMessage}}</b-alert>
        </b-col>
      </b-row>
    </template>
    <template v-if="SuccessAlert">
      <b-row>
        <b-col sm="12">
          <b-alert show variant="success">{{successMessage}}</b-alert>
        </b-col>
      </b-row>
    </template>

    <div class = "text-left">
      <div>
      <b-table
        class="my-table"
        head-row-variant="transparent"
        :sticky-header="this.DynamicHeight"
        variant="success"
        show-empty
        responsive="sm"
        :items="dataUser"
        :fields="fields"
        @row-clicked="companyDetailModal" >

        <template v-slot:cell(actions)="row">
          <!-- {{row.item.resignDate.substring(0,10)}} -->
          <b-button variant="outline-primary" size="sm" @click="changeStatusModal(row.item)" class="mr-1">
            Change Status
          </b-button>
          <b-button variant="outline-danger" size="sm" @click="deleteUserConfirm(row.item.user_id)" class="mr-1">
            Delete
          </b-button>
        </template>

      </b-table>


       <b-pagination
       v-model="currentPage"
       :total-rows="rows()"
       :per-page="perPage"
       limit=6
       aria-controls="my-table"
       size="sm"
       @change="loadPage"
       ></b-pagination>

      </div>

             <b-modal id="deleteModal"
                     v-model="deleteModal"
                     ok-title="Ok" @ok="deleteUser()">
                     Do you really want to delete this User from List ?
             </b-modal>


             <b-modal id="changeStatusModal"
                     v-model="changeStatusToggle"
                     @hide="resetModal"
                     ok-title="Ok" @ok="changeStatus">
                     <div>
                       <p> User : {{this.userNameToEdit}}</p>
                       <p> Current Status : {{this.currentStatus}} </p>
                       <b-form-select v-model="selectedStatus" :options="options" size="sm"></b-form-select>
                     </div>
                     <!-- <label>
                       <input type="file" id="file" accept=".png,.jpg,.jpeg" ref="file" v-on:change="handleFileUpload()"/>
                     </label> -->
                     <template v-if="errorAlertinChangeStatus">
                       <b-row>
                         <b-col sm="12">
                           <b-alert show variant="danger">{{errorMessage}}</b-alert>
                         </b-col>
                       </b-row>
                     </template>
             </b-modal>

    </div>

</div>
</div>
</template>

<script>
import axios from "axios";
import {getToken, getUserDataInSession2, BASE_URL} from '../../utils';
export default {
  data: () => ({
    dataUser: [],
    DataDetail: {},
    fields :[
      { key: 'user_id', label: 'User ID' },
      { key: 'user_name', label: 'User Name' },
      { key: 'role_description', label: 'Role' },
      { key: 'date_created', label: 'Date Created' },
      { key: 'email', label: 'Email' },
      { key: 'status', label: 'Status' },
      { key: 'actions', label: 'Actions' }
    ],
    options :[
      {text:'active', value:'active'},
      {text:'banned', value:'banned'}
    ],
    deleteModal : false,
    addModalToggle : false,
    editModalToogle : false,
    DetailToggle: false,
    changeStatusToggle: false,
    SuccessAlert: false,
    successMessage : '',
    userNameToEdit : '',
    currentStatus : '',
    selectedUserId : '',
    selectedStatus : '',
    userIdToDelete : '',
    currentDate : new Date(),
    errorAlert: false,
    errorAlertinDetail: false,
    errorAlertinEdit: false,
    errorAlertinAdd: false,
    errorAlertinChangeStatus : false,
    errorMessage: '',
    perPage : 10,
    currentPage : 1,
    TotalData : 0,
    DynamicHeight : '',
    HomeLocation : '/home'
  }),
  mounted() {
    try {
 		 this.user_id = String(getUserDataInSession2('UserId').replace(/\"/gi, ''))
 		 this.user_role = getUserDataInSession2('UserRole').replace(/[.",\/#!$%\^&\*;:{}=\-_`~()]/g,"")
 		 this.token = getUserDataInSession2('token').replace(/[.",\/#!$%\^&\*;:{}=\-_`~()]/g,"")
   	 } catch(err) {
   		 console.log("err: ", err)
   	 }
    this.getData()
    this.dynamicHeight()
  },
  created() {
  window.addEventListener("resize", this.myEventHandler);
  },
  destroyed() {
    window.removeEventListener("resize", this.myEventHandler);
  },
  methods: {
    datefunc() {
      this.currentDate = new Date();
    },
    myEventHandler(e) {
    // your code for handling resize...
    this.dynamicHeight()
    },
    dynamicHeight(){
      var TableHeight = window.innerHeight - 230
      this.DynamicHeight =  TableHeight.toString().concat("px")
    },

    getData() {
      var headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      }
      axios.get(`${BASE_URL}/api/v1/userList`,{
            headers
            },
          // }
        ).then(response => {
          if (response.status === 200) {
            if (response.data.code === 400) {
              this.errorAlert = true;
              this.errorMessage = response.data.message;
              setTimeout(() => {this.errorMessage= '',console.log(response.data.message),window.location.href = this.HomeLocation}, 2000);
            } else {
                this.dataUser = response.data.data;
                this.TotalData = Number(response.data.data.total)
            }
          }
        })
    },
    resetModal(){
      this.companyName = ''
      this.companyToAdd = ''
      this.companyNewName = ''
    },
    changeStatusModal(data){
      console.log("data : " + data.user_name)
      this.userNameToEdit = data.user_name;
      this.currentStatus = data.status;
      this.selectedUserId = data.user_id;
      this.changeStatusToggle = true
    },
    changeStatus(){
      if(this.selectedStatus === '') {
        this.errorMessage = "Please Fill the Status";
        this.errorAlertinEdit = true;
        this.changeStatusToggle = true;
      } else {
        var headers = {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`
        };
        axios.put(`${BASE_URL}/api/v1/changeUserStatus`,{
          user_id: String(this.selectedUserId),
          status: this.selectedStatus
        }, {headers}).then(response => {
          if (response.status === 200) {
            if (response.data.code !== 400 && response.data.code !== 200) {
              this.changeStatusToggle = true;
              this.errorMessage = response.data.message;
              this.errorAlertinChangeStatus = true ;
              setTimeout(() => {this.errorAlertinChangeStatus = false, this.errorMessage = '' }, 5000);
            } else if (response.status === 200 && response.data.code === 400) {
              this.changeStatusToggle = true;
              this.errorMessage = response.data.message;
              this.errorAlertinChangeStatus = true ;
              setTimeout(() => {this.AlertMassage = '', console.log(response.data.message),window.location.href = this.HomeLocation}, 2000);
            }
            else {
              this.logdata = response.data;
              this.changeStatusToggle = false
              this.successMessage = response.data.status
              this.SuccessAlert = true
              this.getData()
              setTimeout(() => {this.successMessage = '', this.SuccessAlert = false}, 3000);
            }
          }
          this.resetModal()
        }).catch((error) => {
          if (error.response !== undefined) {
            this.DetailToggle = false
            this.errorMessage = error.response
            this.errorAlertinChangeStatus = true;
            setTimeout(() => {this.errorAlertinChangeStatus = false, this.errorMessage = ''}, 3000);
          } else {
            this.DetailToggle = false
            this.errorMessage = error.response
            this.errorAlertinChangeStatus = true;
            setTimeout(() => {this.errorAlertinChangeStatus = false, this.errorMessage = ''}, 3000);
          }
          this.resetModal()
        });
      }
    },
    deleteUserConfirm(id){
      this.userIdToDelete = id;
      this.deleteModal = true
    },
    deleteUser(){
			// this.token = getUserDataInSession2('token').replace(/[.",\/#!$%\^&\*;:{}=\-_`~()]/g,"")
			var headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      };
			// console.log("going delete post; token: " , this.token)
			axios.delete(`${BASE_URL}/api/v1/deleteUser/${this.userIdToDelete}`, {headers}
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
    resetLogfoModal() {
        this.logModal.title = ''
        this.logModal.content = ''
        this.logdata = ''
      },
    rows() {
      return Number(this.TotalData)
     },
     loadPage(pageNum) {
       // this.getTrades(pageNum);
       this.currentPage = pageNum;
       this.getData()
     }

  }
};
</script>

<style scoped>
.my-table {
  position: sticky;
  cursor: pointer;
  font-size:  14px;
}
.red_color {
  color: red;
}
/deep/ .my-table th {
  position: sticky;
  /* background-color: #f4f7ff; */

  background-color: #007bff;
  color: white;
  font-size:  16px;
  font-weight: 500;
}

</style>
