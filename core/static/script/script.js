function displayImage() {
    const fileInput = document.getElementById('uploadImage');
    const previewImage = document.getElementById('previewImage');
    const imageLabel = document.querySelector('.image-label');
    
    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
            imageLabel.textContent = fileInput.files[0].name;
        }
        reader.readAsDataURL(fileInput.files[0]);
    } else {
        previewImage.src = '#';
        previewImage.style.display = 'none';
        imageLabel.textContent = 'Upload Profile Image';
    }
}
