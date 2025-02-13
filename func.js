let btn_gatya_takesyobo = document.querySelector("#gatya_takesyobo");
let btn_gatya_idolone = document.querySelector("#gatya_idolone");
let btn_gatya_takesyobo_idolone = document.querySelector("#gatya_takesyobo_idolone");
let inpfield_min_age = document.querySelector("#min_age");
let inpfield_max_age = document.querySelector("#max_age");

function gatya_func(csv_filename) {

    // 年齢の下限と上限を取得
    let min_age = inpfield_min_age.value;
    let max_age = inpfield_max_age.value;

    if (!min_age) {
        min_age = -100;
    }

    if (!max_age) {
        max_age = 100;
    }

    min_age = parseInt(min_age, 10);
    max_age = parseInt(max_age, 10);

    // CSVファイルを fetch() で読み込み
    let url_array = [];

    fetch(csv_filename)
        .then(response => response.text())
        .then(data => {
            // CSVを行ごとに分割
            const rows = data.split('\n');
            const tableBody = document.querySelector('#csv-table tbody');

            // rows = ["URL1,Name1,Birth1,Release1,Age1", "URL2,Name2,Birth2,Release2,Age2", ...];

            rows.forEach(row => {
                const cols = row.split(',');
                let DVD_url = cols[0];
                let age_at_release = cols[4];

                if (min_age <= age_at_release && age_at_release <= max_age) {
                    url_array.push(DVD_url);
                }
            });

            if (url_array.length > 0) {
                let randomIndex = Math.floor(Math.random() * url_array.length);
                let randomUrl = url_array[randomIndex];
                window.open(randomUrl, "_blank");
            }
        })
        .catch(error => console.error('Error reading CSV:', error));


}

btn_gatya_takesyobo.addEventListener("click", () => gatya_func("output_takesyobo.csv"));
btn_gatya_idolone.addEventListener("click", () => gatya_func("output_idolone.csv"));
btn_gatya_takesyobo_idolone.addEventListener("click", () => gatya_func("output_merge.csv"));

