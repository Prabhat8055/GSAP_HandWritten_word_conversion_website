// js for uploading the image 
document.querySelectorAll(".input_hidden").forEach((inputElement) => {
  const dropZoneElement = inputElement.closest(".drop-zone");
  dropZoneElement.onclick = function () {
    console.log("clicked");
    inputElement.click();
  };
  document
    .getElementById("imageUpload")
    .addEventListener("change", function () {
      const imageInput = this;
      const imageDiv = document.getElementById("drop");

      if (imageInput.files && imageInput.files[0]) {
        const uploadedImageName = imageInput.files[0].name;
        imageDiv.textContent = "Uploaded Image: " + uploadedImageName;
      }
    });

  dropZoneElement.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZoneElement.classList.add("lal");
  });

  ["dragleave", "dragend"].forEach((type) => {
    dropZoneElement.addEventListener(type, (e) => {
      dropZoneElement.classList.remove("lal");
    });
  });

  dropZoneElement.addEventListener("drop", (e) => {
    e.preventDefault();
    if (e.dataTransfer.files) {
      inputElement.files = e.dataTransfer.files;
      const name = e.dataTransfer.files[0].name;
      var new_text = document.getElementById("drop");
      new_text.innerHTML = "Uploaded Image: " + name;
    }
  });
});
