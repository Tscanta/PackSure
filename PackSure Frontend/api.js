/**
 * PackSure API Service Layer
 * Connects the PackSure frontend to the Legal Metrology compliance backend.
 */

const PackSureAPI = (function () {
    // Configurable base URL: can be set via window.PACKSURE_API_URL or localStorage
    const getBaseUrl = function () {
    // Explicit API URL has highest priority
    if (typeof window !== "undefined" && window.PACKSURE_API_URL) {
        return window.PACKSURE_API_URL.replace(/\/+$/, "");
    }

    // Saved API URL
    try {
        const storedUrl = localStorage.getItem("packSureApiUrl");
        if (storedUrl) {
            return storedUrl.replace(/\/+$/, "");
        }
    } catch (e) {
        // Ignore storage access issues
    }

    // Local development
    if (
        typeof window !== "undefined" &&
        (window.location.hostname === "localhost" ||
         window.location.hostname === "127.0.0.1")
    ) {
        return "http://localhost:8000";
    }

    // Production: use the same domain as the frontend
    if (typeof window !== "undefined") {
        return window.location.origin;
    }

    return "http://localhost:8000";
};

    /**
     * Converts a base64 DataURL to a Blob
     */
    function dataUrlToBlob(dataUrl) {
        if (!dataUrl || typeof dataUrl !== "string" || !dataUrl.startsWith("data:")) {
            return null;
        }
        try {
            const parts = dataUrl.split(",");
            const mimeMatch = parts[0].match(/:(.*?);/);
            const mime = mimeMatch ? mimeMatch[1] : "image/png";
            const bstr = atob(parts[1]);
            let n = bstr.length;
            const u8arr = new Uint8Array(n);
            while (n--) {
                u8arr[n] = bstr.charCodeAt(n);
            }
            return new Blob([u8arr], { type: mime });
        } catch (e) {
            console.error("Failed to convert dataUrl to Blob:", e);
            return null;
        }
    }

    /**
     * Standardized fetch wrapper with friendly error handling
     */
    async function request(endpoint, options = {}) {
        const baseUrl = getBaseUrl();
        const url = `${baseUrl}${endpoint}`;

        try {
            const response = await fetch(url, options);

            if (!response.ok) {
                let errorDetail = "";
                try {
                    const errJson = await response.json();
                    errorDetail = errJson.detail || JSON.stringify(errJson);
                } catch (e) {
                    errorDetail = await response.text();
                }

                if (response.status === 422) {
                    throw new Error(
                        errorDetail || "Unable to extract sufficient information from the package. Please upload a clearer image."
                    );
                }

                throw new Error(errorDetail || `Server returned error (${response.status})`);
            }

            return await response.json();
        } catch (err) {
            // Check if network / connection error
            if (
                err.name === "TypeError" &&
                (err.message.includes("Failed to fetch") ||
                 err.message.includes("NetworkError") ||
                 err.message.includes("Load failed"))
            ) {
                throw new Error(
                    `Unable to connect to the inspection server at ${baseUrl}. Please make sure the backend is running.`
                );
            }
            throw err;
        }
    }

    return {
        getBaseUrl,
        dataUrlToBlob,

        // Health check
        async checkHealth() {
            return request("/");
        },

        // Run inspection with JSON ProductInput
        async inspectProduct(productData) {
            return request("/inspect", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(productData),
            });
        },

        // Run inspection with an uploaded image file or Blob
        async inspectImage(imageFileOrBlob, manualProductData = {}) {
            const formData = new FormData();
            const filename = imageFileOrBlob.name || "package_evidence.png";
            formData.append("file", imageFileOrBlob, filename);

            if (manualProductData.name) {
                formData.append("product_name", manualProductData.name);
            }
            if (manualProductData.manufacturer) {
                formData.append("manufacturer", manualProductData.manufacturer);
            }
            if (manualProductData.quantity) {
                formData.append("net_quantity", manualProductData.quantity);
            }
            if (manualProductData.mrp) {
                formData.append("mrp", manualProductData.mrp);
            }
            if (manualProductData.category) {
                formData.append("product_category", manualProductData.category);
            }
            if (manualProductData.batch) {
                formData.append("batch_number", manualProductData.batch);
            }
            if (manualProductData.packingDate) {
                formData.append("manufacturing_date", manualProductData.packingDate);
            }

            return request("/inspect/image", {
                method: "POST",
                body: formData,
            });
        },

        // Extract OCR data only
        async extractData(imageFileOrBlob) {
            const formData = new FormData();
            const filename = imageFileOrBlob.name || "package.png";
            formData.append("file", imageFileOrBlob, filename);

            return request("/extract", {
                method: "POST",
                body: formData,
            });
        },

        // Fetch compliance rules
        async getRules() {
            return request("/rules");
        },

        // Fetch registered products
        async getProducts() {
            return request("/products");
        },

        // Fetch inspections
        async getInspections() {
            return request("/inspections");
        },

        // Fetch inspection by ID
        async getInspection(id) {
            return request(`/inspections/${id}`);
        },

        // Fetch violations for an inspection
        async getViolations(inspectionId) {
            return request(`/inspections/${inspectionId}/violations`);
        },
    };
})();

if (typeof window !== "undefined") {
    window.PackSureAPI = PackSureAPI;
}
