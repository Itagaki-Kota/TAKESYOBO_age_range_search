// CSVファイルを fetch() で読み込み
fetch("http://localhost:8000/output2.csv")
    .then(response => response.text())
    .then(data => {
        // CSVを行ごとに分割
        const rows = data.split('\n');
        const tableBody = document.querySelector('#csv-table tbody');

        // rows = ["URL1,Name1,Birth1,Release1,Age1", "URL2,Name2,Birth2,Release2,Age2", ...];

        rows.forEach(row => {
            const cols = row.split(',');
            let age_at_release = cols[4];

            if (age_at_release >= 25) {
                const tr = document.createElement('tr');

                cols.forEach(col => {
                    const td = document.createElement('td');
                    td.textContent = col;
                    tr.appendChild(td);
                });

                tableBody.appendChild(tr);
            }
        
        });
    })
    .catch(error => console.error('Error reading CSV:', error));
