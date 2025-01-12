var ready = 0;
var runda = 1;

document.querySelectorAll('.clickable-image').forEach(img => {
    img.addEventListener('click', function() {
        if (ready == 1) {
            this.classList.toggle('selected');
            
            fetch(`/choose-kostka?item_id=${this.id}`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Dodatkowe operacje po kliknięciu (jeśli potrzebne)
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

function startAutoRefresh(interval) {
    setInterval(() => {
        loadData();
    }, interval);
}

function updateData() {
    fetch('/update-data')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadData();
            }
        });
}

window.onload = function() {
    loadData();
    ready = 0;
}