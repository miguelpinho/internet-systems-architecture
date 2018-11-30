$("#fenix_login_btn_nav, #fenix_login_btn_header").on("click", ()=>{

    //Get client_id from api:

    let oReq = new XMLHttpRequest(); // New ajax request

    oReq.addEventListener("load", () => {
        let request_url = "https://fenix.tecnico.ulisboa.pt/oauth/userdialog";
        let redirect_url = "";
        let client_id = "";
        try {
            let response = JSON.parse(oReq.responseText);
            client_id = response["client_id"];
            redirect_url = response["redirect_url"]
        }
        catch (e) {
            console.log("Could not handle client_id request response");
            alert("Could not process the login request, please try later");
            return ;
        }


        request_url = request_url + `?client_id=${client_id}&redirect_uri=${redirect_url}`;
        console.log("Redirecting to: "+ request_url);
        location.href = request_url
    });

    oReq.open("GET", "/auth/client_id");
    oReq.setRequestHeader("Content-type", "application/json");
    oReq.send();

});
