// =========================================
// PACKSURE JAVASCRIPT
// =========================================


// =========================================
// INSPECTION FILTERING
// =========================================

const searchInput =
    document.getElementById("inspectionSearch");

const statusFilter =
    document.getElementById("statusFilter");

const dateFilter =
    document.getElementById("dateFilter");


// =========================================
// FILTER FUNCTION
// =========================================

function filterInspections() {

    // Get current search text
    const searchValue =
        searchInput
            ? searchInput.value.toLowerCase().trim()
            : "";


    // Get selected status
    const selectedStatus =
        statusFilter
            ? statusFilter.value
            : "all";


    // Get selected date
    const selectedDate =
        dateFilter
            ? dateFilter.value
            : "all";


    // Get all table rows
    const rows =
        document.querySelectorAll(
            ".inspection-table tbody tr"
        );


    // Check every inspection
    rows.forEach(function (row) {

        // -----------------------------
        // SEARCH
        // -----------------------------

        const rowText =
            row.textContent.toLowerCase();

        const matchesSearch =
            rowText.includes(searchValue);


        // -----------------------------
        // STATUS
        // -----------------------------

        const statusElement =
            row.querySelector(".status");

        const rowStatus =
            statusElement
                ? statusElement.textContent
                    .toLowerCase()
                    .trim()
                : "";


        let matchesStatus = true;


        if (selectedStatus !== "all") {

            if (
                selectedStatus === "pass" &&
                rowStatus !== "pass"
            ) {
                matchesStatus = false;
            }


            if (
                selectedStatus === "review" &&
                rowStatus !== "review"
            ) {
                matchesStatus = false;
            }


            if (
                selectedStatus === "issue" &&
                rowStatus !== "potential issue"
            ) {
                matchesStatus = false;
            }

        }


        // -----------------------------
        // DATE
        // -----------------------------

        const dateCell =
            row.querySelector("td:nth-child(4)");

        const rowDate =
            dateCell
                ? dateCell.textContent.trim()
                : "";


        let matchesDate = true;


        /*
            Our sample records are:

            04 Sep 2026 → Today
            03 Sep 2026 → This Week
            02 Sep 2026 → This Week
        */


        if (selectedDate === "today") {

            matchesDate =
                rowDate === "04 Sep 2026";

        }


        else if (selectedDate === "week") {

            matchesDate =
                rowDate === "04 Sep 2026" ||
                rowDate === "03 Sep 2026" ||
                rowDate === "02 Sep 2026";

        }


        else if (selectedDate === "month") {

            matchesDate =
                rowDate.includes("Sep 2026");

        }


        // -----------------------------
        // FINAL RESULT
        // -----------------------------

        if (
            matchesSearch &&
            matchesStatus &&
            matchesDate
        ) {

            row.style.display = "";

        }

        else {

            row.style.display = "none";

        }

    });

}


// =========================================
// SEARCH EVENT
// =========================================

if (searchInput) {

    searchInput.addEventListener(
        "input",
        filterInspections
    );

}


// =========================================
// STATUS EVENT
// =========================================

if (statusFilter) {

    statusFilter.addEventListener(
        "change",
        filterInspections
    );

}


// =========================================
// DATE EVENT
// =========================================

if (dateFilter) {

    dateFilter.addEventListener(
        "change",
        filterInspections
    );

}const continueInspection = document.getElementById("continueInspection");

if (continueInspection) {

    continueInspection.addEventListener("click", function () {

        const location = document.getElementById("inspectionLocation");
        const type = document.getElementById("inspectionType");

        if (!location.value.trim()) {
            alert("Please enter the inspection location.");
            location.focus();
            return;
        }

        if (!type.value) {
            alert("Please select the inspection type.");
            type.focus();
            return;
        }

        window.location.href = "product-details.html";

    });

}const continueProduct = document.getElementById("continueProduct");

if (continueProduct) {

    continueProduct.addEventListener("click", function () {

        const productName = document.getElementById("productName");
        const manufacturer = document.getElementById("manufacturer");

        if (!productName.value.trim()) {
            alert("Please enter the product name.");
            productName.focus();
            return;
        }

        if (!manufacturer.value.trim()) {
            alert("Please enter the manufacturer / packer.");
            manufacturer.focus();
            return;
        }

        window.location.href = "evidence.html";

    });

}// Evidence Image Preview

function setupImagePreview(inputId, previewId) {

    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);

    if (!input || !preview) {
        return;
    }

    input.addEventListener("change", function () {

        const file = input.files[0];

        if (!file) {
            return;
        }

        if (!file.type.startsWith("image/")) {
            alert("Please select an image file.");
            input.value = "";
            return;
        }

        const reader = new FileReader();

        reader.onload = function (event) {

            preview.innerHTML = `
                <img
                    src="${event.target.result}"
                    alt="Uploaded package evidence"
                >
            `;

            preview.style.display = "block";
        };

        reader.readAsDataURL(file);

    });
}


setupImagePreview("frontImage", "frontPreview");

setupImagePreview("backImage", "backPreview");

setupImagePreview("sideImage", "sidePreview");
// Continue from Evidence

const continueEvidence = document.getElementById("continueEvidence");

if (continueEvidence) {

    continueEvidence.addEventListener("click", function () {

        const frontImage = document.getElementById("frontImage");
        const backImage = document.getElementById("backImage");

        if (!frontImage.files.length && !backImage.files.length) {
            alert("Please upload at least one package image.");
            return;
        }

        window.location.href = "review.html";

    });

}// Product Search and Filters

const productSearch = document.getElementById("productSearch");
const productCategoryFilter = document.getElementById("productCategoryFilter");
const productStatusFilter = document.getElementById("productStatusFilter");

function filterProducts() {

    const searchValue = productSearch
        ? productSearch.value.toLowerCase().trim()
        : "";

    const selectedCategory = productCategoryFilter
        ? productCategoryFilter.value
        : "all";

    const selectedStatus = productStatusFilter
        ? productStatusFilter.value
        : "all";

    const rows = document.querySelectorAll(
        ".inspection-table tbody tr"
    );

    rows.forEach(function (row) {

        const rowText = row.textContent.toLowerCase();

        const matchesSearch =
            rowText.includes(searchValue);


        // Category
        const categoryCell = row.querySelector("td:nth-child(3)");

        const rowCategory = categoryCell
            ? categoryCell.textContent.toLowerCase().trim()
            : "";


        let matchesCategory = true;

        if (selectedCategory !== "all") {

            if (
                selectedCategory === "food" &&
                rowCategory !== "food & grocery"
            ) {
                matchesCategory = false;
            }

            if (
                selectedCategory === "beverages" &&
                rowCategory !== "beverages"
            ) {
                matchesCategory = false;
            }

            if (
                selectedCategory === "household" &&
                rowCategory !== "household products"
            ) {
                matchesCategory = false;
            }

            if (
                selectedCategory === "personal" &&
                rowCategory !== "personal care"
            ) {
                matchesCategory = false;
            }

            if (
                selectedCategory === "electrical" &&
                rowCategory !== "electrical / consumer goods"
            ) {
                matchesCategory = false;
            }

        }


        // Status
        const statusElement = row.querySelector(".status");

        const rowStatus = statusElement
            ? statusElement.textContent.toLowerCase().trim()
            : "";


        let matchesStatus = true;

        if (selectedStatus !== "all") {

            if (
                selectedStatus === "pass" &&
                rowStatus !== "pass"
            ) {
                matchesStatus = false;
            }

            if (
                selectedStatus === "review" &&
                rowStatus !== "review"
            ) {
                matchesStatus = false;
            }

            if (
                selectedStatus === "issue" &&
                rowStatus !== "potential issue"
            ) {
                matchesStatus = false;
            }

        }


        // Show / Hide row
        row.style.display =
            matchesSearch &&
            matchesCategory &&
            matchesStatus
                ? ""
                : "none";

    });
}


// Search
if (productSearch) {
    productSearch.addEventListener(
        "input",
        filterProducts
    );
}


// Category
if (productCategoryFilter) {
    productCategoryFilter.addEventListener(
        "change",
        filterProducts
    );
}


// Status
if (productStatusFilter) {
    productStatusFilter.addEventListener(
        "change",
        filterProducts
    );
}