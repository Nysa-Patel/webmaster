// Navbar mobile toggle
document.querySelector('.navbar-toggle').addEventListener('click', function() {
  this.classList.toggle('open');
  document.querySelector('.navbar-links').classList.toggle('open');
});

// Hero parallax scroll
const hero = document.querySelector('.hero');

if (hero) {
  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const scale = Math.max(0.92, 1 - scrolled * 0.0001);
    hero.style.transform = `scale(${scale})`;
  });
}

// Carousel
const carousel = document.querySelector('.carousel');

if (carousel) {
  const track = carousel.querySelector('.carousel-track');
  const slides = track.querySelectorAll('.carousel-slide');
  const dots = carousel.querySelectorAll('.carousel-dot');
  const prevBtn = carousel.querySelector('.carousel-prev');
  const nextBtn = carousel.querySelector('.carousel-next');
  let current = 0;
  let autoTimer;

  function goTo(index) {
    current = (index + slides.length) % slides.length;
    track.style.transform = 'translateX(-' + (current * 100) + '%)';
    dots.forEach(function(d, i) {
      d.classList.toggle('active', i === current);
    });
  }

  function startAuto() {
    autoTimer = setInterval(function() { goTo(current + 1); }, 4000);
  }

  function resetAuto() {
    clearInterval(autoTimer);
    startAuto();
  }

  prevBtn.addEventListener('click', function() { goTo(current - 1); resetAuto(); });
  nextBtn.addEventListener('click', function() { goTo(current + 1); resetAuto(); });
  dots.forEach(function(dot, i) {
    dot.addEventListener('click', function() { goTo(i); resetAuto(); });
  });

  startAuto();
}

//Numbers increasing on scroll
const counters = document.querySelectorAll(".count span");
const container = document.querySelector(".count");

let activated = false;

window.addEventListener("scroll", () => {

  if(
    pageYOffset > container.offsetTop - container.offsetHeight - 200 && activated === false ) {
      counters.forEach(counter => {

        counter.innerText = 0;
        let count = 0;

        function updateCount() {
          const target = parseInt(counter.dataset.count);

          if(count < target) {
            count ++;
            counter.innerText = count;
            setTimeout(updateCount, 10);
          } else {
            counter.innerText = target;
          }
        }
        updateCount();
        activated = true;
      });
    } else if ( pageYOffset < container.offsetTop - container.offsetHeight - 500 || pageYOffset === 0 && activated === true){
      counters.forEach(counter => {
        counter.innerText = 0;
    });
    activated = false;
    }
});