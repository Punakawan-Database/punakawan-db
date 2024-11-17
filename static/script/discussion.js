let isProductClicked = false;

$(document).ready(function() {
    $('.dropdown-menu').on('click', '.list-group-item', function() {
        var selectedItem = $(this).find('h5').text();
        var selectedProductId = $(this).data('id');        
        $('#product_id').val(selectedProductId);
        $('.dropdown-toggle').text(selectedItem);
        isProductClicked = true;
    });

    // Event listener untuk membuka modal
    $('#exampleModal').on('show.bs.modal', async function () {
        await showProduct(); // Memanggil fungsi showProduct saat modal dibuka
    });
});

const discussionDataElement = document.getElementById('my-data');
async function getDiscussion() {
    const discussionUrl = discussionDataElement.getAttribute('data-discussion-url');
    const response = await fetch(discussionUrl);
    
    if (!response.ok) {
        console.error('Respons jaringan tidak ok:', response.statusText);
        return []; // Kembalikan array kosong atau tangani kesalahan sesuai kebutuhan
    }
    
    try {
        return await response.json();
    } catch (error) {
        console.error('Kesalahan saat parsing JSON:', error);
        return []; // Tangani kesalahan sesuai kebutuhan
    }
}
async function getProduct() {
    const productUrl = discussionDataElement.getAttribute('data-product');
    return fetch(productUrl).then((res) => res.json())
}

async function refreshDiscussion() {
    document.getElementById("discussion_container").innerHTML = "";
    const allDiscussion = await getDiscussion();

    let htmlString = `<table class="table table-row-spacing">
                        <tr style="height:50px;">
                            <th scope="col" style="width:400px;">Produk</th>
                            <th scope="col" style="width:100px;">Pengguna</th>
                            <th scope="col" style="width:100px;"></th>
                        </tr>
                        <tbody class="table-group-divider">
    `;

    allDiscussion.forEach((item) => {
        let database_url=discussionDataElement.getAttribute('database-url');
        const rowUrl = database_url.replace('9999', item.pk);
        let deleteButton = '';
        if (item.fields.owned_by_current_user) {
            deleteButton = `<button class="btn btn-primary" style="font-size:12px;height: auto; text-align: center; background-color: #90ee90;" onclick="event.stopPropagation(); deleteDiscussion('${item.fields.user}',${item.pk}); return false; ">Delete</button>`;
        }
        console.log(item.fields.owned_by_current_user)
        htmlString += ` <tr class="mb-1 clickable-row " data-id="${item.pk}" data-url="${rowUrl}" style="height:50px;">
                                <td class="overflow-control" style="width:300px;max-width: 285px;">${item.fields.topic}</td>
                                <td class="overflow-control" style="width:300px;max-width: 285px;">${item.fields.product}</td>
                                <td class="overflow-control" style="width:100px;max-width: 100px;">${item.fields.user}</td>
                                <td class="overflow-control" style="width:100px;max-width: 100px;"> 
                                    ${deleteButton}
                                </td>
                        </tr>`
    });
    htmlString +=  `</tbody></table>`
    document.getElementById("discussion_container").innerHTML = htmlString
    document.querySelectorAll('.clickable-row').forEach(row => {
    row.addEventListener('click', () => {
        const url = row.getAttribute('data-url');
        window.location.href = url;
        });
    });
}

function navigateToDiscussion(url) {
    window.location.href = url;
}

refreshDiscussion()

async function showProduct(){
    document.getElementsByClassName("list-group")[0].innerHTML = "";
    const allProduct = await getProduct();

    let stringHTML="";
    allProduct.forEach((item) => {
        stringHTML += `<a href="#" class="list-group-item list-group-item-action" data-id="${item.pk}">
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">${item.fields.name}</h5>
                    </div>
                    <small class="text-body-secondary">${item.fields.restaurant}</small>
                    </a>    `
    });
    document.getElementsByClassName("list-group")[0].innerHTML = stringHTML;
}

function addDiscussion() {
    let formData = new FormData(document.querySelector('#form'));
    let isEmptyFieldDetected = false;
    if(isProductClicked == false){
        alert("Pastikan semua terisi, silakan ulangi");
        return false;
    }
    for (let [key, value] of formData.entries()) {
        if (value.trim() === "") {
            isEmptyFieldDetected = true;
            break;
        }
    }

    if (isEmptyFieldDetected) {
        alert("Pastikan semua terisi, silakan ulangi");
        return false;
    }

    fetch(discussionDataElement.getAttribute('create-comment'), {
        method: "POST",
        body: new FormData(document.querySelector('#form'))
    }).then(refreshDiscussion)

    document.getElementById("form").reset()
    document.getElementById("dropdown-product").innerText = "Pilih Produk"
    return false
}

document.getElementById("button_add").onclick = addDiscussion

function deleteDiscussion(username,commentId) {
    const url = `/delete_comment/${username}/${commentId}`;
        fetch(url, {
            method: "DELETE",
        }).then(response => {
            refreshDiscussion();
        })
        .catch(error => {
            console.error("Error deleting comment:", error);
            alert("Error deleting comment. Please try again later."); // Display an alert with an error message
        });
        return false
    }