function requiredItem() {
    let item = document.getElementsByName("tags[]");
    let atLeastOne = false;

    for (i = 0; i < item.length; i++) {
        if (item[i].checked == true) {
            atLeastOne = true;
            break;
        }
    }

    if (atLeastOne == true) {
        for (i = 0; i < item.length; i++) {
            item[i].required = false;
        }
    } else {
        for (i = 0; i < item.length; i++) {
            item[i].required = true;
        }
    }

}

function correctYear() {
    let year = parseInt(document.getElementById("year").value);
    let regex1 = new RegExp("^[0-9]{4}$");

    if (regex1.test(year) == false) {
        document.getElementById("year").value = 2015;
    }

    if (year < 1995) {
        document.getElementById("year").value = 1995;
    } else if (year > 2022) {
        document.getElementById("year").value = 2022;
    }
}

function correctScore() {
    let score = parseInt(document.getElementById("minScore").value);
    let regex2 = new RegExp("^[0-9]{1,2}$");

    if (regex2.test(score) == false) {
        document.getElementById("minScore").value = 6;
    }

    if (score < 0) {
        document.getElementById("minScore").value = 0;
    } else if (score > 10) {
        document.getElementById("minScore").value = 10;
    }
}

