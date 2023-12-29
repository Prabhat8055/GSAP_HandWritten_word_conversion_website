import splitType from "https://cdn.skypack.dev/pin/split-type@v0.3.3-CfnMrsWrI78YdAYcUWty/mode=imports/optimized/split-type.js";
const ourText = new splitType("h1.heading", { types: "chars" });
const chars = ourText.chars;

gsap.fromTo(
  chars,
  {
    y: 100,
    opacity: 0,
  },
  {
    y: 0,
    opacity: 1,
    stagger: 0.05,
    duration: 2,
    ease: "power4.out",
  }
);

// main page one GSAP

var tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".one",
    start: "50% 50%",
    end: "120% 50%",
    scrub: true,
    pin: ".one",
    // markers: true,
  },
});

tl.to(
  ".headding-para",
  {
    rotateX: "90deg",
    opacity: 0,
    duration: 1.5,
  },
  "kaka"
);
tl.to(
  ".bottom-content",
  {
    rotateX: "-90deg",
    opacity: 0,
    display: "none",
    duration: 1.5,
  },
  "kaka"
);

tl.to(
  ".middle-ele",
  {
    width: "100vw",
    height: "45vh",
    scale: 2.3,
    borderRadius: 0,
    // ease: Expo.easeInOut,
  },
  "kaka"
);
// changing color of nav bar pink//
tl.to(
  "nav",
  {
    backgroundColor: "#FCC4F0",
    color: "black",
    delay: 0.6,
  },
  "kaka"
);
tl.to(
  ".cntre-nav,#color-change",
  {
    backgroundColor: "#FCC4F0",
    color: "black",
    delay: 0.6,
  },
  "kaka"
);

// hidden para
tl.to(
  ".inner",
  {
    delay: 0.6,
    opacity: 1,
    ease: "slow(0.2, 0.5)",
    filter: "none",
  },
  "kaka"
);

// page two
// changing nav bar color to black
var tl2 = gsap.timeline({
  scrollTrigger: {
    trigger: ".two",
    start: "20% 50%",
    end: "50% 50%",
    scrub: true,
  },
});
tl2.to(
  "nav",
  {
    backgroundColor: "black",
    color: "white",
    delay: 0.8,
  },
  "kaka"
);
tl2.to(
  ".cntre-nav,#color-change",
  {
    backgroundColor: "black",
    color: "rgb(124, 124, 111)",
    delay: 0.8,
  },
  "kaka"
);

// preloader
var loader = document.getElementById("preloader");
window.addEventListener("load", function () {
  loader.style.display = "none";
});
