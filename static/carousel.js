let currentIndex = 0;
const items = document.querySelectorAll('.carousel-item');
const totalItems = items.length;

function showNextSlide() {
    items[currentIndex].classList.remove('active');
    currentIndex = (currentIndex + 1) % totalItems; // Ciclo a la primera imagen
    items[currentIndex].classList.add('active');
}

function showPrevSlide() {
    items[currentIndex].classList.remove('active');
    currentIndex = (currentIndex - 1 + totalItems) % totalItems; // Ciclo a la última imagen
    items[currentIndex].classList.add('active');
}

// Cambiar automáticamente cada 10 segundos
setInterval(showNextSlide, 10000);

// Agregar eventos a los botones de navegación
document.querySelector('.carousel-control-next').addEventListener('click', showNextSlide);
document.querySelector('.carousel-control-prev').addEventListener('click', showPrevSlide);