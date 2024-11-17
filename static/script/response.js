async function getDiscussion() {
    let formElement = document.getElementById('url-unique-json');
    let url = formElement.getAttribute('data-url');
    return fetch(url).then((res) => res.json())
}

async function refreshResponse() {
    document.getElementById("list-response").innerHTML = "";
    const allDiscussion = await getDiscussion();

    let htmlString =" ";
    allDiscussion.forEach((item) => {
        let deleteButton = '';
        if (item.fields.owned_by_current_user) {
            deleteButton = `<button class="btn btn-primary" style="font-size:12px;height: auto; text-align: center; style="background-color: #273faa;" onclick="deleteResponse('${item.fields.user}', ${item.pk}); return false;">Delete</button>`;
        }
        htmlString += `         
        <br>
        <div class="card">
            <h7 class="card-header d-flex justify-content-between align-items-center" style="height: 30px;">
                ${item.fields.user} pada ${item.fields.date} 
                <div>
                    ${deleteButton}
                </div>
            </h7>
            <div class="card-body">
                <p class="card-text">${item.fields.response}</p>
            </div>
        </div>
        `
    });
    document.getElementById("list-response").innerHTML = htmlString

}

refreshResponse()

function addResponse() {
    let formElement = document.querySelector('#form');
    let url = formElement.getAttribute('data-url');
    fetch(url, {
            method: "POST",
            body: new FormData(document.querySelector('#form'))
        }).then(refreshResponse)

        document.getElementById("form").reset()
        return false
}

document.getElementById("button_add").onclick = addResponse

function deleteResponse(username, commentId) {
    const url = `/delete_comment/${username}/${commentId}`;
        fetch(url, {
            method: "DELETE",
        }).then(response => {
            if (response.status === 201) {
                refreshResponse();
            } else {
                console.error("Failed to delete comment");
                alert("Ini bukan komentar dari akun Anda, Anda tidak bisa menghapusnya :)"); // Display an alert with an error message

            }
        })
        .catch(error => {
            console.error("Error deleting comment:", error);
            alert("Error deleting comment. Please try again later."); // Display an alert with an error message
        });
        return false
    }
