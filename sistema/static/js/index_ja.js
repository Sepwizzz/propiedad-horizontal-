// owl carousel things

$('.home_carousel').owlCarousel({
    loop: true,
    margin: 0,
    dots: true,
    nav: false,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 1
        },
        1000: {
            items: 1
        }
    }
});

//navbar

window.addEventListener('scroll', function(){
    let navbar = document.getElementById("navbar");
    navbar.classList.toggle("fixed", this.window.scrollY > 0);
})


let MenuBtn = document.querySelector("#menu-btn");

//menu section

let menutabs = document.querySelector(".menu-tabs");
menutabs.addEventListener("click", function(e){
    if(e.target.classList.contains("menu-tab-item") && !e.target.classList.contains("active"))
    {

        const target = e.target.getAttribute("data-target");

        menutabs.querySelector(".active").classList.remove("active");

        e.target.classList.add("active");

        let menuSection = document.querySelector(".menu-section");

        menuSection.querySelector(".menu-tab-content.show").classList.remove("show");
        
        menuSection.querySelector(target).classList.add("show");

    }
})


$('.team-carousel').owlCarousel({
    loop: true,
    margin: 20,
    dots: false,
    nav: true,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 2
        },
        1000: {
            items: 3
        }
    }
});