document.addEventListener("DOMContentLoaded", () => {
    const uploaders = document.querySelectorAll("[data-image-upload]");

    const MAX_SIZE = 700 * 1024;
    const MIN_WIDTH = 640;
    const MIN_HEIGHT = 360;
    const MAX_WIDTH = 2400;
    const MAX_HEIGHT = 2400;

    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/webp",
    ];

    uploaders.forEach((uploader) => {
        const input = uploader.querySelector(".fc-image-input");
        const browseButton = uploader.querySelector(".fc-image-browse");
        const previewContainer = uploader.querySelector(
            ".fc-image-preview-container"
        );

        const single = uploader.dataset.single === "true";
        const maxFiles = Number(uploader.dataset.maxFiles);

        let selectedFiles = [];

        browseButton.addEventListener("click", () => {
            input.click();
        });

        input.addEventListener("change", () => {
            addFiles(input.files);
            input.value = "";
        });

        uploader.addEventListener("dragover", (event) => {
            event.preventDefault();
            uploader.classList.add("is-dragging");
        });

        uploader.addEventListener("dragleave", () => {
            uploader.classList.remove("is-dragging");
        });

        uploader.addEventListener("drop", (event) => {
            event.preventDefault();

            uploader.classList.remove("is-dragging");

            addFiles(event.dataTransfer.files);
        });

        function addFiles(files) {
            const incomingFiles = Array.from(files);

            if (single) {
                selectedFiles = [];

                if (incomingFiles.length > 0) {
                    validateAndAdd(incomingFiles[0]);
                }

                return;
            }

            for (const file of incomingFiles) {
                if (selectedFiles.length >= maxFiles) {
                    showUploadMessage(
                        `You can upload a maximum of ${maxFiles} supporting images.`
                    );
                    break;
                }

                validateAndAdd(file);
            }
        }

        function validateAndAdd(file) {
            if (!allowedTypes.includes(file.type)) {
                showUploadMessage(
                    `${file.name}: Only JPG, PNG and WebP images are allowed.`
                );
                return;
            }

            if (file.size > MAX_SIZE) {
                showUploadMessage(
                    `${file.name}: Image must be 700 KB or smaller.`
                );
                return;
            }

            const image = new Image();

            image.onload = () => {
                if (
                    image.width < MIN_WIDTH ||
                    image.height < MIN_HEIGHT
                ) {
                    showUploadMessage(
                        `${file.name}: Image must be at least 640×360 pixels.`
                    );
                    return;
                }

                if (
                    image.width > MAX_WIDTH ||
                    image.height > MAX_HEIGHT
                ) {
                    showUploadMessage(
                        `${file.name}: Image cannot exceed 2400×2400 pixels.`
                    );
                    return;
                }

                if (single) {
                    selectedFiles = [file];
                } else {
                    selectedFiles.push(file);
                }

                renderPreviews();
            };

            image.onerror = () => {
                showUploadMessage(
                    `${file.name}: This image could not be read.`
                );
            };

            image.src = URL.createObjectURL(file);
        }

        function renderPreviews() {
            previewContainer.innerHTML = "";

            selectedFiles.forEach((file, index) => {
                const preview = document.createElement("div");

                preview.className = "fc-image-preview";

                const image = document.createElement("img");

                image.src = URL.createObjectURL(file);
                image.alt = file.name;

                const overlay = document.createElement("div");

                overlay.className = "fc-image-preview-overlay";

                const name = document.createElement("span");

                name.textContent = file.name;

                const remove = document.createElement("button");

                remove.type = "button";
                remove.className = "fc-image-remove";
                remove.innerHTML = '<i class="bi bi-x-lg"></i>';
                remove.setAttribute(
                    "aria-label",
                    `Remove ${file.name}`
                );

                remove.addEventListener("click", () => {
                    selectedFiles.splice(index, 1);
                    renderPreviews();
                });

                overlay.appendChild(name);
                overlay.appendChild(remove);

                preview.appendChild(image);
                preview.appendChild(overlay);

                previewContainer.appendChild(preview);
            });

            updateCounter();
        }

        function updateCounter() {
            const counter = uploader
                .closest(".fc-image-upload-section")
                ?.querySelector(".fc-image-counter strong");

            if (counter) {
                counter.textContent = selectedFiles.length;
            }

            if (!single) {
                uploader.classList.toggle(
                    "is-full",
                    selectedFiles.length >= maxFiles
                );
            }
        }

        function showUploadMessage(message) {
            const existing = uploader.querySelector(
                ".fc-image-upload-message"
            );

            if (existing) {
                existing.remove();
            }

            const messageElement = document.createElement("div");

            messageElement.className = "fc-image-upload-message";
            messageElement.innerHTML = `
                <i class="bi bi-exclamation-circle"></i>
                <span>${message}</span>
            `;

            uploader.prepend(messageElement);

            setTimeout(() => {
                messageElement.remove();
            }, 4000);
        }
    });
});