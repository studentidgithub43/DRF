axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

new Vue({
    el: '#registerapp',
    delimiters: ['[[', ']]'],
    data: function (){
        return {
            username: "",
            email: "",
            password: "",
            token: "",
            user: {}
        }    
    },
    methods: {
        registerUser: function(){
            function ValidateEmail(mail) 
            {
                if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))
                {
                    return true
                }
                alert("You have entered an invalid email address!")
                return false
            }
            if(this.username === "" || this.email === "" || this.password === ""){
                alert("Must enter all details");
                return;
            }
            var userMeta = {
                'username': this.username,
                'email': this.email,
                'password': this.password,
                'type': 'free'
            }
            if(ValidateEmail(this.email)){
                axios.post(
                    '/api/register/', userMeta
                ).then(resp => {
                    resp_data = resp.data
                    if(resp_data['status'] === 400){
                        alert("User already found.")
                        return
                    }
                    window.location.href = '/';
                }).catch(error => {
                    console.log(error);
                    alert("Error in creating the account.")
                })
            }else{
                return;
            }
        }
    }
})