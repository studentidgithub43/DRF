axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";


new Vue({
    el: '#dashboard',
    delimiters: ['[[', ']]'],
    data: function (){
        return {
            user: ""
        }    
    },
    methods: {
        logoutUser: function(){
            let token = window.localStorage.getItem("token");
            console.log(token);
            axios.defaults.headers.common['Authorization'] = `Token aeaf8cb665320d30746a68202787797d8235e2a16f38de2ba17f43b89ca20ab0`;
            axios.post(
                '/api/logout/'
            ).then(resp => {
                //
            }).catch(error => {
                console.log(error);
            });
        }
    },
    mounted: function(){
        let _token = window.localStorage.getItem("token");
    }
})