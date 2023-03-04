function deleteUser(userid){
    fetch("/delete-user",{
        method:"POST",
        body:JSON.stringify({userid: userid}),
    }).then((_res) => {
        window.location.href = "/admin.html";
    })
}

function deleteLoan(loanid){
    fetch("/delete-loan",{
        method:"POST",
        body:JSON.stringify({loanid: loanid}),
    }).then((_res) => {
        window.location.href = "/admin.html";
    })
}