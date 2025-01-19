var ready = 0;
var runda = 1;
var messageElement = null;
var kropka=0;
var rzuty=3;

document.querySelectorAll('.clickable-image').forEach(img => {
    img.addEventListener('click', function() {
        if (ready == 1) {
            this.classList.toggle('selected');
            
            fetch(`/choose-kostka?item_id=${this.id}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        ;
                    }
                });
        }
    });
});

function loadData() {
    fetch('/get-data')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector("#data-table tbody");
            tableBody.innerHTML = "";
            data.forEach(row => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <th>${row.id}</th>
                    <td class="${row.status}">${row.player1}</td>
                    <td class="${row.status2}">${row.player2}</td>
                `;
                tableBody.appendChild(tr);
            });
            addCellListeners();
        });

    fetch('get-kostki')
        .then(response => response.json())
        .then(data => {
            const tabelka = data;
            tabelka.forEach((value, index) => {
                document.getElementById(`Kosc${index + 1}`).src = `/static/images/kostka${value}.svg`;
            });
        });

    let gracz = runda%2;
    if(gracz==0)gracz=2;
    document.getElementById("nrTury").innerText = "Tura: Gracz " + gracz;
    document.getElementById("nrRzutu").innerText = "Pozostałe rzuty: " + rzuty;
    ready = 1;
}

function koniecgry() {
    fetch('koniec-gry')
        .then(response => response.json())
        .then(data => {
            if (data.wynik == "1") {
                alert("Wygrał gracz 1.");
            } else if (data.wynik == "2") {
                alert("Wygrał gracz 2.");
            } else {
                alert("Remis!");
            }
        });
    loadData();
    ready = 0;
    runda = 1;
}

function addCellListeners() {
    document.querySelectorAll("td").forEach(cell => {
        cell.addEventListener("click", () => {
            if (ready == 1 && cell.className == "gray") {
                const row = cell.parentNode;
                const rowIndex = row.rowIndex;
                fetch(`/choose-item?item_id=${rowIndex}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.querySelectorAll('.clickable-image').forEach(function(img) {
                                img.classList.remove('selected');
                            });
                            deleteMessage();
                            rzuty = 3;
                            loadData();
                            ready = 0;
                            runda = runda + 1;
                            if (runda > 26) {
                                koniecgry();
                            }
                        }
                    });
            }
        });
    });
}

function deleteMessage() {
    if (messageElement) {
        document.body.removeChild(messageElement);
        messageElement = null;
    }
}

function createMessage(message){
    if (!messageElement) {
        messageElement = document.createElement("div");
        messageElement.style.position = "fixed";
        messageElement.style.top = "10%";
        messageElement.style.left = "50%";
        messageElement.style.transform = "translate(-50%, -50%)";
        messageElement.style.backgroundColor = "#f8d7da";
        messageElement.style.color = "#721c24";
        messageElement.style.padding = "10px";
        messageElement.style.border = "2px solid rgb(238, 112, 112)";
        messageElement.style.borderRadius = "5px";
        messageElement.style.boxShadow = "0px 4px 6px rgba(0, 0, 0, 0.1)";
        messageElement.style.zIndex = "1000";
        messageElement.style.width = "200px";

        document.body.appendChild(messageElement);
    }
    messageElement.innerText = message;
}

function startAutoRefresh(interval) {
    setInterval(() => {
        fetch('/check-possible')
            .then(response => response.json())
            .then(data => {
                if(data.wynik=="1") {
                    deleteMessage();
                    rzuty = rzuty - 1;
                    loadData();
                } else if(data.wynik=="2"){
                    ready=0;
                    kropka_text=""
                    kropka = (kropka+1)%8;
                    let liczba_kropek=Math.floor(kropka/2);
                    for(let i=0;i<liczba_kropek;i++)
                    {
                        kropka_text = kropka_text + ".";
                    }
                    createMessage("Losowanie w toku"+kropka_text);
                } else if(data.wynik=="3"){
                    createMessage("Nie masz już ponownych rzutów");
                }

            })
    }, interval);
}

function updateData() {
    fetch('/update-data')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                ;
            }
        });
}

window.onload = function() {
    loadData();
    ready = 0;
    startAutoRefresh(200);
}
