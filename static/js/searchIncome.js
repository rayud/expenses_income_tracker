const searchField = document.querySelector("#searchField");

const tableOuput = document.querySelector('.table-output');

const appTable = document.querySelector('.app-table');

const paginationContainer = document.querySelector(".pagination-container");

const tableBody = document.querySelector(".table-body");

const noResult = document.querySelector(".no-result");
console.log(noResult);

tableOuput.getElementsByClassName.display = "none";

searchField.addEventListener('keyup', (e)=>{
    const searchValue = e.target.value;
    if (searchValue.trim().length > 0) {
        fetch("/income/search-incomes/", {
            method: "POST", 
            body: JSON.stringify({ searchText: searchValue}),
        }) 
        .then((res) => res.json())
        .then((data) => {
            tableBody.innerHTML = "";
            appTable.style.display = "none";

            console.log(data)
            if (data.length == 0) {
                paginationContainer.style.display="none";
                noResult.style.display = "block";
                noResult.innerHTML = "No Results Found";
                tableOuput.style.display = "none"
            } else {
                paginationContainer.style.display="none";
                noResult.style.display = "none";
                tableOuput.style.display = "block"
                data.forEach((item) => {
                    let lin = `/income/edit-income/${item.id}`;
                    console.log(lin);

                    let tr = document.createElement("tr");

                    let td1 = document.createElement("td");
                    td1.textContent = item.amount;
                    tr.appendChild(td1);

                    let td2 = document.createElement("td");
                    td2.textContent = item.source;
                    tr.appendChild(td2);

                    let td3 = document.createElement("td");
                    td3.textContent = item.description;
                    tr.appendChild(td3);

                    let td4 = document.createElement("td");
                    td4.textContent = item.date;
                    tr.appendChild(td4);

                    let td5 = document.createElement("td");
                    let link = document.createElement("a");
                    link.href = lin;
                    link.textContent = "Edit";
                    link.className = "btn btn-secondary btn-sm";
                    td5.appendChild(link);
                    tr.appendChild(td5);

                    tableBody.appendChild(tr);

                });
            }
        });
    } else {
        
        appTable.style.display ="block";
        tableOuput.style.display="none";
        noResult.style.display = "none"
        paginationContainer.style.display="block";
    }
})