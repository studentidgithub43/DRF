axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

new Vue({
    el: '#loginapp',
    delimiters: ['[[', ']]'],
    data: function (){
        return {
            username: "",
            password: ""
        }
    },
    methods: {
        loginUser: function(){
            var user = {
                "username": this.username,
                "password": this.password
            }
            if(this.username === "" || this.password === ""){
                alert("Must enter all details");
                return;
            }
            axios.post(
                '/api/login/', user
                ).then(resp => {
                    resp_data = resp.data;
                    window.localStorage.setItem("token", resp_data['token']);
                    window.location.href = '/';
                }).catch(error => {
                    console.log(error);
                    alert("Error in logging in.");
                });
        }
    },
    mounted: function(){
        let _token = window.localStorage.getItem('token');
    }
});