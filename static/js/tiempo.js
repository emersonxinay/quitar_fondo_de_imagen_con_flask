document.addEventListener("DOMContentLoaded", function () {
  function updateCountdown() {
    const now = new Date();
    const nextChristmas = new Date(nextChristmasISO);

    const timeUntilChristmas = nextChristmas - now;

    if (timeUntilChristmas <= 0) {
      document.getElementById('countdown').textContent = "¡Es Navidad!";
      return;
    }

    const days = Math.floor(timeUntilChristmas / (1000 * 60 * 60 * 24));
    const hours = Math.floor((timeUntilChristmas % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeUntilChristmas % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeUntilChristmas % (1000 * 60)) / 1000);

    document.getElementById('days').textContent = String(days).padStart(2, '0');
    document.getElementById('hours').textContent = String(hours).padStart(2, '0');
    document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
    document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
  }

  // Actualizar el contador cada segundo
  setInterval(updateCountdown, 1000);

  // Inicializar el contador
  updateCountdown();
});
